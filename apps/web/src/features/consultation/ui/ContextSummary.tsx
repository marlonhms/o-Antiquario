import type {
  DerivedContext,
  Setting,
  TimePeriod,
  WeatherBand,
} from "../domain/consultation-schema.ts";
import { formatContextOneLiner } from "../domain/derive-context.ts";

export function ContextSummary({
  context,
  isOpen,
  onToggleOpen,
  onUpdateSetting,
  onUpdateWeather,
  onUpdatePeriod,
}: {
  context: DerivedContext;
  isOpen: boolean;
  onToggleOpen: () => void;
  onUpdateSetting: (setting: Setting) => void;
  onUpdateWeather: (band: WeatherBand) => void;
  onUpdatePeriod: (period: TimePeriod) => void;
}) {
  const summaryText = formatContextOneLiner(context);

  return (
    <div className="context-summary-bar">
      <div className="context-summary-text">
        <span className="context-indicator" aria-hidden="true">📍</span>
        <span>{summaryText}</span>
      </div>

      <button
        className="context-edit-trigger"
        onClick={onToggleOpen}
        type="button"
        aria-expanded={isOpen}
      >
        {isOpen ? "fechar" : "corrigir"}
      </button>

      {isOpen && (
        <div className="context-popover" role="dialog" aria-label="Ajustar contexto do momento">
          <div className="popover-section">
            <small>Período</small>
            <div className="mini-chips">
              {(["morning", "afternoon", "evening", "night"] as const).map((p) => {
                const label = p === "morning" ? "Manhã" : p === "afternoon" ? "Tarde" : p === "evening" ? "Noite" : "Madrugada";
                const active = context.period === p;
                return (
                  <button
                    key={p}
                    type="button"
                    className={`mini-chip ${active ? "is-active" : ""}`}
                    onClick={() => onUpdatePeriod(p)}
                  >
                    {label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="popover-section">
            <small>Ambiente</small>
            <div className="mini-chips">
              {(["indoor", "outdoor", "mixed"] as const).map((s) => {
                const label = s === "indoor" ? "Interno" : s === "outdoor" ? "Ar livre" : "Misto";
                const active = context.setting === s;
                return (
                  <button
                    key={s}
                    type="button"
                    className={`mini-chip ${active ? "is-active" : ""}`}
                    onClick={() => onUpdateSetting(s)}
                  >
                    {label}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="popover-section">
            <small>Clima</small>
            <div className="mini-chips">
              {(["cold", "mild", "hot"] as const).map((w) => {
                const label = w === "cold" ? "Fresco/Frio" : w === "mild" ? "Ameno" : "Quente";
                const active = context.weatherBand === w;
                return (
                  <button
                    key={w}
                    type="button"
                    className={`mini-chip ${active ? "is-active" : ""}`}
                    onClick={() => onUpdateWeather(w)}
                  >
                    {label}
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
