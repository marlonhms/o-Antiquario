import { z } from "zod";

const hash = z.string().regex(/^[a-f0-9]{64}$/);

const ReleaseFileSchema = z.object({
  path: z.string().min(1),
  sha256: hash,
  bytes: z.number().int().nonnegative(),
}).strict();

export const CatalogReleaseManifestSchema = z.object({
  schemaVersion: z.literal(1),
  releaseId: z.string().regex(/^catalog-web-v1-[a-f0-9]{12}$/),
  contentHash: hash,
  catalogVersion: z.string().regex(/^catalog-v1-[a-f0-9]{12}$/),
  knowledgeReleaseId: z.string().regex(/^knowledge-v[12]-[a-f0-9]{12}$/),
  counts: z.object({
    fragrances: z.number().int().nonnegative(),
    brands: z.number().int().nonnegative(),
    perfumers: z.number().int().nonnegative(),
    countries: z.number().int().nonnegative(),
    olfactoryDescriptors: z.number().int().nonnegative(),
    semanticClaims: z.number().int().nonnegative(),
    semanticPropertyKinds: z.number().int().nonnegative(),
    knowledgeLinks: z.number().int().nonnegative(),
    searchTerms: z.number().int().nonnegative(),
    ambiguousClusters: z.number().int().nonnegative(),
  }).strict(),
  sources: z.array(z.object({
    id: z.string().min(1),
    license: z.string().min(1),
    retrievedAt: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  }).strict()).min(1),
  files: z.object({
    fragrances: ReleaseFileSchema,
    entities: ReleaseFileSchema,
    semantic_claims: ReleaseFileSchema,
    search_index: ReleaseFileSchema,
    resolution_report: ReleaseFileSchema,
  }).strict(),
}).strict();

export type CatalogReleaseManifest = z.infer<typeof CatalogReleaseManifestSchema>;

export const CatalogSearchIndexSchema = z.object({
  schemaVersion: z.literal(1),
  documentIds: z.array(z.string().min(1)),
  terms: z.record(z.string(), z.array(z.number().int().nonnegative())),
}).strict();

export type CatalogSearchIndex = z.infer<typeof CatalogSearchIndexSchema>;

export function normalizeCatalogQuery(value: string): string {
  return value
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLocaleLowerCase("pt-BR")
    .replace(/[^a-z0-9]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function searchCatalogIndex(index: CatalogSearchIndex, query: string): readonly string[] {
  const tokens = normalizeCatalogQuery(query).split(" ").filter((token) => token.length >= 2);
  if (tokens.length === 0) return [];
  const matches = tokens.map((token) => {
    const positions = new Set<number>();
    for (const [term, termPositions] of Object.entries(index.terms)) {
      if (term === token || term.startsWith(token)) {
        for (const position of termPositions) positions.add(position);
      }
    }
    return positions;
  });
  const [first, ...rest] = matches;
  if (!first) return [];
  return [...first]
    .filter((position) => rest.every((positions) => positions.has(position)))
    .sort((left, right) => left - right)
    .map((position) => index.documentIds[position])
    .filter((id): id is string => Boolean(id));
}

export async function loadCatalogReleaseManifest(
  url = "/catalog/manifest.json",
  request: typeof fetch = fetch,
): Promise<CatalogReleaseManifest> {
  const response = await request(url, { headers: { Accept: "application/json" } });
  if (!response.ok) throw new Error(`Catálogo indisponível: HTTP ${response.status}`);
  return CatalogReleaseManifestSchema.parse(await response.json());
}
