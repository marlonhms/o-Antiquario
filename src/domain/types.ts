export type Confidence = "high" | "medium" | "low" | "unknown";

export type EvidenceKind =
  | "manufacturer"
  | "open_source"
  | "curated"
  | "community"
  | "estimated"
  | "user";

export interface Evidence {
  readonly sourceId: string;
  readonly kind: EvidenceKind;
  readonly confidence: Confidence;
  readonly license?: string;
  readonly sourceUrl?: string;
  readonly retrievedAt?: string;
  readonly sampleSize?: number;
}

export interface WeightedTag {
  readonly id: string;
  readonly weight: number;
}

export interface MetricEstimate {
  /** Valor normalizado entre 0 e 1. */
  readonly value: number;
  readonly confidence: Confidence;
  readonly sampleSize?: number;
  readonly evidence?: readonly Evidence[];
}

export interface LongevityEstimate {
  readonly minimumHours: number;
  readonly maximumHours: number;
  readonly confidence: Confidence;
  readonly sampleSize?: number;
  readonly evidence?: readonly Evidence[];
}

export interface PerformanceProfile {
  readonly longevity: LongevityEstimate;
  readonly projection: MetricEstimate;
  readonly sillage: MetricEstimate;
}

export interface ClimateProfile {
  readonly idealTemperatureMinC?: number;
  readonly idealTemperatureMaxC?: number;
  /** Preferência de umidade normalizada entre 0 (seca) e 1 (úmida). */
  readonly idealHumidity?: number;
  readonly indoorFit?: number;
  readonly outdoorFit?: number;
}

export interface Fragrance {
  readonly id: string;
  readonly name: string;
  readonly brand: string;
  readonly family: string;
  readonly segments: readonly string[];
  readonly concentrations: readonly string[];
  readonly topNotes: readonly string[];
  readonly heartNotes: readonly string[];
  readonly baseNotes: readonly string[];
  readonly accords: readonly WeightedTag[];
  readonly occasions: readonly WeightedTag[];
  /** 0 = casual, 1 = muito formal. */
  readonly formality: number;
  readonly performance: PerformanceProfile;
  readonly climate: ClimateProfile;
  /** Faixa relativa de preço de 1 a 5. */
  readonly priceTier?: 1 | 2 | 3 | 4 | 5;
  readonly dataConfidence: Confidence;
  readonly evidence: readonly Evidence[];
}

export interface PreferenceProfile {
  /** Valores entre -1 (rejeita) e 1 (adora). */
  readonly notePreferences?: Readonly<Record<string, number>>;
  readonly accordPreferences?: Readonly<Record<string, number>>;
  readonly familyPreferences?: Readonly<Record<string, number>>;
  readonly segmentPreferences?: Readonly<Record<string, number>>;
  readonly hardAvoidNotes?: readonly string[];
  readonly likedFragranceIds?: readonly string[];
  readonly dislikedFragranceIds?: readonly string[];
  /** 0 = familiaridade, 1 = descoberta. */
  readonly noveltyPreference?: number;
}

export interface WearHistorySummary {
  readonly fragranceId: string;
  readonly wearCount: number;
  readonly wouldWearAgainRate?: number;
  readonly averageRating?: number;
  readonly averageLongevityHours?: number;
  readonly averageProjection?: number;
}

export type Setting = "indoor" | "outdoor" | "mixed";
export type Crowding = "low" | "medium" | "high";

export interface RecommendationContext {
  readonly occasion?: string;
  readonly temperatureC?: number;
  /** Umidade relativa normalizada entre 0 e 1. */
  readonly humidity?: number;
  readonly setting?: Setting;
  readonly crowding?: Crowding;
  readonly formality?: number;
  readonly desiredProjection?: number;
  readonly durationHours?: number;
  readonly maximumPriceTier?: 1 | 2 | 3 | 4 | 5;
  readonly strictBudget?: boolean;
  readonly availableOnly?: boolean;
  readonly collectionIds?: readonly string[];
  readonly excludedFragranceIds?: readonly string[];
  /** Teto rígido de projeção para ambientes sensíveis. */
  readonly projectionCeiling?: number;
}

export interface ScoringWeights {
  readonly preference: number;
  readonly context: number;
  readonly performance: number;
  readonly history: number;
  readonly budget: number;
  readonly confidence: number;
  readonly novelty: number;
}

export type ScoreFactorName = keyof ScoringWeights;

export interface ScoreFactor {
  readonly name: ScoreFactorName;
  readonly score: number;
  readonly weight: number;
  readonly contribution: number;
  readonly reasons: readonly string[];
}

export interface ScoredCandidate {
  readonly fragrance: Fragrance;
  readonly score: number;
  readonly rawScore: number;
  readonly confidence: number;
  readonly factors: readonly ScoreFactor[];
  readonly strengths: readonly string[];
  readonly tradeoffs: readonly string[];
}

export type ExclusionCode =
  | "explicitly_excluded"
  | "explicitly_disliked"
  | "hard_avoided_note"
  | "not_in_collection"
  | "over_strict_budget"
  | "unknown_price_under_strict_budget"
  | "projection_above_ceiling";

export interface ExcludedCandidate {
  readonly fragranceId: string;
  readonly code: ExclusionCode;
  readonly message: string;
}

export interface RecommendationOptions {
  readonly limit?: number;
  readonly candidatePoolSize?: number;
  /** 0 desliga a diversidade; 1 aplica a penalidade máxima. */
  readonly diversityStrength?: number;
  readonly weights?: Partial<ScoringWeights>;
}

export interface RecommendationResult {
  readonly recommendations: readonly ScoredCandidate[];
  readonly candidatePool: readonly ScoredCandidate[];
  readonly excluded: readonly ExcludedCandidate[];
  readonly weights: ScoringWeights;
  readonly engineVersion: string;
}
