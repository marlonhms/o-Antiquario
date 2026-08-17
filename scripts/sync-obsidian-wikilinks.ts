import { readdir, readFile, writeFile } from "node:fs/promises";
import { join, relative, resolve } from "node:path";
import yaml from "yaml";
import { parseKnowledgeMarkdown } from "../src/knowledge/markdown.ts";
import { normalizeKnowledgeReference } from "../src/knowledge/links.ts";
import type { KnowledgeDocument } from "../src/knowledge/schema.ts";

interface DocIndexItem {
  id: string;
  type: string;
  title: string;
  fileName: string;
  relativePath: string;
  document: KnowledgeDocument;
}

interface TaxonomyNote {
  id: string;
  pt: string;
  en: string;
  aliases?: string[];
  family_ids?: string[];
}

interface TaxonomyData {
  notes?: TaxonomyNote[];
  accords?: Array<{ id: string; pt: string; en: string; family_ids?: string[] }>;
}

async function discoverFiles(dir: string, root: string): Promise<string[]> {
  const entries = await readdir(dir, { withFileTypes: true });
  const results: string[] = [];
  for (const entry of entries) {
    if (entry.name.startsWith(".")) continue;
    const abs = join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...await discoverFiles(abs, root));
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      results.push(relative(root, abs).replaceAll("\\", "/"));
    }
  }
  return results.sort();
}

const FAMILY_TO_ACCORD_SLUGS: Record<string, string[]> = {
  citrica: ["Citricos", "Fresco"],
  floral: ["floral"],
  amadeirada: ["Amadeirado"],
  ambarada: ["ambarado"],
  aromatica: ["Fresco", "verde"],
  verde: ["verde", "Fresco"],
  frutada: ["frutado"],
  especiada: ["especiado"],
  gourmand: ["gourmand", "doce"],
  couro: ["couro"],
  aquatica: ["aquatico", "Fresco"],
  almiscarada: ["atalcado"],
  terrosa: ["terroso"],
  resinosa: ["resinoso", "ambarado"],
  aldeidica: ["Fresco"],
};

