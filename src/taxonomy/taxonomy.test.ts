import assert from "node:assert/strict";
import test from "node:test";

import { FIXTURE_FRAGRANCES } from "../recommender/fixtures.ts";
import {
  buildTaxonomyIndex,
  loadTaxonomy,
  normalizeOlfactiveText,
  resolveAccord,
  resolveNote,
  validateTaxonomy,
  validateTaxonomySources,
} from "./taxonomy.ts";

test("a taxonomia oficial cumpre a cobertura mínima", async () => {
  const taxonomy = await loadTaxonomy();

  assert.ok(taxonomy.families.length >= 10);
  assert.ok(taxonomy.accords.length >= 20);
  assert.ok(taxonomy.notes.length >= 150);
});

test("normalização ignora acentos, caixa, hífens e espaços repetidos", () => {
  assert.equal(normalizeOlfactiveText("  Flor-DE-Laranjeira  "), "flor de laranjeira");
  assert.equal(normalizeOlfactiveText("PIMENTA_ROSA"), "pimenta rosa");
  assert.equal(normalizeOlfactiveText("NÉROLI"), "neroli");
});

test("notas podem ser resolvidas em português, inglês e por sinônimo", async () => {
  const index = buildTaxonomyIndex(await loadTaxonomy());

  assert.equal(resolveNote(index, "limão")?.id, "limao-siciliano");
  assert.equal(resolveNote(index, "LEMON")?.id, "limao-siciliano");
  assert.equal(resolveNote(index, "orris")?.id, "iris");
  assert.equal(resolveNote(index, "terra molhada")?.id, "petricor");
});

test("acordes podem ser resolvidos sem acentos", async () => {
  const index = buildTaxonomyIndex(await loadTaxonomy());

  assert.equal(resolveAccord(index, "cítrico")?.id, "citrico");
  assert.equal(resolveAccord(index, "fresh spicy")?.id, "especiado-fresco");
  assert.equal(resolveAccord(index, "almiscarado")?.id, "almiscarado");
});

test("todas as notas e acordes usados no catálogo sintético são conhecidos", async () => {
  const index = buildTaxonomyIndex(await loadTaxonomy());
  const missing = new Set<string>();

  for (const fragrance of FIXTURE_FRAGRANCES) {
    for (const accord of fragrance.accords) {
      if (!resolveAccord(index, accord.id)) missing.add(`acorde:${accord.id}`);
    }
    for (const note of [...fragrance.topNotes, ...fragrance.heartNotes, ...fragrance.baseNotes]) {
      if (!resolveNote(index, note)) missing.add(`nota:${note}`);
    }
  }

  assert.deepEqual([...missing], []);
});

test("IDs duplicados e referências de família inválidas são rejeitados", async () => {
  const taxonomy = await loadTaxonomy();
  const duplicate = structuredClone(taxonomy);
  duplicate.notes.push(structuredClone(duplicate.notes[0]!));
  assert.throws(() => validateTaxonomy(duplicate), /ID duplicado/);

  const badReference = structuredClone(taxonomy);
  badReference.notes[0]!.family_ids = ["familia-inexistente"];
  assert.throws(() => validateTaxonomy(badReference), /família inexistente/);
});

test("fontes não aprovadas para core são recusadas", async () => {
  const taxonomy = await loadTaxonomy();
  const invalid = structuredClone(taxonomy);
  invalid.notes[0]!.source_ids = ["fragrantica"];

  await assert.rejects(() => validateTaxonomySources(invalid), /não podem alimentar o core/);
});
