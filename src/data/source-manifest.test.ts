import assert from "node:assert/strict";
import test from "node:test";

import { loadSourceManifest, summarizeSourceManifest, validateSourceManifest } from "./source-manifest.ts";

test("o manifesto oficial é válido e mantém fontes arriscadas fora do core", async () => {
  const manifest = await loadSourceManifest();
  const summary = summarizeSourceManifest(manifest);

  assert.equal(manifest.sources.length, 11);
  assert.equal(summary.allowed_core, 5);
  assert.equal(summary.allowed_isolated, 1);
  assert.equal(summary.reference_only, 1);
  assert.equal(summary.pending_review, 3);
  assert.equal(summary.prohibited, 1);
  assert.equal(manifest.sources.find((source) => source.id === "fragrantica")?.storage.layer, "rejected");
});

test("IDs duplicados são rejeitados", async () => {
  const manifest = await loadSourceManifest();
  const duplicated = structuredClone(manifest);
  duplicated.sources.push(structuredClone(duplicated.sources[0]!));

  assert.throws(() => validateSourceManifest(duplicated), /identificador duplicado/);
});

test("uma licença não compatível não pode entrar no core", async () => {
  const manifest = await loadSourceManifest();
  const invalid = structuredClone(manifest);
  invalid.sources[0]!.license.compatibility = "unverified";

  assert.throws(() => validateSourceManifest(invalid), /fontes core exigem licença compatível/);
});

test("uma fonte isolada não pode escrever no catálogo core", async () => {
  const manifest = await loadSourceManifest();
  const invalid = structuredClone(manifest);
  const isolated = invalid.sources.find((source) => source.classification === "allowed_isolated");
  assert.ok(isolated);
  isolated.storage.layer = "core";

  assert.throws(() => validateSourceManifest(invalid), /fontes isoladas não podem escrever/);
});

test("uma fonte proibida não pode declarar acesso automatizado", async () => {
  const manifest = await loadSourceManifest();
  const invalid = structuredClone(manifest);
  const prohibited = invalid.sources.find((source) => source.classification === "prohibited");
  assert.ok(prohibited);
  prohibited.access.automated = "allowed";

  assert.throws(() => validateSourceManifest(invalid), /fontes proibidas devem bloquear automação/);
});

