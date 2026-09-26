#!/usr/bin/env node
// Dependency-free guide validation and safe, offline HTML assembly.
import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { parseArgs } from "node:util";

export const MOODS = ["teacher", "storyteller", "builder", "detective", "guard", "sweeper", "dizzy", "reader"];
export const LABELS = ["search", "youType", "agentUses", "beta", "when", "see", "example", "tip", "tried", "progress", "picker", "pickerIntro", "restart", "result", "firstRun", "glossary", "openFile", "chapters", "noMatch", "installedScope", "repositoryScope"];
const MIAO = "喵！";
const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const asArray = (value) => Array.isArray(value) ? value : [];
const decorated = (value) => typeof value === "string" && value.trimEnd().endsWith(MIAO);
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const nonempty = (value) => typeof value === "string" && value.trim().length > 0;

export function safeSourceLink(value) {
  if (!nonempty(value) || /[\u0000-\u0020\u007f\\]/.test(value) || value.startsWith("//")) return false;
  if (/^[a-z][a-z0-9+.-]*:/i.test(value)) {
    try { return ["https:", "http:", "file:"].includes(new URL(value).protocol); }
    catch { return false; }
  }
  return true;
}

export function validateGuide(data, inventory) {
  const errors = [];
  const need = (condition, message) => { if (!condition) errors.push(message); };
  if (!data || typeof data !== "object" || Array.isArray(data)) return ["Guide must be an object"];
  if (!inventory || !Array.isArray(inventory.skills)) return ["An independently gathered skill inventory is required"];
  need(["installed", "repository"].includes(inventory.scope), "Inventory scope must be installed or repository");
  need(data.scope === inventory.scope, "Guide scope must match the inventory; a checkout is not proof of installation");
  for (const field of ["lang", "title", "subtitle", "source", "generated", "footer"]) need(nonempty(data[field]), `Missing ${field}`);
  for (const label of LABELS) need(nonempty(data.labels?.[label]), `Missing label: ${label}`);
  need(nonempty(data.cat?.name), "The guide needs a cat name");
  need(nonempty(data.intro?.heading) && nonempty(data.intro?.bubble), "The introduction needs a heading and bubble");
  need(Array.isArray(data.intro?.paragraphs) && data.intro.paragraphs.length > 0 && data.intro.paragraphs.every(nonempty), "The introduction needs prose paragraphs");

  const expected = new Map();
  for (const entry of inventory.skills) {
    if (!isObject(entry)) { errors.push("Inventory entries must be objects"); continue; }
    need(SLUG.test(entry.name || ""), `Invalid inventory name: ${entry.name}`);
    need(!expected.has(entry.name), `Duplicate inventory entry: ${entry.name}`);
    need(["you", "agent"].includes(entry.invoke), `Invalid inventory invocation: ${entry.name}`);
    need(typeof entry.beta === "boolean", `Inventory beta flag must be explicit: ${entry.name}`);
    expected.set(entry.name, entry);
  }
  need(expected.size > 0, "Inventory is empty; explain missing access instead of inventing a guide");
  const names = new Map(), chapterIds = new Set();
  need(Array.isArray(data.chapters) && data.chapters.length > 0, "No chapters");
  for (const chapter of asArray(data.chapters)) {
    if (!isObject(chapter)) { errors.push("Chapters must be objects"); continue; }
    need(SLUG.test(chapter.id || ""), `Invalid chapter id: ${chapter.id}`);
    need(!chapterIds.has(chapter.id), `Duplicate chapter id: ${chapter.id}`);
    chapterIds.add(chapter.id);
    need(nonempty(chapter.title) && nonempty(chapter.blurb), `Chapter needs a title and blurb: ${chapter.id}`);
    if (chapter.mood) need(MOODS.includes(chapter.mood), `Unknown mood: ${chapter.mood}`);
    need(Array.isArray(chapter.skills) && chapter.skills.length > 0, `Empty chapter: ${chapter.id}`);
    for (const skill of asArray(chapter.skills)) {
      if (!isObject(skill)) { errors.push("Skill cards must be objects"); continue; }
      need(SLUG.test(skill.name || ""), `Invalid skill name: ${skill.name}`);
      need(!names.has(skill.name), `Duplicate card: ${skill.name}`);
      names.set(skill.name, skill);
      const entry = expected.get(skill.name);
      need(Boolean(entry), `Card absent from inventory: ${skill.name}`);
      if (entry) {
        need(skill.invoke === entry.invoke, `Invocation mismatch: ${skill.name}`);
        need(skill.beta === entry.beta, `Beta flag mismatch: ${skill.name}`);
      }
      if (skill.mood) need(MOODS.includes(skill.mood), `Unknown card mood: ${skill.mood}`);
      for (const field of ["oneLiner", "when", "see", "example", "tip", "working", "broken", "file"]) need(nonempty(skill[field]), `Missing ${field}: ${skill.name}`);
      need(!decorated(skill.example), `Copyable example has a decorative marker: ${skill.name}`);
      need(safeSourceLink(skill.file), `Unsafe source link: ${skill.name}`);
      if (skill.invoke === "you") need(new RegExp(`^/${skill.name}(?:\\s|$)`).test(skill.example || ""), `User-invoked example must begin with /${skill.name}`);
    }
  }
  for (const name of expected.keys()) need(names.has(name), `Missing card: ${name}`);

  const questions = new Map();
  need(Array.isArray(data.picker?.questions) && data.picker.questions.length > 0, "No picker questions");
  for (const q of asArray(data.picker?.questions)) {
    if (!isObject(q)) { errors.push("Picker questions must be objects"); continue; }
    need(SLUG.test(q.id || "") && !questions.has(q.id), `Invalid or duplicate picker question: ${q.id}`);
    need(nonempty(q.text), `Picker question needs text: ${q.id}`);
    need(Array.isArray(q.options) && q.options.length >= 2 && q.options.length <= 6, `Picker needs 2 to 6 options: ${q.id}`);
    questions.set(q.id, q);
    for (const option of asArray(q.options)) {
      if (!isObject(option)) { errors.push(`Picker options must be objects: ${q.id}`); continue; }
      need(nonempty(option.label), `Picker option needs a label: ${q.id}`);
      need(Boolean(option.next) !== Boolean(option.skill), `Picker option must have exactly one target: ${q.id}`);
      if (option.skill) {
        need(names.has(option.skill), `Picker points to an unavailable skill: ${option.skill}`);
        need(!decorated(option.prompt), `Copyable picker prompt has a decorative marker: ${option.skill}`);
        need(nonempty(option.prompt), `Picker leaf needs a prompt: ${option.skill}`);
        const skill = names.get(option.skill);
        if (skill?.invoke === "you") need(new RegExp(`^/${skill.name}(?:\\s|$)`).test(option.prompt || ""), `Picker prompt must begin with /${skill.name}`);
      }
    }
  }
  need(questions.has(data.picker?.start), "Picker start question does not exist");
  for (const q of questions.values()) {
    for (const option of asArray(q.options)) if (isObject(option) && option.next) need(questions.has(option.next), `Missing picker target: ${option.next}`);
  }
  const visited = new Set(), reachableSkills = new Set();
  function visit(id, ancestors = new Set()) {
    if (ancestors.has(id)) { errors.push(`Picker cycle at ${id}`); return; }
    const q = questions.get(id);
    if (!q) return;
    if (ancestors.size >= 4) { errors.push(`Picker exceeds four questions at ${id}`); return; }
    visited.add(id);
    const next = new Set([...ancestors, id]);
    for (const option of asArray(q.options)) {
      if (!isObject(option)) continue;
      if (option.next) visit(option.next, next);
      if (option.skill) reachableSkills.add(option.skill);
    }
  }
  visit(data.picker?.start);
  for (const id of questions.keys()) need(visited.has(id), `Unreachable picker question: ${id}`);
  for (const name of ["tell-a-story", "cattytest", "verify", "test-audit", "research"]) {
    if (expected.has(name)) need(reachableSkills.has(name), `Picker omits an important installed route: ${name}`);
  }
  need(data.firstRun === undefined || Array.isArray(data.firstRun), "First run must be an array");
  for (const step of asArray(data.firstRun)) {
    if (!isObject(step)) { errors.push("First-run steps must be objects"); continue; }
    need(!decorated(step.type), "First-run command has a decorative marker");
    need(nonempty(step.type) && nonempty(step.watch), "First-run steps need a command and an observation");
    for (const [, command] of (step.type || "").matchAll(/(?:^|\s|→)\/([a-z][a-z0-9-]*)/g)) {
      need(names.has(command) || ["clear", "compact", "new"].includes(command), `First run names an unavailable command: ${command}`);
    }
  }
  need(data.glossary === undefined || Array.isArray(data.glossary), "Glossary must be an array");
  for (const entry of asArray(data.glossary)) need(isObject(entry) && nonempty(entry.term) && nonempty(entry.plain), "Glossary entries need a term and explanation");
  need(Buffer.byteLength(JSON.stringify(data), "utf8") <= 150 * 1024, "Guide data exceeds 150 KB");
  return [...new Set(errors)];
}

