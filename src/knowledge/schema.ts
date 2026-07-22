import { z } from "zod";

const isoDate = z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "use a data ISO YYYY-MM-DD");
const stableSegment = z.string().regex(/^[a-z][a-z0-9-]*$/, "use kebab-case ASCII");

export const KnowledgeDocumentTypeSchema = z.enum([
  "index",
  "fragrance",
  "olfactory-note",
  "accord",
  "raw-material",
  "context",
  "science",
  "guide",
]);

export const KnowledgeConfidenceSchema = z.enum(["high", "medium", "low", "unknown"]);
export const KnowledgeReviewStatusSchema = z.enum(["draft", "review", "approved", "deprecated"]);

export const KnowledgeEvidenceSchema = z.object({
  source_id: z.string().regex(/^[a-z][a-z0-9_]*$/),
  kind: z.enum(["open_source", "curated", "scientific", "manufacturer", "community"]),
  license: z.string().min(2),
  confidence: KnowledgeConfidenceSchema,
  claim_scope: z.string().min(12),
  locator: z.string().url().optional(),
  retrieved_at: isoDate.optional(),
}).strict();

export const KnowledgeRelationSchema = z.object({
  predicate: stableSegment,
  target: z.string().regex(
    /^antiquario:[a-z][a-z0-9-]*:[a-z][a-z0-9-]*$/,
    "use um ID global como antiquario:tipo:slug",
  ),
}).strict();

export const KnowledgeFrontmatterSchema = z.object({
  schema_version: z.literal(1),
  id: z.string().regex(
    /^antiquario:[a-z][a-z0-9-]*:[a-z][a-z0-9-]*$/,
    "use um ID global como antiquario:tipo:slug",
  ),
  project: z.literal("o-antiquario"),
  type: KnowledgeDocumentTypeSchema,
  title: z.string().min(2).max(160),
  aliases: z.array(z.string().min(1)).default([]),
  external_ids: z.object({
    wikidata: z.string().regex(/^Q[1-9][0-9]*$/).optional(),
  }).strict().default({}),
  tags: z.array(stableSegment).min(1),
  source_ids: z.array(z.string().regex(/^[a-z][a-z0-9_]*$/)).min(1),
  license: z.string().min(2),
  confidence: KnowledgeConfidenceSchema,
  review_status: KnowledgeReviewStatusSchema,
  updated_at: isoDate,
  language: z.literal("pt-BR"),
  summary: z.string().min(24).max(500),
  evidence: z.array(KnowledgeEvidenceSchema).min(1),
  relations: z.array(KnowledgeRelationSchema).default([]),
}).strict().superRefine((document, context) => {
  const [, idType] = document.id.split(":");
  if (idType !== document.type) {
    context.addIssue({
      code: "custom",
      path: ["id"],
      message: `o tipo do ID '${idType}' difere de '${document.type}'`,
    });
  }

  const sourceIds = new Set(document.source_ids);
  if (sourceIds.size !== document.source_ids.length) {
    context.addIssue({ code: "custom", path: ["source_ids"], message: "contém fontes duplicadas" });
  }

  const evidenceSourceIds = new Set(document.evidence.map((evidence) => evidence.source_id));
  for (const sourceId of sourceIds) {
    if (!evidenceSourceIds.has(sourceId)) {
      context.addIssue({
        code: "custom",
        path: ["evidence"],
        message: `a fonte '${sourceId}' não possui evidência correspondente`,
      });
    }
  }
  for (const sourceId of evidenceSourceIds) {
    if (!sourceIds.has(sourceId)) {
      context.addIssue({
        code: "custom",
        path: ["evidence"],
        message: `a evidência '${sourceId}' não aparece em source_ids`,
      });
    }
  }
});

export type KnowledgeDocumentType = z.infer<typeof KnowledgeDocumentTypeSchema>;
export type KnowledgeConfidence = z.infer<typeof KnowledgeConfidenceSchema>;
export type KnowledgeReviewStatus = z.infer<typeof KnowledgeReviewStatusSchema>;
export type KnowledgeEvidence = z.infer<typeof KnowledgeEvidenceSchema>;
export type KnowledgeRelation = z.infer<typeof KnowledgeRelationSchema>;
export type KnowledgeFrontmatter = z.infer<typeof KnowledgeFrontmatterSchema>;

export interface WikiLink {
  readonly target: string;
  readonly alias?: string;
  readonly heading?: string;
}

export interface KnowledgeDocument extends KnowledgeFrontmatter {
  readonly path: string;
  readonly body: string;
  readonly wikiLinks: readonly WikiLink[];
  readonly contentHash: string;
}

export interface KnowledgeEdge {
  readonly source: string;
  readonly target: string;
  readonly predicate: string;
  readonly origin: "frontmatter" | "wikilink";
}

export interface KnowledgeChunk {
  readonly id: string;
  readonly documentId: string;
  readonly documentType: KnowledgeDocumentType;
  readonly title: string;
  readonly heading: string;
  readonly order: number;
  readonly content: string;
  readonly tags: readonly string[];
  readonly sourceIds: readonly string[];
  readonly license: string;
  readonly confidence: KnowledgeConfidence;
  readonly updatedAt: string;
  readonly relatedDocumentIds: readonly string[];
  readonly contentHash: string;
}

export const KnowledgeManifestSchema = z.object({
  schemaVersion: z.literal(1),
  releaseId: z.string().regex(/^knowledge-v1-[a-f0-9]{12}$/),
  contentHash: z.string().regex(/^[a-f0-9]{64}$/),
  latestDocumentDate: isoDate,
  counts: z.object({
    documents: z.number().int().nonnegative(),
    chunks: z.number().int().nonnegative(),
    nodes: z.number().int().nonnegative(),
    edges: z.number().int().nonnegative(),
  }).strict(),
  sources: z.array(z.string()),
  files: z.object({
    documents: z.literal("documents.json"),
    chunks: z.literal("chunks.json"),
    graph: z.literal("graph.json"),
  }).strict(),
}).strict();

export type KnowledgeManifest = z.infer<typeof KnowledgeManifestSchema>;
