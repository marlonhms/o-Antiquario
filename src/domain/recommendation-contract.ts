import { z } from "zod";

import type { Confidence, Fragrance } from "./types.ts";

export const ConfidenceSchema = z.enum(["high", "medium", "low", "unknown"]);
export const EvidenceKindSchema = z.enum([
  "manufacturer",
  "open_source",
  "curated",
  "community",
  "estimated",
  "user",
]);

export const EvidenceSchema = z.object({
  sourceId: z.string().min(1),
  kind: EvidenceKindSchema,
  confidence: ConfidenceSchema,
  license: z.string().optional(),
  sourceUrl: z.string().url().optional(),
  retrievedAt: z.string().optional(),
  sampleSize: z.number().nonnegative().optional(),
}).strict();

export const WeightedTagSchema = z.object({
  id: z.string().min(1),
  weight: z.number().min(0).max(1),
}).strict();

export const MetricEstimateSchema = z.object({
  value: z.number().min(0).max(1),
  confidence: ConfidenceSchema,
  sampleSize: z.number().nonnegative().optional(),
  evidence: z.array(EvidenceSchema).optional(),
}).strict();

export const LongevityEstimateSchema = z.object({
  minimumHours: z.number().nonnegative(),
  maximumHours: z.number().nonnegative(),
  confidence: ConfidenceSchema,
  sampleSize: z.number().nonnegative().optional(),
  evidence: z.array(EvidenceSchema).optional(),
}).strict();

export const PerformanceProfileSchema = z.object({
  longevity: LongevityEstimateSchema,
  projection: MetricEstimateSchema,
  sillage: MetricEstimateSchema,
}).strict();

export const ClimateProfileSchema = z.object({
  idealTemperatureMinC: z.number().optional(),
  idealTemperatureMaxC: z.number().optional(),
  idealHumidity: z.number().min(0).max(1).optional(),
  indoorFit: z.number().min(0).max(1).optional(),
  outdoorFit: z.number().min(0).max(1).optional(),
}).strict();

export const EligibleForRecommendationSchema = z.object({
  id: z.string().min(1),
  name: z.string().min(1),
  brand: z.string().min(1),
  family: z.string().min(1),
  segments: z.array(z.string()).readonly(),
  concentrations: z.array(z.string()).min(1, "ao menos uma concentração é exigida").readonly(),
  topNotes: z.array(z.string()).readonly(),
  heartNotes: z.array(z.string()).readonly(),
  baseNotes: z.array(z.string()).readonly(),
  accords: z.array(WeightedTagSchema).readonly(),
  occasions: z.array(WeightedTagSchema).readonly(),
  formality: z.number().min(0).max(1),
  performance: PerformanceProfileSchema,
  climate: ClimateProfileSchema,
  priceTier: z.union([z.literal(1), z.literal(2), z.literal(3), z.literal(4), z.literal(5)]).optional(),
  dataConfidence: ConfidenceSchema,
  evidence: z.array(EvidenceSchema).min(1, "ao menos uma evidência aprovada é exigida").readonly(),
}).strict();

export type EligibleForRecommendation = Fragrance;


export interface RecommendationGateReport {
  readonly eligibleCount: number;
  readonly minimumRequired: number;
  readonly passesGate: boolean;
  readonly invalidReasons: readonly { readonly id: string; readonly issues: readonly string[] }[];
}

export function validateRecommendationEligibility(input: unknown): {
  readonly success: boolean;
  readonly data?: EligibleForRecommendation;
  readonly issues?: readonly string[];
} {
  const result = EligibleForRecommendationSchema.safeParse(input);
  if (result.success) {
    return { success: true, data: result.data as Fragrance };
  }
  return {
    success: false,
    issues: result.error.issues.map((issue) => `${issue.path.join(".")}: ${issue.message}`),
  };
}
