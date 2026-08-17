import type { AtmosphereIntent } from "../domain/consultation-schema.ts";

interface AtmosphereOption {
  readonly id: AtmosphereIntent;
  readonly title: string;
  readonly description: string;
  readonly sensoryTag: string;
  readonly icon: string;
  readonly auraColor: string;
}

const ATMOSPHERE_OPTIONS: readonly AtmosphereOption[] = [
  {
    id: "fresh_luminous",
    title: "Fresca e Luminosa",
    description: "Cítricos cintilantes, brisa marinha e claridade radiante.",
    sensoryTag: "Cítrico · Aquático · Fresco",
    icon: "🌊",
    auraColor: "#62c9d8",
  },
  {
    id: "clean_serene",
    title: "Limpa e Serena",
    description: "Herbal aromático, sensação de banho tomado e toque verde natural.",
    sensoryTag: "Aromático · Verde · Atalcado",
    icon: "🍃",
    auraColor: "#78d7b0",
  },
  {
    id: "warm_comforting",
    title: "Confortável e Acolhedora",
    description: "Baunilha aveludada, especiarias doces e aconchego nostálgico.",
    sensoryTag: "Gourmand · Doce · Baunilha",
    icon: "🧁",
    auraColor: "#cf7f9c",
  },
  {
    id: "elegant_memorable",
    title: "Elegante e Marcante",
    description: "Madeiras nobres, sofisticação atemporal e presença refinada.",
    sensoryTag: "Amadeirado · Chipre · Floral",
    icon: "🏛️",
    auraColor: "#c1845d",
  },
  {
    id: "mysterious_magnetic",
    title: "Misteriosa e Magnética",
    description: "Âmbar profundo, resinas orientais e sensualidade noturna envolvente.",
    sensoryTag: "Oriental · Âmbar · Especiado",
    icon: "🌙",
    auraColor: "#e29a55",
  },
  {
    id: "surprise_me",
    title: "Surpreenda-me",
    description: "Deixe o Antiquário escolher um caminho inesperado e instigante.",
    sensoryTag: "Curadoria Livre · Serendipidade",
    icon: "🎲",
    auraColor: "#d5b477",
  },
];

export function AtmospherePicker({
  selected,
  onSelect,
}: {
  selected: AtmosphereIntent;
  onSelect: (atmosphere: AtmosphereIntent) => void;
}) {
  return (
    <div className="picker-container" aria-label="Escolha da atmosfera">
      <div className="picker-grid">
        {ATMOSPHERE_OPTIONS.map((option) => {
          const isSelected = selected === option.id;
          return (
            <button
              className={`choice-card choice-card-atmosphere ${isSelected ? "is-selected" : ""}`}
              key={option.id}
              onClick={() => onSelect(option.id)}
              style={{ "--option-aura": option.auraColor } as React.CSSProperties}
              type="button"
              aria-pressed={isSelected}
            >
              <span className="choice-icon" aria-hidden="true">{option.icon}</span>
              <div className="choice-content">
                <strong>{option.title}</strong>
                <p>{option.description}</p>
                <small className="choice-tag">{option.sensoryTag}</small>
              </div>
              <span className="choice-radio" aria-hidden="true" />
            </button>
          );
        })}
      </div>
    </div>
  );
}
