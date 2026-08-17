import assert from "node:assert/strict";
import { resolve } from "node:path";
import test from "node:test";

import { loadSourceManifest } from "../data/source-manifest.ts";
import { compileKnowledgeVault, loadKnowledgeVault } from "./compiler.ts";
import { extractWikiLinks, parseKnowledgeMarkdown } from "./markdown.ts";
import { resolveKnowledgeGraph } from "./links.ts";
import { assertRelationContract, buildExpandedKnowledgeGraph, inspectKnowledgeGraph } from "./graph.ts";
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
  assert.equal(first.manifest.schemaVersion, 2);
  assert.equal(first.manifest.counts.documents, first.documents.length);
  assert.equal(
    first.manifest.counts.evidenceNodes,
    first.documents.reduce((total, document) => total + document.evidence.length, 0),
  );
  assert.ok(first.documents.every((document) => document.evidence.length >= 1));
  assert.ok(first.manifest.counts.documents >= 30);
  assert.ok(first.manifest.counts.typedRelations > 0);
  assert.ok(first.manifest.counts.chunks > 0);
  assert.ok(first.manifest.counts.edges > first.manifest.counts.documents);
  assert.deepEqual(
    first.manifest.sources,
    [...new Set(first.documents.flatMap((document) => document.source_ids))].sort(),
  );

  assert.equal(first.health.readiness.status, "blocked");
  assert.equal(first.health.issues.some((issue) => issue.code === "no-approved-commercial-fragrances"), false);
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

test("permite nomes homônimos quando relações usam IDs e rejeita wikilink ambíguo", async () => {
  const documents = await loadKnowledgeVault(vaultDirectory);
  const fixture = documents[0]!;
  const brand: KnowledgeDocument = {
    ...fixture,
    id: "antiquario:brand:homonimo",
    type: "brand",
    title: "Nome compartilhado",
    path: "Marca-Homonima.md",
    wikiLinks: [],
    relations: [],
  };
  const perfumer: KnowledgeDocument = {
    ...fixture,
    id: "antiquario:perfumer:homonimo",
    type: "perfumer",
    title: "Nome compartilhado",
    path: "Perfumista-Homonimo.md",
    wikiLinks: [],
    relations: [],
  };
  assert.doesNotThrow(() => resolveKnowledgeGraph([brand, perfumer]));
  assert.throws(
    () => resolveKnowledgeGraph([{ ...brand, wikiLinks: [{ target: "Nome compartilhado" }] }, perfumer]),
    /wikilink ambíguo/,
  );
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

test("rejeita predicado sem contrato para o tipo de entidade", async () => {
  const documents = await loadKnowledgeVault(vaultDirectory);
  const bergamota = documents.find((document) => document.id === "antiquario:olfactory-note:bergamota")!;
  const invalid: KnowledgeDocument = {
    ...bergamota,
    relations: [{ predicate: "has-note", target: "antiquario:olfactory-note:vetiver" }],
  };
  assert.throws(
    () => resolveKnowledgeGraph([invalid, ...documents.filter((document) => document.id !== bergamota.id)]),
    /não permite olfactory-note/,
  );
});

test("separa relações científicas de declarações comerciais de perfume", async () => {
  const documents = await loadKnowledgeVault(vaultDirectory);
  const fixture = documents.find((document) => document.id === "antiquario:olfactory-note:bergamota")!;
  const molecule: KnowledgeDocument = {
    ...fixture,
    id: "antiquario:molecule:geraniol",
    type: "molecule",
    title: "Geraniol",
  };
  const descriptor: KnowledgeDocument = {
    ...fixture,
    id: "antiquario:odor-descriptor:floral",
    type: "odor-descriptor",
    title: "Floral",
  };
  const fragrance: KnowledgeDocument = {
    ...fixture,
    id: "antiquario:fragrance:exemplo",
    type: "fragrance",
    title: "Fragrância de exemplo",
  };

  assert.doesNotThrow(() => assertRelationContract(molecule, descriptor, "described-as"));
  assert.throws(
    () => assertRelationContract(fragrance, descriptor, "described-as"),
    /não permite fragrance → odor-descriptor/,
  );
  assert.throws(
    () => assertRelationContract(molecule, fixture, "has-note"),
    /não permite molecule → olfactory-note/,
  );
});

test("incorpora estudos científicos sem criar relações comerciais de perfume", async () => {
  const documents = await loadKnowledgeVault(vaultDirectory);
  const taxonomyStudy = documents.find(
    (document) => document.id === "antiquario:science:taxonomia-multilingue-termos-olfativos",
  );
  const aiStudy = documents.find(
    (document) => document.id === "antiquario:science:ia-perfumaria-ciencia-informacao",
  );

  const mahdaviStudy = documents.find(
    (document) => document.id === "antiquario:science:estudo-mahdavi-sons-do-aroma-sinestesia",
  );

  assert.ok(taxonomyStudy);
  assert.ok(aiStudy);
  assert.ok(mahdaviStudy);
  assert.equal(taxonomyStudy.type, "science");
  assert.equal(aiStudy.type, "science");
  assert.equal(mahdaviStudy.type, "science");
  assert.deepEqual(taxonomyStudy.source_ids, ["menini_2022_olfactory_taxonomy"]);
  assert.deepEqual(aiStudy.source_ids, ["vechiato_vidotti_2024_ai_perfumery"]);
  assert.deepEqual(mahdaviStudy.source_ids, ["mahdavi_2020_sons_do_aroma"]);
  assert.deepEqual(taxonomyStudy.relations, []);
  assert.deepEqual(aiStudy.relations, []);
  assert.deepEqual(mahdaviStudy.relations, []);
  assert.match(taxonomyStudy.body, /Derivações proibidas/);
  assert.match(aiStudy.body, /Derivações proibidas/);
  assert.match(mahdaviStudy.body, /Derivações proibidas/);
});

test("grafo expandido conecta cada documento à sua evidência", async () => {
  const documents = await loadKnowledgeVault(vaultDirectory);
  const graph = resolveKnowledgeGraph(documents);
  const expanded = buildExpandedKnowledgeGraph(documents, graph.edges);
  const health = inspectKnowledgeGraph(documents, expanded);
  const expectedEvidenceCount = documents.reduce((total, document) => total + document.evidence.length, 0);
  assert.equal(expectedEvidenceCount, expanded.nodes.filter((node) => node.kind === "evidence").length);
  assert.equal(expectedEvidenceCount, expanded.edges.filter((edge) => edge.predicate === "supported-by").length);
  assert.equal(health.graph.documentNodes, documents.length);
  assert.equal(health.graph.evidenceNodes, expectedEvidenceCount);
  assert.equal(health.graph.evidenceLinks, expectedEvidenceCount);

  assert.deepEqual(
    health.connectivity.isolatedDocumentIds,
    ["antiquario:brand:natura"],
  );
});
