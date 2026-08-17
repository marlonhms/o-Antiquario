import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname } from "node:path";

import type { Evidence } from "../domain/types.ts";
import type { CompiledKnowledge } from "../knowledge/compiler.ts";
import type { KnowledgeDocument } from "../knowledge/schema.ts";

export const PRESENTATION_READINESS_VERSION = "presentation-readiness-v1";

export type PresentationReadinessStatus = "ready" | "olfactory_reference_only" | "blocked";
export type PresentationIssueSeverity = "blocking" | "ranking_blocking" | "warning";

export type PresentationIssueCode =
  | "placeholder_name"
  | "brand_not_structured"
  | "placeholder_brand"
  | "family_placeholder"
  | "olfactory_content_insufficient"
  | "layered_claim_not_supported"
  | "evidence_missing"
  | "source_locator_missing"
  | "concentration_not_declared"
  | "context_not_evidenced"
  | "performance_not_evidenced"
  | "document_forbids_ranking"
  | "source_document_missing";

export interface PresentationIssue {
  readonly code: PresentationIssueCode;
  readonly severity: PresentationIssueSeverity;
  readonly message: string;
}

export interface PresentationCandidate {
  readonly id: string;
  readonly name: string;
  readonly brand: string;
  readonly family: string;
  readonly noteCount: number;
  readonly accordCount: number;
  readonly evidence: readonly Evidence[];
}

export interface PresentationReadinessItem {
  readonly fragranceId: string;
  readonly documentId: string | null;
  readonly name: string;
  readonly brand: string;
  readonly status: PresentationReadinessStatus;
  readonly dimensions: {
    readonly identity: boolean;
    readonly olfactoryExplanation: boolean;
    readonly traceability: boolean;
    readonly concentration: boolean;
    readonly context: boolean;
    readonly performance: boolean;
  };
  readonly coverage: {
    readonly noteCount: number;
    readonly accordCount: number;
    readonly sourceIds: readonly string[];
    readonly evidenceWithLocator: number;
  };
  readonly issues: readonly PresentationIssue[];
}

export interface PresentationReadinessReport {
  readonly schemaVersion: 1;
  readonly policyVersion: typeof PRESENTATION_READINESS_VERSION;
  readonly reportId: string;
  readonly knowledgeReleaseId: string;
  readonly catalogReleaseId: string;
  readonly counts: {
    readonly evaluated: number;
    readonly ready: number;
    readonly olfactoryReferenceOnly: number;
    readonly blocked: number;
  };
  readonly issueCounts: Readonly<Record<string, number>>;
  readonly policy: {
    readonly minimumOlfactoryTerms: number;
    readonly requiresStructuredBrand: true;
    readonly requiresDeclaredConcentrationForRanking: true;
    readonly requiresScopedContextEvidenceForRanking: true;
    readonly requiresScopedPerformanceEvidenceForRanking: true;
    readonly wikidataDescriptorsAreNotPyramidLayers: true;
  };
  readonly items: readonly PresentationReadinessItem[];
}

const PLACEHOLDERS = new Set([
  "",
  "desconhecida",
  "desconhecido",
  "unknown",
  "n/a",
  "nao-classificada",
  "não-classificada",
]);

const OLFACTORY_PREDICATES = new Set([
  "declares-top-note",
  "declares-heart-note",
  "declares-base-note",
  "declares-unlayered-note",
  "has-top-note",
  "has-heart-note",
  "has-base-note",
  "has-note",
]);

const CONTEXT_SCOPE = /\b(contexto|ocasi[aã]o|clima|temperatura|ambiente|context|occasion|climate)\b/iu;
const PERFORMANCE_SCOPE = /\b(desempenho|dura[cç][aã]o|longevidade|proje[cç][aã]o|silagem|performance|longevity|projection|sillage)\b/iu;

function normalize(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("pt-BR")
    .trim();
}

function isPlaceholder(value: string): boolean {
  return PLACEHOLDERS.has(normalize(value));
}

function issue(
  code: PresentationIssueCode,
  severity: PresentationIssueSeverity,
  message: string,
): PresentationIssue {
  return { code, severity, message };
}

function relationCount(document: KnowledgeDocument, predicates: ReadonlySet<string>): number {
  return document.relations.filter((relation) => predicates.has(relation.predicate)).length;
}

