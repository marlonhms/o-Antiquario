import test from "node:test";
import assert from "node:assert/strict";

import { ConsultationIntentV2Schema } from "./consultation-schema.ts";
import { DEFAULT_INTENT_V2, migrateV1ToV2 } from "./migrate-v1-to-v2.ts";
import { deriveContext, deriveAccordWeights, formatContextOneLiner } from "./derive-context.ts";
import { consultationReducer, type ConsultationState } from "./consultation-reducer.ts";

test("schema V2 valida intenção padrão", () => {
  const result = ConsultationIntentV2Schema.safeParse(DEFAULT_INTENT_V2);
  assert.ok(result.success);
});

test("migração V1 para V2 converte ocasiões e descarta campos numéricos obsoletos", () => {
  const legacyV1 = JSON.stringify({
    occasion: "escritório",
    setting: "indoor",
    crowding: "high",
    temperatureC: 32,
    humidity: 0.8,
    durationHours: 8,
    desiredProjection: 0.7,
    maximumPriceTier: 4,
    strictBudget: true,
    sensitiveEnvironment: true,
    noveltyPreference: 0.8,
    likedAccords: ["amadeirado", "cítrico"],
    avoidedAccords: ["doce"],
    hardAvoidNotes: ["baunilha"],
  });

  const migrated = migrateV1ToV2(legacyV1);
  assert.equal(migrated.schemaVersion, 2);
  assert.equal(migrated.occasion, "work");
  assert.equal(migrated.atmosphere, "elegant_memorable");
  assert.equal(migrated.discovery, "exploratory");
  assert.deepEqual(migrated.hardAvoidNotes, ["baunilha"]);
  assert.deepEqual(migrated.avoidedCanonicalIds, ["doce"]);
  assert.equal(migrated.sensitiveEnvironment, true);

  // Garante que campos numéricos obsoletos não foram adicionados
  assert.equal((migrated as Record<string, unknown>).temperatureC, undefined);
  assert.equal((migrated as Record<string, unknown>).durationHours, undefined);
  assert.equal((migrated as Record<string, unknown>).desiredProjection, undefined);
});

test("derivação de contexto produz resumo e pesos consistentes para a atmosfera", () => {
  const intent = {
    ...DEFAULT_INTENT_V2,
    occasion: "work" as const,
    atmosphere: "fresh_luminous" as const,
  };

  const context = deriveContext(intent, new Date("2026-08-17T14:00:00"));
  assert.equal(context.period, "afternoon");
  assert.equal(context.setting, "indoor");
  assert.equal(context.weatherBand, "mild");

  const oneLiner = formatContextOneLiner(context);
  assert.match(oneLiner, /Hoje à tarde/);
  assert.match(oneLiner, /Ambiente interno/);
  assert.match(oneLiner, /Clima ameno/);

  const weights = deriveAccordWeights("fresh_luminous");
  assert.ok(weights["cítrico"] > 0.8);
  assert.ok(weights["aquático"] > 0.8);
});

test("consultationReducer transita passos corretamente ao selecionar momento e atmosfera", () => {
  const initial: ConsultationState = {
    step: "moment",
    intent: DEFAULT_INTENT_V2,
    isRefinementOpen: false,
    isContextCorrectionOpen: false,
  };

  const afterMoment = consultationReducer(initial, {
    type: "SELECT_OCCASION",
    occasion: "date",
  });
  assert.equal(afterMoment.step, "atmosphere");
  assert.equal(afterMoment.intent.occasion, "date");

  const afterAtmosphere = consultationReducer(afterMoment, {
    type: "SELECT_ATMOSPHERE",
    atmosphere: "mysterious_magnetic",
  });
  assert.equal(afterAtmosphere.step, "results");
  assert.equal(afterAtmosphere.intent.atmosphere, "mysterious_magnetic");
});
