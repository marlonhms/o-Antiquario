import type { DataSource, SourceManifest } from "../data/source-manifest.ts";
import type { KnowledgeDocument } from "./schema.ts";

export interface KnowledgeValidationReport {
  readonly documents: number;
  readonly approvedDocuments: number;
  readonly sourceIds: readonly string[];
}

function validateEvidenceLicense(document: KnowledgeDocument, source: DataSource): void {
  for (const evidence of document.evidence.filter((item) => item.source_id === source.id)) {
    if (evidence.license !== source.license.identifier) {
      throw new Error(
        `${document.path}: licença '${evidence.license}' difere do manifesto para '${source.id}' (${source.license.identifier})`,
      );
    }
  }
}

export function validateKnowledgeDocuments(
  documents: readonly KnowledgeDocument[],
  manifest: SourceManifest,
): KnowledgeValidationReport {
  const ids = new Set<string>();
  const paths = new Set<string>();
  const sources = new Map(manifest.sources.map((source) => [source.id, source]));
  const usedSources = new Set<string>();

  for (const document of documents) {
    if (ids.has(document.id)) throw new Error(`ID de conhecimento duplicado '${document.id}'`);
    if (paths.has(document.path.toLocaleLowerCase("pt-BR"))) {
      throw new Error(`Caminho de conhecimento duplicado '${document.path}'`);
    }
    ids.add(document.id);
    paths.add(document.path.toLocaleLowerCase("pt-BR"));

    for (const sourceId of document.source_ids) {
      const source = sources.get(sourceId);
      if (!source) throw new Error(`${document.path}: fonte desconhecida '${sourceId}'`);
      usedSources.add(sourceId);
      validateEvidenceLicense(document, source);

      if (document.review_status === "approved" && source.classification !== "allowed_core") {
        throw new Error(
          `${document.path}: documento aprovado não pode usar a fonte '${sourceId}' (${source.classification})`,
        );
      }
    }
  }

  return {
    documents: documents.length,
    approvedDocuments: documents.filter((document) => document.review_status === "approved").length,
    sourceIds: [...usedSources].sort(),
  };
}