function hasScopedEvidence(document: KnowledgeDocument, pattern: RegExp): boolean {
  return document.evidence.some((evidence) => pattern.test(evidence.claim_scope));
}

function explicitRankingProhibition(document: KnowledgeDocument): boolean {
  const normalizedBody = normalize(document.body);
  return normalizedBody.includes("nao deve ser usado pelo motor de ranking")
    || normalizedBody.includes("nao e uma recomendacao");
}

function auditItem(fragrance: PresentationCandidate, document: KnowledgeDocument | undefined): PresentationReadinessItem {
  if (!document) {
    return {
      fragranceId: fragrance.id,
      documentId: null,
      name: fragrance.name,
      brand: fragrance.brand,
      status: "blocked",
      dimensions: {
        identity: false,
        olfactoryExplanation: false,
        traceability: false,
        concentration: false,
        context: false,
        performance: false,
      },
      coverage: {
        noteCount: fragrance.noteCount,
        accordCount: fragrance.accordCount,
        sourceIds: [],
        evidenceWithLocator: fragrance.evidence.filter((evidence) => Boolean(evidence.sourceUrl)).length,
      },
      issues: [issue("source_document_missing", "blocking", "O candidato não possui documento correspondente no Knowledge Core.")],
    };
  }

  const issues: PresentationIssue[] = [];
  const brandRelations = document.relations.filter((relation) => relation.predicate === "belongs-to-brand");
  const noteCount = fragrance.noteCount;
  const structuredOlfactoryRelations = relationCount(document, OLFACTORY_PREDICATES);
  const evidenceWithLocator = document.evidence.filter((evidence) => Boolean(evidence.locator)).length;
  const wikidataLayerConflict = document.source_ids.includes("wikidata")
    && /P5872/u.test(document.body)
    && structuredOlfactoryRelations > 0;
  const rankingForbidden = explicitRankingProhibition(document);

  if (isPlaceholder(fragrance.name)) {
    issues.push(issue("placeholder_name", "blocking", "O nome comercial é vazio ou um placeholder."));
  }
  if (brandRelations.length !== 1) {
    issues.push(issue(
      "brand_not_structured",
      "blocking",
      brandRelations.length === 0
        ? "A marca não está estruturada como relação única no Knowledge Core."
        : "A identidade possui mais de uma marca e precisa ser reconciliada.",
    ));
  }
  if (isPlaceholder(fragrance.brand)) {
    issues.push(issue("placeholder_brand", "blocking", "A marca exibida ainda é um placeholder."));
  }
  if (isPlaceholder(fragrance.family)) {
    issues.push(issue("family_placeholder", "warning", "A família olfativa ainda não foi classificada."));
  }
  if (structuredOlfactoryRelations < 2 || noteCount + fragrance.accordCount < 2) {
    issues.push(issue(
      "olfactory_content_insufficient",
      "blocking",
      "Faltam ao menos dois elementos olfativos estruturados para explicar a fragrância.",
    ));
  }
  if (wikidataLayerConflict) {
    issues.push(issue(
      "layered_claim_not_supported",
      "blocking",
      "Descritores Wikidata P5872 foram posicionados em camadas sem evidência de pirâmide.",
    ));
  }
  if (document.evidence.length === 0 || fragrance.evidence.length === 0) {
    issues.push(issue("evidence_missing", "blocking", "A fragrância não possui evidência rastreável."));
  }
  if (evidenceWithLocator === 0) {
    issues.push(issue("source_locator_missing", "warning", "A evidência não possui um localizador direto para consulta."));
  }
  const declaredConcentrations = document.relations.filter((relation) => relation.predicate === "declares-concentration");
  if (declaredConcentrations.length === 0) {
    issues.push(issue(
      "concentration_not_declared",
      "ranking_blocking",
      "A concentração usada pelo motor não está estruturada como declaração da fonte.",
    ));
  }
  const contextEvidenced = Boolean(document.recommendation_profile) && hasScopedEvidence(document, CONTEXT_SCOPE);
  if (!contextEvidenced) {
    issues.push(issue(
      "context_not_evidenced",
      "ranking_blocking",
      "Ocasião e clima ainda não possuem evidência com escopo explícito.",
    ));
  }
  const performanceEvidenced = Boolean(document.recommendation_profile?.performance)
    && hasScopedEvidence(document, PERFORMANCE_SCOPE);
  if (!performanceEvidenced) {
    issues.push(issue(
      "performance_not_evidenced",
      "ranking_blocking",
      "Duração, projeção e silagem ainda não possuem evidência com escopo explícito.",
    ));
  }
  if (rankingForbidden) {
    issues.push(issue(
      "document_forbids_ranking",
      "blocking",
      "O próprio documento declara que não deve alimentar o ranking.",
    ));
  }

  const identity = !issues.some((item) => [
    "placeholder_name",
    "brand_not_structured",
    "placeholder_brand",
  ].includes(item.code));
  const olfactoryExplanation = !issues.some((item) => [
    "olfactory_content_insufficient",
    "layered_claim_not_supported",
  ].includes(item.code));
  const traceability = !issues.some((item) => item.code === "evidence_missing");
  const concentration = declaredConcentrations.length > 0;
  const blocked = issues.some((item) => item.severity === "blocking");
  const rankingBlocked = issues.some((item) => item.severity === "ranking_blocking");
  const status: PresentationReadinessStatus = blocked
    ? "blocked"
    : rankingBlocked
      ? "olfactory_reference_only"
      : "ready";

  return {
    fragranceId: fragrance.id,
    documentId: document.id,
    name: fragrance.name,
    brand: fragrance.brand,
    status,
    dimensions: {
      identity,
      olfactoryExplanation,
      traceability,
      concentration,
      context: contextEvidenced,
      performance: performanceEvidenced,
    },
    coverage: {
      noteCount,
      accordCount: fragrance.accordCount,
      sourceIds: [...document.source_ids].sort(),
      evidenceWithLocator,
    },
    issues,
  };
}

