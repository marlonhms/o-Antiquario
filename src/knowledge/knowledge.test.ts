import assert from "node:assert/strict";
import { resolve } from "node:path";
import test from "node:test";

import { loadSourceManifest } from "../data/source-manifest.ts";
import { compileKnowledgeVault, loadKnowledgeVault } from "./compiler.ts";
import { extractWikiLinks, parseKnowledgeMarkdown } from "./markdown.ts";
import { resolveKnowledgeGraph } from "./links.ts";
import type { KnowledgeDocument } from "./schema.ts";
import { validateKnowledgeDocuments } from "./validation.ts";

const vaultDirectory = resolve(process.cwd(), "knowledge", "vault");

test("extrai wikilinks com alias e heading", () => {
  assert.deepEqual(extractWikiLinks("[[Vetiver]] [[Citricos|Cítricos]] [[Guia#Uso|aplicação]]"), [
    { target: "Vetiver" },
    { target: "Citricos", alias: "Cítricos" },
    { target: "Guia", heading: "Uso", alias: "aplicação" },
  ]);
});

test("exige que o H1 corresponda ao título do frontmatter", () => {
  const markdown = `---
schema_version: 1
id: antiquario:guide:teste
project: o-antiquario
type: guide
title: Título esperado
aliases: []
tags: [teste]
source_ids: [internal_curated]
license: CC0-1.0
confidence: high
review_status: approved
updated_at: 2026-07-22
language: pt-BR
summary: Documento suficientemente descritivo para testar o parser.
evidence:
  - source_id: internal_curated
    kind: curated
    license: CC0-1.0
    confidence: high
    claim_scope: Conteúdo original criado exclusivamente para este teste.
relations: []
---

# Outro título

Conteúdo.`;
  assert.throws(() => parseKnowledgeMarkdown(markdown, "Teste.md"), /difere do título/);
});

test("compila o vault real de forma determinística", async () => {
  const manifest = await loadSourceManifest();
  const first = await compileKnowledgeVault(vaultDirectory, manifest);
  const second = await compileKnowledgeVault(vaultDirectory, manifest);

  assert.equal(first.manifest.contentHash, second.manifest.contentHash);
  assert.equal(first.manifest.releaseId, second.manifest.releaseId);
  assert.equal(first.manifest.counts.documents, 10);
  assert.ok(first.manifest.counts.chunks >= first.manifest.counts.documents);
  assert.ok(first.manifest.counts.edges > first.manifest.counts.documents);
  assert.deepEqual(first.manifest.sources, ["internal_curated"]);
  assert.ok(first.chunks.every((chunk) => chunk.content.length > 24));
});

test("rejeita wikilink sem destino", async () => {
  const documents = await loadKnowledgeVault(vaultDirectory);
  const first = documents[0]!;
  const invalid: KnowledgeDocument = {
    ...first,
    wikiLinks: [...first.wikiLinks, { target: "Nota-Inexistente" }],
  };
  assert.throws(() => resolveKnowledgeGraph([invalid, ...documents.slice(1)]), /wikilink não resolvido/);
});

test("impede fonte pendente em documento aprovado", async () => {
  const manifest = await loadSourceManifest();
  const documents = await loadKnowledgeVault(vaultDirectory);
  const first = documents[0]!;
  const invalid: KnowledgeDocument = {
    ...first,
    source_ids: ["pyrfume"],
    evidence: [{
      source_id: "pyrfume",
      kind: "scientific",
      license: "MIT",
      confidence: "medium",
      claim_scope: "Dataset ainda pendente de revisão individual.",
    }],
  };
  assert.throws(() => validateKnowledgeDocuments([invalid], manifest), /documento aprovado não pode usar/);
});
