import { useEffect, useMemo, useRef, useState } from "react";
import type { CSSProperties, FormEvent } from "react";

import type {
  Confidence,
  RecommendationContext,
  RecommendationResult,
  ScoreFactorName,
} from "@core/domain/types.ts";
import { loadCatalogReleaseManifest, type CatalogReleaseManifest } from "@core/catalog/release.ts";
import { FIXTURE_FRAGRANCES } from "@core/recommender/fixtures.ts";
import { recommend } from "@core/recommender/recommend.ts";
import type { Fragrance } from "@core/domain/types.ts";
import type { CompiledRecommendationCatalog } from "@core/catalog/recommendation-compiler.ts";

type Setting = "indoor" | "outdoor" | "mixed";
type Crowding = "low" | "medium" | "high";

interface ConsultantForm {
  occasion: string;
  setting: Setting;
  crowding: Crowding;
  temperatureC: number;
  humidity: number;
  durationHours: number;
  desiredProjection: number;
  maximumPriceTier: 1 | 2 | 3 | 4 | 5;
  strictBudget: boolean;
  sensitiveEnvironment: boolean;
  noveltyPreference: number;
  likedAccords: string[];
  avoidedAccords: string[];
  hardAvoidNotes: string[];
}

const STORAGE_KEY = "o-antiquario:consultant-form:v1";

const DEFAULT_FORM: ConsultantForm = {
  occasion: "escritório",
  setting: "indoor",
  crowding: "high",
  temperatureC: 30,
  humidity: 0.72,
  durationHours: 7,
  desiredProjection: 0.4,
  maximumPriceTier: 3,
  strictBudget: false,
  sensitiveEnvironment: true,
  noveltyPreference: 0.55,
  likedAccords: ["cítrico", "amadeirado"],
  avoidedAccords: ["doce"],
  hardAvoidNotes: [],
};


const FORMALITY_BY_OCCASION: Record<string, number> = {
  casual: 0.25,
  esporte: 0.2,
  escritório: 0.62,
  encontro: 0.68,
  festa: 0.72,
  formal: 0.92,
};

const FACTOR_LABELS: Record<ScoreFactorName, string> = {
  preference: "Preferências",
  context: "Contexto",
  performance: "Desempenho",
  history: "Histórico",
  budget: "Orçamento",
  confidence: "Confiança",
  novelty: "Descoberta",
};

const ACCORD_AURAS: Record<string, string> = {
  cítrico: "#d8f29a",
  verde: "#78d7b0",
  aromático: "#8dd7c6",
  aquático: "#62c9d8",
  floral: "#d995c5",
  atalcado: "#c8b6db",
  almiscarado: "#d9d4e2",
  frutado: "#e39a9e",
  amadeirado: "#c1845d",
  ambarado: "#e29a55",
  doce: "#cf7f9c",
  especiado: "#c95d68",
};

const CONSULTATION_STEPS = [
  { number: "01", short: "Contexto", title: "O momento", description: "Onde o perfume encontrará você?" },
  { number: "02", short: "Presença", title: "Sua presença", description: "Defina o alcance e o tempo do rastro." },
  { number: "03", short: "Memória", title: "Sua memória", description: "Atrações, recusas e espaço para descoberta." },
] as const;

interface FactualFragrance {
  id: string;
  wikidataId: string;
  name: string;
  launchYear: number | null;
  officialWebsite: string | null;
  brandIds: string[];
  perfumerIds: string[];
  countryIds: string[];
  olfactoryDescriptorIds: string[];
  topNotes?: string[];
  heartNotes?: string[];
  baseNotes?: string[];
}

interface CatalogEntity {
  id: string;
  name: string;
}

interface FactualEntities {
  brands: CatalogEntity[];
  perfumers: CatalogEntity[];
  countries: CatalogEntity[];
  olfactoryDescriptors: CatalogEntity[];
}

interface SemanticClaim {
  fragranceId: string;
  propertyId: string;
  propertyLabel: string;
  valueLabel: string;
}

interface FactualLibraryData {
  fragrances: FactualFragrance[];
  entities: FactualEntities;
  claims: SemanticClaim[];
}

async function loadFactualLibrary(): Promise<FactualLibraryData> {
  const [fragranceResponse, entityResponse, claimResponse] = await Promise.all([
    fetch("/catalog/fragrances.json"),
    fetch("/catalog/entities.json"),
    fetch("/catalog/semantic-claims.json"),
  ]);
  if (!fragranceResponse.ok || !entityResponse.ok || !claimResponse.ok) {
    throw new Error("Acervo factual indisponível");
  }
  const [fragrancePayload, entityPayload, claimPayload] = await Promise.all([
    fragranceResponse.json() as Promise<{ items: FactualFragrance[] }>,
    entityResponse.json() as Promise<FactualEntities>,
    claimResponse.json() as Promise<{ items: SemanticClaim[] }>,
  ]);
  return { fragrances: fragrancePayload.items, entities: entityPayload, claims: claimPayload.items };
}

