import type {
  ExcludedCandidate,
  ExclusionCode,
  Fragrance,
  PreferenceProfile,
  RecommendationContext,
} from "../domain/types.ts";
import { normalizeId } from "./math.ts";

interface Exclusion {
  readonly code: ExclusionCode;
  readonly message: string;
}

function includesNormalized(values: readonly string[] | undefined, target: string): boolean {
  if (!values) return false;
  const normalizedTarget = normalizeId(target);
  return values.some((value) => normalizeId(value) === normalizedTarget);
}

export function exclusionFor(
  fragrance: Fragrance,
  profile: PreferenceProfile,
  context: RecommendationContext,
): Exclusion | undefined {
  if (includesNormalized(context.excludedFragranceIds, fragrance.id)) {
    return {
      code: "explicitly_excluded",
      message: `${fragrance.name} foi excluído deste pedido.`,
    };
  }

  if (includesNormalized(profile.dislikedFragranceIds, fragrance.id)) {
    return {
      code: "explicitly_disliked",
      message: `${fragrance.name} consta como fragrância rejeitada pelo usuário.`,
    };
  }

  const hardAvoids = new Set((profile.hardAvoidNotes ?? []).map(normalizeId));
  const allNotes = [...fragrance.topNotes, ...fragrance.heartNotes, ...fragrance.baseNotes];
  const avoidedNote = allNotes.find((note) => hardAvoids.has(normalizeId(note)));
  if (avoidedNote) {
    return {
      code: "hard_avoided_note",
      message: `${fragrance.name} contém a nota evitada “${avoidedNote}”.`,
    };
  }

  if (context.availableOnly && !includesNormalized(context.collectionIds, fragrance.id)) {
    return {
      code: "not_in_collection",
      message: `${fragrance.name} não está na coleção informada.`,
    };
  }

  if (
    context.strictBudget &&
    context.maximumPriceTier !== undefined &&
    fragrance.priceTier === undefined
  ) {
    return {
      code: "unknown_price_under_strict_budget",
      message: `${fragrance.name} não possui faixa de preço confirmada para um orçamento rígido.`,
    };
  }

  if (
    context.strictBudget &&
    context.maximumPriceTier !== undefined &&
    fragrance.priceTier !== undefined &&
    fragrance.priceTier > context.maximumPriceTier
  ) {
    return {
      code: "over_strict_budget",
      message: `${fragrance.name} está acima da faixa de preço máxima.`,
    };
  }

  if (
    context.projectionCeiling !== undefined &&
    fragrance.performance.projection.value > context.projectionCeiling
  ) {
    return {
      code: "projection_above_ceiling",
      message: `${fragrance.name} excede o teto de projeção do ambiente.`,
    };
  }

  return undefined;
}

export function partitionByEligibility(
  fragrances: readonly Fragrance[],
  profile: PreferenceProfile,
  context: RecommendationContext,
): { eligible: Fragrance[]; excluded: ExcludedCandidate[] } {
  const eligible: Fragrance[] = [];
  const excluded: ExcludedCandidate[] = [];

  for (const fragrance of fragrances) {
    const exclusion = exclusionFor(fragrance, profile, context);
    if (exclusion) {
      excluded.push({ fragranceId: fragrance.id, ...exclusion });
    } else {
      eligible.push(fragrance);
    }
  }

  return { eligible, excluded };
}
