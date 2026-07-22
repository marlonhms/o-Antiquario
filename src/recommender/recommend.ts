import type {
  Fragrance,
  PreferenceProfile,
  RecommendationContext,
  RecommendationOptions,
  RecommendationResult,
  WearHistorySummary,
} from "../domain/types.ts";
import { assertValidContext, assertValidFragrances, assertValidProfile } from "../domain/validation.ts";
import { diversify } from "./diversity.ts";
import { normalizeId } from "./math.ts";
import { partitionByEligibility } from "./rules.ts";
import { resolveWeights, scoreFragrance } from "./scoring.ts";

export const ENGINE_VERSION = "0.1.0";

function historyMap(history: readonly WearHistorySummary[]): Map<string, WearHistorySummary> {
  return new Map(history.map((item) => [normalizeId(item.fragranceId), item]));
}

export function recommend(
  fragrances: readonly Fragrance[],
  profile: PreferenceProfile,
  context: RecommendationContext,
  history: readonly WearHistorySummary[] = [],
  options: RecommendationOptions = {},
): RecommendationResult {
  assertValidFragrances(fragrances);
  assertValidProfile(profile);
  assertValidContext(context);

  const weights = resolveWeights(options.weights);
  const limit = Math.max(1, Math.floor(options.limit ?? 3));
  const candidatePoolSize = Math.max(limit, Math.floor(options.candidatePoolSize ?? 10));
  const diversityStrength = options.diversityStrength ?? 0.55;
  const partition = partitionByEligibility(fragrances, profile, context);
  const personalHistory = historyMap(history);

  const allScored = partition.eligible
    .map((fragrance) => scoreFragrance(fragrance, profile, context, personalHistory, weights))
    .sort((left, right) => right.score - left.score || left.fragrance.id.localeCompare(right.fragrance.id));
  const candidatePool = allScored.slice(0, candidatePoolSize);
  const recommendations = diversify(candidatePool, limit, diversityStrength);

  return {
    recommendations,
    candidatePool,
    excluded: partition.excluded,
    weights,
    engineVersion: ENGINE_VERSION,
  };
}
