import { z } from "zod";

export const OccasionPresetSchema = z.enum([
  "work",
  "date",
  "celebration",
  "casual",
  "outdoor",
  "other",
]);

export type OccasionPreset = z.infer<typeof OccasionPresetSchema>;

export const AtmosphereIntentSchema = z.enum([
  "fresh_luminous",
  "clean_serene",
  "warm_comforting",
  "elegant_memorable",
  "mysterious_magnetic",
  "surprise_me",
]);

export type AtmosphereIntent = z.infer<typeof AtmosphereIntentSchema>;

export const WeatherBandSchema = z.enum(["cold", "mild", "hot"]);
export type WeatherBand = z.infer<typeof WeatherBandSchema>;

export const TimePeriodSchema = z.enum(["morning", "afternoon", "evening", "night"]);
export type TimePeriod = z.infer<typeof TimePeriodSchema>;

export const SettingSchema = z.enum(["indoor", "outdoor", "mixed"]);
export type Setting = z.infer<typeof SettingSchema>;

export const CrowdingSchema = z.enum(["low", "medium", "high"]);
export type Crowding = z.infer<typeof CrowdingSchema>;

export const DiscoveryPreferenceSchema = z.enum(["familiar", "balanced", "exploratory"]);
export type DiscoveryPreference = z.infer<typeof DiscoveryPreferenceSchema>;

export const ContextObservationSchema = z.object({
  field: z.string(),
  origin: z.enum(["browser", "weather", "preset", "user_correction"]),
  observedAt: z.string().optional(),
  confidence: z.enum(["declared", "observed", "curated"]),
});

export type ContextObservation = z.infer<typeof ContextObservationSchema>;

export const DerivedContextSchema = z.object({
  period: TimePeriodSchema,
  setting: SettingSchema,
  crowding: CrowdingSchema,
  weatherBand: WeatherBandSchema,
  temperatureC: z.number().optional(),
  humidity: z.number().optional(),
  values: z.array(ContextObservationSchema).default([]),
});

export type DerivedContext = z.infer<typeof DerivedContextSchema>;

export const ConsultationIntentV2Schema = z.object({
  schemaVersion: z.literal(2),
  occasion: OccasionPresetSchema,
  atmosphere: AtmosphereIntentSchema,
  freeTextOccasion: z.string().optional(),
  knownFragranceIds: z.array(z.string()).default([]),
  avoidedCanonicalIds: z.array(z.string()).default([]),
  hardAvoidNotes: z.array(z.string()).default([]),
  sensitiveEnvironment: z.boolean().default(false),
  budget: z.object({
    currency: z.literal("BRL"),
    maximumCents: z.number().int().positive().optional(),
  }).optional(),
  discovery: DiscoveryPreferenceSchema.default("balanced"),
  customContextOverrides: z.object({
    setting: SettingSchema.optional(),
    weatherBand: WeatherBandSchema.optional(),
    period: TimePeriodSchema.optional(),
  }).optional(),
});

export type ConsultationIntentV2 = z.infer<typeof ConsultationIntentV2Schema>;
