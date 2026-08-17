import { useEffect, useMemo, useReducer, useRef, useState } from "react";
import type { CSSProperties } from "react";

import type {
  Confidence,
  RecommendationResult,
  ScoreFactorName,
} from "@core/domain/types.ts";
import { loadCatalogReleaseManifest, type CatalogReleaseManifest } from "@core/catalog/release.ts";
import { recommend } from "@core/recommender/recommend.ts";
import type { Fragrance } from "@core/domain/types.ts";
import type { CompiledRecommendationCatalog } from "@core/catalog/recommendation-compiler.ts";
import type {
  OlfactoryReference,
  OlfactoryReferenceCatalog,
} from "@core/catalog/olfactory-reference.ts";
import { deriveSynesthesia } from "@core/domain/synesthesia.ts";

import type {
  ConsultationIntentV2,
  Setting,
  TimePeriod,
  WeatherBand,
} from "./features/consultation/domain/consultation-schema.ts";
import {
  DEFAULT_INTENT_V2,
  STORAGE_KEY_V1,
  STORAGE_KEY_V2,
  migrateV1ToV2,
} from "./features/consultation/domain/migrate-v1-to-v2.ts";
import {
  deriveAccordWeights,
  deriveContext,
  deriveFormalityByOccasion,
} from "./features/consultation/domain/derive-context.ts";
import {
  consultationReducer,
  type ConsultationState,
} from "./features/consultation/domain/consultation-reducer.ts";
import { MomentPicker } from "./features/consultation/ui/MomentPicker.tsx";
import { AtmospherePicker } from "./features/consultation/ui/AtmospherePicker.tsx";
import { ContextSummary } from "./features/consultation/ui/ContextSummary.tsx";
import { RefinementDrawer } from "./features/consultation/ui/RefinementDrawer.tsx";

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

const CORE_ACCORD_OPTIONS = Object.keys(ACCORD_AURAS);
const CORE_NOTE_OPTIONS = ["bergamota", "baunilha", "cedro", "jasmim", "lavanda", "patchouli", "rosa", "sândalo", "vetiver"];

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
  concentrations?: string[];
  referenceReadiness?: "olfactory_reference_only";
  referenceLimitations?: string[];
  referenceSources?: string[];
  recordLabel?: string;
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

async function loadOlfactoryReferenceCatalog(): Promise<OlfactoryReferenceCatalog> {
  const response = await fetch("/catalog/olfactory-reference-catalog.json");
  if (!response.ok) throw new Error("Catálogo de referências olfativas indisponível");
  return response.json() as Promise<OlfactoryReferenceCatalog>;
}

function referenceTerms(reference: OlfactoryReference) {
  return [
    ...reference.pyramid.top,
    ...reference.pyramid.heart,
    ...reference.pyramid.base,
    ...reference.pyramid.unlayered,
    ...reference.accords,
  ];
}

function referenceNotes(reference: OlfactoryReference) {
  return [
    ...reference.pyramid.top,
    ...reference.pyramid.heart,
    ...reference.pyramid.base,
    ...reference.pyramid.unlayered,
  ];
}

function normalizeOption(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("pt-BR")
    .trim();
}

