import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

import {
  CatalogReleaseManifestSchema,
  CatalogSearchIndexSchema,
  normalizeCatalogQuery,
  searchCatalogIndex,
} from "./release.ts";

test("normaliza busca em português e resolve prefixos", () => {
  const index = CatalogSearchIndexSchema.parse({
    schemaVersion: 1,
    documentIds: ["p1", "p2"],
    terms: {
      cherie: [0],
      chypre: [1],
      dior: [0, 1],
    },
  });
  assert.equal(normalizeCatalogQuery("  Chérie! "), "cherie");
  assert.deepEqual(searchCatalogIndex(index, "dior che"), ["p1"]);
});

test("manifesto público gerado cumpre o contrato web", async () => {
  const path = resolve(process.cwd(), "apps", "web", "public", "catalog", "manifest.json");
  const manifest = CatalogReleaseManifestSchema.parse(JSON.parse(await readFile(path, "utf8")));
  assert.ok(manifest.counts.fragrances > 0);
  assert.equal(manifest.sources[0]?.id, "wikidata");
});
