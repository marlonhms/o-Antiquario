import { mkdir, writeFile } from "node:fs/promises";
import { join, resolve } from "node:path";

import {
  EligibleForRecommendationSchema,
  validateRecommendationEligibility,
  type EligibleForRecommendation,
  type RecommendationGateReport,
} from "../domain/recommendation-contract.ts";
import type { Fragrance } from "../domain/types.ts";

export interface CompiledRecommendationCatalog {
  readonly schemaVersion: 1;
  readonly releaseId: string;
  readonly createdAt: string;
  readonly fragrances: readonly Fragrance[];
  readonly gateReport: RecommendationGateReport;
}

export const MINIMUM_RECOMMENDATION_GATE_COUNT = 20;

export function evaluateRecommendationGate(
  candidates: readonly unknown[],
  minimumRequired = MINIMUM_RECOMMENDATION_GATE_COUNT,
): {
  readonly eligible: readonly Fragrance[];
  readonly gateReport: RecommendationGateReport;
} {
  const eligible: Fragrance[] = [];
  const invalidReasons: { id: string; issues: string[] }[] = [];

  for (const candidate of candidates) {
    const validation = validateRecommendationEligibility(candidate);
    if (validation.success && validation.data) {
      eligible.push(validation.data);
    } else {
      const id = (candidate as { id?: string })?.id ?? "unknown";
      invalidReasons.push({
        id,
        issues: validation.issues ? [...validation.issues] : ["estrutura inválida"],
      });
    }
  }

  const gateReport: RecommendationGateReport = {
    eligibleCount: eligible.length,
    minimumRequired,
    passesGate: eligible.length >= minimumRequired,
    invalidReasons,
  };

  return { eligible, gateReport };
}

export async function compileRecommendationCatalog(options: {
  readonly candidates: readonly unknown[];
  readonly outputDirectory?: string;
  readonly minimumGateRequired?: number;
}): Promise<CompiledRecommendationCatalog> {
  const outputDirectory = options.outputDirectory ?? resolve(process.cwd(), "data", "releases");
  const { eligible, gateReport } = evaluateRecommendationGate(
    options.candidates,
    options.minimumGateRequired ?? MINIMUM_RECOMMENDATION_GATE_COUNT,
  );

  const createdAt = new Date().toISOString();
  const compiled: CompiledRecommendationCatalog = {
    schemaVersion: 1,
    releaseId: `recommendation-catalog-v1-${createdAt.slice(0, 10)}`,
    createdAt,
    fragrances: eligible,
    gateReport,
  };

  await mkdir(outputDirectory, { recursive: true });
  await writeFile(
    join(outputDirectory, "recommendation-catalog.json"),
    `${JSON.stringify(compiled, null, 2)}\n`,
    "utf8",
  );

  return compiled;
}
