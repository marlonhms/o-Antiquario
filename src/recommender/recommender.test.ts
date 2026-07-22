import assert from "node:assert/strict";
import test from "node:test";

import type { Fragrance, ScoringWeights } from "../domain/types.ts";
import { explainResult } from "./explain.ts";
import { FIXTURE_FRAGRANCES } from "./fixtures.ts";
import { recommend } from "./recommend.ts";
import { resolveWeights } from "./scoring.ts";

const ONLY_HISTORY: ScoringWeights = {
  preference: 0,
  context: 0,
  performance: 0,
  history: 1,
  budget: 0,
  confidence: 0,
  novelty: 0,
};

test("recomenda uma opção fresca e controlada para escritório quente e cheio", () => {
  const result = recommend(
    FIXTURE_FRAGRANCES,
    {
      notePreferences: { bergamota: 0.9, vetiver: 0.8, limão: 0.7 },
      accordPreferences: { cítrico: 1, amadeirado: 0.65, doce: -0.8 },
      noveltyPreference: 0.6,
    },
    {
      occasion: "escritório",
      setting: "indoor",
      crowding: "high",
      temperatureC: 30,
      humidity: 0.78,
      desiredProjection: 0.4,
      durationHours: 7,
      maximumPriceTier: 3,
      projectionCeiling: 0.72,
    },
  );

  assert.equal(result.recommendations[0]?.fragrance.id, "brisa-vetiver");
  assert.ok(result.recommendations[0]!.score > 0.7);
  assert.ok(result.excluded.some((item) => item.fragranceId === "ambar-noturno"));
});

test("uma nota marcada como evitação rígida exclui o perfume antes do score", () => {
  const result = recommend(
    FIXTURE_FRAGRANCES,
    { hardAvoidNotes: ["BAUNILHA"] },
    { occasion: "encontro" },
  );

  assert.ok(!result.candidatePool.some((item) => item.fragrance.id === "ambar-noturno"));
  assert.deepEqual(
    result.excluded.find((item) => item.fragranceId === "ambar-noturno")?.code,
    "hard_avoided_note",
  );
});

test("orçamento rígido exclui faixas superiores", () => {
  const result = recommend(FIXTURE_FRAGRANCES, {}, { maximumPriceTier: 2, strictBudget: true });

  const excludedIds = result.excluded
    .filter((item) => item.code === "over_strict_budget")
    .map((item) => item.fragranceId);
  assert.ok(excludedIds.includes("ambar-noturno"));
  assert.ok(excludedIds.includes("cha-de-iris"));
  assert.ok(result.candidatePool.every((item) => (item.fragrance.priceTier ?? 1) <= 2));
});

test("histórico pessoal usa prior neutro e ganha força após usos repetidos", () => {
  const result = recommend(
    FIXTURE_FRAGRANCES,
    {},
    {},
    [
      { fragranceId: "pomar-solar", wearCount: 12, wouldWearAgainRate: 1, averageRating: 5 },
      { fragranceId: "brisa-vetiver", wearCount: 12, wouldWearAgainRate: 0.1, averageRating: 1 },
    ],
    { weights: ONLY_HISTORY },
  );

  assert.equal(result.recommendations[0]?.fragrance.id, "pomar-solar");
  assert.ok(result.candidatePool.at(-1)!.fragrance.id === "brisa-vetiver");
});

test("dados de baixa confiança aproximam o score do prior neutro", () => {
  const highConfidence = FIXTURE_FRAGRANCES.find((item) => item.id === "brisa-vetiver")!;
  const lowConfidence: Fragrance = {
    ...highConfidence,
    id: "brisa-vetiver-incerto",
    name: "Brisa Vetiver Incerto",
    dataConfidence: "unknown",
    evidence: [{ sourceId: "estimativa", kind: "estimated", confidence: "unknown" }],
    performance: {
      longevity: { ...highConfidence.performance.longevity, confidence: "unknown", sampleSize: 0 },
      projection: { ...highConfidence.performance.projection, confidence: "unknown", sampleSize: 0 },
      sillage: { ...highConfidence.performance.sillage, confidence: "unknown", sampleSize: 0 },
    },
  };

  const result = recommend(
    [lowConfidence, highConfidence],
    { accordPreferences: { cítrico: 1, amadeirado: 1 } },
    { occasion: "escritório", temperatureC: 28, durationHours: 7 },
    [],
    { limit: 2, diversityStrength: 0 },
  );

  assert.equal(result.candidatePool[0]?.fragrance.id, "brisa-vetiver");
  assert.ok(result.candidatePool[0]!.confidence > result.candidatePool[1]!.confidence);
});

