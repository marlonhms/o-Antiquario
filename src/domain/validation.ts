import type { Fragrance, PreferenceProfile, RecommendationContext, WeightedTag } from "./types.ts";

function assertNonEmpty(value: string, label: string): void {
  if (!value.trim()) throw new TypeError(`${label} não pode ser vazio.`);
}

function assertFinite(value: number, label: string): void {
  if (!Number.isFinite(value)) throw new RangeError(`${label} deve ser um número finito.`);
}

function assertUnit(value: number, label: string): void {
  assertFinite(value, label);
  if (value < 0 || value > 1) throw new RangeError(`${label} deve estar entre 0 e 1.`);
}

function assertOptionalUnit(value: number | undefined, label: string): void {
  if (value !== undefined) assertUnit(value, label);
}

function assertTags(tags: readonly WeightedTag[], label: string): void {
  const ids = new Set<string>();
  for (const tag of tags) {
    assertNonEmpty(tag.id, `${label}.id`);
    assertUnit(tag.weight, `${label}.${tag.id}.weight`);
    const id = tag.id.trim().toLocaleLowerCase("pt-BR");
    if (ids.has(id)) throw new TypeError(`${label} contém o identificador duplicado “${tag.id}”.`);
    ids.add(id);
  }
}

export function assertValidFragrance(fragrance: Fragrance): void {
  assertNonEmpty(fragrance.id, "fragrance.id");
  assertNonEmpty(fragrance.name, `${fragrance.id}.name`);
  assertNonEmpty(fragrance.brand, `${fragrance.id}.brand`);
  assertNonEmpty(fragrance.family, `${fragrance.id}.family`);
  assertUnit(fragrance.formality, `${fragrance.id}.formality`);
  assertTags(fragrance.accords, `${fragrance.id}.accords`);
  assertTags(fragrance.occasions, `${fragrance.id}.occasions`);

  const { performance, climate } = fragrance;
  assertFinite(performance.longevity.minimumHours, `${fragrance.id}.longevity.minimumHours`);
  assertFinite(performance.longevity.maximumHours, `${fragrance.id}.longevity.maximumHours`);
  if (performance.longevity.minimumHours < 0) {
    throw new RangeError(`${fragrance.id}.longevity.minimumHours não pode ser negativo.`);
  }
  if (performance.longevity.maximumHours < performance.longevity.minimumHours) {
    throw new RangeError(`${fragrance.id}.longevity possui intervalo invertido.`);
  }
  assertUnit(performance.projection.value, `${fragrance.id}.projection.value`);
  assertUnit(performance.sillage.value, `${fragrance.id}.sillage.value`);

  if (climate.idealTemperatureMinC !== undefined) {
    assertFinite(climate.idealTemperatureMinC, `${fragrance.id}.climate.idealTemperatureMinC`);
  }
  if (climate.idealTemperatureMaxC !== undefined) {
    assertFinite(climate.idealTemperatureMaxC, `${fragrance.id}.climate.idealTemperatureMaxC`);
  }
  if (
    climate.idealTemperatureMinC !== undefined &&
    climate.idealTemperatureMaxC !== undefined &&
    climate.idealTemperatureMaxC < climate.idealTemperatureMinC
  ) {
    throw new RangeError(`${fragrance.id}.climate possui intervalo térmico invertido.`);
  }
  assertOptionalUnit(climate.idealHumidity, `${fragrance.id}.climate.idealHumidity`);
  assertOptionalUnit(climate.indoorFit, `${fragrance.id}.climate.indoorFit`);
  assertOptionalUnit(climate.outdoorFit, `${fragrance.id}.climate.outdoorFit`);

  if (fragrance.priceTier !== undefined && (!Number.isInteger(fragrance.priceTier) || fragrance.priceTier < 1 || fragrance.priceTier > 5)) {
    throw new RangeError(`${fragrance.id}.priceTier deve ser um inteiro entre 1 e 5.`);
  }
}

export function assertValidFragrances(fragrances: readonly Fragrance[]): void {
  const ids = new Set<string>();
  for (const fragrance of fragrances) {
    assertValidFragrance(fragrance);
    const id = fragrance.id.trim().toLocaleLowerCase("pt-BR");
    if (ids.has(id)) throw new TypeError(`Identificador duplicado: ${fragrance.id}`);
    ids.add(id);
  }
}

function assertPreferenceRecord(values: Readonly<Record<string, number>> | undefined, label: string): void {
  for (const [key, value] of Object.entries(values ?? {})) {
    assertNonEmpty(key, `${label}.key`);
    assertFinite(value, `${label}.${key}`);
    if (value < -1 || value > 1) throw new RangeError(`${label}.${key} deve estar entre -1 e 1.`);
  }
}

export function assertValidProfile(profile: PreferenceProfile): void {
  assertPreferenceRecord(profile.notePreferences, "notePreferences");
  assertPreferenceRecord(profile.accordPreferences, "accordPreferences");
  assertPreferenceRecord(profile.familyPreferences, "familyPreferences");
  assertPreferenceRecord(profile.segmentPreferences, "segmentPreferences");
  assertOptionalUnit(profile.noveltyPreference, "noveltyPreference");
}

export function assertValidContext(context: RecommendationContext): void {
  assertOptionalUnit(context.humidity, "humidity");
  assertOptionalUnit(context.formality, "formality");
  assertOptionalUnit(context.desiredProjection, "desiredProjection");
  assertOptionalUnit(context.projectionCeiling, "projectionCeiling");

  if (context.temperatureC !== undefined) {
    assertFinite(context.temperatureC, "temperatureC");
    if (context.temperatureC < -90 || context.temperatureC > 60) {
      throw new RangeError("temperatureC está fora da faixa operacional de -90 a 60 °C.");
    }
  }

  if (context.durationHours !== undefined) {
    assertFinite(context.durationHours, "durationHours");
    if (context.durationHours <= 0 || context.durationHours > 168) {
      throw new RangeError("durationHours deve ser maior que zero e menor ou igual a 168.");
    }
  }
}