async function loadRecommendationCatalog(): Promise<readonly Fragrance[]> {
  const response = await fetch("/catalog/recommendation-catalog.json");
  if (!response.ok) {
    throw new Error("Catálogo de recomendação indisponível");
  }
  const payload = await response.json() as CompiledRecommendationCatalog;
  return payload.fragrances;
}

function mergeRecommendationIntoFactual(
  library: FactualLibraryData,
  recommendationCatalog: readonly Fragrance[],
): FactualLibraryData {
  if (!recommendationCatalog || recommendationCatalog.length === 0) return library;

  const existingMap = new Map(library.fragrances.map((f) => [f.id, f]));
  const existingByName = new Map(library.fragrances.map((f) => [f.name.toLowerCase().trim(), f]));
  const updatedLibraryFragrances = [...library.fragrances];
  const newFragrances: FactualFragrance[] = [];
  const newBrands = [...library.entities.brands];
  const newDescriptors = [...library.entities.olfactoryDescriptors];

  const brandMap = new Map(newBrands.map((b) => [b.id, b.name]));
  const descriptorMap = new Map(newDescriptors.map((d) => [d.id, d.name]));

  for (const item of recommendationCatalog) {
    const descriptorIds: string[] = [];
    const allNotesAndAccords = [
      ...item.accords.map((a) => a.id),
      ...item.topNotes,
      ...item.heartNotes,
      ...item.baseNotes,
    ];

    for (const tag of allNotesAndAccords) {
      const descId = `desc-${tag.toLowerCase()}`;
      if (!descriptorMap.has(descId)) {
        newDescriptors.push({ id: descId, name: tag });
        descriptorMap.set(descId, tag);
      }
      if (!descriptorIds.includes(descId)) {
        descriptorIds.push(descId);
      }
    }

    const existing = existingMap.get(item.id) || existingByName.get(item.name.toLowerCase().trim());
    if (existing) {
      if (item.topNotes && item.topNotes.length > 0) existing.topNotes = [...item.topNotes];
      if (item.heartNotes && item.heartNotes.length > 0) existing.heartNotes = [...item.heartNotes];
      if (item.baseNotes && item.baseNotes.length > 0) existing.baseNotes = [...item.baseNotes];

      for (const descId of descriptorIds) {
        if (!existing.olfactoryDescriptorIds.includes(descId)) {
          existing.olfactoryDescriptorIds.push(descId);
        }
      }
      continue;
    }

    const brandId = `brand-${item.brand.toLowerCase()}`;
    if (!brandMap.has(brandId)) {
      const brandName = item.brand === "o-boticario" ? "O Boticário" : item.brand;
      newBrands.push({ id: brandId, name: brandName });
      brandMap.set(brandId, brandName);
    }

    newFragrances.push({
      id: item.id,
      wikidataId: "Curadoria Oficial PDF",
      name: item.name,
      launchYear: null,
      officialWebsite: "https://www.boticario.com.br",
      brandIds: [brandId],
      perfumerIds: [],
      countryIds: [],
      olfactoryDescriptorIds: descriptorIds,
      topNotes: [...item.topNotes],
      heartNotes: [...item.heartNotes],
      baseNotes: [...item.baseNotes],
    });
  }

  return {
    fragrances: [...newFragrances, ...updatedLibraryFragrances],
    entities: {
      ...library.entities,
      brands: newBrands,
      olfactoryDescriptors: newDescriptors,
    },
    claims: library.claims,
  };
}

function entityNames(ids: readonly string[], index: ReadonlyMap<string, string>): string[] {
  return ids.map((id) => index.get(id)).filter((name): name is string => Boolean(name));
}

function auraColor(accord: string | undefined, fallback: string): string {
  if (!accord) return fallback;
  const exact = ACCORD_AURAS[accord];
  if (exact) return exact;
  const partial = Object.entries(ACCORD_AURAS).find(([name]) => accord.includes(name));
  return partial?.[1] ?? fallback;
}

function hexToRgb(hex: string): [number, number, number] {
  const normalized = hex.replace("#", "");
  return [
    Number.parseInt(normalized.slice(0, 2), 16),
    Number.parseInt(normalized.slice(2, 4), 16),
    Number.parseInt(normalized.slice(4, 6), 16),
  ];
}

