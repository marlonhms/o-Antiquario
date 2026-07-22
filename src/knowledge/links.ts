import type { KnowledgeDocument, KnowledgeEdge } from "./schema.ts";
import { assertRelationContract } from "./graph.ts";

export function normalizeKnowledgeReference(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("pt-BR")
    .replace(/\.md$/i, "")
    .replace(/[_–—-]+/g, " ")
    .replace(/[^\p{Letter}\p{Number}:\s]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function documentReferences(document: KnowledgeDocument): readonly string[] {
  const fileName = document.path.split("/").at(-1)?.replace(/\.md$/i, "") ?? document.title;
  const idSlug = document.id.split(":").at(-1) ?? document.id;
  return [document.id, document.title, fileName, idSlug, ...document.aliases];
}

export interface ResolvedKnowledgeGraph {
  readonly edges: readonly KnowledgeEdge[];
  readonly relatedByDocument: ReadonlyMap<string, readonly string[]>;
}

export function resolveKnowledgeGraph(documents: readonly KnowledgeDocument[]): ResolvedKnowledgeGraph {
  const byId = new Map(documents.map((document) => [document.id, document]));
  const references = new Map<string, string>();

  for (const document of documents) {
    for (const reference of documentReferences(document)) {
      const normalized = normalizeKnowledgeReference(reference);
      const owner = references.get(normalized);
      if (owner && owner !== document.id) {
        throw new Error(`Referência ambígua '${reference}' pertence a '${owner}' e '${document.id}'`);
      }
      references.set(normalized, document.id);
    }
  }

  const edges = new Map<string, KnowledgeEdge>();
  const related = new Map<string, Set<string>>(documents.map((document) => [document.id, new Set()]));
  const addEdge = (edge: KnowledgeEdge): void => {
    if (edge.source === edge.target) return;
    const key = `${edge.source}\u0000${edge.target}\u0000${edge.predicate}\u0000${edge.origin}`;
    edges.set(key, edge);
    related.get(edge.source)?.add(edge.target);
    related.get(edge.target)?.add(edge.source);
  };

  for (const document of documents) {
    for (const relation of document.relations) {
      if (!byId.has(relation.target)) {
        throw new Error(`${document.path}: relação aponta para ID inexistente '${relation.target}'`);
      }
      assertRelationContract(document, byId.get(relation.target)!, relation.predicate);
      addEdge({ source: document.id, target: relation.target, predicate: relation.predicate, origin: "frontmatter" });
    }

    for (const link of document.wikiLinks) {
      const target = references.get(normalizeKnowledgeReference(link.target));
      if (!target) throw new Error(`${document.path}: wikilink não resolvido '[[${link.target}]]'`);
      addEdge({ source: document.id, target, predicate: "references", origin: "wikilink" });
    }
  }

  return {
    edges: [...edges.values()].sort((left, right) => {
      return `${left.source}:${left.target}:${left.predicate}:${left.origin}`.localeCompare(
        `${right.source}:${right.target}:${right.predicate}:${right.origin}`,
      );
    }),
    relatedByDocument: new Map(
      [...related].map(([id, ids]) => [id, [...ids].sort()] as const),
    ),
  };
}