export function buildPresentationReadinessReport(
  knowledge: CompiledKnowledge,
  fragrances: readonly PresentationCandidate[],
  catalogReleaseId: string,
): PresentationReadinessReport {
  const documentsByCandidateId = new Map(
    knowledge.documents
      .filter((document) => document.type === "fragrance")
      .map((document) => [document.id.split(":").at(-1)!, document]),
  );
  const items = fragrances
    .map((fragrance) => auditItem(fragrance, documentsByCandidateId.get(fragrance.id)))
    .sort((left, right) => left.fragranceId.localeCompare(right.fragranceId));
  const issueCounts = Object.fromEntries(
    [...items.flatMap((item) => item.issues).reduce((counts, item) => {
      counts.set(item.code, (counts.get(item.code) ?? 0) + 1);
      return counts;
    }, new Map<string, number>())]
      .sort(([left], [right]) => left.localeCompare(right)),
  );
  const identityPayload = {
    policyVersion: PRESENTATION_READINESS_VERSION,
    knowledgeReleaseId: knowledge.manifest.releaseId,
    catalogReleaseId,
    items,
  };
  const contentHash = createHash("sha256").update(JSON.stringify(identityPayload)).digest("hex");
  return {
    schemaVersion: 1,
    policyVersion: PRESENTATION_READINESS_VERSION,
    reportId: `presentation-readiness-v1-${contentHash.slice(0, 12)}`,
    knowledgeReleaseId: knowledge.manifest.releaseId,
    catalogReleaseId,
    counts: {
      evaluated: items.length,
      ready: items.filter((item) => item.status === "ready").length,
      olfactoryReferenceOnly: items.filter((item) => item.status === "olfactory_reference_only").length,
      blocked: items.filter((item) => item.status === "blocked").length,
    },
    issueCounts,
    policy: {
      minimumOlfactoryTerms: 2,
      requiresStructuredBrand: true,
      requiresDeclaredConcentrationForRanking: true,
      requiresScopedContextEvidenceForRanking: true,
      requiresScopedPerformanceEvidenceForRanking: true,
      wikidataDescriptorsAreNotPyramidLayers: true,
    },
    items,
  };
}

export async function writePresentationReadinessReport(
  report: PresentationReadinessReport,
  outputPath: string,
): Promise<void> {
  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(report, null, 2)}\n`, "utf8");
}