function MagneticField({ primary, secondary }: { primary: string; secondary: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const context = canvas.getContext("2d");
    if (!context) return;
    const surface: HTMLCanvasElement = canvas;
    const drawingContext: CanvasRenderingContext2D = context;

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const primaryRgb = hexToRgb(primary);
    const secondaryRgb = hexToRgb(secondary);
    const pointer = { x: window.innerWidth * 0.68, y: window.innerHeight * 0.34 };
    const particles = Array.from({ length: reducedMotion ? 18 : 54 }, (_, index) => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      angle: Math.random() * Math.PI * 2,
      speed: 0.16 + Math.random() * 0.34,
      phase: index * 0.73,
      tone: index % 3 === 0 ? secondaryRgb : primaryRgb,
    }));
    let animationFrame = 0;
    let width = 0;
    let height = 0;

    function resize(): void {
      const ratio = Math.min(window.devicePixelRatio || 1, 1.75);
      width = window.innerWidth;
      height = window.innerHeight;
      surface.width = Math.round(width * ratio);
      surface.height = Math.round(height * ratio);
      surface.style.width = `${width}px`;
      surface.style.height = `${height}px`;
      drawingContext.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function followPointer(event: PointerEvent): void {
      pointer.x = event.clientX;
      pointer.y = event.clientY;
    }

    function draw(time = 0): void {
      drawingContext.clearRect(0, 0, width, height);
      drawingContext.globalCompositeOperation = "lighter";

      for (const particle of particles) {
        const previousX = particle.x;
        const previousY = particle.y;
        const distanceX = pointer.x - particle.x;
        const distanceY = pointer.y - particle.y;
        const distance = Math.max(80, Math.hypot(distanceX, distanceY));
        const magneticPull = Math.min(0.018, 14 / distance ** 1.35);

        particle.angle += Math.sin(time * 0.00016 + particle.phase) * 0.006;
        particle.x += Math.cos(particle.angle) * particle.speed + distanceX * magneticPull * 0.012;
        particle.y += Math.sin(particle.angle) * particle.speed + distanceY * magneticPull * 0.012;

        if (particle.x < -20) particle.x = width + 20;
        if (particle.x > width + 20) particle.x = -20;
        if (particle.y < -20) particle.y = height + 20;
        if (particle.y > height + 20) particle.y = -20;

        const [red, green, blue] = particle.tone;
        drawingContext.beginPath();
        drawingContext.moveTo(previousX, previousY);
        drawingContext.lineTo(particle.x, particle.y);
        drawingContext.strokeStyle = `rgba(${red}, ${green}, ${blue}, 0.22)`;
        drawingContext.lineWidth = 0.65;
        drawingContext.stroke();

        drawingContext.beginPath();
        drawingContext.arc(particle.x, particle.y, 0.7, 0, Math.PI * 2);
        drawingContext.fillStyle = `rgba(${red}, ${green}, ${blue}, 0.36)`;
        drawingContext.fill();
      }

      if (!reducedMotion) animationFrame = window.requestAnimationFrame(draw);
    }

    resize();
    draw();
    window.addEventListener("resize", resize);
    window.addEventListener("pointermove", followPointer, { passive: true });

    return () => {
      window.cancelAnimationFrame(animationFrame);
      window.removeEventListener("resize", resize);
      window.removeEventListener("pointermove", followPointer);
    };
  }, [primary, secondary]);

  return <canvas className="magnetic-field" ref={canvasRef} aria-hidden="true" />;
}

function readStoredForm(): ConsultantForm {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    return stored ? { ...DEFAULT_FORM, ...JSON.parse(stored) } : DEFAULT_FORM;
  } catch {
    return DEFAULT_FORM;
  }
}

function toggleValue(values: string[], value: string): string[] {
  return values.includes(value) ? values.filter((item) => item !== value) : [...values, value];
}

function confidenceLabel(confidence: Confidence): string {
  return { high: "alta", medium: "média", low: "baixa", unknown: "desconhecida" }[confidence];
}

function projectionLabel(value: number): string {
  if (value < 0.34) return "íntima";
  if (value < 0.55) return "moderada";
  if (value < 0.76) return "marcante";
  return "intensa";
}

function recommendationContext(form: ConsultantForm): RecommendationContext {
  return {
    occasion: form.occasion,
    setting: form.setting,
    crowding: form.crowding,
    temperatureC: form.temperatureC,
    humidity: form.humidity,
    formality: FORMALITY_BY_OCCASION[form.occasion] ?? 0.5,
    desiredProjection: form.desiredProjection,
    durationHours: form.durationHours,
    maximumPriceTier: form.maximumPriceTier,
    strictBudget: form.strictBudget,
    projectionCeiling: form.sensitiveEnvironment ? 0.72 : undefined,
  };
}

function runRecommendation(form: ConsultantForm, catalog: readonly Fragrance[]): RecommendationResult {
  return recommend(
    catalog.length > 0 ? catalog : FIXTURE_FRAGRANCES,
    {
      accordPreferences: Object.fromEntries([
        ...form.likedAccords.map((accord) => [accord, 0.95]),
        ...form.avoidedAccords.map((accord) => [accord, -0.9]),
      ]),
      hardAvoidNotes: form.hardAvoidNotes,
      noveltyPreference: form.noveltyPreference,
    },
    recommendationContext(form),
  );
}

function ScoreRing({ score }: { score: number }) {
  const percentage = Math.round(score * 100);
  return (
    <div className="score-ring" style={{ "--score": `${percentage * 3.6}deg` } as CSSProperties}>
      <span>{percentage}</span>
      <small>%</small>
    </div>
  );
}

