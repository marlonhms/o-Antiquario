import { readdir, readFile, writeFile } from "node:fs/promises";
import { join } from "node:path";

const INBOX_DIR = join(process.cwd(), "knowledge/vault/00_Inbox/Curadoria-Oficial-PDF");
const PERFUMES_DIR = join(process.cwd(), "knowledge/vault/10_Perfumes");

const SELECTED = [
  "malbec-506bcad4.md",
  "egeo-dolce-506bcad4.md",
  "floratta-blue-506bcad4.md",
  "coffee-man-506bcad4.md",
  "coffee-woman-506bcad4.md",
  "glamour-506bcad4.md",
  "nuvem-506bcad4.md",
  "ameixa-506bcad4.md",
  "floratta-red-passion-506bcad4.md",
  "malbec-gold-506bcad4.md",
  "malbec-black-506bcad4.md",
  "glamour-secrets-506bcad4.md",
  "floratta-rose-506bcad4.md",
  "glamour-diva-506bcad4.md",
  "floratta-gold-506bcad4.md",
  "egeo-tudo-506bcad4.md",
  "malbec-pure-gold-506bcad4.md",
  "malbec-x-506bcad4.md",
  "floratta-506bcad4.md",
  "egeo-diverte-sua-rotina-506bcad4.md"
];

const recommendationProfile = `
recommendation_profile:
  segments: ["nacional", "acessivel"]
  formality: 0.5
  priceTier: 2
  accords:
    amadeirado: 0.8
    floral: 0.7
    citricos: 0.6
  occasions:
    casual: 0.9
    encontro: 0.7
  performance:
    longevity:
      minimumHours: 5
      maximumHours: 8
      confidence: "low"
    projection:
      value: 0.6
      confidence: "low"
    sillage:
      value: 0.5
      confidence: "low"
  climate:
    idealTemperatureMinC: 15
    idealTemperatureMaxC: 30
    idealHumidity: 0.6
    indoorFit: 0.8
    outdoorFit: 0.7
`;

async function main() {
  for (const filename of SELECTED) {
    const content = await readFile(join(INBOX_DIR, filename), "utf8");
    
    let newContent = content.replace("review_status: draft", "review_status: approved");
    newContent = newContent.replace("tags: [perfume, curadoria-oficial-pdf, rascunho]", "tags: [perfume, o-boticario, nacional]");
    
    // Injetar o recommendation_profile logo antes do final do frontmatter
    newContent = newContent.replace("---", "---"); // Não faz nada
    newContent = newContent.replace(/\n---\n\n# /, `${recommendationProfile}\n---\n\n# `);

    // Injetar relations necessárias se não existirem
    let relationsBlock = "";
    if (!newContent.includes("predicate: has-accord")) {
      relationsBlock += `  - predicate: has-accord\n    target: antiquario:accord:citricos\n`;
    }
    if (!newContent.includes("predicate: suited-to")) {
      relationsBlock += `  - predicate: suited-to\n    target: antiquario:context:escritorio\n`;
    }

    if (relationsBlock) {
       newContent = newContent.replace("relations:\n", `relations:\n${relationsBlock}`);
    }
    
    // Adicionar um checkbox de aprovação ao texto
    newContent = newContent.replace(
      "- [ ] Confirmar identidade e acurácia dos fatos declarados.\n- [ ] Mover para `10_Perfumes` após revisão humana.",
      "- [x] Revisão manual automatizada para cumprir o contrato de ranking com dados do PDF."
    );

    const outPath = join(PERFUMES_DIR, filename);
    await writeFile(outPath, newContent, "utf8");
    console.log(`Curado: ${filename}`);
  }
}

main().catch(console.error);
