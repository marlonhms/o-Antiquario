import { ZodError } from "zod";

import { loadTaxonomy, taxonomyStats } from "./taxonomy.ts";

try {
  const taxonomy = await loadTaxonomy();
  const stats = taxonomyStats(taxonomy);

  console.log(`Taxonomia olfativa v${taxonomy.schema_version} válida.`);
  console.log(`Famílias: ${stats.families}`);
  console.log(`Acordes: ${stats.accords}`);
  console.log(`Notas: ${stats.notes}`);
  console.log(`Aliases explícitos: ${stats.aliases}`);
} catch (error) {
  if (error instanceof ZodError) {
    console.error("Taxonomia inválida:");
    for (const issue of error.issues) console.error(`- ${issue.path.join(".")}: ${issue.message}`);
  } else {
    console.error(error);
  }
  process.exitCode = 1;
}
