import type {
  Fragrance,
  PreferenceProfile,
  RecommendationContext,
  ScoreFactor,
  ScoredCandidate,
  ScoringWeights,
  WearHistorySummary,
} from "../domain/types.ts";
import {
  boundedPreference,
  clamp,
  confidenceValue,
  distanceFit,
  mean,
  normalizeId,
  preferenceToFit,
  rangeFit,
  sampleConfidence,
  weightedTagMap,
} from "./math.ts";

export const DEFAULT_WEIGHTS: ScoringWeights = Object.freeze({
  preference: 0.3,
  context: 0.25,
  performance: 0.15,
  history: 0.1,
  budget: 0.1,
  confidence: 0.05,
  novelty: 0.05,
});

function normalizedPreferences(values: Readonly<Record<string, number>> | undefined): Map<string, number> {
  return new Map(
    Object.entries(values ?? {}).map(([key, value]) => [normalizeId(key), clamp(value, -1, 1)]),
  );
}

function preferenceFactor(fragrance: Fragrance, profile: PreferenceProfile): Omit<ScoreFactor, "weight" | "contribution"> {
  const notePreferences = normalizedPreferences(profile.notePreferences);
  const accordPreferences = normalizedPreferences(profile.accordPreferences);
  const familyPreferences = normalizedPreferences(profile.familyPreferences);
  const segmentPreferences = normalizedPreferences(profile.segmentPreferences);
  const reasons: string[] = [];
  const values: number[] = [];

  const noteLayers: Array<[readonly string[], number]> = [
    [fragrance.topNotes, 0.75],
    [fragrance.heartNotes, 1],
    [fragrance.baseNotes, 0.9],
  ];

  for (const [notes, layerWeight] of noteLayers) {
    for (const note of notes) {
      const preference = boundedPreference(notePreferences.get(normalizeId(note)));
      if (preference === undefined) continue;
      values.push(preferenceToFit(preference) * layerWeight + 0.5 * (1 - layerWeight));
      if (preference >= 0.5) reasons.push(`combina com a preferência pela nota ${note}`);
      if (preference <= -0.5) reasons.push(`contém a nota pouco apreciada ${note}`);
    }
  }

  for (const accord of fragrance.accords) {
    const preference = boundedPreference(accordPreferences.get(normalizeId(accord.id)));
    if (preference === undefined) continue;
    values.push(preferenceToFit(preference) * clamp(accord.weight) + 0.5 * (1 - clamp(accord.weight)));
    if (preference >= 0.5) reasons.push(`reforça o acorde ${accord.id}`);
    if (preference <= -0.5) reasons.push(`o acorde ${accord.id} pode conflitar com o gosto informado`);
  }

  const familyPreference = boundedPreference(familyPreferences.get(normalizeId(fragrance.family)));
  if (familyPreference !== undefined) {
    values.push(preferenceToFit(familyPreference));
    if (familyPreference >= 0.5) reasons.push(`pertence à família ${fragrance.family} preferida`);
  }

  for (const segment of fragrance.segments) {
    const segmentPreference = boundedPreference(segmentPreferences.get(normalizeId(segment)));
    if (segmentPreference !== undefined) values.push(preferenceToFit(segmentPreference));
  }

  if ((profile.likedFragranceIds ?? []).some((id) => normalizeId(id) === normalizeId(fragrance.id))) {
    values.push(1);
    reasons.push("já foi marcada como apreciada");
  }

  return {
    name: "preference",
    score: mean(values),
    reasons,
  };
}