function mergeOlfactoryReferencesIntoFactual(
  library: FactualLibraryData,
  catalog: OlfactoryReferenceCatalog | null,
): FactualLibraryData {
  if (!catalog || catalog.references.length === 0) return library;

  const fragrances = library.fragrances.map((fragrance) => ({
    ...fragrance,
    brandIds: [...fragrance.brandIds],
    perfumerIds: [...fragrance.perfumerIds],
    countryIds: [...fragrance.countryIds],
    olfactoryDescriptorIds: [...fragrance.olfactoryDescriptorIds],
  }));
  const byId = new Map(fragrances.map((fragrance) => [fragrance.id, fragrance]));
  const byName = new Map(fragrances.map((fragrance) => [fragrance.name.toLocaleLowerCase("pt-BR").trim(), fragrance]));
  const brands = [...library.entities.brands];
  const perfumers = [...library.entities.perfumers];
  const descriptors = [...library.entities.olfactoryDescriptors];
  const brandIds = new Set(brands.map((brand) => brand.id));
  const perfumerIds = new Set(perfumers.map((perfumer) => perfumer.id));
  const descriptorIds = new Set(descriptors.map((descriptor) => descriptor.id));

  for (const reference of catalog.references) {
    if (!brandIds.has(reference.brand.id)) {
      brands.push({ id: reference.brand.id, name: reference.brand.name });
      brandIds.add(reference.brand.id);
    }
    for (const perfumer of reference.perfumers) {
      if (!perfumerIds.has(perfumer.id)) {
        perfumers.push(perfumer);
        perfumerIds.add(perfumer.id);
      }
    }
    const terms = referenceTerms(reference);
    for (const item of terms) {
      if (!descriptorIds.has(item.id)) {
        descriptors.push({ id: item.id, name: item.label });
        descriptorIds.add(item.id);
      }
    }
    const existing = byId.get(reference.id)
      ?? byName.get(reference.name.toLocaleLowerCase("pt-BR").trim());
    const metadata: Pick<
      FactualFragrance,
      "topNotes" | "heartNotes" | "baseNotes" | "concentrations" | "referenceReadiness" | "referenceLimitations" | "referenceSources"
    > = {
      topNotes: reference.pyramid.top.map((item) => item.label),
      heartNotes: reference.pyramid.heart.map((item) => item.label),
      baseNotes: reference.pyramid.base.map((item) => item.label),
      concentrations: reference.concentrations.map((item) => item.label),
      referenceReadiness: reference.readiness,
      referenceLimitations: [...reference.limitations],
      referenceSources: reference.evidence.map((item) => item.sourceId),
    };
    if (existing) {
      existing.brandIds = [...new Set([...existing.brandIds, reference.brand.id])];
      existing.perfumerIds = [...new Set([...existing.perfumerIds, ...reference.perfumers.map((item) => item.id)])];
      existing.olfactoryDescriptorIds = [...new Set([
        ...existing.olfactoryDescriptorIds,
        ...terms.map((item) => item.id),
      ])];
      Object.assign(existing, metadata);
      existing.recordLabel = "Referência olfativa";
      existing.officialWebsite ??= reference.evidence.find((item) => item.locator)?.locator ?? null;
      continue;
    }
    const created: FactualFragrance = {
      id: reference.id,
      wikidataId: "OlfactoryReference",
      name: reference.name,
      launchYear: null,
      officialWebsite: reference.evidence.find((item) => item.locator)?.locator ?? null,
      brandIds: [reference.brand.id],
      perfumerIds: reference.perfumers.map((item) => item.id),
      countryIds: [],
      olfactoryDescriptorIds: [...new Set(terms.map((item) => item.id))],
      recordLabel: "Referência olfativa",
      ...metadata,
    };
    fragrances.push(created);
    byId.set(created.id, created);
    byName.set(created.name.toLocaleLowerCase("pt-BR").trim(), created);
  }

  return {
    fragrances,
    entities: { ...library.entities, brands, perfumers, olfactoryDescriptors: descriptors },
    claims: library.claims,
  };
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

function readStoredIntent(): ConsultationIntentV2 {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY_V2) || window.localStorage.getItem(STORAGE_KEY_V1);
    return migrateV1ToV2(raw);
  } catch {
    return DEFAULT_INTENT_V2;
  }
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

