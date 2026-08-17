import assert from "node:assert/strict";
import { test } from "node:test";

import type { CompiledKnowledge } from "../knowledge/compiler.ts";
import type { KnowledgeDocument } from "../knowledge/schema.ts";
import { compileRecommendationCandidates } from "./knowledge-adapter.ts";

const EVIDENCE = [{
  source_id: "official_catalog_o_boticario",
  kind: "manufacturer" as const,
  license: "uso-interno",
  confidence: "medium" as const,
  claim_scope: "Identidade e composição declaradas pelo fabricante.",
}];

function document(overrides: Partial<KnowledgeDocument>): KnowledgeDocument {
  return {
    schema_version: 1,
    id: "antiquario:fragrance:teste",
    project: "o-antiquario",
    type: "fragrance",
    title: "Perfume Teste",
    aliases: [],
    external_ids: {},
    tags: ["perfume"],
    source_ids: ["official_catalog_o_boticario"],
    license: "uso-interno",
    confidence: "medium",
    review_status: "approved",
    updated_at: "2026-08-17",
    language: "pt-BR",
    summary: "Documento factual suficiente para o teste do adaptador.",
    evidence: EVIDENCE,
    relations: [],
    path: "10_Perfumes/teste.md",
    body: "# Perfume Teste",
    wikiLinks: [],
    contentHash: "test",
    ...overrides,
  };
}

function knowledge(fragranceOverrides: Partial<KnowledgeDocument> = {}): CompiledKnowledge {
  const fragrance = document({
    relations: [
      { predicate: "belongs-to-brand", target: "antiquario:brand:o-boticario" },
      { predicate: "belongs-to-family", target: "antiquario:olfactory-family:amadeirado" },
      { predicate: "declares-concentration", target: "antiquario:concentration:eau-de-parfum" },
      { predicate: "declares-top-note", target: "antiquario:olfactory-note:bergamota" },
      { predicate: "has-accord", target: "antiquario:accord:citricos" },
    ],
    recommendation_profile: {
      formality: 0.7,
      performance: {
        longevity: { minimumHours: 6, maximumHours: 8, confidence: "medium" },
        projection: { value: 0.6, confidence: "medium" },
        sillage: { value: 0.5, confidence: "medium" },
      },
    },
    ...fragranceOverrides,
  });
  const documents = [
    fragrance,
    document({ id: "antiquario:brand:o-boticario", type: "brand", title: "O Boticário" }),
    document({ id: "antiquario:olfactory-family:amadeirado", type: "olfactory-family", title: "Amadeirado" }),
    document({ id: "antiquario:concentration:eau-de-parfum", type: "concentration", title: "Eau de Parfum" }),
  ];
  return { documents } as unknown as CompiledKnowledge;
}

test("compila apenas fatos e perfil explicitamente declarados", () => {
  const [candidate] = compileRecommendationCandidates(knowledge());

  assert.ok(candidate);
  assert.equal(candidate.brand, "O Boticário");
  assert.equal(candidate.family, "amadeirado");
  assert.deepEqual(candidate.concentrations, ["Eau de Parfum"]);
  assert.deepEqual(candidate.topNotes, ["bergamota"]);
  assert.deepEqual(candidate.segments, []);
  assert.deepEqual(candidate.climate, {});
  assert.deepEqual(candidate.accords, [], "não deve inventar peso para acorde sem peso explícito");
  assert.equal(candidate.priceTier, undefined);
});

test("não promove fragrância sem família, concentração ou perfil contextual", () => {
  const base = knowledge().documents[0]!;
  const withoutFamily = base.relations.filter((relation) => relation.predicate !== "belongs-to-family");
  const withoutConcentration = base.relations.filter((relation) => relation.predicate !== "declares-concentration");

  assert.equal(compileRecommendationCandidates(knowledge({ relations: withoutFamily })).length, 0);
  assert.equal(compileRecommendationCandidates(knowledge({ relations: withoutConcentration })).length, 0);
  assert.equal(compileRecommendationCandidates(knowledge({ recommendation_profile: undefined })).length, 0);
});
