import assert from "node:assert/strict";
import { test } from "node:test";

import { FIXTURE_FRAGRANCES } from "../recommender/fixtures.ts";
import type { Fragrance } from "../domain/types.ts";
import type { CompiledKnowledge } from "../knowledge/compiler.ts";
import type { KnowledgeDocument } from "../knowledge/schema.ts";
import {
  buildPresentationReadinessReport,
  type PresentationCandidate,
} from "./presentation-readiness.ts";

function presentationCandidate(fragrance: Fragrance): PresentationCandidate {
  return {
    id: fragrance.id,
    name: fragrance.name,
    brand: fragrance.brand,
    family: fragrance.family,
    noteCount: fragrance.topNotes.length + fragrance.heartNotes.length + fragrance.baseNotes.length,
    accordCount: fragrance.accords.length,
    evidence: fragrance.evidence,
  };
}


function documentFor(
  fragrance: Fragrance,
  overrides: Partial<KnowledgeDocument> = {},
): KnowledgeDocument {
  return {
    schema_version: 1,
    id: `antiquario:fragrance:${fragrance.id}`,
    project: "o-antiquario",
    type: "fragrance",
    title: fragrance.name,
    aliases: [],
    external_ids: {},
    tags: ["perfume"],
    source_ids: ["manufacturer_fixture"],
    license: "CC0-1.0",
    confidence: "high",
    review_status: "approved",
    updated_at: "2026-08-17",
    language: "pt-BR",
    summary: "Documento factual completo para o teste de apresentação.",
    evidence: [{
      source_id: "manufacturer_fixture",
      kind: "manufacturer",
      license: "CC0-1.0",
      confidence: "high",
      claim_scope: "Identidade, pirâmide olfativa, concentração, contexto, clima e desempenho com duração e projeção.",
      locator: "https://example.test/perfume",
      retrieved_at: "2026-08-17",
    }],
    relations: [
      { predicate: "belongs-to-brand", target: "antiquario:brand:marca-fixture" },
      { predicate: "declares-concentration", target: "antiquario:concentration:eau-de-parfum" },
      { predicate: "declares-top-note", target: "antiquario:olfactory-note:bergamota" },
      { predicate: "declares-base-note", target: "antiquario:olfactory-note:vetiver" },
    ],
    recommendation_profile: {
      performance: fragrance.performance,
      climate: fragrance.climate,
      occasions: { escritorio: 0.8 },
    },
    path: `10_Perfumes/${fragrance.id}.md`,
    body: `# ${fragrance.name}`,
    wikiLinks: [],
    contentHash: "a".repeat(64),
    ...overrides,
  };
}

function knowledgeWith(documents: readonly KnowledgeDocument[]): CompiledKnowledge {
  return {
    documents,
    chunks: [],
    edges: [],
    health: {} as CompiledKnowledge["health"],
    manifest: {
      schemaVersion: 2,
      releaseId: "knowledge-v2-aaaaaaaaaaaa",
      contentHash: "a".repeat(64),
      latestDocumentDate: "2026-08-17",
      counts: { documents: documents.length, chunks: 0, nodes: 0, edges: 0, evidenceNodes: 0, typedRelations: 0 },
      sources: ["manufacturer_fixture"],
      files: { documents: "documents.json", chunks: "chunks.json", graph: "graph.json", health: "graph-health.json" },
    },
    validation: { documents: documents.length, approvedDocuments: documents.length, sourceIds: ["manufacturer_fixture"] },
  };
}

test("libera somente fragrância com identidade, conteúdo e evidência completos", () => {
  const fragrance = FIXTURE_FRAGRANCES[0]!;
  const report = buildPresentationReadinessReport(
    knowledgeWith([documentFor(fragrance)]),
    [presentationCandidate(fragrance)],
    "catalog-fixture",
  );

  assert.equal(report.counts.ready, 1);
  assert.equal(report.items[0]?.status, "ready");
  assert.deepEqual(report.items[0]?.issues, []);
});

test("preserva referência olfativa sem promover estimativas a recomendação contextual", () => {
  const fragrance = FIXTURE_FRAGRANCES[0]!;
  const document = documentFor(fragrance, {
    relations: [
      { predicate: "belongs-to-brand", target: "antiquario:brand:marca-fixture" },
      { predicate: "has-top-note", target: "antiquario:olfactory-note:bergamota" },
      { predicate: "has-base-note", target: "antiquario:olfactory-note:vetiver" },
    ],
    evidence: [{
      source_id: "manufacturer_fixture",
      kind: "open_source",
      license: "CC0-1.0",
      confidence: "medium",
      claim_scope: "Estrutura da pirâmide olfativa do perfume.",
    }],
    recommendation_profile: undefined,
  });
  const report = buildPresentationReadinessReport(
    knowledgeWith([document]),
    [presentationCandidate(fragrance)],
    "catalog-fixture",
  );
  const item = report.items[0]!;

  assert.equal(item.status, "olfactory_reference_only");
  assert.equal(item.dimensions.olfactoryExplanation, true);
  assert.equal(item.dimensions.performance, false);
  assert.ok(item.issues.some((entry) => entry.code === "concentration_not_declared"));
  assert.ok(item.issues.some((entry) => entry.code === "source_locator_missing"));
});

test("bloqueia descritor Wikidata colocado em pirâmide e documento que proíbe ranking", () => {
  const base = FIXTURE_FRAGRANCES[0]!;
  const fragrance: Fragrance = { ...base, brand: "Desconhecida" };
  const document = documentFor(fragrance, {
    source_ids: ["wikidata"],
    evidence: [{
      source_id: "wikidata",
      kind: "open_source",
      license: "CC0-1.0",
      confidence: "medium",
      claim_scope: "Identidade e descritores olfativos P5872.",
      locator: "https://www.wikidata.org/wiki/Q1",
    }],
    relations: [
      { predicate: "has-top-note", target: "antiquario:olfactory-note:bergamota" },
      { predicate: "has-base-note", target: "antiquario:olfactory-note:vetiver" },
    ],
    body: "Descritores P5872, sem camada de pirâmide. Este rascunho não é uma recomendação e não deve ser usado pelo motor de ranking.",
  });
  const report = buildPresentationReadinessReport(
    knowledgeWith([document]),
    [presentationCandidate(fragrance)],
    "catalog-fixture",
  );
  const codes = report.items[0]!.issues.map((entry) => entry.code);

  assert.equal(report.items[0]?.status, "blocked");
  assert.ok(codes.includes("brand_not_structured"));
  assert.ok(codes.includes("placeholder_brand"));
  assert.ok(codes.includes("layered_claim_not_supported"));
  assert.ok(codes.includes("document_forbids_ranking"));
});

test("relatório é determinístico e independente da ordem de entrada", () => {
  const first = FIXTURE_FRAGRANCES[0]!;
  const second = FIXTURE_FRAGRANCES[1]!;
  const knowledge = knowledgeWith([documentFor(first), documentFor(second)]);
  const forward = buildPresentationReadinessReport(
    knowledge,
    [presentationCandidate(first), presentationCandidate(second)],
    "catalog-fixture",
  );
  const reverse = buildPresentationReadinessReport(
    knowledge,
    [presentationCandidate(second), presentationCandidate(first)],
    "catalog-fixture",
  );

  assert.equal(forward.reportId, reverse.reportId);
  assert.deepEqual(forward.items, reverse.items);
});
