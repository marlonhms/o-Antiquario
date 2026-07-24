import { resolve } from "node:path";
import { buildKnowledge } from "../knowledge/compiler.ts";
import { compileRecommendationCandidates } from "./knowledge-adapter.ts";
import { compileRecommendationCatalog } from "./recommendation-compiler.ts";

async function main() {
  console.log("Reconstruindo grafo de conhecimento e compilação de recomendação...");
  const knowledge = await buildKnowledge();
  const candidates = compileRecommendationCandidates(knowledge);
  
  if (candidates.length === 0) {
    console.log("Nenhum candidato a recomendação aprovado encontrado no Obsidian.");
    return;
  }

  const outputDirectory = resolve(process.cwd(), "data", "releases");
  const webPublicDirectory = resolve(process.cwd(), "apps", "web", "public", "catalog");

  const compiled = await compileRecommendationCatalog({
    candidates,
    outputDirectory,
    minimumGateRequired: 20,
  });

  await compileRecommendationCatalog({
    candidates,
    outputDirectory: webPublicDirectory,
    minimumGateRequired: 20,
  });

  console.log(`Catálogo de Recomendação gerado e copiado para public/catalog! (${compiled.fragrances.length} fragrâncias elegíveis)`);
  if (!compiled.gateReport.passesGate) {
    console.warn("ALERTA: O catálogo gerado não atingiu a cota mínima do gate de recomendação (20 perfumes).");
  }
}

main().catch((err) => {
  console.error("Erro ao gerar catálogo de recomendação:", err);
  process.exit(1);
});