function RecommendationCard({
  candidate,
  position,
}: {
  candidate: RecommendationResult["recommendations"][number];
  position: number;
}) {
  const { fragrance } = candidate;
  const longevity = fragrance.performance.longevity;
  const auraStyle = {
    "--aura-primary": auraColor(fragrance.accords[0]?.id, "#d5b477"),
    "--aura-secondary": auraColor(fragrance.accords[1]?.id, "#76294e"),
  } as CSSProperties;

  return (
    <article className={`recommendation-card recommendation-${position}`} style={auraStyle}>
      <div className="ranking-column" aria-label={`Posição ${position}`}>
        <span className="ranking-label">Escolha</span>
        <strong>0{position}</strong>
      </div>

      <div className="bottle-mark" aria-hidden="true">
        <span className="bottle-cap" />
        <span className="bottle-body">{fragrance.brand.charAt(0)}</span>
      </div>

      <div className="recommendation-copy">
        <div className="eyebrow-row">
          <span>{fragrance.family}</span>
          <span>{fragrance.concentrations[0]}</span>
          <span>confiança {confidenceLabel(fragrance.dataConfidence)}</span>
        </div>
        <h3>{fragrance.name}</h3>
        <p className="brand-name">{fragrance.brand}</p>

        <p className="recommendation-reason">{candidate.strengths.slice(0, 3).join(" · ")}</p>

        <div className="metric-strip" aria-label="Métricas estimadas">
          <span>
            <small>Duração</small>
            {longevity.minimumHours}–{longevity.maximumHours}h
          </span>
          <span>
            <small>Projeção</small>
            {projectionLabel(fragrance.performance.projection.value)}
          </span>
          <span>
            <small>Preço</small>
            faixa {fragrance.priceTier ?? "?"}/5
          </span>
        </div>

        <div className="scent-evolution" aria-label="Evolução olfativa">
          <span>
            <small>Abertura</small>
            {fragrance.topNotes.slice(0, 2).join(" · ")}
          </span>
          <i aria-hidden="true" />
          <span>
            <small>Coração</small>
            {fragrance.heartNotes.slice(0, 2).join(" · ")}
          </span>
          <i aria-hidden="true" />
          <span>
            <small>Rastro</small>
            {fragrance.baseNotes.slice(0, 2).join(" · ")}
          </span>
        </div>

        <details className="factor-details">
          <summary>Como chegamos aqui</summary>
          <div className="factor-list">
            {candidate.factors.map((factor) => (
              <div className="factor-row" key={factor.name}>
                <span>{FACTOR_LABELS[factor.name]}</span>
                <div className="factor-track" aria-hidden="true">
                  <i style={{ width: `${Math.round(factor.score * 100)}%` }} />
                </div>
                <strong>{Math.round(factor.score * 100)}</strong>
              </div>
            ))}
          </div>
          {candidate.tradeoffs.length > 0 && (
            <p className="tradeoff">Atenção: {candidate.tradeoffs.join("; ")}.</p>
          )}
        </details>
      </div>

      <ScoreRing score={candidate.score} />
    </article>
  );
}

function ChipGroup({
  legend,
  options,
  selected,
  onToggle,
  tone = "positive",
}: {
  legend: string;
  options: readonly string[];
  selected: readonly string[];
  onToggle: (value: string) => void;
  tone?: "positive" | "negative";
}) {
  return (
    <fieldset className="chip-fieldset">
      <legend>{legend}</legend>
      <div className="chip-grid">
        {options.map((option) => {
          const active = selected.includes(option);
          return (
            <button
              aria-pressed={active}
              className={`preference-chip ${active ? `is-active ${tone}` : ""}`}
              key={option}
              onClick={() => onToggle(option)}
              type="button"
            >
              {option}
            </button>
          );
        })}
      </div>
    </fieldset>
  );
}

