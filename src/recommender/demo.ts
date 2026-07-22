import { explainResult } from "./explain.ts";
import { FIXTURE_FRAGRANCES } from "./fixtures.ts";
import { recommend } from "./recommend.ts";

const result = recommend(
  FIXTURE_FRAGRANCES,
  {
    notePreferences: { bergamota: 0.9, vetiver: 0.8, baunilha: -0.8 },
    accordPreferences: { cítrico: 1, amadeirado: 0.7, doce: -0.8 },
    hardAvoidNotes: ["oud"],
    noveltyPreference: 0.55,
  },
  {
    occasion: "escritório",
    setting: "indoor",
    crowding: "high",
    temperatureC: 30,
    humidity: 0.75,
    durationHours: 7,
    desiredProjection: 0.4,
    maximumPriceTier: 3,
    projectionCeiling: 0.75,
  },
);

console.log(explainResult(result));
console.log(`\nExcluídos por regras duras: ${result.excluded.length}`);
