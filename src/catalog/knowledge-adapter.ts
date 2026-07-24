import type { CompiledKnowledge } from "../knowledge/compiler.ts";
import type { KnowledgeDocument } from "../knowledge/schema.ts";
import type { EligibleForRecommendation } from "../domain/recommendation-contract.ts";
import type { Confidence, Evidence, Fragrance, WeightedTag } from "../domain/types.ts";

function extractTargetSlug(target: string): string {
  const parts = target.split(":");
  return parts[parts.length - 1]!;
}

function parseConfidence(confidence: string): Confidence {
  if (["high", "medium", "low"].includes(confidence)) return confidence as Confidence;
  return "unknown";
}

function getEvidence(doc: KnowledgeDocument): Evidence[] {
  return doc.evidence.map((ev) => ({
    sourceId: ev.source_id,
    kind: (ev.kind === "scientific" ? "curated" : ev.kind) as Evidence["kind"],
    confidence: parseConfidence(ev.confidence),
    license: ev.license,
    sourceUrl: ev.locator,
    retrievedAt: ev.retrieved_at,
  }));
}

export function compileRecommendationCandidates(
  knowledge: CompiledKnowledge
): readonly EligibleForRecommendation[] {
  const candidates: EligibleForRecommendation[] = [];

  for (const doc of knowledge.documents) {
    if (doc.type !== "fragrance" || doc.review_status !== "approved") {
      continue;
    }

    const brand = doc.relations.find((r) => r.predicate === "belongs-to-brand")?.target || "Desconhecida";
    const family = doc.relations.find((r) => r.predicate === "belongs-to-family")?.target || "não-classificada";

    const topNotes: string[] = [];
    const heartNotes: string[] = [];
    const baseNotes: string[] = [];
    const concentrations: string[] = [];
    const accords: WeightedTag[] = [];
    const occasions: WeightedTag[] = [];

    const profile = doc.recommendation_profile || {};

    for (const rel of doc.relations) {
      const slug = extractTargetSlug(rel.target);
      if (rel.predicate === "declares-top-note" || rel.predicate === "has-top-note") topNotes.push(slug);
      if (rel.predicate === "declares-heart-note" || rel.predicate === "has-heart-note") heartNotes.push(slug);
      if (rel.predicate === "declares-base-note" || rel.predicate === "has-base-note") baseNotes.push(slug);
      if (rel.predicate === "declares-unlayered-note" || rel.predicate === "has-note") {
        heartNotes.push(slug); // fallback
      }
      if (rel.predicate === "declares-concentration") concentrations.push(slug);
      if (rel.predicate === "has-accord") {
        accords.push({ id: slug, weight: profile.accords?.[slug] ?? 0.8 });
      }
      if (rel.predicate === "suited-to") {
        occasions.push({ id: slug, weight: profile.occasions?.[slug] ?? 0.8 });
      }
    }

    if (concentrations.length === 0) concentrations.push("eau-de-parfum");

    const defaultPerformance = {
      longevity: { minimumHours: 4, maximumHours: 6, confidence: "low" as Confidence },
      projection: { value: 0.5, confidence: "low" as Confidence },
      sillage: { value: 0.5, confidence: "low" as Confidence },
    };

    const defaultClimate = {
      idealTemperatureMinC: 15,
      idealTemperatureMaxC: 30,
      idealHumidity: 0.5,
      indoorFit: 0.8,
      outdoorFit: 0.8,
    };

    const candidate: Fragrance = {
      id: extractTargetSlug(doc.id),
      name: doc.title,
      brand: extractTargetSlug(brand),
      family: extractTargetSlug(family),
      segments: profile.segments || ["acessivel"],
      concentrations,
      topNotes,
      heartNotes,
      baseNotes,
      accords,
      occasions,
      formality: profile.formality ?? 0.5,
      performance: profile.performance || defaultPerformance,
      climate: profile.climate || defaultClimate,
      priceTier: profile.priceTier || 2,
      dataConfidence: parseConfidence(doc.confidence),
      evidence: getEvidence(doc),
    };

    candidates.push(candidate);
  }

  return candidates;
}