function FactualLibrary({ library }: { library: FactualLibraryData }) {
  const [query, setQuery] = useState("");
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const entityIndex = useMemo(() => new Map(
    [
      ...library.entities.brands,
      ...library.entities.perfumers,
      ...library.entities.countries,
      ...library.entities.olfactoryDescriptors,
    ].map((entity) => [entity.id, entity.name]),
  ), [library]);
  const normalizedQuery = query.trim().toLocaleLowerCase("pt-BR");
  const filtered = useMemo(() => library.fragrances.filter((fragrance) => {
    const terms = [
      fragrance.name,
      ...entityNames(fragrance.brandIds, entityIndex),
      ...entityNames(fragrance.perfumerIds, entityIndex),
      ...entityNames(fragrance.olfactoryDescriptorIds, entityIndex),
    ].join(" ").toLocaleLowerCase("pt-BR");
    return !normalizedQuery || terms.includes(normalizedQuery);
  }), [entityIndex, library.fragrances, normalizedQuery]);
  const selected = filtered.find((fragrance) => fragrance.id === selectedId) ?? filtered[0];
  const selectedClaims = selected ? library.claims.filter((claim) => claim.fragranceId === selected.id) : [];

  return (
    <section className="factual-library" id="acervo" aria-label="Acervo factual de perfumaria">
      <div className="library-heading">
        <div>
          <p className="section-kicker">Acervo factual</p>
          <h2>Perfumes, sem névoa nos dados.</h2>
        </div>
        <p>{library.fragrances.length} perfumes · {library.entities.olfactoryDescriptors.length} descritores · dados Wikidata</p>
      </div>

      <div className="library-toolbar">
        <label>
          <span>Buscar no acervo</span>
          <input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="nome, marca, perfumista ou descritor"
          />
        </label>
        <small>{filtered.length} resultado{filtered.length === 1 ? "" : "s"}</small>
      </div>

      <div className="library-layout">
        <div className="library-list" role="list">
          {filtered.slice(0, 16).map((fragrance) => {
            const active = fragrance.id === selected?.id;
            const brand = entityNames(fragrance.brandIds, entityIndex)[0] ?? "marca não declarada";
            return (
              <button
                className={`library-item ${active ? "is-active" : ""}`}
                type="button"
                key={fragrance.id}
                onClick={() => setSelectedId(fragrance.id)}
                role="listitem"
              >
                <span>{fragrance.name.charAt(0)}</span>
                <strong>{fragrance.name}</strong>
                <small>{brand}{fragrance.launchYear ? ` · ${fragrance.launchYear}` : ""}</small>
              </button>
            );
          })}
          {filtered.length === 0 && <p className="library-empty">Nenhum perfume corresponde a esta busca.</p>}
        </div>

        {selected && (
          <article className="library-detail">
            <div className="library-detail-title">
              <span className="detail-seal">{selected.name.charAt(0)}</span>
              <div>
                <p className="section-kicker">Registro factual · {selected.wikidataId}</p>
                <h3>{selected.name}</h3>
                <p>{entityNames(selected.brandIds, entityIndex).join(" · ") || "Marca não declarada"}</p>
              </div>
            </div>

            <div className="factual-columns">
              <div>
                <small>Perfumista</small>
                <p>{entityNames(selected.perfumerIds, entityIndex).join(" · ") || "não declarado"}</p>
              </div>
              <div>
                <small>Origem</small>
                <p>{entityNames(selected.countryIds, entityIndex).join(" · ") || "não declarada"}</p>
              </div>
              <div>
                <small>Lançamento</small>
                <p>{selected.launchYear ?? "não declarado"}</p>
              </div>
            </div>

            {((selected.topNotes && selected.topNotes.length > 0) ||
              (selected.heartNotes && selected.heartNotes.length > 0) ||
              (selected.baseNotes && selected.baseNotes.length > 0)) && (
              <div className="fact-group">
                <small>Pirâmide Olfativa (Extração Oficial PDF)</small>
                <div style={{ display: "flex", flexDirection: "column", gap: "6px", fontSize: "0.85rem", marginTop: "6px" }}>
                  {selected.topNotes && selected.topNotes.length > 0 && (
                    <div><b style={{ opacity: 0.7, marginRight: "6px" }}>Saída:</b> {selected.topNotes.join(", ")}</div>
                  )}
                  {selected.heartNotes && selected.heartNotes.length > 0 && (
                    <div><b style={{ opacity: 0.7, marginRight: "6px" }}>Coração:</b> {selected.heartNotes.join(", ")}</div>
                  )}
                  {selected.baseNotes && selected.baseNotes.length > 0 && (
                    <div><b style={{ opacity: 0.7, marginRight: "6px" }}>Fundo:</b> {selected.baseNotes.join(", ")}</div>
                  )}
                </div>
              </div>
            )}

            <div className="fact-group">
              <small>Descritores olfativos declarados</small>
              <div className="fact-chips">
                {entityNames(selected.olfactoryDescriptorIds, entityIndex).slice(0, 18).map((name) => <span key={name}>{name}</span>)}
                {selected.olfactoryDescriptorIds.length === 0 && <em>não declarados no Wikidata</em>}
              </div>
            </div>

            {selectedClaims.length > 0 && (
              <div className="fact-group">
                <small>Outras declarações estruturadas</small>
                <div className="claim-list">
                  {selectedClaims.map((claim) => <span key={`${claim.propertyId}:${claim.valueLabel}`}><b>{claim.propertyLabel}</b>{claim.valueLabel}</span>)}
                </div>
              </div>
            )}

            <div className="detail-foot">
              <span>Dados estruturados · CC0</span>
              {selected.officialWebsite && <a href={selected.officialWebsite} target="_blank" rel="noreferrer">site declarado ↗</a>}
            </div>
          </article>
        )}
      </div>
    </section>
  );
}

