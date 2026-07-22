import type { Fragrance, ScoredCandidate } from "../domain/types.ts";
import { clamp, normalizeId } from "./math.ts";

function jaccard(left: ReadonlySet<string>, right: ReadonlySet<string>): number {
  const union = new Set([...left, ...right]);
  if (union.size === 0) return 0;
  let intersection = 0;
  for (const item of left) if (right.has(item)) intersection += 1;
  return intersection / union.size;
}

function normalizedSet(values: readonly string[]): Set<string> {
  return new Set(values.map(normalizeId));
}

export function fragranceSimilarity(left: Fragrance, right: Fragrance): number {
  if (left.id === right.id) return 1;

  const leftNotes = normalizedSet([...left.topNotes, ...left.heartNotes, ...left.baseNotes]);
  const rightNotes = normalizedSet([...right.topNotes, ...right.heartNotes, ...right.baseNotes]);
  const leftAccords = normalizedSet(left.accords.map((accord) => accord.id));
  const rightAccords = normalizedSet(right.accords.map((accord) => accord.id));
  const familyMatch = normalizeId(left.family) === normalizeId(right.family) ? 1 : 0;
  const brandMatch = normalizeId(left.brand) === normalizeId(right.brand) ? 1 : 0;

  return clamp(
    jaccard(leftNotes, rightNotes) * 0.45 +
      jaccard(leftAccords, rightAccords) * 0.35 +
      familyMatch * 0.15 +
      brandMatch * 0.05,
  );
}

export function diversify(
  candidates: readonly ScoredCandidate[],
  limit: number,
  diversityStrength: number,
): ScoredCandidate[] {
  if (limit <= 0 || candidates.length === 0) return [];
  const remaining = [...candidates];
  const selected: ScoredCandidate[] = [remaining.shift()!];
  const strength = clamp(diversityStrength);

  while (selected.length < limit && remaining.length > 0) {
    let bestIndex = 0;
    let bestUtility = Number.NEGATIVE_INFINITY;

    for (let index = 0; index < remaining.length; index += 1) {
      const candidate = remaining[index]!;
      const maximumSimilarity = Math.max(
        ...selected.map((item) => fragranceSimilarity(candidate.fragrance, item.fragrance)),
      );
      // A qualidade continua dominante; diversidade desempata candidatos próximos.
      const utility = candidate.score - strength * maximumSimilarity * 0.22;
      if (utility > bestUtility) {
        bestUtility = utility;
        bestIndex = index;
      }
    }

    selected.push(remaining.splice(bestIndex, 1)[0]!);
  }

  // A diversidade decide a composição do conjunto; a apresentação final
  // permanece ordenada pela compatibilidade calculada.
  return selected.sort(
    (left, right) => right.score - left.score || left.fragrance.id.localeCompare(right.fragrance.id),
  );
}