function contextFactor(fragrance: Fragrance, context: RecommendationContext): Omit<ScoreFactor, "weight" | "contribution"> {
  const reasons: string[] = [];
  const values: number[] = [];

  if (context.occasion) {
    const occasionWeight = weightedTagMap(fragrance.occasions).get(normalizeId(context.occasion));
    values.push(occasionWeight ?? 0.35);
    if (occasionWeight !== undefined && occasionWeight >= 0.7) {
      reasons.push(`tem boa adequação para ${context.occasion}`);
    } else if (occasionWeight === undefined || occasionWeight < 0.45) {
      reasons.push(`tem pouca evidência de adequação para ${context.occasion}`);
    }
  }

  if (context.formality !== undefined) {
    const fit = distanceFit(fragrance.formality, clamp(context.formality), 0.75);
    values.push(fit);
    if (fit >= 0.8) reasons.push("nível de formalidade compatível");
    if (fit < 0.45) reasons.push("formalidade pouco compatível");
  }

  if (
    context.temperatureC !== undefined &&
    fragrance.climate.idealTemperatureMinC !== undefined &&
    fragrance.climate.idealTemperatureMaxC !== undefined
  ) {
    const fit = rangeFit(
      context.temperatureC,
      fragrance.climate.idealTemperatureMinC,
      fragrance.climate.idealTemperatureMaxC,
      14,
    );
    values.push(fit);
    if (fit >= 0.8) reasons.push("faixa térmica favorável");
    if (fit < 0.45) reasons.push("temperatura distante da faixa ideal estimada");
  }

  if (context.humidity !== undefined && fragrance.climate.idealHumidity !== undefined) {
    const fit = distanceFit(clamp(context.humidity), clamp(fragrance.climate.idealHumidity), 0.8);
    values.push(fit);
    if (fit >= 0.8) reasons.push("boa compatibilidade com a umidade informada");
  }

  if (context.setting) {
    const indoor = clamp(fragrance.climate.indoorFit ?? 0.5);
    const outdoor = clamp(fragrance.climate.outdoorFit ?? 0.5);
    const fit = context.setting === "indoor" ? indoor : context.setting === "outdoor" ? outdoor : mean([indoor, outdoor]);
    values.push(fit);
    if (fit >= 0.8) reasons.push(`boa adequação para ambiente ${context.setting}`);
  }

  if (context.crowding === "high" && context.setting !== "outdoor") {
    const crowdFit = distanceFit(fragrance.performance.projection.value, 0.35, 0.8);
    values.push(crowdFit);
    if (crowdFit < 0.5) reasons.push("a projeção pode incomodar em ambiente cheio");
  }

  return { name: "context", score: mean(values), reasons };
}

function performanceFactor(
  fragrance: Fragrance,
  context: RecommendationContext,
): Omit<ScoreFactor, "weight" | "contribution"> {
  const reasons: string[] = [];
  const values: number[] = [];

  if (context.desiredProjection !== undefined) {
    const fit = distanceFit(
      fragrance.performance.projection.value,
      clamp(context.desiredProjection),
      0.85,
    );
    values.push(fit);
    if (fit >= 0.82) reasons.push("projeção próxima da desejada");
    if (fit < 0.45) reasons.push("projeção distante da desejada");
  }

  if (context.durationHours !== undefined) {
    const { minimumHours, maximumHours } = fragrance.performance.longevity;
    const fit = rangeFit(context.durationHours, minimumHours, maximumHours, 5);
    values.push(fit);
    if (fit >= 0.8) reasons.push("duração estimada cobre o período desejado");
    if (context.durationHours > maximumHours && fit < 0.65) reasons.push("pode exigir reaplicação");
  }

  return { name: "performance", score: mean(values), reasons };
}

function historyFactor(
  fragrance: Fragrance,
  history: ReadonlyMap<string, WearHistorySummary>,
): Omit<ScoreFactor, "weight" | "contribution"> {
  const record = history.get(normalizeId(fragrance.id));
  if (!record || record.wearCount <= 0) {
    return { name: "history", score: 0.5, reasons: ["ainda sem histórico pessoal suficiente"] };
  }

  const values: number[] = [];
  if (record.wouldWearAgainRate !== undefined) values.push(clamp(record.wouldWearAgainRate));
  if (record.averageRating !== undefined) values.push(clamp(record.averageRating / 5));

  // Evidência pessoal cresce com o número de usos, mas mantém prior neutro.
  const evidenceStrength = clamp(1 - Math.exp(-record.wearCount / 5));
  const observed = mean(values);
  const score = 0.5 + (observed - 0.5) * evidenceStrength;
  const reasons = [
    score >= 0.65
      ? `histórico pessoal positivo em ${record.wearCount} uso(s)`
      : score <= 0.4
        ? `histórico pessoal desfavorável em ${record.wearCount} uso(s)`
        : "histórico pessoal ainda inconclusivo",
  ];

  return { name: "history", score, reasons };
}

function budgetFactor(fragrance: Fragrance, context: RecommendationContext): Omit<ScoreFactor, "weight" | "contribution"> {
  if (context.maximumPriceTier === undefined || fragrance.priceTier === undefined) {
    return { name: "budget", score: 0.6, reasons: ["faixa de preço não comparável"] };
  }

  const delta = fragrance.priceTier - context.maximumPriceTier;
  if (delta <= 0) return { name: "budget", score: 1, reasons: ["dentro da faixa de preço"] };
  if (delta === 1) return { name: "budget", score: 0.4, reasons: ["ligeiramente acima da faixa de preço"] };
  return { name: "budget", score: 0.08, reasons: ["acima da faixa de preço"] };
}

