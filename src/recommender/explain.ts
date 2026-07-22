import type { RecommendationResult, ScoredCandidate } from "../domain/types.ts";

function percent(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export function explainCandidate(candidate: ScoredCandidate, position: number): string {
  const strengths = candidate.strengths.join("; ");
  const tradeoffs = candidate.tradeoffs.length > 0 ? ` Atenção: ${candidate.tradeoffs.join("; ")}.` : "";
  return `${position}. ${candidate.fragrance.name}, de ${candidate.fragrance.brand} — compatibilidade ${percent(candidate.score)}. ${strengths}.${tradeoffs}`;
}

export function explainResult(result: RecommendationResult): string {
  if (result.recommendations.length === 0) {
    return "Nenhuma fragrância atende às restrições informadas. Tente flexibilizar orçamento, coleção ou notas evitadas.";
  }

  const lines = result.recommendations.map((candidate, index) => explainCandidate(candidate, index + 1));
  return [
    `Recomendações calculadas pelo motor ${result.engineVersion}:`,
    ...lines,
    "As métricas de desempenho são estimativas e podem variar conforme pele, aplicação e ambiente.",
  ].join("\n");
}
