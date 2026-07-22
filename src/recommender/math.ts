import type { Confidence, WeightedTag } from "../domain/types.ts";

export function clamp(value: number, minimum = 0, maximum = 1): number {
  if (!Number.isFinite(value)) return minimum;
  return Math.min(maximum, Math.max(minimum, value));
}

export function mean(values: readonly number[], fallback = 0.5): number {
  if (values.length === 0) return fallback;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

export function normalizeId(value: string): string {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim()
    .toLocaleLowerCase("pt-BR");
}

export function confidenceValue(confidence: Confidence): number {
  switch (confidence) {
    case "high":
      return 1;
    case "medium":
      return 0.72;
    case "low":
      return 0.4;
    case "unknown":
      return 0.2;
  }
}

export function sampleConfidence(sampleSize?: number): number {
  if (!sampleSize || sampleSize <= 0) return 0.25;
  // Satura gradualmente; evita tratar poucas avaliações como consenso.
  return clamp(1 - Math.exp(-sampleSize / 30));
}

export function distanceFit(actual: number, desired: number, tolerance = 1): number {
  if (tolerance <= 0) return actual === desired ? 1 : 0;
  return clamp(1 - Math.abs(actual - desired) / tolerance);
}

export function rangeFit(value: number, minimum: number, maximum: number, falloff: number): number {
  if (value >= minimum && value <= maximum) return 1;
  const distance = value < minimum ? minimum - value : value - maximum;
  return clamp(1 - distance / Math.max(falloff, 0.001));
}

export function weightedTagMap(tags: readonly WeightedTag[]): Map<string, number> {
  return new Map(tags.map((tag) => [normalizeId(tag.id), clamp(tag.weight)]));
}

export function boundedPreference(value: number | undefined): number | undefined {
  return value === undefined ? undefined : clamp(value, -1, 1);
}

export function preferenceToFit(preference: number): number {
  return clamp((preference + 1) / 2);
}
