import { sha256 } from "./markdown.ts";
import type {
  KnowledgeDocument,
  KnowledgeDocumentType,
  KnowledgeEdge,
  KnowledgeEvidence,
} from "./schema.ts";

type RelationContract = Readonly<{
  sources: readonly KnowledgeDocumentType[];
  targets: readonly KnowledgeDocumentType[];
}>;

const ALL_DOCUMENT_TYPES: readonly KnowledgeDocumentType[] = [
  "index", "fragrance", "olfactory-note", "accord", "raw-material", "context", "science", "guide", "brand", "perfumer"
];

export const RELATION_CONTRACTS: Readonly<Record<string, RelationContract>> = {
  indexes: { sources: ["index"], targets: ALL_DOCUMENT_TYPES.filter((type) => type !== "index") },
  "has-note": { sources: ["fragrance"], targets: ["olfactory-note"] },
  "has-accord": { sources: ["fragrance"], targets: ["accord"] },
  "suited-to": { sources: ["fragrance", "olfactory-note", "accord"], targets: ["context"] },
  "has-facet": { sources: ["olfactory-note"], targets: ["accord"] },
  "found-in": { sources: ["olfactory-note"], targets: ["fragrance"] },
  "contrasts-with": { sources: ["olfactory-note", "accord"], targets: ["olfactory-note", "accord"] },
  "includes-note": { sources: ["accord"], targets: ["olfactory-note"] },
  "expressed-by": { sources: ["accord"], targets: ["fragrance"] },
  favors: { sources: ["context"], targets: ["olfactory-note", "accord"] },
  "compatible-example": { sources: ["context"], targets: ["fragrance"] },
  "governed-by": { sources: ["guide"], targets: ["index", "guide"] },
  "belongs-to-brand": { sources: ["fragrance"], targets: ["brand"] },
  "created-by": { sources: ["fragrance"], targets: ["perfumer"] },
  "has-top-note": { sources: ["fragrance"], targets: ["olfactory-note"] },
  "has-heart-note": { sources: ["fragrance"], targets: ["olfactory-note"] },
  "has-base-note": { sources: ["fragrance"], targets: ["olfactory-note"] },
};

export function assertRelationContract(source: KnowledgeDocument, target: KnowledgeDocument, predicate: string): void {
  const contract = RELATION_CONTRACTS[predicate];
  if (!contract) throw new Error(`${source.path}: predicado de grafo não reconhecido '${predicate}'`);
  if (!contract.sources.includes(source.type) || !contract.targets.includes(target.type)) {
    throw new Error(`${source.path}: relação '${predicate}' não permite ${source.type} → ${target.type}`);
  }
}

export interface KnowledgeDocumentGraphNode {
  readonly id: string;
  readonly kind: "document";
  readonly documentType: KnowledgeDocumentType;
  readonly title: string;
  readonly path: string;
  readonly tags: readonly string[];
  readonly confidence: KnowledgeDocument["confidence"];
}

export interface KnowledgeEvidenceGraphNode {
  readonly id: string;
  readonly kind: "evidence";
  readonly documentId: string;
  readonly sourceId: string;
  readonly license: string;
  readonly confidence: KnowledgeEvidence["confidence"];
  readonly claimScope: string;
  readonly locator?: string;
  readonly retrievedAt?: string;
}

export type KnowledgeGraphNode = KnowledgeDocumentGraphNode | KnowledgeEvidenceGraphNode;

export interface ExpandedKnowledgeGraph {
  readonly nodes: readonly KnowledgeGraphNode[];
  readonly edges: readonly KnowledgeEdge[];
}

function evidenceId(documentId: string, evidence: KnowledgeEvidence, index: number): string {
  const fingerprint = sha256(JSON.stringify({ documentId, evidence, index })).slice(0, 16);
  return `${documentId}:evidence:${String(index + 1).padStart(3, "0")}-${fingerprint}`;
}

function compareEdges(left: KnowledgeEdge, right: KnowledgeEdge): number {
  return `${left.source}:${left.target}:${left.predicate}:${left.origin}`.localeCompare(
    `${right.source}:${right.target}:${right.predicate}:${right.origin}`,
  );
}

