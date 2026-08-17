import type { Fragrance } from "./types.ts";

/**
 * Pistas transmodais baseadas no estudo científico de correspondências
 * olfativas-auditivas (Mahdavi et al., 2020), oitavas de Piesse (1867),
 * experimentos de Spence & Crisinel (2012) e sinestesia aroma-cor (Myrissi / Givaudan).
 */
export interface VoiceProfile {
  readonly tone: "suave_jovem" | "aveludada_calma" | "grave_madura" | "intensa_envolvente";
  readonly tempo: "fresco_dinamico" | "suave_moderado" | "pausado_envolvente";
  readonly description: string;
}

export interface ChromaticAura {
  readonly dominantHsl: string;
  readonly secondaryHsl: string;
  readonly accentHsl: string;
  readonly gradientCss: string;
  readonly colorFamily: string;
}

export interface SynestheticProfile {
  /** Pista da natureza correspondente (Mahdavi et al., Tabela 5) */
  readonly naturalSoundscape: string;
  /** Clima e gênero musical congruente (Mahdavi et al.) */
  readonly musicalMood: string;
  /** Instrumentos e timbres prioritários segundo experimentos psicoacústicos (Piesse / Spence) */
  readonly primaryInstruments: readonly string[];
  /** Perfil e tom de voz congruente para o narrador / Companion (Mahdavi et al., Seção 4.3) */
  readonly voiceProfile: VoiceProfile;
  /** Aura cromática sinestésica harmônica (Myrissi / Givaudan) */
  readonly chromaticAura: ChromaticAura;
  /** Descritores poéticos e emocionais derivados (paradigma KAORIUM) */
  readonly emotionalDescriptors: readonly string[];
}

