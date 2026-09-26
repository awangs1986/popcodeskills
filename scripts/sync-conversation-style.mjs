#!/usr/bin/env node
// Ship the same local instructions even when a skill is installed on its own.
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

export const MARKER = "喵！";
export const START = "<!-- cat-skills:conversation:start -->";
export const END = "<!-- cat-skills:conversation:end -->";
export const DOC_START = "<!-- cat-skills:conversation-doc:start -->";
export const DOC_END = "<!-- cat-skills:conversation-doc:end -->";
export const PROJECT_START = "<!-- cat-skills:project-conversation:start -->";
export const PROJECT_END = "<!-- cat-skills:project-conversation:end -->";
const BUCKETS = ["engineering", "productivity", "in-progress", "misc", "deprecated"];
const PROMOTED = new Set(["engineering", "productivity"]);

export function stripConversationMarker(text) {
  return text.replaceAll(MARKER, "");
}

export function extractBlock(text, start, end) {
  const starts = text.split(start).length - 1;
  const ends = text.split(end).length - 1;
  if (!starts && !ends) return null;
  if (starts !== 1 || ends !== 1 || text.indexOf(end) < text.indexOf(start)) {
    throw new Error(`Malformed or duplicated block: ${start}`);
  }
  return text.slice(text.indexOf(start), text.indexOf(end) + end.length);
}

export function upsertBlock(text, block, start, end, before = null) {
  const old = extractBlock(text, start, end);
  if (old !== null) return text.replace(old, block);
  if (before !== null) {
    if (!text.includes(before)) throw new Error(`Missing insertion point: ${before}`);
    return text.replace(before, `${block}\n\n${before}`);
  }
  return `${text.trimEnd()}\n\n${block}\n`;
}

export function skillFiles(repo) {
  const files = [];
  for (const bucket of BUCKETS) {
    const dir = join(repo, "skills", bucket);
    if (!existsSync(dir)) continue;
    for (const name of readdirSync(dir).sort()) {
      const path = `skills/${bucket}/${name}/SKILL.md`;
      if (existsSync(join(repo, path))) files.push({ path, bucket, name });
    }
  }
  return files;
}

export function conversationUpdates(repo) {
  const read = (path) => readFileSync(join(repo, path), "utf8");
  const canonical = read(".agents/conversation-style.md");
  const block = extractBlock(canonical, START, END);
  const docBlock = extractBlock(canonical, DOC_START, DOC_END);
  if (!block || !docBlock || !block.includes(MARKER)) {
    throw new Error("Conversation source is missing a required block or literal marker");
  }
  const projectBlock = block
    .replace(START, PROJECT_START)
    .replace(END, PROJECT_END)
    .replace("## Conversation style", "### Conversation style");
  const updates = [];
  for (const { path, bucket, name } of skillFiles(repo)) {
    const original = read(path);
    let updated = upsertBlock(original, block, START, END);
    if (name === "setup-matt-pocock-skills") {
      const insertion = "### Language\n";
      updated = upsertBlock(updated, projectBlock, PROJECT_START, PROJECT_END, insertion);
    }
    if (updated !== original) updates.push({ path, original, updated });
    if (PROMOTED.has(bucket)) {
      const docPath = `docs/${bucket}/${name}.md`;
      if (!existsSync(join(repo, docPath))) throw new Error(`Missing docs page: ${docPath}`);
      const doc = read(docPath);
      const updatedDoc = upsertBlock(doc, docBlock, DOC_START, DOC_END, "## When to reach for it\n");
      if (doc !== updatedDoc) updates.push({ path: docPath, original: doc, updated: updatedDoc });
    }
  }
  return updates;
}

export function conversationProblems(repo) {
  try {
    return conversationUpdates(repo).map(({ path }) => `${path}: missing or stale conversation style; run npm run sync-conversation-style`);
  } catch (error) {
    return [error.message];
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  if (args.some((arg) => arg !== "--check")) {
    console.error("Usage: node scripts/sync-conversation-style.mjs [--check]");
    process.exitCode = 1;
  } else {
    const repo = resolve(dirname(fileURLToPath(import.meta.url)), "..");
    try {
      const updates = conversationUpdates(repo);
      if (args.includes("--check") && updates.length) {
        for (const { path } of updates) console.error(`${path}: conversation style needs syncing`);
        process.exitCode = 1;
      } else {
        for (const { path, updated } of updates) writeFileSync(join(repo, path), updated);
        console.log(`conversation-style: ${skillFiles(repo).length} skills checked; ${updates.length} files synchronized.`);
      }
    } catch (error) {
      console.error(error.message);
      process.exitCode = 1;
    }
  }
}
