import { createHash } from "node:crypto";

import { parse } from "yaml";

import {
  KnowledgeFrontmatterSchema,
  type KnowledgeChunk,
  type KnowledgeDocument,
  type WikiLink,
} from "./schema.ts";

const WIKI_LINK_PATTERN = /\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]/g;

export function sha256(value: string): string {
  return createHash("sha256").update(value).digest("hex");
}

export function extractWikiLinks(markdown: string): readonly WikiLink[] {
  return [...markdown.matchAll(WIKI_LINK_PATTERN)].map((match) => ({
    target: match[1]!.trim(),
    ...(match[2]?.trim() ? { heading: match[2].trim() } : {}),
    ...(match[3]?.trim() ? { alias: match[3].trim() } : {}),
  }));
}

export function stripWikiMarkup(markdown: string): string {
  return markdown.replace(WIKI_LINK_PATTERN, (_match, target: string, _heading: string, alias: string) => {
    return (alias || target).trim();
  });
}

export function parseKnowledgeMarkdown(contents: string, relativePath: string): KnowledgeDocument {
  const normalized = contents.replace(/^\uFEFF/, "").replace(/\r\n/g, "\n");
  if (!normalized.startsWith("---\n")) {
    throw new Error(`${relativePath}: frontmatter YAML ausente`);
  }

  const closing = normalized.indexOf("\n---\n", 4);
  if (closing < 0) throw new Error(`${relativePath}: frontmatter YAML não foi fechado`);

  const rawFrontmatter = normalized.slice(4, closing);
  const body = normalized.slice(closing + 5).trim();
  const frontmatter = KnowledgeFrontmatterSchema.parse(parse(rawFrontmatter));
  const firstHeading = body.match(/^#\s+(.+)$/m)?.[1]?.trim();
  if (!firstHeading) throw new Error(`${relativePath}: o documento precisa de um título H1`);
  if (firstHeading !== frontmatter.title) {
    throw new Error(`${relativePath}: H1 '${firstHeading}' difere do título '${frontmatter.title}'`);
  }

  return {
    ...frontmatter,
    path: relativePath.replaceAll("\\", "/"),
    body,
    wikiLinks: extractWikiLinks(body),
    contentHash: sha256(`${rawFrontmatter}\n${body}`),
  };
}

interface SemanticSection {
  readonly heading: string;
  readonly content: string;
}

function semanticSections(document: KnowledgeDocument): readonly SemanticSection[] {
  const lines = document.body.split("\n");
  const sections: { heading: string; lines: string[] }[] = [];
  let current = { heading: "Resumo", lines: [] as string[] };

  for (const line of lines) {
    if (line.startsWith("# ")) continue;
    if (line.startsWith("## ")) {
      if (current.lines.join("\n").trim()) sections.push(current);
      current = { heading: line.slice(3).trim(), lines: [] };
    } else {
      current.lines.push(line);
    }
  }
  if (current.lines.join("\n").trim()) sections.push(current);

  return sections.map((section) => ({
    heading: section.heading,
    content: stripWikiMarkup(section.lines.join("\n")).replace(/\n{3,}/g, "\n\n").trim(),
  }));
}

function splitLongSection(content: string, maximumCharacters = 1_800): readonly string[] {
  if (content.length <= maximumCharacters) return [content];
  const paragraphs = content.split(/\n\s*\n/);
  const pieces: string[] = [];
  let current = "";
  for (const paragraph of paragraphs) {
    const candidate = current ? `${current}\n\n${paragraph}` : paragraph;
    if (candidate.length <= maximumCharacters || !current) {
      current = candidate;
    } else {
      pieces.push(current);
      current = paragraph;
    }
  }
  if (current) pieces.push(current);
  return pieces;
}

export function chunkKnowledgeDocument(
  document: KnowledgeDocument,
  relatedDocumentIds: readonly string[],
): readonly KnowledgeChunk[] {
  const chunks: KnowledgeChunk[] = [];
  let order = 0;
  for (const section of semanticSections(document)) {
    const parts = splitLongSection(section.content);
    for (const [partIndex, part] of parts.entries()) {
      const heading = parts.length > 1 ? `${section.heading} — parte ${partIndex + 1}` : section.heading;
      const content = `${document.title}\n${heading}\n\n${part}`;
      chunks.push({
        id: `${document.id}:chunk:${String(order + 1).padStart(3, "0")}`,
        documentId: document.id,
        documentType: document.type,
        title: document.title,
        heading,
        order,
        content,
        tags: document.tags,
        sourceIds: document.source_ids,
        license: document.license,
        confidence: document.confidence,
        updatedAt: document.updated_at,
        relatedDocumentIds,
        contentHash: sha256(content),
      });
      order += 1;
    }
  }
  return chunks;
}