export function buildExpandedKnowledgeGraph(
  documents: readonly KnowledgeDocument[],
  documentEdges: readonly KnowledgeEdge[],
): ExpandedKnowledgeGraph {
  const documentNodes: KnowledgeDocumentGraphNode[] = documents.map((document) => ({
    id: document.id,
    kind: "document",
    documentType: document.type,
    title: document.title,
    path: document.path,
    tags: document.tags,
    confidence: document.confidence,
  }));
  const evidenceNodes: KnowledgeEvidenceGraphNode[] = [];
  const evidenceEdges: KnowledgeEdge[] = [];
  for (const document of documents) {
    for (const [index, evidence] of document.evidence.entries()) {
      const id = evidenceId(document.id, evidence, index);
      evidenceNodes.push({
        id,
        kind: "evidence",
        documentId: document.id,
        sourceId: evidence.source_id,
        license: evidence.license,
        confidence: evidence.confidence,
        claimScope: evidence.claim_scope,
        ...(evidence.locator ? { locator: evidence.locator } : {}),
        ...(evidence.retrieved_at ? { retrievedAt: evidence.retrieved_at } : {}),
      });
      evidenceEdges.push({ source: document.id, target: id, predicate: "supported-by", origin: "evidence" });
    }
  }
  return {
    nodes: [...documentNodes, ...evidenceNodes].sort((left, right) => left.id.localeCompare(right.id)),
    edges: [...documentEdges, ...evidenceEdges].sort(compareEdges),
  };
}

export type GraphHealthSeverity = "warning" | "error";

export interface KnowledgeGraphHealthIssue {
  readonly code: string;
  readonly severity: GraphHealthSeverity;
  readonly message: string;
  readonly documentId?: string;
}

export interface KnowledgeGraphHealthReport {
  readonly schemaVersion: 2;
  readonly graph: {
    readonly documentNodes: number;
    readonly evidenceNodes: number;
    readonly typedRelations: number;
    readonly wikiReferences: number;
    readonly evidenceLinks: number;
  };
  readonly connectivity: {
    readonly isolatedDocumentIds: readonly string[];
    readonly components: readonly { readonly anchor: string; readonly documentIds: readonly string[] }[];
  };
  readonly editorialCoverage: {
    readonly approvedFragrances: number;
    readonly approvedCommercialFragrances: number;
    readonly withExternalIdentity: number;
    readonly withNotes: number;
    readonly withAccords: number;
    readonly withContexts: number;
    readonly recommendationReady: number;
  };
  readonly readiness: {
    readonly status: "blocked" | "pilot" | "core";
    readonly pilotMinimum: number;
    readonly coreMinimum: number;
    readonly reason: string;
  };
  readonly issues: readonly KnowledgeGraphHealthIssue[];
}

function documentComponents(documents: readonly KnowledgeDocument[], edges: readonly KnowledgeEdge[]) {
  const neighbors = new Map(documents.map((document) => [document.id, new Set<string>()]));
  for (const edge of edges.filter((edge) => edge.origin !== "evidence")) {
    neighbors.get(edge.source)?.add(edge.target);
    neighbors.get(edge.target)?.add(edge.source);
  }
  const unseen = new Set(documents.map((document) => document.id));
  const components: { anchor: string; documentIds: readonly string[] }[] = [];
  while (unseen.size > 0) {
    const anchor = [...unseen].sort()[0]!;
    const pending = [anchor];
    const component = new Set<string>();
    unseen.delete(anchor);
    while (pending.length > 0) {
      const current = pending.pop()!;
      component.add(current);
      for (const neighbor of neighbors.get(current) ?? []) {
        if (unseen.delete(neighbor)) pending.push(neighbor);
      }
    }
    components.push({ anchor, documentIds: [...component].sort() });
  }
  return {
    components: components.sort((left, right) => left.anchor.localeCompare(right.anchor)),
    isolatedDocumentIds: [...neighbors].filter(([, related]) => related.size === 0).map(([id]) => id).sort(),
  };
}