function normalizeTag(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

/**
 * Deriva deterministicamente o perfil sinestésico (som, música, voz, cor e metáfora)
 * para qualquer fragrância do catálogo.
 */
export function deriveSynesthesia(fragrance: Fragrance): SynestheticProfile {
  const familyNorm = normalizeTag(fragrance.family);
  const accordIds = new Set(fragrance.accords.map((a) => normalizeTag(a.id)));
  const allNotes = new Set([
    ...fragrance.topNotes.map(normalizeTag),
    ...fragrance.heartNotes.map(normalizeTag),
    ...fragrance.baseNotes.map(normalizeTag),
  ]);

  const isAquaticOrCitrus =
    familyNorm.includes("citric") ||
    familyNorm.includes("aquat") ||
    accordIds.has("citrico") ||
    accordIds.has("aquatico") ||
    accordIds.has("fresco") ||
    accordIds.has("marinho") ||
    accordIds.has("ozonico");

  const isWoodyOrEarthy =
    familyNorm.includes("amadeirad") ||
    familyNorm.includes("wood") ||
    accordIds.has("amadeirado") ||
    accordIds.has("terroso") ||
    accordIds.has("vetiver") ||
    accordIds.has("patchouli");

  const isOrientalOrAmber =
    familyNorm.includes("oriental") ||
    familyNorm.includes("ambar") ||
    familyNorm.includes("adocicad") ||
    accordIds.has("oriental") ||
    accordIds.has("ambarado") ||
    accordIds.has("balsamico") ||
    accordIds.has("especiado-quente");

  const isGourmandOrSweet =
    accordIds.has("gourmand") ||
    accordIds.has("doce") ||
    accordIds.has("baunilha") ||
    allNotes.has("baunilha") ||
    allNotes.has("fava-tonka") ||
    allNotes.has("caramelo") ||
    allNotes.has("chocolate");

  const isFloral =
    familyNorm.includes("floral") ||
    accordIds.has("floral") ||
    accordIds.has("flores-brancas") ||
    accordIds.has("rosas");

  const isLeatherOrDark =
    accordIds.has("couro") ||
    accordIds.has("fumo") ||
    accordIds.has("incenso") ||
    accordIds.has("animálico") ||
    accordIds.has("animalico");

  // 1. Pistas da Natureza (Mahdavi et al. 2020, Tabela 5)
  let naturalSoundscape: string;
  if (isAquaticOrCitrus) {
    naturalSoundscape = "Ondas do mar, brisa costeira e respingos de água pura";
  } else if (isFloral) {
    naturalSoundscape = "Brisa suave de primavera em jardim florido ao amanhecer";
  } else if (isWoodyOrEarthy) {
    naturalSoundscape = "Sussurro do vento entre árvores antigas e solo de floresta úmida";
  } else if (isOrientalOrAmber) {
    naturalSoundscape = "Calor crepuscular, brisa do deserto e pássaros ao entardecer";
  } else if (isGourmandOrSweet) {
    naturalSoundscape = "Tarde tépida e ensolarada com brisa doce e serena";
  } else if (isLeatherOrDark) {
    naturalSoundscape = "Vento denso da meia-noite sobre rochas e terra firme";
  } else {
    naturalSoundscape = "Brisa suave da natureza com folhas verdes e ar fresco";
  }

  // 2. Clima e Gênero Musical (Mahdavi et al. 2020, Seção 4.2)
  let musicalMood: string;
  if (isAquaticOrCitrus) {
    musicalMood = "Pop acústico leve, andamento fresco e notas de piano cristalino";
  } else if (isFloral) {
    musicalMood = "Música clássica romântica suave e melodias folclóricas delicadas";
  } else if (isWoodyOrEarthy) {
    musicalMood = "Blues intimista, violão clássico e arranjos amadeirados serenos";
  } else if (isOrientalOrAmber) {
    musicalMood = "Flamenco espanhol expressivo, violão encorpado e temas noturnos quentes";
  } else if (isGourmandOrSweet) {
    musicalMood = "Balada suave envolvente, pop melódico e acordes acolhedores";
  } else if (isLeatherOrDark) {
    musicalMood = "Rock atmosférico marcante ou música erudita densa e dramática";
  } else {
    musicalMood = "Arranjo instrumental elegante com harmonia equilibrada";
  }

  // 3. Instrumentos Primários (Piesse 1867 & Spence/Crisinel 2012)
  let primaryInstruments: readonly string[];
  if (isAquaticOrCitrus) {
    primaryInstruments = ["Piano (oitavas agudas)", "Flauta transversal", "Harpa cristalina"];
  } else if (isFloral) {
    primaryInstruments = ["Piano clássico", "Oboé", "Violino suave"];
  } else if (isWoodyOrEarthy) {
    primaryInstruments = ["Violoncelo", "Violão acústico de cordas de nylon", "Fagote"];
  } else if (isOrientalOrAmber) {
    primaryInstruments = ["Violão flamenco", "Alaúde / Cordas orientais", "Metais quentes"];
  } else if (isGourmandOrSweet) {
    primaryInstruments = ["Piano acústico caloroso", "Sopros de madeira suaves", "Violão doce"];
  } else if (isLeatherOrDark) {
    primaryInstruments = ["Contrabaixo acústico", "Trompas graves", "Cordas densas em staccato"];
  } else {
    primaryInstruments = ["Piano", "Cordas orquestrais", "Sopros de madeira"];
  }

  // 4. Voz Congruente para o Narrador (Mahdavi et al. 2020, Seção 4.3)
  let voiceProfile: VoiceProfile;
  if (isAquaticOrCitrus) {
    voiceProfile = {
      tone: "suave_jovem",
      tempo: "fresco_dinamico",
      description: "Voz límpida, jovem e arejada, transmitindo o frescor e a vivacidade da abertura.",
    };
  } else if (isFloral) {
    voiceProfile = {
      tone: "suave_jovem",
      tempo: "suave_moderado",
      description: "Voz suave, melodiosa e acolhedora, destacando a delicadeza e a harmonia botânica.",
    };
  } else if (isWoodyOrEarthy) {
    voiceProfile = {
      tone: "grave_madura",
      tempo: "suave_moderado",
      description: "Voz madura, calma e confiante, refletindo a estabilidade e a nobreza das madeiras.",
    };
  } else if (isOrientalOrAmber || isLeatherOrDark) {
    voiceProfile = {
      tone: "intensa_envolvente",
      tempo: "pausado_envolvente",
      description: "Voz aveludada, sensual e pausada, que acompanha a evolução profunda e quente do rastro.",
    };
  } else if (isGourmandOrSweet) {
    voiceProfile = {
      tone: "aveludada_calma",
      tempo: "suave_moderado",
      description: "Voz doce, calorosa e reconfortante, criando um ambiente sensorial acolhedor.",
    };
  } else {
    voiceProfile = {
      tone: "aveludada_calma",
      tempo: "suave_moderado",
      description: "Voz serena e elegante, com cadência balanceada para consultoria olfativa.",
    };
  }

  // 5. Aura Cromática Sinestésica (Myrissi / Givaudan)
  let chromaticAura: ChromaticAura;
  if (isAquaticOrCitrus) {
    chromaticAura = {
      dominantHsl: "hsl(198, 85%, 42%)",
      secondaryHsl: "hsl(165, 75%, 45%)",
      accentHsl: "hsl(52, 95%, 62%)",
      gradientCss: "linear-gradient(135deg, hsla(198, 85%, 35%, 0.45), hsla(165, 75%, 40%, 0.35))",
      colorFamily: "Azul Oceânico & Cítrico Solar",
    };
  } else if (isFloral) {
    chromaticAura = {
      dominantHsl: "hsl(335, 65%, 55%)",
      secondaryHsl: "hsl(285, 50%, 60%)",
      accentHsl: "hsl(40, 80%, 75%)",
      gradientCss: "linear-gradient(135deg, hsla(335, 65%, 45%, 0.45), hsla(285, 50%, 50%, 0.35))",
      colorFamily: "Rosa Pétala & Champanhe Floral",
    };
  } else if (isWoodyOrEarthy) {
    chromaticAura = {
      dominantHsl: "hsl(28, 55%, 32%)",
      secondaryHsl: "hsl(145, 40%, 28%)",
      accentHsl: "hsl(38, 75%, 60%)",
      gradientCss: "linear-gradient(135deg, hsla(28, 55%, 25%, 0.55), hsla(145, 40%, 22%, 0.45))",
      colorFamily: "Mogno Nobre & Musgo Florestal",
    };
  } else if (isOrientalOrAmber) {
    chromaticAura = {
      dominantHsl: "hsl(348, 65%, 28%)",
      secondaryHsl: "hsl(24, 75%, 38%)",
      accentHsl: "hsl(42, 90%, 58%)",
      gradientCss: "linear-gradient(135deg, hsla(348, 65%, 22%, 0.6), hsla(24, 75%, 30%, 0.45))",
      colorFamily: "Vinho Profundo & Âmbar Radiante",
    };
  } else if (isGourmandOrSweet) {
    chromaticAura = {
      dominantHsl: "hsl(26, 70%, 38%)",
      secondaryHsl: "hsl(38, 80%, 55%)",
      accentHsl: "hsl(12, 65%, 48%)",
      gradientCss: "linear-gradient(135deg, hsla(26, 70%, 30%, 0.55), hsla(38, 80%, 45%, 0.4))",
      colorFamily: "Caramelo Dourado & Cacau Aveludado",
    };
  } else if (isLeatherOrDark) {
    chromaticAura = {
      dominantHsl: "hsl(220, 30%, 18%)",
      secondaryHsl: "hsl(0, 0%, 22%)",
      accentHsl: "hsl(35, 60%, 50%)",
      gradientCss: "linear-gradient(135deg, hsla(220, 30%, 14%, 0.65), hsla(0, 0%, 18%, 0.55))",
      colorFamily: "Grafite Noturno & Couro Antigo",
    };
  } else {
    chromaticAura = {
      dominantHsl: "hsl(345, 45%, 25%)",
      secondaryHsl: "hsl(42, 60%, 50%)",
      accentHsl: "hsl(42, 85%, 65%)",
      gradientCss: "linear-gradient(135deg, hsla(345, 45%, 20%, 0.5), hsla(42, 60%, 40%, 0.35))",
      colorFamily: "Bordeaux & Champagne Antiquário",
    };
  }

  // 6. Descritores Emocionais (Paradigma KAORIUM - Scentmatic)
  let emotionalDescriptors: readonly string[];
  if (isAquaticOrCitrus) {
    emotionalDescriptors = ["Claridade revigorante", "Frescor imediato", "Brisa pura"];
  } else if (isFloral) {
    emotionalDescriptors = ["Elegância serena", "Afeto botânico", "Luminosidade suave"];
  } else if (isWoodyOrEarthy) {
    emotionalDescriptors = ["Solidez atemporal", "Conexão terrosa", "Presença sóbria"];
  } else if (isOrientalOrAmber) {
    emotionalDescriptors = ["Mistério envolvente", "Calor magnético", "Opulência noturna"];
  } else if (isGourmandOrSweet) {
    emotionalDescriptors = ["Conforto acolhedor", "Dulzura refinada", "Memória nostálgica"];
  } else if (isLeatherOrDark) {
    emotionalDescriptors = ["Caráter imponente", "Profundidade enigmática", "Rastro indelével"];
  } else {
    emotionalDescriptors = ["Harmonia refinada", "Presença distinta", "Assinatura memorável"];
  }

  return {
    naturalSoundscape,
    musicalMood,
    primaryInstruments,
    voiceProfile,
    chromaticAura,
    emotionalDescriptors,
  };
}
