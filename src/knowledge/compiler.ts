import { readdir, readFile, writeFile, mkdir } from "node:fs/promises";
import { join, relative, resolve } from "node:path";

import { loadSourceManifest, type SourceManifest } from "../data/source-manifest.ts";
import { chunkKnowledgeDocument, parseKnowledgeMarkdown, sha256 } from "./markdown.ts";
import { resolveKnowledgeGraph } from "./links.ts";
import {
  KnowledgeManifestSchema,
  type KnowledgeChunk,
  type KnowledgeDocument,
  type KnowledgeEdge,
  type KnowledgeManifest,
} from "./schema.ts";
import { validateKnowledgeDocuments, type KnowledgeValidationReport } from "./validation.ts";

export interface CompiledKnowledge {
  readonly documents: readonly KnowledgeDocument[];
  readonly chunks: readonly KnowledgeChunk[];
  readonly edges: readonly KnowledgeEdge[];
  readonly manifest: KnowledgeManifest;
  readonly validation: KnowledgeValidationReport;
}

async function discoverMarkdownFiles(directory: string, root = directory): Promise<readonly string[]> {
  const entries = await readdir(directory, { withFileTypes: true });
  const files: string[] = [];
  for (const entry of entries) {
    if (entry.name.startsWith(".")) continue;
    const absolute = join(directory, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === "00_Inbox") continue;
      files.push(...await discoverMarkdownFiles(absolute, root));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      files.push(relative(root, absolute).replaceAll("\\", "/"));
    }
  }
  return files.sort();
}

export async function loadKnowledgeVault(vaultDirectory: string): Promise<readonly KnowledgeDocument[]> {
  const files = await discoverMarkdownFiles(vaultDirectory);
  return Promise.all(files.map(async (path) => {
    const contents = await readFile(join(vaultDirectory, path), "utf8");
    return parseKnowledgeMarkdown(contents, path);
  }));
}

function publicDocument(document: KnowledgeDocument): Record<string, unknown> {
  const { wikiLinks: _wikiLinks, ...serializable } = document;
  return serializable;
}

function stableJson(value: unknown): string {
  return `${JSON.stringify(value, null, 2)}\n`;
}

export async function compileKnowledgeVault(
  vaultDirectory: string,
  sourceManifest: SourceManifest,
): Promise<CompiledKnowledge> {
  const loaded = await loadKnowledgeVault(vaultDirectory);
  const validation = validateKnowledgeDocuments(loaded, sourceManifest);
  const approved = loaded
    .filter((document) => document.review_status === "approved")
    .sort((left, right) => left.id.localeCompare(right.id));
  const graph = resolveKnowledgeGraph(approved);
  const chunks = approved.flatMap((document) => chunkKnowledgeDocument(
    document,
    graph.relatedByDocument.get(document.id) ?? [],
  ));

  const contentPayload = {
    documents: approved.map(publicDocument),
    chunks,
    edges: graph.edges,
  };
  const contentHash = sha256(JSON.stringify(contentPayload));
  const latestDocumentDate = approved.map((document) => document.updated_at).sort().at(-1);
  if (!latestDocumentDate) throw new Error("O vault não possui documentos aprovados");

  const manifest = KnowledgeManifestSchema.parse({
    schemaVersion: 1,
    releaseId: `knowledge-v1-${contentHash.slice(0, 12)}`,
    contentHash,
    latestDocumentDate,
    counts: {
      documents: approved.length,
      chunks: chunks.length,
      nodes: approved.length,
      edges: graph.edges.length,
    },
    sources: [...new Set(approved.flatMap((document) => document.source_ids))].sort(),
    files: {
      documents: "documents.json",
      chunks: "chunks.json",
      graph: "graph.json",
    },
  });

  return { documents: approved, chunks, edges: graph.edges, manifest, validation };
}

export async function writeCompiledKnowledge(compiled: CompiledKnowledge, outputDirectory: string): Promise<void> {
  await mkdir(outputDirectory, { recursive: true });
  const nodes = compiled.documents.map((document) => ({
    id: document.id,
    title: document.title,
    type: document.type,
    path: document.path,
    tags: document.tags,
    confidence: document.confidence,
  }));
  await Promise.all([
    writeFile(join(outputDirectory, "documents.json"), stableJson(compiled.documents.map(publicDocument)), "utf8"),
    writeFile(join(outputDirectory, "chunks.json"), stableJson(compiled.chunks), "utf8"),
    writeFile(join(outputDirectory, "graph.json"), stableJson({ nodes, edges: compiled.edges }), "utf8"),
    writeFile(join(outputDirectory, "knowledge-manifest.json"), stableJson(compiled.manifest), "utf8"),
  ]);
}

export interface BuildKnowledgeOptions {
  readonly vaultDirectory?: string;
  readonly outputDirectory?: string;
  readonly sourceManifestPath?: string;
}

export async function buildKnowledge(options: BuildKnowledgeOptions = {}): Promise<CompiledKnowledge> {
  const vaultDirectory = options.vaultDirectory ?? resolve(process.cwd(), "knowledge", "vault");
  const outputDirectory = options.outputDirectory ?? resolve(process.cwd(), "knowledge", "compiled");
  const sourceManifest = await loadSourceManifest(options.sourceManifestPath);
  const compiled = await compileKnowledgeVault(vaultDirectory, sourceManifest);
  await writeCompiledKnowledge(compiled, outputDirectory);
  return compiled;
}

export function formatKnowledgeSummary(compiled: CompiledKnowledge): string {
  return [
    `Knowledge Core ${compiled.manifest.releaseId}`,
    `${compiled.manifest.counts.documents} documentos aprovados`,
    `${compiled.manifest.counts.chunks} chunks semânticos`,
    `${compiled.manifest.counts.edges} sinapses`,
    `hash ${compiled.manifest.contentHash.slice(0, 16)}`,
  ].join(" · ");
}