function runRecommendationV2(
  intent: ConsultationIntentV2,
  catalog: readonly Fragrance[],
): RecommendationResult {
  const context = deriveContext(intent);
  const accordWeights = deriveAccordWeights(intent.atmosphere);
  const accordPreferences: Record<string, number> = { ...accordWeights };
  for (const avoided of intent.avoidedCanonicalIds) {
    accordPreferences[avoided] = -0.9;
  }

  const noveltyPreference =
    intent.discovery === "familiar" ? 0.25 : intent.discovery === "exploratory" ? 0.85 : 0.55;

  return recommend(
    catalog,
    {
      accordPreferences,
      hardAvoidNotes: intent.hardAvoidNotes,
      noveltyPreference,
    },
    {
      occasion: intent.occasion,
      setting: context.setting,
      crowding: context.crowding,
      temperatureC: context.temperatureC,
      humidity: context.humidity,
      formality: deriveFormalityByOccasion(intent.occasion),
      projectionCeiling: intent.sensitiveEnvironment ? 0.72 : undefined,
    },
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
  const synesthesia = deriveSynesthesia(fragrance);
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
          <span>{synesthesia.chromaticAura.colorFamily}</span>
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

        <div className="synesthetic-atmosphere" aria-label="Atmosfera sinestésica e pistas transmodais">
          <div className="synesthetic-header">
            <span className="synesthetic-tag">Aura Sinestésica</span>
            <span className="synesthetic-soundscape-tag">{synesthesia.naturalSoundscape}</span>
          </div>
          <div className="synesthetic-grid">
            <div className="synesthetic-item">
              <small>🎵 Trilha & Timbres</small>
              <p>{synesthesia.musicalMood}</p>
              <span className="instruments-badge">{synesthesia.primaryInstruments.slice(0, 2).join(" · ")}</span>
            </div>
            <div className="synesthetic-item">
              <small>🎙️ Voz do Companion</small>
              <p>{synesthesia.voiceProfile.description}</p>
            </div>
          </div>
          <div className="emotional-descriptors" aria-label="Descritores poéticos KAORIUM">
            {synesthesia.emotionalDescriptors.map((desc) => (
              <span className="emotional-chip" key={desc}>{desc}</span>
            ))}
          </div>
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

function referenceToFragrance(reference: OlfactoryReference): Fragrance {
  return {
    id: reference.id,
    name: reference.name,
    brand: reference.brand.name,
    family: reference.family?.name ?? reference.accords[0]?.label ?? "amadeirado",
    segments: ["nacional", "referencia"],
    concentrations: reference.concentrations.map((c) => c.label),
    topNotes: reference.pyramid.top.map((n) => n.label),
    heartNotes: reference.pyramid.heart.map((n) => n.label),
    baseNotes: reference.pyramid.base.map((n) => n.label),
    accords: reference.accords.map((a) => ({ id: a.label, weight: 0.85 })),
    occasions: [],
    formality: 0.5,
    performance: {
      longevity: { minimumHours: 5, maximumHours: 8, confidence: "medium" },
      projection: { value: 0.5, confidence: "medium" },
      sillage: { value: 0.5, confidence: "medium" },
    },
    climate: {},
    dataConfidence: "medium",
    evidence: [],
  };
}

function ReferenceCard({ reference }: { reference: OlfactoryReference }) {
  const synesthesia = useMemo(() => deriveSynesthesia(referenceToFragrance(reference)), [reference]);
  const noteCount = reference.pyramid.top.length
    + reference.pyramid.heart.length
    + reference.pyramid.base.length
    + reference.pyramid.unlayered.length;
  const declared = referenceTerms(reference).some((item) => item.claimNature === "declared");
  const layers = [
    { label: "Saída", terms: reference.pyramid.top },
    { label: "Coração", terms: reference.pyramid.heart },
    { label: "Fundo", terms: reference.pyramid.base },
    { label: "Sem camada", terms: reference.pyramid.unlayered },
  ].filter((layer) => layer.terms.length > 0);

  return (
    <article className="reference-card" style={{ "--aura-primary": synesthesia.chromaticAura.dominantHsl } as CSSProperties}>
      <div className="reference-card-head">
        <span aria-hidden="true">{reference.name.charAt(0)}</span>
        <div>
          <small>{declared ? "declaração estruturada" : "pirâmide estruturada na fonte"}</small>
          <h3>{reference.name}</h3>
          <p>{reference.brand.name}</p>
        </div>
      </div>
      {(reference.concentrations.length > 0 || reference.accords.length > 0) && (
        <div className="reference-structure">
          {reference.concentrations.length > 0 && (
            <p><small>Concentração na fonte</small>{reference.concentrations.map((item) => item.label).join(" · ")}</p>
          )}
          {reference.accords.length > 0 && (
            <p><small>Acordes principais</small>{reference.accords.slice(0, 5).map((item) => item.label).join(" · ")}</p>
          )}
        </div>
      )}

      {/* Atmosfera Sinestésica & Áudio-Olfato (Estudos Mahdavi et al., 2020 e KAORIUM) */}
      <div className="synesthetic-atmosphere" aria-label="Atmosfera e sinestesia áudio-olfativa">
        <div className="synesthetic-header">
          <small>Atmosfera Sinestésica</small>
          <span className="synesthetic-badge" style={{ color: synesthesia.chromaticAura.dominantHsl }}>
            Aura {synesthesia.chromaticAura.colorFamily}
          </span>
        </div>
        <div className="synesthetic-grid">
          <div className="synesthetic-item">
            <small>Som da Natureza</small>
            <p>{synesthesia.naturalSoundscape}</p>
          </div>
          <div className="synesthetic-item">
            <small>🎵 Trilha & Timbres</small>
            <p>{synesthesia.musicalMood}</p>
            <span className="instruments-badge">
              {synesthesia.primaryInstruments.slice(0, 2).join(" · ")}
            </span>
          </div>
          <div className="synesthetic-item">
            <small>🎙️ Voz do Companion</small>
            <p>{synesthesia.voiceProfile.description}</p>
          </div>
        </div>
        <div className="emotional-descriptors" aria-label="Descritores poéticos KAORIUM">
          {synesthesia.emotionalDescriptors.map((desc) => (
            <span className="emotional-chip" key={desc}>{desc}</span>
          ))}
        </div>
      </div>

      <div className="reference-pyramid">
        {layers.map((layer) => (
          <div key={layer.label}>
            <small>{layer.label}</small>
            <p>{layer.terms.slice(0, 5).map((item) => item.label).join(" · ")}</p>
          </div>
        ))}
      </div>
      <footer>
        <span>{noteCount} termos olfativos</span>
        {reference.evidence.find((item) => item.locator)?.locator
          ? <a href={reference.evidence.find((item) => item.locator)!.locator} target="_blank" rel="noreferrer">ver registro da fonte ↗</a>
          : <span>{[...new Set(reference.evidence.map((item) => item.sourceId))].join(" · ")}</span>}
      </footer>
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
        <p>{library.fragrances.length} perfumes · {library.entities.olfactoryDescriptors.length} termos · fontes abertas aprovadas</p>
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
                <p className="section-kicker">Registro factual · {selected.recordLabel ?? selected.wikidataId}</p>
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
              <div>
                <small>Concentração na fonte</small>
                <p>{selected.concentrations?.join(" · ") || "não declarada"}</p>
              </div>
            </div>

            {((selected.topNotes && selected.topNotes.length > 0) ||
              (selected.heartNotes && selected.heartNotes.length > 0) ||
              (selected.baseNotes && selected.baseNotes.length > 0)) && (
              <div className="fact-group">
                <small>{selected.referenceReadiness
                  ? "Pirâmide olfativa estruturada na fonte"
                  : "Pirâmide olfativa (extração oficial PDF)"}</small>
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

            {selected.referenceReadiness && (
              <div className="reference-boundary" role="note">
                <strong>Referência olfativa</strong>
                <p>Este registro ajuda a compreender o cheiro, mas não sustenta indicação de ocasião, clima, fixação ou projeção.</p>
              </div>
            )}

            <div className="fact-group">
              <small>{selected.referenceReadiness ? "Termos olfativos estruturados" : "Descritores olfativos declarados"}</small>
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
              {selected.officialWebsite && <a href={selected.officialWebsite} target="_blank" rel="noreferrer">registro da fonte ↗</a>}
            </div>
          </article>
        )}
      </div>
    </section>
  );
}

export function App() {
  const [consultationState, dispatch] = useReducer(consultationReducer, {
    step: "moment",
    intent: readStoredIntent(),
    isRefinementOpen: false,
    isContextCorrectionOpen: false,
  });

  const { intent, step, isRefinementOpen, isContextCorrectionOpen } = consultationState;
  const derivedContext = useMemo(() => deriveContext(intent), [intent]);

  const [catalogManifest, setCatalogManifest] = useState<CatalogReleaseManifest | null>(null);
  const [rawFactualLibrary, setFactualLibrary] = useState<FactualLibraryData | null>(null);
  const [recommendationCatalog, setRecommendationCatalog] = useState<readonly Fragrance[]>([]);
  const [recommendationStatus, setRecommendationStatus] = useState<"loading" | "ready" | "unavailable">("loading");
  const [referenceCatalog, setReferenceCatalog] = useState<OlfactoryReferenceCatalog | null>(null);

  const factualLibrary = useMemo(
    () => rawFactualLibrary
      ? mergeRecommendationIntoFactual(
        mergeOlfactoryReferencesIntoFactual(rawFactualLibrary, referenceCatalog),
        recommendationCatalog,
      )
      : null,
    [rawFactualLibrary, recommendationCatalog, referenceCatalog],
  );

  const dynamicAccordOptions = useMemo(() => {
    const accords = new Set<string>();
    for (const f of recommendationCatalog) {
      for (const a of f.accords) {
        accords.add(a.id);
      }
    }
    for (const reference of referenceCatalog?.references ?? []) {
      for (const accord of reference.accords) accords.add(accord.label);
    }
    return accords.size > 0 ? Array.from(accords).sort() : CORE_ACCORD_OPTIONS;
  }, [recommendationCatalog, referenceCatalog]);

  const dynamicNoteOptions = useMemo(() => {
    const notes = new Set<string>();
    for (const f of recommendationCatalog) {
      for (const n of f.topNotes) notes.add(n);
      for (const n of f.heartNotes) notes.add(n);
      for (const n of f.baseNotes) notes.add(n);
    }
    const frequency = new Map<string, number>();
    for (const reference of referenceCatalog?.references ?? []) {
      for (const item of referenceNotes(reference)) {
        frequency.set(item.label, (frequency.get(item.label) ?? 0) + 1);
      }
    }
    if (frequency.size > 0) {
      return [...frequency]
        .sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0], "pt-BR"))
        .slice(0, 18)
        .map(([label]) => label);
    }
    return notes.size > 0 ? Array.from(notes).sort() : CORE_NOTE_OPTIONS;
  }, [recommendationCatalog, referenceCatalog]);

  const referenceExamples = useMemo(() => {
    const avoidedNotes = new Set(intent.hardAvoidNotes.map(normalizeOption));
    const avoidedAccords = new Set(intent.avoidedCanonicalIds.map(normalizeOption));
    const targetWeights = deriveAccordWeights(intent.atmosphere);
    const likedAccords = new Set(Object.keys(targetWeights).map(normalizeOption));

    const matchCount = (reference: OlfactoryReference) => reference.accords
      .filter((item) => likedAccords.has(normalizeOption(item.label))).length;

    return [...(referenceCatalog?.references ?? [])]
      .filter((reference) => !referenceNotes(reference).some((item) => avoidedNotes.has(normalizeOption(item.label))))
      .filter((reference) => !reference.accords.some((item) => avoidedAccords.has(normalizeOption(item.label))))
      .sort((left, right) => {
        const matchDifference = matchCount(right) - matchCount(left);
        const coverageDifference = referenceNotes(right).length - referenceNotes(left).length;
        return matchDifference || coverageDifference || left.name.localeCompare(right.name, "pt-BR");
      })
      .slice(0, 3);
  }, [intent.avoidedCanonicalIds, intent.hardAvoidNotes, intent.atmosphere, referenceCatalog]);

  const result = useMemo(() => runRecommendationV2(intent, recommendationCatalog), [intent, recommendationCatalog]);
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
    loadOlfactoryReferenceCatalog()
      .then((catalog) => {
        if (active) setReferenceCatalog(catalog);
      })
      .catch(() => {
        if (active) setReferenceCatalog(null);
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
        if (active) {
          setRecommendationCatalog(catalog);
          setRecommendationStatus("ready");
        }
      })
      .catch(() => {
        if (active) {
          setRecommendationCatalog([]);
          setRecommendationStatus("unavailable");
        }
      });
    return () => {
      active = false;
    };
  }, []);

  const hasRankableFragrances = recommendationCatalog.length > 0;
  const factualCount = factualLibrary?.fragrances.length ?? catalogManifest?.counts.fragrances ?? 0;

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
            ? `Base factual ${catalogManifest.releaseId} pronta. Recomendações só são liberadas após validação de evidência.`
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
              Declare o momento e a sensação desejada. O motor deriva o contexto e consulta fatos
              aprovados para responder com clareza — sem exigir estimativas técnicas ou jargões complexos.
            </p>
            <div className="sensory-legend" aria-label="Pilares da curadoria">
              <span>01 momento</span>
              <span>02 atmosfera</span>
              <span>03 curadoria</span>
            </div>
          </div>
        </section>

        <div className="demo-notice" role="note">
          <strong>{hasRankableFragrances ? "Curadoria validada" : "Acervo factual ativo"}</strong>
          <span>{hasRankableFragrances
            ? `${recommendationCatalog.length} fragrâncias atravessaram o gate de recomendação.`
            : recommendationStatus === "loading"
              ? "Validando as evidências disponíveis para recomendação contextual."
              : `${referenceCatalog?.count ?? 0} referências olfativas e ${factualCount} registros reais podem ser explorados; o ranking contextual permanece em calibração.`}</span>
        </div>

        <section className="consultation-layout" id="consultation" aria-label="Consulta olfativa simplificada">
          <div className="consultation-panel">
            <nav className="consultation-steps" aria-label="Etapas da consulta">
              <button
                className={step === "moment" ? "is-current" : "is-complete"}
                type="button"
                onClick={() => dispatch({ type: "SET_STEP", step: "moment" })}
                aria-current={step === "moment" ? "step" : undefined}
              >
                <span>01</span>
                <small>Momento</small>
              </button>
              <button
                className={step === "atmosphere" ? "is-current" : step === "results" ? "is-complete" : ""}
                type="button"
                onClick={() => dispatch({ type: "SET_STEP", step: "atmosphere" })}
                aria-current={step === "atmosphere" ? "step" : undefined}
              >
                <span>02</span>
                <small>Atmosfera</small>
              </button>
              <button
                className={step === "results" ? "is-current" : ""}
                type="button"
                onClick={() => dispatch({ type: "SET_STEP", step: "results" })}
                aria-current={step === "results" ? "step" : undefined}
              >
                <span>03</span>
                <small>Curadoria</small>
              </button>
            </nav>

            {step === "moment" && (
              <div className="consultation-step">
                <div className="step-heading">
                  <div>
                    <span className="panel-number">01</span>
                    <span>
                      <h2>Para qual momento?</h2>
                      <p>Onde e quando o perfume encontrará você?</p>
                    </span>
                  </div>
                  <button className="text-button" onClick={() => dispatch({ type: "RESET_ALL" })} type="button">restaurar</button>
                </div>

                <MomentPicker
                  selected={intent.occasion}
                  onSelect={(occ) => {
                    dispatch({ type: "SELECT_OCCASION", occasion: occ });
                  }}
                />
              </div>
            )}

            {step === "atmosphere" && (
              <div className="consultation-step">
                <div className="step-heading">
                  <div>
                    <span className="panel-number">02</span>
                    <span>
                      <h2>Que atmosfera você quer criar?</h2>
                      <p>Qual sensação sensorial e assinatura pessoal você deseja transmitir?</p>
                    </span>
                  </div>
                  <button className="text-button" onClick={() => dispatch({ type: "RESET_ALL" })} type="button">restaurar</button>
                </div>

                <AtmospherePicker
                  selected={intent.atmosphere}
                  onSelect={(atm) => {
                    dispatch({ type: "SELECT_ATMOSPHERE", atmosphere: atm });
                    window.requestAnimationFrame(() => {
                      document.getElementById("recommendations")?.scrollIntoView({ behavior: "smooth", block: "start" });
                    });
                  }}
                />

                <div className="step-actions">
                  <button
                    className="secondary-action"
                    type="button"
                    onClick={() => dispatch({ type: "SET_STEP", step: "moment" })}
                  >
                    <b aria-hidden="true">←</b>
                    <span>Voltar</span>
                  </button>
                </div>
              </div>
            )}

            {step === "results" && (
              <div className="consultation-step">
                <div className="step-heading">
                  <div>
                    <span className="panel-number">03</span>
                    <span>
                      <h2>Sua Curadoria Pessoal</h2>
                      <p>Caminhos olfativos calculados para o seu momento.</p>
                    </span>
                  </div>
                  <div className="step-heading-actions">
                    <button
                      className="pill-action"
                      onClick={() => dispatch({ type: "SET_REFINEMENT_OPEN", isOpen: true })}
                      type="button"
                    >
                      ⚙️ Ajustar detalhes
                    </button>
                    <button className="text-button" onClick={() => dispatch({ type: "RESET_ALL" })} type="button">restaurar</button>
                  </div>
                </div>

                <ContextSummary
                  context={derivedContext}
                  isOpen={isContextCorrectionOpen}
                  onToggleOpen={() => dispatch({ type: "SET_CONTEXT_CORRECTION_OPEN", isOpen: !isContextCorrectionOpen })}
                  onUpdateSetting={(s) => dispatch({ type: "SET_CONTEXT_OVERRIDE", overrides: { setting: s } })}
                  onUpdateWeather={(w) => dispatch({ type: "SET_CONTEXT_OVERRIDE", overrides: { weatherBand: w } })}
                  onUpdatePeriod={(p) => dispatch({ type: "SET_CONTEXT_OVERRIDE", overrides: { period: p } })}
                />

                <div className="step-actions">
                  <button
                    className="secondary-action"
                    type="button"
                    onClick={() => dispatch({ type: "SET_STEP", step: "atmosphere" })}
                  >
                    <b aria-hidden="true">←</b>
                    <span>Mudar atmosfera</span>
                  </button>
                  <button
                    className="primary-action"
                    type="button"
                    onClick={() => dispatch({ type: "SET_REFINEMENT_OPEN", isOpen: true })}
                  >
                    <span>Refinar preferências</span>
                    <b aria-hidden="true">⚙️</b>
                  </button>
                </div>
              </div>
            )}
          </div>

          <section className="results-panel" id="recommendations" aria-live="polite">
            <div className="result-aurora" aria-hidden="true" />
            <div className="results-heading">
              <div>
                <p className="section-kicker">
                  {hasRankableFragrances ? "Curadoria calculada" : "Curadoria sensorial de referências"}
                </p>
                <h2>
                  {hasRankableFragrances
                    ? "Três caminhos possíveis"
                    : "Três referências para explorar"}
                </h2>
              </div>
              <div className="result-meta">
                <span className="live-aura"><i /> atmosfera responsiva</span>
                <span>{hasRankableFragrances ? `motor ${result.engineVersion}` : "correspondência áudio-olfativa ativa"}</span>
                {result.excluded.length > 0 && <span>{result.excluded.length} exclusão(ões)</span>}
              </div>
            </div>

            {hasRankableFragrances ? (
              result.recommendations.length > 0 ? (
                <div className="recommendation-list">
                  {result.recommendations.map((candidate, index) => (
                    <RecommendationCard candidate={candidate} position={index + 1} key={candidate.fragrance.id} />
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  <span aria-hidden="true">∅</span>
                  <h3>Nenhuma opção atravessou todos os filtros com os critérios atuais.</h3>
                  <p>Flexibilize uma nota proibida ou o teto de projeção no menu de refinamento.</p>
                </div>
              )
            ) : (
              referenceExamples.length > 0 ? (
                <div className="recommendation-list">
                  {referenceExamples.map((reference) => (
                    <ReferenceCard reference={reference} key={reference.id} />
                  ))}
                </div>
              ) : (
                <div className="empty-state">
                  <span aria-hidden="true">∅</span>
                  <h3>Nenhuma referência olfativa encontrada para a combinação atual.</h3>
                  <p>Tente selecionar outra atmosfera ou flexibilizar os acordes a evitar no refinamento.</p>
                </div>
              )
            )}

            <footer className="results-footnote">
              <span>Nota de curadoria</span>
              <p>
                {hasRankableFragrances
                  ? "Desempenho é uma estimativa coletiva. Pele, tecido, quantidade aplicada e ventilação podem transformar a experiência."
                  : "Aproximações olfativas e correspondências transmodais baseadas nos estudos de Mahdavi et al. (2020) e Piesse (1867). O Antiquário separa rigorosamente fatos de composição de estimativas de desempenho."}
              </p>
            </footer>
          </section>
        </section>

        {factualLibrary && <FactualLibrary library={factualLibrary} />}

        <RefinementDrawer
          isOpen={isRefinementOpen}
          intent={intent}
          availableAccords={dynamicAccordOptions}
          availableNotes={dynamicNoteOptions}
          onClose={() => dispatch({ type: "SET_REFINEMENT_OPEN", isOpen: false })}
          onToggleAvoidedAccord={(acc) => dispatch({ type: "TOGGLE_AVOIDED_ACCORD", accord: acc })}
          onToggleHardAvoidNote={(not) => dispatch({ type: "TOGGLE_HARD_AVOID_NOTE", note: not })}
          onToggleSensitiveEnvironment={(val) => dispatch({ type: "UPDATE_INTENT", updates: { sensitiveEnvironment: val } })}
          onSelectDiscovery={(disc) => dispatch({ type: "UPDATE_INTENT", updates: { discovery: disc } })}
        />
      </main>
    </div>
  );
}
