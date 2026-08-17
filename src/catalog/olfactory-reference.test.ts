import assert from "node:assert/strict";
import { test } from "node:test";

import type { CompiledKnowledge } from "../knowledge/compiler.ts";
import type { KnowledgeDocument, KnowledgeDocumentType } from "../knowledge/schema.ts";
import { compileOlfactoryReferenceCatalog } from "./olfactory-reference.ts";

function document(
  id: string,
  type: KnowledgeDocumentType,
  title: string,
  overrides: Partial<KnowledgeDocument> = {},
): KnowledgeDocument {
  return {
    schema_version: 1,
    id,
    project: "o-antiquario",
    type,
    title,
    aliases: [],
    external_ids: {},
    tags: [type],
    source_ids: ["parfumo_dataset"],
    license: "CC0-1.0",
    confidence: "medium",
    review_status: "approved",
    updated_at: "2026-08-17",
    language: "pt-BR",
    summary: "Documento factual de teste para referência olfativa.",
    evidence: [{
      source_id: "parfumo_dataset",
      kind: "open_source",
      license: "CC0-1.0",
      confidence: "medium",
      claim_scope: "Estrutura da pirâmide olfativa publicada na fonte.",
    }],
    relations: [],
    path: `${type}/${id.split(":").at(-1)}.md`,
    body: `# ${title}`,
    wikiLinks: [],
    contentHash: "a".repeat(64),
    ...overrides,
  };
}

function knowledge(documents: readonly KnowledgeDocument[]): CompiledKnowledge {
  return {
    documents,
    chunks: [],
    edges: [],
    health: {} as CompiledKnowledge["health"],
    validation: {} as CompiledKnowledge["validation"],
    manifest: {
      schemaVersion: 2,
      releaseId: "knowledge-v2-aaaaaaaaaaaa",
      contentHash: "a".repeat(64),
      latestDocumentDate: "2026-08-17",
      counts: { documents: documents.length, chunks: 0, nodes: 0, edges: 0, evidenceNodes: 0, typedRelations: 0 },
      sources: ["parfumo_dataset"],
      files: { documents: "documents.json", chunks: "chunks.json", graph: "graph.json", health: "graph-health.json" },
    },
  };
}

const brand = document("antiquario:brand:marca-teste", "brand", "Marca Teste");
const bergamot = document("antiquario:olfactory-note:bergamota", "olfactory-note", "Bergamota");
const vetiver = document("antiquario:olfactory-note:vetiver", "olfactory-note", "Vetiver");
const concentration = document("antiquario:concentration:eau-de-toilette", "concentration", "Eau de Toilette");
const perfumer = document("antiquario:perfumer:ana-nariz", "perfumer", "Ana Nariz");
const reference = document("antiquario:fragrance:referencia", "fragrance", "Referência", {
  relations: [
    { predicate: "belongs-to-brand", target: brand.id },
    { predicate: "has-top-note", target: bergamot.id },
    { predicate: "declares-base-note", target: vetiver.id },
    { predicate: "has-concentration", target: concentration.id },
    { predicate: "created-by", target: perfumer.id },
  ],
});
const blocked = document("antiquario:fragrance:bloqueada", "fragrance", "Bloqueada", {
  relations: [
    { predicate: "has-top-note", target: bergamot.id },
    { predicate: "has-base-note", target: vetiver.id },
  ],
});

test("publica apenas referências olfativas auditadas sem campos contextuais", () => {
  const catalog = compileOlfactoryReferenceCatalog(knowledge([reference, blocked, brand, bergamot, vetiver, concentration, perfumer]));
  const item = catalog.references[0]!;

  assert.equal(catalog.count, 1);
  assert.equal(item.name, "Referência");
  assert.equal(item.brand.name, "Marca Teste");
  assert.equal(item.pyramid.top[0]?.label, "Bergamota");
  assert.equal(item.pyramid.top[0]?.claimNature, "source_structured");
  assert.equal(item.pyramid.base[0]?.claimNature, "declared");
  assert.equal(item.concentrations[0]?.label, "Eau de Toilette");
  assert.equal(item.concentrations[0]?.claimNature, "source_structured");
  assert.equal(item.perfumers[0]?.name, "Ana Nariz");
  assert.ok(item.limitations.includes("performance_not_evidenced"));
  assert.equal("performance" in item, false);
  assert.equal("climate" in item, false);
  assert.equal("occasions" in item, false);
  assert.equal("score" in item, false);
});

test("catálogo é determinístico mesmo quando a ordem dos documentos muda", () => {
  const forward = compileOlfactoryReferenceCatalog(knowledge([reference, blocked, brand, bergamot, vetiver, concentration, perfumer]));
  const reverse = compileOlfactoryReferenceCatalog(knowledge([perfumer, concentration, vetiver, bergamot, brand, blocked, reference]));

  assert.equal(forward.releaseId, reverse.releaseId);
  assert.deepEqual(forward.references, reverse.references);
});
