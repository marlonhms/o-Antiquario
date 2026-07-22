import { buildKnowledge, formatKnowledgeSummary } from "./compiler.ts";

const compiled = await buildKnowledge();
console.log(formatKnowledgeSummary(compiled));
