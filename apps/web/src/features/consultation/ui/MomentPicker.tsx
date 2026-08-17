import type { OccasionPreset } from "../domain/consultation-schema.ts";

interface MomentOption {
  readonly id: OccasionPreset;
  readonly title: string;
  readonly description: string;
  readonly icon: string;
}

const MOMENT_OPTIONS: readonly MomentOption[] = [
  {
    id: "work",
    title: "Trabalho ou Estudo",
    description: "Foco, elegância discreta e conforto para ambientes compartilhados.",
    icon: "💼",
  },
  {
    id: "date",
    title: "Encontro",
    description: "Magnetismo intimista, charme envolvente e presença próxima.",
    icon: "🕯️",
  },
  {
    id: "celebration",
    title: "Celebração & Festa",
    description: "Opulência, rastro marcante e energia para momentos especiais.",
    icon: "✨",
  },
  {
    id: "casual",
    title: "Dia Casual",
    description: "Descontração, versatilidade e bem-estar para a rotina diária.",
    icon: "☕",
  },
  {
    id: "outdoor",
    title: "Ao Ar Livre",
    description: "Frescor expansivo, vitalidade solar e sintonia com a natureza.",
    icon: "🌿",
  },
  {
    id: "other",
    title: "Outro Momento",
    description: "Uma ocasião particular com liberdade para explorar qualquer caminho.",
    icon: "🧭",
  },
];

export function MomentPicker({
  selected,
  onSelect,
}: {
  selected: OccasionPreset;
  onSelect: (occasion: OccasionPreset) => void;
}) {
  return (
    <div className="picker-container" aria-label="Escolha do momento">
      <div className="picker-grid">
        {MOMENT_OPTIONS.map((option) => {
          const isSelected = selected === option.id;
          return (
            <button
              className={`choice-card ${isSelected ? "is-selected" : ""}`}
              key={option.id}
              onClick={() => onSelect(option.id)}
              type="button"
              aria-pressed={isSelected}
            >
              <span className="choice-icon" aria-hidden="true">{option.icon}</span>
              <div className="choice-content">
                <strong>{option.title}</strong>
                <p>{option.description}</p>
              </div>
              <span className="choice-radio" aria-hidden="true" />
            </button>
          );
        })}
      </div>
    </div>
  );
}
