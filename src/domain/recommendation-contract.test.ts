import assert from "node:assert/strict";
import { test } from "node:test";

import { validateRecommendationEligibility } from "./recommendation-contract.ts";
import { FIXTURE_FRAGRANCES } from "../recommender/fixtures.ts";

test("valida que as fragrâncias de demonstração cumprem o contrato EligibleForRecommendation", () => {
  for (const fragrance of FIXTURE_FRAGRANCES) {
    const result = validateRecommendationEligibility(fragrance);
    assert.equal(result.success, true, `Fragrância sintética ${fragrance.id} falhou no contrato: ${result.issues?.join(", ")}`);
  }
});

test("rejeita uma fragrância sem concentrações declaradas", () => {
  const invalid = {
    ...FIXTURE_FRAGRANCES[0],
    concentrations: [],
  };
  const result = validateRecommendationEligibility(invalid);
  assert.equal(result.success, false);
  assert.ok(result.issues?.some((issue) => issue.toLowerCase().includes("concentra")));
});


test("rejeita uma fragrância sem evidências aprovadas", () => {
  const invalid = {
    ...FIXTURE_FRAGRANCES[0],
    evidence: [],
  };
  const result = validateRecommendationEligibility(invalid);
  assert.equal(result.success, false);
  assert.ok(result.issues?.some((issue) => issue.includes("evidência")));
});
