import type {
  AtmosphereIntent,
  ConsultationIntentV2,
  DerivedContext,
  OccasionPreset,
  Setting,
  TimePeriod,
  WeatherBand,
} from "./consultation-schema.ts";

export function deriveTimePeriod(date: Date = new Date()): TimePeriod {
  const hour = date.getHours();
  if (hour >= 5 && hour < 12) return "morning";
  if (hour >= 12 && hour < 18) return "afternoon";
  if (hour >= 18 && hour < 23) return "evening";
  return "night";
}

export function formatPeriodLabel(period: TimePeriod): string {
  switch (period) {
    case "morning":
      return "Hoje pela manhã";
    case "afternoon":
      return "Hoje à tarde";
    case "evening":
      return "Hoje à noite";
    case "night":
      return "Madrugada";
  }
}

export function formatSettingLabel(setting: Setting): string {
  switch (setting) {
    case "indoor":
      return "Ambiente interno";
    case "outdoor":
      return "Ao ar livre";
    case "mixed":
      return "Ambiente misto";
  }
}

export function formatWeatherBandLabel(band: WeatherBand): string {
  switch (band) {
    case "cold":
      return "Clima fresco/frio";
    case "mild":
      return "Clima ameno";
    case "hot":
      return "Clima quente";
  }
}

export function deriveContext(
  intent: ConsultationIntentV2,
  now: Date = new Date(),
): DerivedContext {
  const period = intent.customContextOverrides?.period ?? deriveTimePeriod(now);

  let defaultSetting: Setting = "indoor";
  let defaultCrowding: DerivedContext["crowding"] = "medium";
  let defaultWeather: WeatherBand = "mild";

  switch (intent.occasion) {
    case "work":
      defaultSetting = "indoor";
      defaultCrowding = "medium";
      defaultWeather = "mild";
      break;
    case "date":
      defaultSetting = "indoor";
      defaultCrowding = "low";
      defaultWeather = "mild";
      break;
    case "celebration":
      defaultSetting = "mixed";
      defaultCrowding = "high";
      defaultWeather = "mild";
      break;
    case "outdoor":
      defaultSetting = "outdoor";
      defaultCrowding = "medium";
      defaultWeather = "hot";
      break;
    case "casual":
      defaultSetting = "mixed";
      defaultCrowding = "medium";
      defaultWeather = "mild";
      break;
    case "other":
      defaultSetting = "mixed";
      defaultCrowding = "medium";
      defaultWeather = "mild";
      break;
  }

  const setting = intent.customContextOverrides?.setting ?? defaultSetting;
  const weatherBand = intent.customContextOverrides?.weatherBand ?? defaultWeather;

  return {
    period,
    setting,
    crowding: defaultCrowding,
    weatherBand,
    temperatureC: weatherBand === "hot" ? 30 : weatherBand === "cold" ? 16 : 22,
    humidity: 0.65,
    values: [
      {
        field: "period",
        origin: intent.customContextOverrides?.period ? "user_correction" : "browser",
        confidence: "observed",
      },
      {
        field: "setting",
        origin: intent.customContextOverrides?.setting ? "user_correction" : "preset",
        confidence: intent.customContextOverrides?.setting ? "declared" : "curated",
      },
      {
        field: "weatherBand",
        origin: intent.customContextOverrides?.weatherBand ? "user_correction" : "preset",
        confidence: intent.customContextOverrides?.weatherBand ? "declared" : "curated",
      },
    ],
  };
}

export function formatContextOneLiner(context: DerivedContext): string {
  const period = formatPeriodLabel(context.period);
  const setting = formatSettingLabel(context.setting);
  const weather = formatWeatherBandLabel(context.weatherBand);
  return `${period} · ${setting} · ${weather}`;
}

export function deriveAccordWeights(atmosphere: AtmosphereIntent): Record<string, number> {
  switch (atmosphere) {
    case "fresh_luminous":
      return { cítrico: 0.95, aquático: 0.85, fresco: 0.9, aromático: 0.7 };
    case "clean_serene":
      return { aromático: 0.95, verde: 0.85, atalcado: 0.75, floral: 0.65 };
    case "warm_comforting":
      return { gourmand: 0.9, doce: 0.85, baunilha: 0.95, ambarado: 0.75 };
    case "elegant_memorable":
      return { amadeirado: 0.95, chipre: 0.85, floral: 0.75, especiado: 0.65 };
    case "mysterious_magnetic":
      return { oriental: 0.95, especiado: 0.9, ambarado: 0.85, couro: 0.8 };
    case "surprise_me":
      return {};
  }
}

export function deriveFormalityByOccasion(occasion: OccasionPreset): number {
  switch (occasion) {
    case "casual":
      return 0.25;
    case "outdoor":
      return 0.2;
    case "work":
      return 0.62;
    case "date":
      return 0.68;
    case "celebration":
      return 0.85;
    case "other":
      return 0.5;
  }
}