function confidenceFactor(fragrance: Fragrance): Omit<ScoreFactor, "weight" | "contribution"> {
  const performance = fragrance.performance;
  const metricConfidences = [
    confidenceValue(fragrance.dataConfidence),
    confidenceValue(performance.longevity.confidence),
    confidenceValue(performance.projection.confidence),
    confidenceValue(performance.sillage.confidence),
  ];
  const sampleSizes = [
    performance.longevity.sampleSize,
    performance.projection.sampleSize,
    performance.sillage.sampleSize,
  ].filter((value): value is number => value !== undefined);

  const evidenceConfidence = mean(fragrance.evidence.map((item) => confidenceValue(item.confidence)), 0.35);
  const sampleScore = mean(sampleSizes.map(sampleConfidence), 0.35);
  const score = mean([...metricConfidences, evidenceConfidence, sampleScore]);

  return {
    name: "confidence",
    score,
    reasons: [
      score >= 0.78
        ? "dados com boa sustentação"
        : score < 0.45
          ? "dados escassos ou estimados"
          : "confiança moderada nos dados",
    ],
  };
}

function noveltyFactor(
  fragrance: Fragrance,
  profile: PreferenceProfile,
  history: ReadonlyMap<string, WearHistorySummary>,
): Omit<ScoreFactor, "weight" | "contribution"> {
  const desiredNovelty = clamp(profile.noveltyPreference ?? 0.45);
  const wearCount = history.get(normalizeId(fragrance.id))?.wearCount ?? 0;
  const actualNovelty = Math.exp(-wearCount / 4);
  const score = distanceFit(actualNovelty, desiredNovelty, 1);

  return {
    name: "novelty",
    score,
    reasons: [
      actualNovelty > 0.75
        ? "oferece descoberta"
        : actualNovelty < 0.3
          ? "é uma escolha familiar"
          : "equilibra familiaridade e descoberta",
    ],
  };
}

function attachWeight(
  factor: Omit<ScoreFactor, "weight" | "contribution">,
  weights: ScoringWeights,
): ScoreFactor {
  const weight = weights[factor.name];
  return {
    ...factor,
    score: clamp(factor.score),
    weight,
    contribution: clamp(factor.score) * weight,
  };
}

function summarizeFactors(factors: readonly ScoreFactor[]): { strengths: string[]; tradeoffs: string[] } {
  const ranked = [...factors].sort((a, b) => b.contribution - a.contribution);
  const strengths = ranked
    .filter((factor) => factor.score >= 0.65)
    .flatMap((factor) => factor.reasons.filter((reason) => !reason.includes("pouca") && !reason.includes("distante")))
    .slice(0, 4);
  const tradeoffs = [...factors]
    .filter((factor) => factor.score < 0.55)
    .sort((a, b) => a.score - b.score)
    .flatMap((factor) => factor.reasons)
    .filter((reason) =>
      ["pouca", "distante", "acima", "reaplicação", "escassos"].some((term) =>
        reason.includes(term),
      ),
    )
    .slice(0, 3);

  return {
    strengths: strengths.length > 0 ? strengths : ["compatibilidade geral equilibrada"],
    tradeoffs,
  };
}

export function scoreFragrance(
  fragrance: Fragrance,
  profile: PreferenceProfile,
  context: RecommendationContext,
  history: ReadonlyMap<string, WearHistorySummary>,
  weights: ScoringWeights,
): ScoredCandidate {
  const factors = [
    preferenceFactor(fragrance, profile),
    contextFactor(fragrance, context),
    performanceFactor(fragrance, context),
    historyFactor(fragrance, history),
    budgetFactor(fragrance, context),
    confidenceFactor(fragrance),
    noveltyFactor(fragrance, profile, history),
  ].map((factor) => attachWeight(factor, weights));

  const rawScore = factors.reduce((sum, factor) => sum + factor.contribution, 0);
  const confidence = factors.find((factor) => factor.name === "confidence")?.score ?? 0.2;
  // Baixa confiança aproxima o resultado do prior neutro, evitando falsos vencedores.
  const score = 0.5 + (rawScore - 0.5) * (0.65 + confidence * 0.35);
  const { strengths, tradeoffs } = summarizeFactors(factors);

  return {
    fragrance,
    score: clamp(score),
    rawScore: clamp(rawScore),
    confidence,
    factors,
    strengths,
    tradeoffs,
  };
}

export function resolveWeights(overrides: Partial<ScoringWeights> | undefined): ScoringWeights {
  const merged: ScoringWeights = { ...DEFAULT_WEIGHTS, ...overrides };
  const entries = Object.entries(merged) as Array<[keyof ScoringWeights, number]>;

  for (const [name, value] of entries) {
    if (!Number.isFinite(value) || value < 0) {
      throw new RangeError(`Peso inválido para ${name}: ${value}`);
    }
  }

  const total = entries.reduce((sum, [, value]) => sum + value, 0);
  if (total <= 0) throw new RangeError("A soma dos pesos deve ser maior que zero.");

  return Object.freeze(
    Object.fromEntries(entries.map(([name, value]) => [name, value / total])) as unknown as ScoringWeights,
  );
}