test("diversidade evita preencher o top 3 apenas com variações quase idênticas", () => {
  const withoutDiversity = recommend(
    FIXTURE_FRAGRANCES,
    { accordPreferences: { cítrico: 1, amadeirado: 0.9 }, notePreferences: { vetiver: 1 } },
    { occasion: "escritório", durationHours: 7 },
    [],
    { diversityStrength: 0 },
  );
  const withDiversity = recommend(
    FIXTURE_FRAGRANCES,
    { accordPreferences: { cítrico: 1, amadeirado: 0.9 }, notePreferences: { vetiver: 1 } },
    { occasion: "escritório", durationHours: 7 },
    [],
    { diversityStrength: 1 },
  );

  assert.equal(withDiversity.recommendations[0]?.fragrance.id, withoutDiversity.recommendations[0]?.fragrance.id);
  const diverseIds = withDiversity.recommendations.map((item) => item.fragrance.id);
  assert.ok(diverseIds.some((id) => !id.startsWith("brisa-vetiver")));
});

test("o resultado é determinístico e carrega rastreamento explicável", () => {
  const inputProfile = { accordPreferences: { amadeirado: 0.8 }, noveltyPreference: 0.4 };
  const inputContext = { occasion: "formal", formality: 0.9, durationHours: 8 };
  const first = recommend(FIXTURE_FRAGRANCES, inputProfile, inputContext);
  const second = recommend(FIXTURE_FRAGRANCES, inputProfile, inputContext);

  assert.deepEqual(
    first.recommendations.map((item) => [item.fragrance.id, item.score]),
    second.recommendations.map((item) => [item.fragrance.id, item.score]),
  );
  assert.equal(first.recommendations[0]?.factors.length, 7);
  assert.ok(first.recommendations[0]?.strengths.length);
});

test("fallback textual funciona sem IA e não inventa fragrâncias", () => {
  const result = recommend(
    FIXTURE_FRAGRANCES,
    { accordPreferences: { cítrico: 1 } },
    { occasion: "casual", temperatureC: 31 },
  );
  const explanation = explainResult(result);

  for (const recommendation of result.recommendations) {
    assert.match(explanation, new RegExp(recommendation.fragrance.name));
  }
  assert.match(explanation, /podem variar conforme pele/i);
});

test("pesos customizados são normalizados e pesos inválidos falham cedo", () => {
  const weights = resolveWeights({ preference: 3, context: 2 });
  const total = Object.values(weights).reduce((sum, value) => sum + value, 0);
  assert.ok(Math.abs(total - 1) < 1e-12);
  assert.throws(() => resolveWeights({ preference: -1 }), /Peso inválido/);
});

test("identificadores duplicados falham antes da recomendação", () => {
  const duplicate = { ...FIXTURE_FRAGRANCES[0]! };
  assert.throws(() => recommend([FIXTURE_FRAGRANCES[0]!, duplicate], {}, {}), /duplicado/i);
});

test("dados numéricos inválidos falham cedo em vez de serem corrigidos silenciosamente", () => {
  const invalid: Fragrance = {
    ...FIXTURE_FRAGRANCES[0]!,
    id: "projecao-invalida",
    performance: {
      ...FIXTURE_FRAGRANCES[0]!.performance,
      projection: { ...FIXTURE_FRAGRANCES[0]!.performance.projection, value: 1.4 },
    },
  };

  assert.throws(() => recommend([invalid], {}, {}), /projection\.value deve estar entre 0 e 1/);
  assert.throws(() => recommend(FIXTURE_FRAGRANCES, { noveltyPreference: -0.2 }, {}), /noveltyPreference/);
  assert.throws(() => recommend(FIXTURE_FRAGRANCES, {}, { humidity: 72 }), /humidity/);
});

test("orçamento rígido exclui também preço desconhecido", () => {
  const unknownPrice: Fragrance = {
    ...FIXTURE_FRAGRANCES[0]!,
    id: "preco-desconhecido",
    name: "Preço Desconhecido",
    priceTier: undefined,
  };
  const result = recommend([unknownPrice], {}, { maximumPriceTier: 3, strictBudget: true });

  assert.equal(result.recommendations.length, 0);
  assert.equal(result.excluded[0]?.code, "unknown_price_under_strict_budget");
});