export function App() {
  const [draft, setDraft] = useState<ConsultantForm>(readStoredForm);
  const [revision, setRevision] = useState(1);
  const [consultationStep, setConsultationStep] = useState(0);
  const [catalogManifest, setCatalogManifest] = useState<CatalogReleaseManifest | null>(null);
  const [rawFactualLibrary, setFactualLibrary] = useState<FactualLibraryData | null>(null);
  const [recommendationCatalog, setRecommendationCatalog] = useState<readonly Fragrance[]>([]);
  const factualLibrary = useMemo(
    () => (rawFactualLibrary ? mergeRecommendationIntoFactual(rawFactualLibrary, recommendationCatalog) : null),
    [rawFactualLibrary, recommendationCatalog],
  );
  const dynamicAccordOptions = useMemo(() => {
    const accords = new Set<string>();
    for (const f of recommendationCatalog) {
      for (const a of f.accords) {
        accords.add(a.id);
      }
    }
    return Array.from(accords).sort();
  }, [recommendationCatalog]);

  const dynamicNoteOptions = useMemo(() => {
    const notes = new Set<string>();
    for (const f of recommendationCatalog) {
      for (const n of f.topNotes) notes.add(n);
      for (const n of f.heartNotes) notes.add(n);
      for (const n of f.baseNotes) notes.add(n);
    }
    return Array.from(notes).sort();
  }, [recommendationCatalog]);

  const result = useMemo(() => runRecommendation(draft, recommendationCatalog), [draft, recommendationCatalog]);
  const leadingFragrance = result.recommendations[0]?.fragrance;
  const primaryAura = auraColor(leadingFragrance?.accords[0]?.id, "#78d7b0");
  const secondaryAura = auraColor(leadingFragrance?.accords[1]?.id, "#d995c5");
  const atmosphereStyle = {
    "--active-aura": primaryAura,
    "--active-aura-secondary": secondaryAura,
  } as CSSProperties;

  useEffect(() => {
    let active = true;
    loadCatalogReleaseManifest()
      .then((manifest) => {
        if (active) setCatalogManifest(manifest);
      })
      .catch(() => {
        if (active) setCatalogManifest(null);
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;
    loadFactualLibrary()
      .then((library) => {
        if (active) setFactualLibrary(library);
      })
      .catch(() => {
        if (active) setFactualLibrary(null);
      });
    return () => {
      active = false;
    };
  }, []);

  useEffect(() => {
    let active = true;
    loadRecommendationCatalog()
      .then((catalog) => {
        if (active) setRecommendationCatalog(catalog);
      })
      .catch(() => {
        if (active) setRecommendationCatalog([]);
      });
    return () => {
      active = false;
    };
  }, []);

  function update<K extends keyof ConsultantForm>(key: K, value: ConsultantForm[K]): void {
    setDraft((current) => {
      const next = { ...current, [key]: value };
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  }

  function submit(event: FormEvent<HTMLFormElement>): void {
    event.preventDefault();
    setRevision((current) => current + 1);
    document.getElementById("recommendations")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function reset(): void {
    window.localStorage.removeItem(STORAGE_KEY);
    setDraft(DEFAULT_FORM);
    setRevision((current) => current + 1);
    setConsultationStep(0);
  }

  function moveToStep(step: number): void {
    setConsultationStep(Math.max(0, Math.min(CONSULTATION_STEPS.length - 1, step)));
    if (window.matchMedia("(max-width: 1060px)").matches) {
      window.requestAnimationFrame(() => {
        document.querySelector(".consultation-panel")?.scrollIntoView({ behavior: "smooth", block: "start" });
      });
    }
  }

  return (
    <div className="app-shell" style={atmosphereStyle}>
      <div className="atmosphere" aria-hidden="true">
        <MagneticField primary={primaryAura} secondary={secondaryAura} />
        <span className="aurora aurora-one" />
        <span className="aurora aurora-two" />
        <span className="aurora aurora-three" />
        <span className="perfume-mist mist-one" />
        <span className="perfume-mist mist-two" />
        <span className="grain" />
      </div>

      <header className="site-header">
        <a className="wordmark" href="#top" aria-label="O Antiquário, início">
          <span className="wordmark-seal">OA</span>
          <span>
            <strong>O Antiquário</strong>
            <small>curadoria olfativa pessoal</small>
          </span>
        </a>
        <div
          className="runtime-status"
          title={catalogManifest
            ? `Base factual ${catalogManifest.releaseId} pronta com catálogo curado ativo.`
            : "Todo o cálculo desta tela acontece no seu dispositivo"}
        >
          <i aria-hidden="true" />
          {catalogManifest ? `base factual · ${factualLibrary?.fragrances.length ?? catalogManifest.counts.fragrances} perfumes` : "motor local ativo"}
        </div>
      </header>

      <main id="top">
        <section className="intro-section">
          <div className="intro-index" aria-hidden="true">01 / consulta</div>
          <div className="intro-title">
            <p className="section-kicker">Escolha com intenção</p>
            <h1>O perfume certo<br /><em>para este momento.</em></h1>
            <a className="hero-action" href="#consultation">
              <span>Iniciar consulta</span>
              <b aria-hidden="true">↘</b>
            </a>
          </div>
          <div className="intro-aside">
            <div className="olfactive-orbit" aria-hidden="true">
              <span className="orbit-line orbit-line-one" />
              <span className="orbit-line orbit-line-two" />
              <span className="orbit-core">ar</span>
            </div>
            <p className="intro-copy">
              Conte-nos o clima, o lugar e aquilo que deseja transmitir. O motor cruza contexto,
              desempenho e gosto pessoal — e mostra por que cada escolha faz sentido.
            </p>
            <div className="sensory-legend" aria-label="Pilares da curadoria">
              <span>01 contexto</span>
              <span>02 presença</span>
              <span>03 memória</span>
            </div>
          </div>
        </section>

        <div className="demo-notice" role="note">
          <strong>Catálogo Curado Ativo</strong>
          <span>Exibindo fragrâncias reais curadas a partir da base oficial do O Boticário.</span>
        </div>

        <section className="consultation-layout" id="consultation" aria-label="Consulta olfativa">
          <form className="consultation-panel" onSubmit={submit}>
            <nav className="consultation-steps" aria-label="Etapas da consulta">
              {CONSULTATION_STEPS.map((step, index) => (
                <button
                  className={index === consultationStep ? "is-current" : index < consultationStep ? "is-complete" : ""}
                  type="button"
                  onClick={() => moveToStep(index)}
                  aria-current={index === consultationStep ? "step" : undefined}
                  key={step.number}
                >
                  <span>{step.number}</span>
                  <small>{step.short}</small>
                </button>
              ))}
            </nav>

            <div className="step-heading">
              <div>
                <span className="panel-number">{CONSULTATION_STEPS[consultationStep].number}</span>
                <span>
                  <h2>{CONSULTATION_STEPS[consultationStep].title}</h2>
                  <p>{CONSULTATION_STEPS[consultationStep].description}</p>
                </span>
              </div>
              <button className="text-button" onClick={reset} type="button">restaurar</button>
            </div>

            <div className="consultation-step" key={consultationStep}>
              {consultationStep === 0 && (
                <>
                  <div className="field-grid two-columns">
                    <label>
                      <span>Ocasião</span>
                      <select value={draft.occasion} onChange={(event) => update("occasion", event.target.value)}>
                        <option value="escritório">Escritório</option>
                        <option value="casual">Casual</option>
                        <option value="encontro">Encontro</option>
                        <option value="formal">Evento formal</option>
                        <option value="festa">Festa</option>
                        <option value="esporte">Esporte</option>
                      </select>
                    </label>

                    <label>
                      <span>Ambiente</span>
                      <select value={draft.setting} onChange={(event) => update("setting", event.target.value as Setting)}>
                        <option value="indoor">Interno</option>
                        <option value="outdoor">Externo</option>
                        <option value="mixed">Misto</option>
                      </select>
                    </label>

                    <label>
                      <span>Movimento de pessoas</span>
                      <select value={draft.crowding} onChange={(event) => update("crowding", event.target.value as Crowding)}>
                        <option value="low">Pouco</option>
                        <option value="medium">Moderado</option>
                        <option value="high">Intenso</option>
                      </select>
                    </label>

                    <label>
                      <span>Faixa de preço</span>
                      <select
                        value={draft.maximumPriceTier}
                        onChange={(event) => update("maximumPriceTier", Number(event.target.value) as 1 | 2 | 3 | 4 | 5)}
                      >
                        <option value="1">1 — econômica</option>
                        <option value="2">2 — acessível</option>
                        <option value="3">3 — intermediária</option>
                        <option value="4">4 — premium</option>
                        <option value="5">5 — sem limite</option>
                      </select>
                    </label>
                  </div>

                  <div className="range-group context-ranges">
                    <label>
                      <span>Temperatura <strong>{draft.temperatureC} °C</strong></span>
                      <input
                        type="range"
                        min="5"
                        max="40"
                        value={draft.temperatureC}
                        onChange={(event) => update("temperatureC", Number(event.target.value))}
                      />
                    </label>
                    <label>
                      <span>Umidade <strong>{Math.round(draft.humidity * 100)}%</strong></span>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={draft.humidity * 100}
                        onChange={(event) => update("humidity", Number(event.target.value) / 100)}
                      />
                    </label>
                  </div>

                  <div className="step-insight">
                    <span aria-hidden="true">◌</span>
                    <p>Calor, umidade e circulação alteram a difusão. Usaremos o cenário para equilibrar presença e conforto.</p>
                  </div>
                </>
              )}

              {consultationStep === 1 && (
                <>
                  <div className="presence-meter" aria-hidden="true">
                    <span className="presence-core" />
                    <span className="presence-wave wave-one" />
                    <span className="presence-wave wave-two" />
                    <small>{projectionLabel(draft.desiredProjection)}</small>
                  </div>

                  <div className="range-group presence-ranges">
                    <label>
                      <span>Duração desejada <strong>{draft.durationHours}h</strong></span>
                      <input
                        type="range"
                        min="2"
                        max="14"
                        value={draft.durationHours}
                        onChange={(event) => update("durationHours", Number(event.target.value))}
                      />
                    </label>
                    <label>
                      <span>Projeção <strong>{projectionLabel(draft.desiredProjection)}</strong></span>
                      <input
                        type="range"
                        min="20"
                        max="90"
                        value={draft.desiredProjection * 100}
                        onChange={(event) => update("desiredProjection", Number(event.target.value) / 100)}
                      />
                    </label>
                  </div>

                  <div className="toggle-grid">
                    <label className="toggle-row">
                      <input
                        type="checkbox"
                        checked={draft.sensitiveEnvironment}
                        onChange={(event) => update("sensitiveEnvironment", event.target.checked)}
                      />
                      <span>
                        <strong>Ambiente sensível</strong>
                        bloquear projeção excessiva
                      </span>
                    </label>
                    <label className="toggle-row">
                      <input
                        type="checkbox"
                        checked={draft.strictBudget}
                        onChange={(event) => update("strictBudget", event.target.checked)}
                      />
                      <span>
                        <strong>Orçamento rígido</strong>
                        excluir faixas superiores
                      </span>
                    </label>
                  </div>
                </>
              )}

              {consultationStep === 2 && (
                <>
                  <ChipGroup
                    legend="Acordes que atraem você"
                    options={dynamicAccordOptions}
                    selected={draft.likedAccords}
                    onToggle={(value) => update("likedAccords", toggleValue(draft.likedAccords, value))}
                  />
                  <ChipGroup
                    legend="Acordes que você prefere evitar"
                    options={dynamicAccordOptions}
                    selected={draft.avoidedAccords}
                    onToggle={(value) => update("avoidedAccords", toggleValue(draft.avoidedAccords, value))}
                    tone="negative"
                  />
                  <ChipGroup
                    legend="Notas proibidas nesta consulta"
                    options={dynamicNoteOptions}
                    selected={draft.hardAvoidNotes}
                    onToggle={(value) => update("hardAvoidNotes", toggleValue(draft.hardAvoidNotes, value))}
                    tone="negative"
                  />

                  <label className="novelty-control">
                    <span>
                      Apetite por descoberta
                      <strong>{draft.noveltyPreference < 0.34 ? "familiar" : draft.noveltyPreference > 0.66 ? "explorador" : "equilibrado"}</strong>
                    </span>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={draft.noveltyPreference * 100}
                      onChange={(event) => update("noveltyPreference", Number(event.target.value) / 100)}
                    />
                  </label>
                  <p className="saved-label">Preferências salvas apenas neste dispositivo</p>
                </>
              )}
            </div>

            <div className="step-actions">
              {consultationStep > 0 && (
                <button className="secondary-action" type="button" onClick={() => moveToStep(consultationStep - 1)}>
                  <b aria-hidden="true">←</b>
                  <span>Voltar</span>
                </button>
              )}

              {consultationStep < CONSULTATION_STEPS.length - 1 ? (
                <button className="primary-action" type="button" onClick={() => moveToStep(consultationStep + 1)}>
                  <span>Continuar</span>
                  <b aria-hidden="true">→</b>
                </button>
              ) : (
                <button className="primary-action" type="submit">
                  <span>Revelar minha curadoria</span>
                  <b aria-hidden="true">→</b>
                </button>
              )}
            </div>
          </form>

          <section className="results-panel" id="recommendations" aria-live="polite" key={revision}>
            <div className="result-aurora" aria-hidden="true" />
            <div className="results-heading">
              <div>
                <p className="section-kicker">Curadoria calculada</p>
                <h2>Três caminhos possíveis</h2>
              </div>
              <div className="result-meta">
                <span className="live-aura"><i /> atmosfera responsiva</span>
                <span>motor {result.engineVersion}</span>
                <span>{result.excluded.length} exclusão(ões)</span>
              </div>
            </div>

            {result.recommendations.length > 0 ? (
              <div className="recommendation-list">
                {result.recommendations.map((candidate, index) => (
                  <RecommendationCard candidate={candidate} position={index + 1} key={candidate.fragrance.id} />
                ))}
              </div>
            ) : (
              <div className="empty-state">
                <span aria-hidden="true">∅</span>
                <h3>Nenhuma opção atravessou todos os filtros.</h3>
                <p>Flexibilize uma nota proibida, a faixa de preço ou o teto de projeção.</p>
              </div>
            )}

            <footer className="results-footnote">
              <span>Nota de curadoria</span>
              <p>
                Desempenho é uma estimativa coletiva. Pele, tecido, quantidade aplicada e ventilação podem transformar a experiência.
              </p>
            </footer>
          </section>
        </section>

        {factualLibrary && <FactualLibrary library={factualLibrary} />}
      </main>
    </div>
  );
}
