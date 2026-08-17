import type { CompiledKnowledge } from "../knowledge/compiler.ts";
import type { KnowledgeDocument } from "../knowledge/schema.ts";
import type { EligibleForRecommendation } from "../domain/recommendation-contract.ts";
import type { Confidence, Evidence, Fragrance, WeightedTag } from "../domain/types.ts";
import type { PresentationCandidate } from "./presentation-readiness.ts";

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
  const documentsById = new Map(knowledge.documents.map((document) => [document.id, document]));

  for (const doc of knowledge.documents) {
    if (doc.type !== "fragrance" || doc.review_status !== "approved") {
      continue;
    }

    const brandTarget = doc.relations.find((relation) => relation.predicate === "belongs-to-brand")?.target;
    const familyTarget = doc.relations.find((relation) => relation.predicate === "belongs-to-family")?.target;
    if (!brandTarget || !familyTarget) continue;
    const brand = documentsById.get(brandTarget)?.title ?? extractTargetSlug(brandTarget);
    const family = extractTargetSlug(familyTarget);

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
      if (rel.predicate === "declares-concentration") {
        concentrations.push(documentsById.get(rel.target)?.title ?? slug);
      }
      if (rel.predicate === "has-accord") {
        const weight = profile.accords?.[slug];
        if (typeof weight === "number") accords.push({ id: slug, weight });
      }
      if (rel.predicate === "suited-to") {
        const weight = profile.occasions?.[slug];
        if (typeof weight === "number") occasions.push({ id: slug, weight });
      }
    }

    const hasExplicitProfile = profile
      && typeof profile.formality === "number"
      && profile.performance
      && typeof profile.performance === "object";
    if (concentrations.length === 0 || !hasExplicitProfile) continue;

    const candidate: Fragrance = {
      id: extractTargetSlug(doc.id),
      name: doc.title,
      brand,
      family,
      segments: Array.isArray(profile.segments) ? profile.segments : [],
      concentrations,
      topNotes,
      heartNotes,
      baseNotes,
      accords,
      occasions,
      formality: profile.formality,
      performance: profile.performance,
      climate: profile.climate && typeof profile.climate === "object" ? profile.climate : {},
      ...(profile.priceTier !== undefined ? { priceTier: profile.priceTier } : {}),
      dataConfidence: parseConfidence(doc.confidence),
      evidence: getEvidence(doc),
    };

    candidates.push(candidate);
  }

  return candidates;
}

const PRESENTATION_NOTE_PREDICATES = new Set([
  "declares-top-note",
  "declares-heart-note",
  "declares-base-note",
  "declares-unlayered-note",
  "has-top-note",
  "has-heart-note",
  "has-base-note",
  "has-note",
]);

export function compilePresentationCandidates(
  knowledge: CompiledKnowledge,
): readonly PresentationCandidate[] {
  const documentsById = new Map(knowledge.documents.map((document) => [document.id, document]));
  return knowledge.documents
    .filter((document) => document.type === "fragrance" && document.review_status === "approved")
    .map((document) => {
      const brandTarget = document.relations.find((relation) => relation.predicate === "belongs-to-brand")?.target;
      const familyTarget = document.relations.find((relation) => relation.predicate === "belongs-to-family")?.target;
      return {
        id: extractTargetSlug(document.id),
        name: document.title,
        brand: brandTarget
          ? documentsById.get(brandTarget)?.title ?? extractTargetSlug(brandTarget)
          : "Desconhecida",
        family: familyTarget ? extractTargetSlug(familyTarget) : "não-classificada",
        noteCount: document.relations.filter((relation) => PRESENTATION_NOTE_PREDICATES.has(relation.predicate)).length,
        accordCount: document.relations.filter((relation) => relation.predicate === "has-accord").length,
        evidence: getEvidence(document),
      };
    });
}
