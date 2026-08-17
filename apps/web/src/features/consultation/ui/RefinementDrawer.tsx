import type {
  ConsultationIntentV2,
  DiscoveryPreference,
} from "../domain/consultation-schema.ts";

export function RefinementDrawer({
  isOpen,
  intent,
  availableAccords,
  availableNotes,
  onClose,
  onToggleAvoidedAccord,
  onToggleHardAvoidNote,
  onToggleSensitiveEnvironment,
  onSelectDiscovery,
}: {
  isOpen: boolean;
  intent: ConsultationIntentV2;
  availableAccords: readonly string[];
  availableNotes: readonly string[];
  onClose: () => void;
  onToggleAvoidedAccord: (accord: string) => void;
  onToggleHardAvoidNote: (note: string) => void;
  onToggleSensitiveEnvironment: (value: boolean) => void;
  onSelectDiscovery: (discovery: DiscoveryPreference) => void;
}) {
  if (!isOpen) return null;

  return (
    <div className="refinement-overlay" role="dialog" aria-modal="true" aria-label="Ajustar preferências detalhadas">
      <div className="refinement-modal">
        <header className="refinement-header">
          <div>
            <p className="section-kicker">Refinamento opcional</p>
            <h3>Ajustar detalhes da consulta</h3>
          </div>
          <button className="close-button" onClick={onClose} type="button" aria-label="Fechar refinamento">
            ✕
          </button>
        </header>

        <div className="refinement-body">
          <section className="refinement-section">
            <label className="toggle-row">
              <input
                type="checkbox"
                checked={intent.sensitiveEnvironment}
                onChange={(e) => onToggleSensitiveEnvironment(e.target.checked)}
              />
              <span>
                <strong>Ambiente sensível</strong>
                Limitar rastro e projeção para salas fechadas ou hospitais
              </span>
            </label>
          </section>

          <section className="refinement-section">
            <h4>Apetite por descoberta</h4>
            <div className="discovery-selector">
              {(["familiar", "balanced", "exploratory"] as const).map((d) => {
                const label = d === "familiar" ? "Familiar" : d === "balanced" ? "Equilibrado" : "Explorador";
                const desc = d === "familiar" ? "Priorizar caminhos clássicos e seguros" : d === "balanced" ? "Equilíbrio entre clássicos e novidades" : "Descobrir combinações raras e autorais";
                const active = intent.discovery === d;
                return (
                  <button
                    key={d}
                    type="button"
                    className={`discovery-option ${active ? "is-active" : ""}`}
                    onClick={() => onSelectDiscovery(d)}
                  >
                    <strong>{label}</strong>
                    <small>{desc}</small>
                  </button>
                );
              })}
            </div>
          </section>

          <section className="refinement-section">
            <h4>Acordes que prefere evitar</h4>
            <div className="chip-grid">
              {availableAccords.map((accord) => {
                const isAvoided = intent.avoidedCanonicalIds.includes(accord);
                return (
                  <button
                    key={accord}
                    type="button"
                    className={`preference-chip ${isAvoided ? "is-active negative" : ""}`}
                    onClick={() => onToggleAvoidedAccord(accord)}
                    aria-pressed={isAvoided}
                  >
                    {accord}
                  </button>
                );
              })}
            </div>
          </section>

          <section className="refinement-section">
            <h4>Notas proibidas nesta consulta</h4>
            <div className="chip-grid">
              {availableNotes.map((note) => {
                const isAvoided = intent.hardAvoidNotes.includes(note);
                return (
                  <button
                    key={note}
                    type="button"
                    className={`preference-chip ${isAvoided ? "is-active negative" : ""}`}
                    onClick={() => onToggleHardAvoidNote(note)}
                    aria-pressed={isAvoided}
                  >
                    {note}
                  </button>
                );
              })}
            </div>
          </section>
        </div>

        <footer className="refinement-footer">
          <button className="primary-action" type="button" onClick={onClose}>
            <span>Concluir ajustes</span>
            <b aria-hidden="true">✓</b>
          </button>
        </footer>
      </div>
    </div>
  );
}
