import { resolve } from "node:path";

import { buildKnowledge } from "../knowledge/compiler.ts";
import { compileOlfactoryReferenceCatalog, writeOlfactoryReferenceCatalog } from "./olfactory-reference.ts";

async function main(): Promise<void> {
  const knowledge = await buildKnowledge();
  const catalog = compileOlfactoryReferenceCatalog(knowledge);
  const releasePath = resolve(process.cwd(), "data", "releases", "olfactory-reference-catalog.json");
  const publicPath = resolve(process.cwd(), "apps", "web", "public", "catalog", "olfactory-reference-catalog.json");
  await Promise.all([
    writeOlfactoryReferenceCatalog(catalog, releasePath),
    writeOlfactoryReferenceCatalog(catalog, publicPath),
  ]);
  console.log(JSON.stringify({
    releaseId: catalog.releaseId,
    knowledgeReleaseId: catalog.knowledgeReleaseId,
    references: catalog.count,
    publicPath,
  }, null, 2));
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
