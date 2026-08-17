import test from "node:test";
import assert from "node:assert/strict";

import type { Fragrance } from "./types.ts";
import { deriveSynesthesia } from "./synesthesia.ts";

function createMockFragrance(overrides: Partial<Fragrance>): Fragrance {
  return {
    id: "test-fragrance",
    name: "Test Fragrance",
    brand: "Test House",
    family: "cítrico",
    segments: ["designer"],
    concentrations: ["edp"],
    topNotes: ["bergamota", "limao-siciliano"],
    heartNotes: ["néroli"],
    baseNotes: ["cedro", "musk"],
    accords: [{ id: "cítrico", weight: 0.9 }, { id: "fresco", weight: 0.7 }],
    occasions: [{ id: "trabalho", weight: 0.8 }],
    formality: 0.4,
    performance: {
      longevity: { minimumHours: 6, maximumHours: 8, confidence: "high" },
      projection: { value: 0.6, confidence: "high" },
      sillage: { value: 0.5, confidence: "high" },
    },
    climate: {
      idealTemperatureMinC: 18,
      idealTemperatureMaxC: 32,
      idealHumidity: 0.5,
      indoorFit: 0.9,
      outdoorFit: 0.8,
    },
    priceTier: 3,
    dataConfidence: "high",
    evidence: [{ sourceId: "internal_curated", kind: "curated", confidence: "high" }],
    ...overrides,
  };
}

test("deriva pistas aquáticas/cítricas com som de mar e instrumentos agudos (Mahdavi et al. & Piesse)", () => {
  const citrus = createMockFragrance({
    family: "cítrica",
    accords: [{ id: "cítrico", weight: 0.9 }, { id: "aquático", weight: 0.7 }],
  });

  const profile = deriveSynesthesia(citrus);
  assert.match(profile.naturalSoundscape, /mar|brisa costeira/i);
  assert.match(profile.musicalMood, /piano|fresco|acústico/i);
  assert.equal(profile.voiceProfile.tone, "suave_jovem");
  assert.equal(profile.voiceProfile.tempo, "fresco_dinamico");
  assert.match(profile.chromaticAura.colorFamily, /Azul Oceânico/i);
  assert.ok(profile.emotionalDescriptors.length >= 3);
});

test("deriva pistas amadeiradas com sons de floresta, violão/blues e voz madura (Mahdavi et al.)", () => {
  const woody = createMockFragrance({
    family: "amadeirada",
    accords: [{ id: "amadeirado", weight: 0.95 }, { id: "terroso", weight: 0.8 }],
    topNotes: ["cardamomo"],
    heartNotes: ["cedro"],
    baseNotes: ["vetiver", "patchouli"],
  });

  const profile = deriveSynesthesia(woody);
  assert.match(profile.naturalSoundscape, /floresta|vento|árvores/i);
  assert.match(profile.musicalMood, /blues|violão/i);
  assert.equal(profile.voiceProfile.tone, "grave_madura");
  assert.match(profile.chromaticAura.colorFamily, /Mogno Nobre/i);
  assert.ok(profile.primaryInstruments.includes("Violoncelo") || profile.primaryInstruments.some((i) => i.includes("Violão")));
});

test("deriva pistas orientais/quentes com flamenco/cordas densas e voz intensa (Mahdavi et al.)", () => {
  const oriental = createMockFragrance({
    family: "oriental",
    accords: [{ id: "oriental", weight: 0.9 }, { id: "ambarado", weight: 0.85 }, { id: "especiado-quente", weight: 0.7 }],
    topNotes: ["canela", "cravo"],
    heartNotes: ["benjoim", "ambar"],
    baseNotes: ["baunilha", "fava-tonka", "oud"],
  });

  const profile = deriveSynesthesia(oriental);
  assert.match(profile.naturalSoundscape, /calor|deserto|crepuscular/i);
  assert.match(profile.musicalMood, /flamenco|noturnos quentes|espanhol/i);
  assert.equal(profile.voiceProfile.tone, "intensa_envolvente");
  assert.equal(profile.voiceProfile.tempo, "pausado_envolvente");
  assert.match(profile.chromaticAura.colorFamily, /Vinho Profundo & Âmbar/i);
});

test("deriva pistas florais com sons de jardim, clássica romântica e tons suaves (Mahdavi et al.)", () => {
  const floral = createMockFragrance({
    family: "floral",
    accords: [{ id: "floral", weight: 0.9 }, { id: "flores-brancas", weight: 0.8 }],
    topNotes: ["bergamota"],
    heartNotes: ["jasmim", "rosa-damascena"],
    baseNotes: ["sandalo"],
  });

  const profile = deriveSynesthesia(floral);
  assert.match(profile.naturalSoundscape, /primavera|jardim florido/i);
  assert.match(profile.musicalMood, /romântica|delicadas/i);
  assert.equal(profile.voiceProfile.tone, "suave_jovem");
  assert.match(profile.chromaticAura.colorFamily, /Rosa Pétala & Champanhe/i);
});
