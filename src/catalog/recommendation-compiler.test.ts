import assert from "node:assert/strict";
import { rm } from "node:fs/promises";
import { join } from "node:path";
import { test } from "node:test";

import { compileRecommendationCatalog, evaluateRecommendationGate } from "./recommendation-compiler.ts";
import { FIXTURE_FRAGRANCES } from "../recommender/fixtures.ts";

test("avalia corretamente o gate de elegibilidade com candidatos válidos e inválidos", () => {
  const candidates = [
    ...FIXTURE_FRAGRANCES,
    { id: "invalido-1", name: "Incompleto" },
  ];

  const { eligible, gateReport } = evaluateRecommendationGate(candidates, 5);
  assert.equal(eligible.length, FIXTURE_FRAGRANCES.length);
  assert.equal(gateReport.eligibleCount, FIXTURE_FRAGRANCES.length);
  assert.equal(gateReport.passesGate, true);
  assert.equal(gateReport.invalidReasons.length, 1);
  assert.equal(gateReport.invalidReasons[0].id, "invalido-1");
});

test("compila o catálogo de recomendação e gera o artefato json", async () => {
  const outputDir = join(process.cwd(), "tmp", "test-recommendation-catalog");
  try {
    const compiled = await compileRecommendationCatalog({
      candidates: FIXTURE_FRAGRANCES,
      outputDirectory: outputDir,
      minimumGateRequired: 5,
    });

    assert.equal(compiled.fragrances.length, FIXTURE_FRAGRANCES.length);
    assert.equal(compiled.gateReport.passesGate, true);
  } finally {
    await rm(outputDir, { recursive: true, force: true });
  }
});
