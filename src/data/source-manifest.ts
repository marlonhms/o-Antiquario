import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

import { parse } from "yaml";
import { z } from "zod";

const isoDate = z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "use a data ISO YYYY-MM-DD");
const httpsUrl = z.string().url().refine((value) => value.startsWith("https://"), "use HTTPS");

export const SourceClassificationSchema = z.enum([
  "allowed_core",
  "allowed_isolated",
  "reference_only",
  "pending_review",
  "prohibited",
]);

const LicenseSchema = z.object({
  identifier: z.string().min(2),
  name: z.string().min(3),
  url: httpsUrl,
  scope: z.string().min(12),
  compatibility: z.enum(["core", "isolated", "reference", "unverified", "none"]),
  attribution_required: z.boolean(),
  share_alike: z.boolean(),
}).strict();

const AccessSchema = z.object({
  automated: z.enum(["allowed", "conditional", "blocked_until_review", "prohibited"]),
  methods: z.array(z.string().min(1)).min(1),
  endpoint: httpsUrl.optional(),
  authentication: z.enum(["none", "api_key", "oauth", "account"]),
  conditions: z.array(z.string().min(8)).min(1),
}).strict();

const StorageSchema = z.object({
  layer: z.enum(["core", "obf", "staging", "references", "rejected"]),
  redistribution: z.enum(["allowed", "share_alike", "per_record", "blocked"]),
  attribution_label: z.string().min(2),
}).strict();

const SourceSchema = z.object({
  id: z.string().regex(/^[a-z][a-z0-9_]*$/),
  name: z.string().min(2),
  homepage: httpsUrl,
  classification: SourceClassificationSchema,
  purpose: z.string().min(12),
  license: LicenseSchema,
  access: AccessSchema,
  storage: StorageSchema,
  fields: z.object({
    allowed: z.array(z.string().min(1)),
    forbidden: z.array(z.string().min(1)),
  }).strict(),
  review: z.object({
    reviewed_at: isoDate,
    next_review_at: isoDate,
    evidence_urls: z.array(httpsUrl).min(1),
    notes: z.string().min(12),
  }).strict(),
}).strict().superRefine((source, context) => {
  if (source.review.next_review_at <= source.review.reviewed_at) {
    context.addIssue({
      code: "custom",
      path: ["review", "next_review_at"],
      message: "a próxima revisão deve ocorrer depois da revisão atual",
    });
  }

  if (source.classification === "allowed_core") {
    if (source.license.compatibility !== "core" || source.storage.layer !== "core") {
      context.addIssue({
        code: "custom",
        path: ["classification"],
        message: "fontes core exigem licença compatível e armazenamento core",
      });
    }
    if (source.access.automated !== "allowed") {
      context.addIssue({
        code: "custom",
        path: ["access", "automated"],
        message: "uma fonte core precisa autorizar acesso automatizado",
      });
    }
  }

  if (source.classification === "allowed_isolated") {
    if (source.license.compatibility !== "isolated" || source.storage.layer === "core") {
      context.addIssue({
        code: "custom",
        path: ["storage", "layer"],
        message: "fontes isoladas não podem escrever no catálogo core",
      });
    }
  }

  if (["pending_review", "reference_only"].includes(source.classification) && source.storage.layer === "core") {
    context.addIssue({
      code: "custom",
      path: ["storage", "layer"],
      message: "fontes pendentes ou de referência não podem escrever no catálogo core",
    });
  }

  if (source.classification === "prohibited") {
    if (source.access.automated !== "prohibited" || !source.access.methods.includes("none")) {
      context.addIssue({
        code: "custom",
        path: ["access"],
        message: "fontes proibidas devem bloquear automação e declarar método none",
      });
    }
    if (source.storage.layer !== "rejected" || source.storage.redistribution !== "blocked") {
      context.addIssue({
        code: "custom",
        path: ["storage"],
        message: "fontes proibidas devem permanecer na camada rejected sem redistribuição",
      });
    }
  }
});

export const SourceManifestSchema = z.object({
  schema_version: z.literal(1),
  reviewed_at: isoDate,
  policy: z.object({
    default_classification: z.literal("prohibited"),
    unknown_source_action: z.literal("reject"),
    review_interval_days: z.number().int().min(1).max(365),
    require_https: z.literal(true),
    require_record_provenance: z.literal(true),
  }).strict(),
  sources: z.array(SourceSchema).min(1),
}).strict().superRefine((manifest, context) => {
  const seen = new Set<string>();
  manifest.sources.forEach((source, index) => {
    if (seen.has(source.id)) {
      context.addIssue({
        code: "custom",
        path: ["sources", index, "id"],
        message: `identificador duplicado: ${source.id}`,
      });
    }
    seen.add(source.id);
  });
});

export type SourceClassification = z.infer<typeof SourceClassificationSchema>;
export type SourceManifest = z.infer<typeof SourceManifestSchema>;
export type DataSource = SourceManifest["sources"][number];

export function validateSourceManifest(input: unknown): SourceManifest {
  return SourceManifestSchema.parse(input);
}

export async function loadSourceManifest(
  path = resolve(process.cwd(), "data", "sources.yml"),
): Promise<SourceManifest> {
  const contents = await readFile(path, "utf8");
  return validateSourceManifest(parse(contents));
}

export function summarizeSourceManifest(manifest: SourceManifest): Record<SourceClassification, number> {
  const summary: Record<SourceClassification, number> = {
    allowed_core: 0,
    allowed_isolated: 0,
    reference_only: 0,
    pending_review: 0,
    prohibited: 0,
  };

  for (const source of manifest.sources) summary[source.classification] += 1;
  return summary;
}
