import { delimiter, join } from "node:path";
import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";

const root = process.cwd();
const candidates = [
  process.env.ANTIQUARIO_PYTHON,
  join(root, ".venv", "Scripts", "python.exe"),
  join(root, ".venv", "bin", "python"),
  "python3",
  "python",
].filter(Boolean);

let lastError;
for (const executable of candidates) {
  if (executable.includes(root) && !existsSync(executable)) continue;
  const result = spawnSync(executable, process.argv.slice(2), {
    cwd: root,
    stdio: "inherit",
    env: {
      ...process.env,
      PYTHONUTF8: "1",
      PYTHONPATH: [join(root, "pipeline"), process.env.PYTHONPATH].filter(Boolean).join(delimiter),
    },
  });
  if (!result.error) process.exit(result.status ?? 1);
  lastError = result.error;
  if (result.error.code !== "ENOENT") break;
}

console.error("Python não encontrado. Crie .venv ou defina ANTIQUARIO_PYTHON.");
if (lastError) console.error(lastError.message);
process.exit(1);
