import { ZodError } from "zod";

import { loadSourceManifest, summarizeSourceManifest } from "./source-manifest.ts";

try {
  const manifest = await loadSourceManifest();
  const summary = summarizeSourceManifest(manifest);

  console.log(`Manifesto de fontes v${manifest.schema_version} válido (${manifest.sources.length} fontes).`);
  console.log(`Core permitido: ${summary.allowed_core}`);
  console.log(`Permitidas isoladamente: ${summary.allowed_isolated}`);
  console.log(`Somente referência: ${summary.reference_only}`);
  console.log(`Pendentes: ${summary.pending_review}`);
  console.log(`Proibidas: ${summary.prohibited}`);
} catch (error) {
  if (error instanceof ZodError) {
    console.error("Manifesto de fontes inválido:");
    for (const issue of error.issues) console.error(`- ${issue.path.join(".")}: ${issue.message}`);
  } else {
    console.error(error);
  }
  process.exitCode = 1;
}
