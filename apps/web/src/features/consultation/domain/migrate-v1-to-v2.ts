import {
  type AtmosphereIntent,
  type ConsultationIntentV2,
  type OccasionPreset,
  ConsultationIntentV2Schema,
} from "./consultation-schema.ts";

export const STORAGE_KEY_V2 = "o-antiquario:consultation-intent:v2";
export const STORAGE_KEY_V1 = "o-antiquario:consultant-form:v1";

export const DEFAULT_INTENT_V2: ConsultationIntentV2 = {
  schemaVersion: 2,
  occasion: "work",
  atmosphere: "fresh_luminous",
  knownFragranceIds: [],
  avoidedCanonicalIds: ["doce"],
  hardAvoidNotes: [],
  sensitiveEnvironment: true,
  discovery: "balanced",
};

function mapV1Occasion(occasion: string | undefined): OccasionPreset {
  if (!occasion) return "work";
  const normalized = occasion.toLowerCase().trim();
  if (normalized.includes("escritório") || normalized.includes("trabalho")) return "work";
  if (normalized.includes("encontro")) return "date";
  if (normalized.includes("festa") || normalized.includes("formal") || normalized.includes("celebração")) return "celebration";
  if (normalized.includes("ar livre") || normalized.includes("esporte")) return "outdoor";
  if (normalized.includes("casual")) return "casual";
  return "other";
}

function mapV1Atmosphere(likedAccords: readonly string[] | undefined): AtmosphereIntent {
  if (!likedAccords || likedAccords.length === 0) return "fresh_luminous";
  const set = new Set(likedAccords.map((a) => a.toLowerCase().trim()));

  if (set.has("oriental") || set.has("especiado") || set.has("couro") || set.has("âmbar")) {
    return "mysterious_magnetic";
  }
  if (set.has("amadeirado") || set.has("chipre")) {
    return "elegant_memorable";
  }
  if (set.has("doce") || set.has("baunilha") || set.has("gourmand")) {
    return "warm_comforting";
  }
  if (set.has("aromático") || set.has("verde") || set.has("atalcado")) {
    return "clean_serene";
  }
  if (set.has("cítrico") || set.has("aquático") || set.has("fresco")) {
    return "fresh_luminous";
  }
  return "fresh_luminous";
}

/**
 * Migra dados legados V1 para o contrato V2, descartando campos numéricos/abstratos
 * e garantindo que o estado retornado seja 100% válido.
 */
export function migrateV1ToV2(storedRawJson: string | null): ConsultationIntentV2 {
  if (!storedRawJson) return DEFAULT_INTENT_V2;

  try {
    const parsed: unknown = JSON.parse(storedRawJson);
    if (!parsed || typeof parsed !== "object") return DEFAULT_INTENT_V2;

    // Se já estiver no schema V2
    if ("schemaVersion" in parsed && (parsed as { schemaVersion: unknown }).schemaVersion === 2) {
      const result = ConsultationIntentV2Schema.safeParse(parsed);
      if (result.success) return result.data;
    }

    // Caso contrário, migra da V1
    const v1 = parsed as Record<string, unknown>;
    const occasion = mapV1Occasion(typeof v1.occasion === "string" ? v1.occasion : undefined);
    const likedAccords = Array.isArray(v1.likedAccords) ? v1.likedAccords.filter((i): i is string => typeof i === "string") : [];
    const avoidedAccords = Array.isArray(v1.avoidedAccords) ? v1.avoidedAccords.filter((i): i is string => typeof i === "string") : [];
    const hardAvoidNotes = Array.isArray(v1.hardAvoidNotes) ? v1.hardAvoidNotes.filter((i): i is string => typeof i === "string") : [];

    const novelty = typeof v1.noveltyPreference === "number" ? v1.noveltyPreference : 0.5;
    const discovery = novelty < 0.35 ? "familiar" : novelty > 0.65 ? "exploratory" : "balanced";

    return {
      schemaVersion: 2,
      occasion,
      atmosphere: mapV1Atmosphere(likedAccords),
      knownFragranceIds: [],
      avoidedCanonicalIds: avoidedAccords,
      hardAvoidNotes,
      sensitiveEnvironment: typeof v1.sensitiveEnvironment === "boolean" ? v1.sensitiveEnvironment : false,
      discovery,
    };
  } catch {
    return DEFAULT_INTENT_V2;
  }
}
