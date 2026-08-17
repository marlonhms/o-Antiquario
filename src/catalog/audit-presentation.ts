import { resolve } from "node:path";

import {
  buildPresentationReadinessReport,
  writePresentationReadinessReport,
} from "./presentation-readiness.ts";
import { compilePresentationCandidates } from "./knowledge-adapter.ts";
import { buildKnowledge } from "../knowledge/compiler.ts";

async function main(): Promise<void> {
  const outputPath = resolve(process.cwd(), "data", "reports", "presentation-readiness-report.json");
  const knowledge = await buildKnowledge();
  const candidates = compilePresentationCandidates(knowledge);
  const report = buildPresentationReadinessReport(knowledge, candidates, "knowledge-core-presentation-audit");
  await writePresentationReadinessReport(report, outputPath);

  console.log(JSON.stringify({
    reportId: report.reportId,
    outputPath,
    counts: report.counts,
    leadingIssues: Object.entries(report.issueCounts)
      .sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0]))
      .slice(0, 8)
      .map(([code, count]) => ({ code, count })),
  }, null, 2));
}

main().catch((error: unknown) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