export function renderGuide(template, data, inventory) {
  const errors = validateGuide(data, inventory);
  if (errors.length) throw new Error(errors.join("\n"));
  const slots = [...template.matchAll(/^\/\*ASKCAT_DATA\*\/\r?$/gm)];
  if (slots.length !== 1) throw new Error("Template must have exactly one standalone data slot");
  const json = JSON.stringify(data).replace(/</g, "\\u003c").replace(/\u2028/g, "\\u2028").replace(/\u2029/g, "\\u2029");
  return template.replace(/^\/\*ASKCAT_DATA\*\/\r?$/m, () => `window.ASKCAT = ${json};`);
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const { values } = parseArgs({ options: { data: { type: "string" }, inventory: { type: "string" }, out: { type: "string" }, force: { type: "boolean", default: false } } });
    if (!values.data || !values.inventory || !values.out) throw new Error("Usage: node build-page.mjs --data guide.json --inventory inventory.json --out askcat.html [--force]");
    const templatePath = join(dirname(fileURLToPath(import.meta.url)), "..", "template.html");
    const output = resolve(values.out);
    if ([templatePath, values.data, values.inventory].some((path) => resolve(path) === output)) throw new Error("Output must not overwrite the template or its input files");
    const data = JSON.parse(readFileSync(values.data, "utf8"));
    const inventory = JSON.parse(readFileSync(values.inventory, "utf8"));
    const html = renderGuide(readFileSync(templatePath, "utf8"), data, inventory);
    mkdirSync(dirname(output), { recursive: true });
    writeFileSync(output, html, { flag: values.force ? "w" : "wx" });
    console.log(`Saved ${output}: ${inventory.skills.length} unique skills (${inventory.scope}).`);
  } catch (error) {
    console.error(error.message);
    process.exitCode = 1;
  }
}