export function inspectKnowledgeGraph(
  documents: readonly KnowledgeDocument[],
  graph: ExpandedKnowledgeGraph,
): KnowledgeGraphHealthReport {
  const typedRelations = graph.edges.filter((edge) => edge.origin === "frontmatter");
  const relationsBySource = new Map<string, Set<string>>();
  for (const edge of typedRelations) {
    const predicates = relationsBySource.get(edge.source) ?? new Set<string>();
    predicates.add(edge.predicate);
    relationsBySource.set(edge.source, predicates);
  }
  const fragrances = documents.filter((document) => document.type === "fragrance");
  const commercial = fragrances.filter((document) => !document.tags.includes("fixture"));
  const has = (document: KnowledgeDocument, predicate: string) => relationsBySource.get(document.id)?.has(predicate) ?? false;
  const withExternalIdentity = commercial.filter((document) => Boolean(document.external_ids.wikidata));
  const withNotes = commercial.filter((document) => has(document, "has-note"));
  const withAccords = commercial.filter((document) => has(document, "has-accord"));
  const withContexts = commercial.filter((document) => has(document, "suited-to"));
  const recommendationReady = commercial.filter((document) => (
    has(document, "has-note") && has(document, "has-accord") && has(document, "suited-to")
    && document.confidence !== "unknown"
  ));
  const connectivity = documentComponents(documents, graph.edges);
  const issues: KnowledgeGraphHealthIssue[] = [
    ...connectivity.isolatedDocumentIds.map((documentId) => ({
      code: "isolated-document",
      severity: "error" as const,
      documentId,
      message: "Documento aprovado sem sinapses com o restante do grafo.",
    })),
    ...commercial.flatMap((document) => {
      const missing = ["has-note", "has-accord", "suited-to"].filter((predicate) => !has(document, predicate));
      return missing.length === 0 ? [] : [{
        code: "incomplete-fragrance-structure",
        severity: "warning" as const,
        documentId: document.id,
        message: `Fragrância aprovada sem relações obrigatórias: ${missing.join(", ")}.`,
      }];
    }),
  ];
  if (commercial.length === 0) {
    issues.push({
      code: "no-approved-commercial-fragrances",
      severity: "warning",
      message: "Não há fragrâncias comerciais aprovadas; o RAG ainda não pode sustentar recomendações factuais.",
    });
  }
  const pilotMinimum = 3;
  const coreMinimum = 30;
  const status = recommendationReady.length >= coreMinimum ? "core" : recommendationReady.length >= pilotMinimum ? "pilot" : "blocked";
  const reason = status === "core"
    ? "Há corpus editorial suficiente para o núcleo factual inicial."
    : status === "pilot"
      ? "Há corpus suficiente somente para piloto factual controlado."
      : `São necessárias ${pilotMinimum} fragrâncias comerciais aprovadas e estruturalmente completas para o piloto.`;
  return {
    schemaVersion: 2,
    graph: {
      documentNodes: documents.length,
      evidenceNodes: graph.nodes.filter((node) => node.kind === "evidence").length,
      typedRelations: typedRelations.length,
      wikiReferences: graph.edges.filter((edge) => edge.origin === "wikilink").length,
      evidenceLinks: graph.edges.filter((edge) => edge.origin === "evidence").length,
    },
    connectivity,
    editorialCoverage: {
      approvedFragrances: fragrances.length,
      approvedCommercialFragrances: commercial.length,
      withExternalIdentity: withExternalIdentity.length,
      withNotes: withNotes.length,
      withAccords: withAccords.length,
      withContexts: withContexts.length,
      recommendationReady: recommendationReady.length,
    },
    readiness: { status, pilotMinimum, coreMinimum, reason },
    issues: issues.sort((left, right) => (
      `${left.severity}:${left.code}:${left.documentId ?? ""}`.localeCompare(
        `${right.severity}:${right.code}:${right.documentId ?? ""}`,
      )
    )),
  };
}
