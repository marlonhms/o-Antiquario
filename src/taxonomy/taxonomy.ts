import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

import { parse } from "yaml";
import { z } from "zod";

import { loadSourceManifest } from "../data/source-manifest.ts";

const stableId = z.string().regex(/^[a-z][a-z0-9-]*$/, "use um ID estável em ASCII e kebab-case");
const isoDate = z.string().regex(/^\d{4}-\d{2}-\d{2}$/);

const BaseTermSchema = z.object({
  id: stableId,
  pt: z.string().min(1),
  en: z.string().min(1),
  source_ids: z.array(z.string().regex(/^[a-z][a-z0-9_]*$/)).min(1),
}).strict();

const FamilySchema = BaseTermSchema;

const ClassifiedTermSchema = BaseTermSchema.extend({
  aliases: z.array(z.string().min(1)),
  family_ids: z.array(stableId).min(1),
}).strict();

export function normalizeOlfactiveText(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("pt-BR")
    .replace(/[_–—-]+/g, " ")
    .replace(/[^\p{Letter}\p{Number}\s]/gu, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function addUniqueIdIssues(
  entries: readonly { id: string }[],
  collection: "families" | "accords" | "notes",
  context: z.RefinementCtx,
): void {
  const ids = new Map<string, number>();
  entries.forEach((entry, index) => {
    const previous = ids.get(entry.id);
    if (previous !== undefined) {
      context.addIssue({
        code: "custom",
        path: [collection, index, "id"],
        message: `ID duplicado '${entry.id}' (primeiro em ${collection}.${previous})`,
      });
    }
    ids.set(entry.id, index);
  });
}

function addAliasCollisionIssues(
  entries: readonly { id: string; pt: string; en: string; aliases: readonly string[] }[],
  collection: "accords" | "notes",
  context: z.RefinementCtx,
): void {
  const index = new Map<string, string>();

  entries.forEach((entry, entryIndex) => {
    const labels = [entry.id, entry.pt, entry.en, ...entry.aliases];
    for (const label of labels) {
      const normalized = normalizeOlfactiveText(label);
      const owner = index.get(normalized);
      if (owner && owner !== entry.id) {
        context.addIssue({
          code: "custom",
          path: [collection, entryIndex, "aliases"],
          message: `termo normalizado '${normalized}' pertence a '${owner}' e '${entry.id}'`,
        });
      } else {
        index.set(normalized, entry.id);
      }
    }
  });
}

export const TaxonomySchema = z.object({
  schema_version: z.literal(1),
  locale_default: z.literal("pt-BR"),
  license: z.literal("CC0-1.0"),
  reviewed_at: isoDate,
  families: z.array(FamilySchema).min(10),
  accords: z.array(ClassifiedTermSchema).min(20),
  notes: z.array(ClassifiedTermSchema).min(150),
}).strict().superRefine((taxonomy, context) => {
  addUniqueIdIssues(taxonomy.families, "families", context);
  addUniqueIdIssues(taxonomy.accords, "accords", context);
  addUniqueIdIssues(taxonomy.notes, "notes", context);
  addAliasCollisionIssues(taxonomy.accords, "accords", context);
  addAliasCollisionIssues(taxonomy.notes, "notes", context);

  const familyIds = new Set(taxonomy.families.map((family) => family.id));
  for (const [collectionName, entries] of [
    ["accords", taxonomy.accords],
    ["notes", taxonomy.notes],
  ] as const) {
    entries.forEach((entry, entryIndex) => {
      entry.family_ids.forEach((familyId, familyIndex) => {
        if (!familyIds.has(familyId)) {
          context.addIssue({
            code: "custom",
            path: [collectionName, entryIndex, "family_ids", familyIndex],
            message: `família inexistente '${familyId}'`,
          });
        }
      });
    });
  }
});

export type OlfactiveTaxonomy = z.infer<typeof TaxonomySchema>;
export type OlfactiveFamily = OlfactiveTaxonomy["families"][number];
export type OlfactiveAccord = OlfactiveTaxonomy["accords"][number];
export type OlfactiveNote = OlfactiveTaxonomy["notes"][number];

export interface TaxonomyIndex {
  readonly accords: ReadonlyMap<string, OlfactiveAccord>;
  readonly notes: ReadonlyMap<string, OlfactiveNote>;
}

function buildTermIndex<T extends { id: string; pt: string; en: string; aliases: readonly string[] }>(
  entries: readonly T[],
): ReadonlyMap<string, T> {
  const index = new Map<string, T>();
  for (const entry of entries) {
    for (const label of [entry.id, entry.pt, entry.en, ...entry.aliases]) {
      index.set(normalizeOlfactiveText(label), entry);
    }
  }
  return index;
}

export function buildTaxonomyIndex(taxonomy: OlfactiveTaxonomy): TaxonomyIndex {
  return {
    accords: buildTermIndex(taxonomy.accords),
    notes: buildTermIndex(taxonomy.notes),
  };
}

export function resolveAccord(index: TaxonomyIndex, value: string): OlfactiveAccord | undefined {
  return index.accords.get(normalizeOlfactiveText(value));
}

export function resolveNote(index: TaxonomyIndex, value: string): OlfactiveNote | undefined {
  return index.notes.get(normalizeOlfactiveText(value));
}

export function validateTaxonomy(input: unknown): OlfactiveTaxonomy {
  return TaxonomySchema.parse(input);
}

export async function validateTaxonomySources(taxonomy: OlfactiveTaxonomy): Promise<void> {
  const manifest = await loadSourceManifest();
  const coreSourceIds = new Set(
    manifest.sources
      .filter((source) => source.classification === "allowed_core")
      .map((source) => source.id),
  );

  const invalid: string[] = [];
  for (const [collection, entries] of [
    ["families", taxonomy.families],
    ["accords", taxonomy.accords],
    ["notes", taxonomy.notes],
  ] as const) {
    for (const entry of entries) {
      for (const sourceId of entry.source_ids) {
        if (!coreSourceIds.has(sourceId)) invalid.push(`${collection}.${entry.id}: ${sourceId}`);
      }
    }
  }

  if (invalid.length > 0) {
    throw new Error(`A taxonomia referencia fontes que não podem alimentar o core:\n${invalid.join("\n")}`);
  }
}

export async function loadTaxonomy(
  path = resolve(process.cwd(), "data", "taxonomy", "taxonomy.yml"),
): Promise<OlfactiveTaxonomy> {
  const contents = await readFile(path, "utf8");
  const taxonomy = validateTaxonomy(parse(contents));
  await validateTaxonomySources(taxonomy);
  return taxonomy;
}

export function taxonomyStats(taxonomy: OlfactiveTaxonomy): {
  families: number;
  accords: number;
  notes: number;
  aliases: number;
} {
  return {
    families: taxonomy.families.length,
    accords: taxonomy.accords.length,
    notes: taxonomy.notes.length,
    aliases: [...taxonomy.accords, ...taxonomy.notes].reduce((total, term) => total + term.aliases.length, 0),
  };
}