export async function syncObsidianWikilinks(dryRun: boolean = false): Promise<{ updatedCount: number; totalLinksAdded: number }> {
  const vaultDir = resolve(process.cwd(), "knowledge", "vault");
  const taxonomyPath = resolve(process.cwd(), "data", "taxonomy", "taxonomy.yml");
  const taxonomyRaw = await readFile(taxonomyPath, "utf8");
  const taxonomy = yaml.parse(taxonomyRaw) as TaxonomyData;

  const noteToFamilies = new Map<string, string[]>();
  for (const n of taxonomy.notes ?? []) {
    if (n.family_ids) {
      noteToFamilies.set(n.id, n.family_ids);
      noteToFamilies.set(normalizeKnowledgeReference(n.pt), n.family_ids);
      noteToFamilies.set(normalizeKnowledgeReference(n.en), n.family_ids);
    }
  }

  const filePaths = await discoverFiles(vaultDir, vaultDir);

  const docs: DocIndexItem[] = [];
  const byId = new Map<string, DocIndexItem>();
  const byNormalizedName = new Map<string, DocIndexItem>();

  for (const relPath of filePaths) {
    const fullPath = join(vaultDir, relPath);
    const content = await readFile(fullPath, "utf8");
    try {
      const parsed = parseKnowledgeMarkdown(content, relPath);
      const fileName = relPath.split("/").at(-1)!.replace(/\.md$/i, "");
      const item: DocIndexItem = {
        id: parsed.id,
        type: parsed.type,
        title: parsed.title,
        fileName,
        relativePath: relPath,
        document: parsed,
      };
      docs.push(item);
      byId.set(parsed.id, item);
      byNormalizedName.set(normalizeKnowledgeReference(parsed.title), item);
      byNormalizedName.set(normalizeKnowledgeReference(fileName), item);
    } catch {
      // Ignore invalid files
    }
  }

  // Reference resolver
  const references = new Map<string, Set<string>>();
  for (const doc of docs) {
    const fileName = doc.fileName;
    const idSlug = doc.id.split(":").at(-1) ?? doc.id;
    for (const ref of [doc.id, doc.title, fileName, idSlug, ...doc.document.aliases]) {
      const normalized = normalizeKnowledgeReference(ref);
      const owners = references.get(normalized) ?? new Set<string>();
      owners.add(doc.id);
      references.set(normalized, owners);
    }
  }

  const formatLink = (targetId: string): string => {
    const doc = byId.get(targetId);
    if (!doc) {
      const simpleName = targetId.split(":").at(-1) ?? targetId;
      return `[[${simpleName}]]`;
    }

    const normFileName = normalizeKnowledgeReference(doc.fileName);
    const fileNameOwners = references.get(normFileName);
    if (fileNameOwners && fileNameOwners.size === 1) {
      return `[[${doc.fileName}|${doc.title}]]`;
    }

    const normTitle = normalizeKnowledgeReference(doc.title);
    const titleOwners = references.get(normTitle);
    if (titleOwners && titleOwners.size === 1) {
      return `[[${doc.title}]]`;
    }

    return `[[${doc.id}|${doc.title}]]`;
  };

  // Reverse links collections
  const brandToFragrances = new Map<string, Set<DocIndexItem>>();
  const perfumerToFragrances = new Map<string, Set<DocIndexItem>>();
  const noteToFragrances = new Map<string, Set<DocIndexItem>>();
  const accordToFragrances = new Map<string, Set<DocIndexItem>>();
  const concentrationToFragrances = new Map<string, Set<DocIndexItem>>();
  const contextToFragrances = new Map<string, Set<DocIndexItem>>();

  // Extract from relations AND text facts
  for (const item of docs) {
    if (item.type !== "fragrance") continue;
    const isApproved = item.document.review_status === "approved" && !item.relativePath.startsWith("00_Inbox");

    // 1. Frontmatter relations
    for (const rel of item.document.relations) {
      const target = byId.get(rel.target);
      const targetId = target ? target.id : rel.target;

      if (isApproved) {
        if (rel.predicate === "belongs-to-brand") {
          const list = brandToFragrances.get(targetId) ?? new Set();
          list.add(item);
          brandToFragrances.set(targetId, list);
        } else if (rel.predicate === "created-by") {
          const list = perfumerToFragrances.get(targetId) ?? new Set();
          list.add(item);
          perfumerToFragrances.set(targetId, list);
        } else if (
          rel.predicate.includes("note") ||
          rel.predicate === "has-note" ||
          rel.predicate === "declares-unlayered-note" ||
          rel.predicate.includes("top-note") ||
          rel.predicate.includes("heart-note") ||
          rel.predicate.includes("base-note")
        ) {
          const list = noteToFragrances.get(targetId) ?? new Set();
          list.add(item);
          noteToFragrances.set(targetId, list);
        } else if (rel.predicate === "has-accord") {
          const list = accordToFragrances.get(targetId) ?? new Set();
          list.add(item);
          accordToFragrances.set(targetId, list);
        } else if (rel.predicate === "declares-concentration" || rel.predicate === "has-concentration") {
          const list = concentrationToFragrances.get(targetId) ?? new Set();
          list.add(item);
          concentrationToFragrances.set(targetId, list);
        } else if (rel.predicate === "suited-to") {
          const list = contextToFragrances.get(targetId) ?? new Set();
          list.add(item);
          contextToFragrances.set(targetId, list);
        }
      }
    }

    // 2. Body text facts (Brand, Perfumer)
    if (isApproved) {
      const body = item.document.body;
      const brandMatch = body.match(/^[ \t]*- Marca:\s*(.+)$/m);
      if (brandMatch) {
        const brandRaw = brandMatch[1].trim();
        const matchedBrand = byNormalizedName.get(normalizeKnowledgeReference(brandRaw));
        if (matchedBrand) {
          const list = brandToFragrances.get(matchedBrand.id) ?? new Set();
          list.add(item);
          brandToFragrances.set(matchedBrand.id, list);
        }
      }

      const perfumerMatch = body.match(/^[ \t]*- Perfumista:\s*(.+)$/m);
      if (perfumerMatch) {
        const perfumerRaw = perfumerMatch[1].trim();
        for (const name of perfumerRaw.split(/[,/e&;]+/)) {
          const matchedPerfumer = byNormalizedName.get(normalizeKnowledgeReference(name));
          if (matchedPerfumer) {
            const list = perfumerToFragrances.get(matchedPerfumer.id) ?? new Set();
            list.add(item);
            perfumerToFragrances.set(matchedPerfumer.id, list);
          }
        }
      }
    }
  }

  let updatedCount = 0;
  let totalLinksAdded = 0;

  // 1. Update Fragrances
  for (const item of docs) {
    if (item.type !== "fragrance") continue;
    const fullPath = join(vaultDir, item.relativePath);
    const rawContent = await readFile(fullPath, "utf8");
    const parts = rawContent.split(/---\r?\n/);
    if (parts.length < 3) continue;

    const lineEnding = rawContent.includes("\r\n") ? "\r\n" : "\n";
    const frontmatter = parts[1];
    let body = parts.slice(2).join(`---${lineEnding}`);

    const brandRel = item.document.relations.find((r) => r.predicate === "belongs-to-brand");
    const perfumerRels = item.document.relations.filter((r) => r.predicate === "created-by");
    const concRel = item.document.relations.find((r) => r.predicate === "declares-concentration" || r.predicate === "has-concentration");
    const topNoteRels = item.document.relations.filter((r) => r.predicate === "has-top-note" || r.predicate === "declares-top-note");
    const heartNoteRels = item.document.relations.filter((r) => r.predicate === "has-heart-note" || r.predicate === "declares-heart-note");
    const baseNoteRels = item.document.relations.filter((r) => r.predicate === "has-base-note" || r.predicate === "declares-base-note");
    const unlayeredNoteRels = item.document.relations.filter((r) => r.predicate === "has-note" || r.predicate === "declares-unlayered-note");
    const accordRels = item.document.relations.filter((r) => r.predicate === "has-accord");
    const contextRels = item.document.relations.filter((r) => r.predicate === "suited-to");

    const linkLines: string[] = [];

    // Brand
    if (brandRel) {
      linkLines.push(`- **Casa / Marca:** ${formatLink(brandRel.target)}`);
    } else {
      const m = body.match(/^[ \t]*- Marca:\s*(.+)$/m);
      if (m) {
        const found = byNormalizedName.get(normalizeKnowledgeReference(m[1].trim()));
        if (found) linkLines.push(`- **Casa / Marca:** ${formatLink(found.id)}`);
      }
    }

    // Perfumer
    if (perfumerRels.length > 0) {
      linkLines.push(`- **Perfumista(s):** ${perfumerRels.map((r) => formatLink(r.target)).join(", ")}`);
    } else {
      const m = body.match(/^[ \t]*- Perfumista:\s*(.+)$/m);
      if (m) {
        const foundList: string[] = [];
        for (const name of m[1].split(/[,/e&;]+/)) {
          const found = byNormalizedName.get(normalizeKnowledgeReference(name));
          if (found) foundList.push(formatLink(found.id));
        }
        if (foundList.length > 0) {
          linkLines.push(`- **Perfumista(s):** ${foundList.join(", ")}`);
        }
      }
    }

    // Concentration
    if (concRel) {
      linkLines.push(`- **Concentração:** ${formatLink(concRel.target)}`);
    }

    // Accords
    if (accordRels.length > 0) {
      linkLines.push(`- **Acordes Principais:** ${accordRels.map((r) => formatLink(r.target)).join(", ")}`);
    }

    // Pyramid
    if (topNoteRels.length > 0) {
      linkLines.push(`- **Notas de Saída:** ${topNoteRels.map((r) => formatLink(r.target)).join(", ")}`);
    }
    if (heartNoteRels.length > 0) {
      linkLines.push(`- **Notas de Coração:** ${heartNoteRels.map((r) => formatLink(r.target)).join(", ")}`);
    }
    if (baseNoteRels.length > 0) {
      linkLines.push(`- **Notas de Fundo:** ${baseNoteRels.map((r) => formatLink(r.target)).join(", ")}`);
    }
    if (unlayeredNoteRels.length > 0) {
      linkLines.push(`- **Notas (Sem Camada):** ${unlayeredNoteRels.map((r) => formatLink(r.target)).join(", ")}`);
    }
    if (contextRels.length > 0) {
      linkLines.push(`- **Ocasiões e Contextos:** ${contextRels.map((r) => formatLink(r.target)).join(", ")}`);
    }

    if (linkLines.length > 0) {
      const sectionContent = `## Conexões do Grafo\n\n${linkLines.join("\n")}\n`;
      if (body.includes("## Conexões do Grafo")) {
        body = body.replace(/## Conexões do Grafo[\s\S]*?(?=\n## |$)/, sectionContent);
      } else {
        body = `${body.trimEnd()}\n\n${sectionContent}`;
      }

      if (lineEnding === "\r\n") {
        body = body.replaceAll("\n", "\r\n");
      }

      const newContent = `---${lineEnding}${frontmatter}---${lineEnding}${body}`;
      if (newContent !== rawContent) {
        if (!dryRun) {
          await writeFile(fullPath, newContent, "utf8");
        }
        updatedCount++;
        totalLinksAdded += linkLines.length;
      }
    }
  }

  // 2. Update Notes to connect with Acordes & Fragrances
  for (const item of docs) {
    if (item.type !== "olfactory-note") continue;
    const fullPath = join(vaultDir, item.relativePath);
    const rawContent = await readFile(fullPath, "utf8");
    const parts = rawContent.split(/---\r?\n/);
    if (parts.length < 3) continue;

    const lineEnding = rawContent.includes("\r\n") ? "\r\n" : "\n";
    const frontmatter = parts[1];
    let body = parts.slice(2).join(`---${lineEnding}`);

    const linkSections: string[] = [];

    // Connect to Facet/Accord
    const slug = item.fileName.replace(/^note-/, "");
    const families = noteToFamilies.get(slug) ?? noteToFamilies.get(normalizeKnowledgeReference(item.title)) ?? [];
    const accordSlugs = new Set<string>();
    for (const fam of families) {
      for (const acc of FAMILY_TO_ACCORD_SLUGS[fam] ?? []) {
        accordSlugs.add(acc);
      }
    }
    // Fallback if none found
    if (accordSlugs.size === 0) {
      if (slug.includes("pimenta") || slug.includes("cravo") || slug.includes("canela")) accordSlugs.add("especiado");
      else if (slug.includes("rosa") || slug.includes("jasmim") || slug.includes("flor") || slug.includes("lirio")) accordSlugs.add("floral");
      else if (slug.includes("cedro") || slug.includes("sandalo") || slug.includes("madeira") || slug.includes("vetiver")) accordSlugs.add("Amadeirado");
      else if (slug.includes("limao") || slug.includes("laranja") || slug.includes("bergamota") || slug.includes("toranja") || slug.includes("pomelo")) accordSlugs.add("Citricos");
      else if (slug.includes("baunilha") || slug.includes("caramelo") || slug.includes("acucar") || slug.includes("cacau") || slug.includes("cafe")) accordSlugs.add("gourmand");
      else if (slug.includes("ambar") || slug.includes("benjoim") || slug.includes("balsamo")) accordSlugs.add("ambarado");
      else if (slug.includes("almiscar") || slug.includes("musk")) accordSlugs.add("atalcado");
      else accordSlugs.add("Fresco");
    }

    const accordLinks = [...accordSlugs]
      .map((accSlug) => {
        const found = byNormalizedName.get(normalizeKnowledgeReference(accSlug));
        return found ? formatLink(found.id) : `[[${accSlug}]]`;
      });

    if (accordLinks.length > 0) {
      linkSections.push(`## Acordes e Facetas Relacionadas\n\n${accordLinks.map((l) => `- ${l}`).join("\n")}\n`);
    }

    // Connect to Fragrances
    const fragrances = noteToFragrances.get(item.id);
    if (fragrances && fragrances.size > 0) {
      const fragLinks = [...fragrances]
        .sort((a, b) => a.title.localeCompare(b.title, "pt-BR"))
        .map((f) => `- ${formatLink(f.id)}`);
      linkSections.push(`## Presente nas Fragrâncias\n\n${fragLinks.join("\n")}\n`);
    }

    if (linkSections.length > 0) {
      // Remove old sections if exist
      body = body.replace(/## Acordes e Facetas Relacionadas[\s\S]*?(?=\n## |$)/, "");
      body = body.replace(/## Presente nas Fragrâncias[\s\S]*?(?=\n## |$)/, "");
      body = `${body.trimEnd()}\n\n${linkSections.join("\n")}`;

      if (lineEnding === "\r\n") {
        body = body.replaceAll("\n", "\r\n");
      }

      const newContent = `---${lineEnding}${frontmatter}---${lineEnding}${body}`;
      if (newContent !== rawContent) {
        if (!dryRun) {
          await writeFile(fullPath, newContent, "utf8");
        }
        updatedCount++;
        totalLinksAdded += accordLinks.length + (fragrances?.size ?? 0);
      }
    }
  }

  // Helper for updating entity reverse links
  async function updateEntityReverseLinks(
    type: string,
    targetMap: Map<string, Set<DocIndexItem>>,
    sectionTitle: string,
  ): Promise<void> {
    for (const item of docs) {
      if (item.type !== type) continue;
      const fragrances = targetMap.get(item.id);
      if (!fragrances || fragrances.size === 0) continue;

      const fullPath = join(vaultDir, item.relativePath);
      const rawContent = await readFile(fullPath, "utf8");
      const parts = rawContent.split(/---\r?\n/);
      if (parts.length < 3) continue;

      const lineEnding = rawContent.includes("\r\n") ? "\r\n" : "\n";
      const frontmatter = parts[1];
      let body = parts.slice(2).join(`---${lineEnding}`);

      const fragLinks = [...fragrances]
        .sort((a, b) => a.title.localeCompare(b.title, "pt-BR"))
        .map((f) => `- ${formatLink(f.id)}`);

      const sectionContent = `## ${sectionTitle}\n\n${fragLinks.join("\n")}\n`;
      if (body.includes(`## ${sectionTitle}`)) {
        body = body.replace(new RegExp(`## ${sectionTitle}[\\s\\S]*?(?=\\n## |$)`), sectionContent);
      } else {
        body = `${body.trimEnd()}\n\n${sectionContent}`;
      }

      if (lineEnding === "\r\n") {
        body = body.replaceAll("\n", "\r\n");
      }

      const newContent = `---${lineEnding}${frontmatter}---${lineEnding}${body}`;
      if (newContent !== rawContent) {
        if (!dryRun) {
          await writeFile(fullPath, newContent, "utf8");
        }
        updatedCount++;
        totalLinksAdded += fragLinks.length;
      }
    }
  }

  // 3. Update Brands, Perfumers, Accords, Concentrations, Contexts
  await updateEntityReverseLinks("brand", brandToFragrances, "Fragrâncias no Acervo");
  await updateEntityReverseLinks("perfumer", perfumerToFragrances, "Criações no Acervo");
  await updateEntityReverseLinks("accord", accordToFragrances, "Fragrâncias com este Acorde");
  await updateEntityReverseLinks("concentration", concentrationToFragrances, "Fragrâncias com esta Concentração");
  await updateEntityReverseLinks("context", contextToFragrances, "Fragrâncias Recomendadas");

  return { updatedCount, totalLinksAdded };
}

// CLI Execution
const dryRun = process.argv.includes("--dry-run");
console.log(`Iniciando sincronização de wikilinks para Obsidian (dryRun=${dryRun})...`);
syncObsidianWikilinks(dryRun).then(({ updatedCount, totalLinksAdded }) => {
  console.log(`Sucesso: ${updatedCount} arquivos sincronizados, ${totalLinksAdded} wikilinks tecidos no grafo!`);
}).catch((err) => {
  console.error("Erro na sincronização:", err);
  process.exit(1);
});
