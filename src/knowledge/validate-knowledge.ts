import { compileKnowledgeVault, formatKnowledgeSummary } from "./compiler.ts";
import { loadSourceManifest } from "../data/source-manifest.ts";
import { resolve } from "node:path";

const manifest = await loadSourceManifest();
const compiled = await compileKnowledgeVault(resolve(process.cwd(), "knowledge", "vault"), manifest);
console.log(`${formatKnowledgeSummary(compiled)} · validação concluída sem escrita`);
