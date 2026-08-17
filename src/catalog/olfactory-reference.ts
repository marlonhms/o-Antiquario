import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import { dirname } from "node:path";

import type { CompiledKnowledge } from "../knowledge/compiler.ts";
import type { KnowledgeDocument, KnowledgeEvidence } from "../knowledge/schema.ts";
import { compilePresentationCandidates } from "./knowledge-adapter.ts";
import { buildPresentationReadinessReport, type PresentationIssueCode } from "./presentation-readiness.ts";

export type OlfactoryClaimNature = "declared" | "source_structured";

export interface OlfactoryReferenceTerm {
  readonly id: string;
  readonly label: string;
  readonly claimNature: OlfactoryClaimNature;
}

export interface OlfactoryReferenceEvidence {
  readonly sourceId: string;
  readonly kind: KnowledgeEvidence["kind"];
  readonly license: string;
  readonly confidence: KnowledgeEvidence["confidence"];
  readonly claimScope: string;
  readonly locator?: string;
  readonly retrievedAt?: string;
}

export interface OlfactoryReference {
  readonly id: string;
  readonly documentId: string;
  readonly name: string;
  readonly brand: { readonly id: string; readonly name: string };
  readonly perfumers: readonly { readonly id: string; readonly name: string }[];
  readonly family?: { readonly id: string; readonly name: string };
  readonly concentrations: readonly OlfactoryReferenceTerm[];
  readonly pyramid: {
    readonly top: readonly OlfactoryReferenceTerm[];
    readonly heart: readonly OlfactoryReferenceTerm[];
    readonly base: readonly OlfactoryReferenceTerm[];
    readonly unlayered: readonly OlfactoryReferenceTerm[];
  };
  readonly accords: readonly OlfactoryReferenceTerm[];
  readonly evidence: readonly OlfactoryReferenceEvidence[];
  readonly limitations: readonly PresentationIssueCode[];
  readonly readiness: "olfactory_reference_only";
}

export interface OlfactoryReferenceCatalog {
  readonly schemaVersion: 1;
  readonly releaseId: string;
  readonly knowledgeReleaseId: string;
  readonly generatedFromDate: string;
  readonly count: number;
  readonly references: readonly OlfactoryReference[];
}

const NOTE_LAYER_BY_PREDICATE: Readonly<Record<string, keyof OlfactoryReference["pyramid"]>> = {
  "declares-top-note": "top",
  "declares-heart-note": "heart",
  "declares-base-note": "base",
  "declares-unlayered-note": "unlayered",
  "has-top-note": "top",
  "has-heart-note": "heart",
  "has-base-note": "base",
  "has-note": "unlayered",
};

function slug(id: string): string {
  return id.split(":").at(-1)!;
}

function labelFor(target: string, documentsById: ReadonlyMap<string, KnowledgeDocument>): string {
  return documentsById.get(target)?.title ?? slug(target);
}

function claimNature(predicate: string): OlfactoryClaimNature {
  return predicate.startsWith("declares-") ? "declared" : "source_structured";
}

function term(
  predicate: string,
  target: string,
  documentsById: ReadonlyMap<string, KnowledgeDocument>,
): OlfactoryReferenceTerm {
  return {
    id: target,
    label: labelFor(target, documentsById),
    claimNature: claimNature(predicate),
  };
}

function evidence(item: KnowledgeEvidence): OlfactoryReferenceEvidence {
  return {
    sourceId: item.source_id,
    kind: item.kind,
    license: item.license,
    confidence: item.confidence,
    claimScope: item.claim_scope,
    ...(item.locator ? { locator: item.locator } : {}),
    ...(item.retrieved_at ? { retrievedAt: item.retrieved_at } : {}),
  };
}

function compileReference(
  document: KnowledgeDocument,
  limitations: readonly PresentationIssueCode[],
  documentsById: ReadonlyMap<string, KnowledgeDocument>,
): OlfactoryReference {
  const brandTarget = document.relations.find((relation) => relation.predicate === "belongs-to-brand")!.target;
  const familyTarget = document.relations.find((relation) => relation.predicate === "belongs-to-family")?.target;
  const pyramid: Record<keyof OlfactoryReference["pyramid"], OlfactoryReferenceTerm[]> = {
    top: [],
    heart: [],
    base: [],
    unlayered: [],
  };
  const accords: OlfactoryReferenceTerm[] = [];
  const concentrations: OlfactoryReferenceTerm[] = [];
  const perfumers: { id: string; name: string }[] = [];

  for (const relation of document.relations) {
    const layer = NOTE_LAYER_BY_PREDICATE[relation.predicate];
    if (layer) pyramid[layer].push(term(relation.predicate, relation.target, documentsById));
    if (relation.predicate === "has-accord") {
      accords.push(term(relation.predicate, relation.target, documentsById));
    }
    if (["declares-concentration", "has-concentration"].includes(relation.predicate)) {
      concentrations.push(term(relation.predicate, relation.target, documentsById));
    }
    if (relation.predicate === "created-by") {
      perfumers.push({ id: relation.target, name: labelFor(relation.target, documentsById) });
    }
  }

  return {
    id: slug(document.id),
    documentId: document.id,
    name: document.title,
    brand: { id: brandTarget, name: labelFor(brandTarget, documentsById) },
    perfumers,
    ...(familyTarget
      ? { family: { id: familyTarget, name: labelFor(familyTarget, documentsById) } }
      : {}),
    concentrations,
    pyramid,
    accords,
    evidence: document.evidence.map(evidence),
    limitations: [...new Set(limitations)].sort(),
    readiness: "olfactory_reference_only",
  };
}

export function compileOlfactoryReferenceCatalog(knowledge: CompiledKnowledge): OlfactoryReferenceCatalog {
  const presentationCandidates = compilePresentationCandidates(knowledge);
  const readiness = buildPresentationReadinessReport(
    knowledge,
    presentationCandidates,
    "olfactory-reference-catalog",
  );
  const documentsById = new Map(knowledge.documents.map((document) => [document.id, document]));
  const references = readiness.items
    .filter((item) => item.status === "olfactory_reference_only" && item.documentId)
    .map((item) => compileReference(
      documentsById.get(item.documentId!)!,
      item.issues.map((issue) => issue.code),
      documentsById,
    ))
    .sort((left, right) => left.id.localeCompare(right.id));
  const identity = {
    schemaVersion: 1 as const,
    knowledgeReleaseId: knowledge.manifest.releaseId,
    generatedFromDate: knowledge.manifest.latestDocumentDate,
    count: references.length,
    references,
  };
  const contentHash = createHash("sha256").update(JSON.stringify(identity)).digest("hex");
  return {
    ...identity,
    releaseId: `olfactory-reference-v1-${contentHash.slice(0, 12)}`,
  };
}

export async function writeOlfactoryReferenceCatalog(
  catalog: OlfactoryReferenceCatalog,
  outputPath: string,
): Promise<void> {
  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(catalog, null, 2)}\n`, "utf8");
}
