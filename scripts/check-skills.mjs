#!/usr/bin/env node
// Checks the repo invariants CLAUDE.md states for skills, mechanically.
// Exits 1 with one line per problem; exits 0 silently-ish when clean.
//
//   node scripts/check-skills.mjs        (or: npm run check-skills)

import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { basename, dirname, join, relative } from "node:path";
import { fileURLToPath } from "node:url";
import { conversationProblems, stripConversationMarker } from "./sync-conversation-style.mjs";
import { routeCoverageProblems } from "./route-coverage.mjs";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (p) => readFileSync(join(repo, p), "utf8");
const problems = [];
const problem = (s) => problems.push(s);

const PROMOTED = ["engineering", "productivity"];
const NON_PROMOTED = ["misc", "in-progress", "deprecated"];

function skillsIn(bucket) {
  const dir = join(repo, "skills", bucket);
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((n) => existsSync(join(dir, n, "SKILL.md")))
    .sort();
}

function frontmatter(text) {
  const m = text.match(/^---\n([\s\S]*?)\n---/);
  return m ? m[1] : "";
}

const plugin = JSON.parse(read(".claude-plugin/plugin.json"));
const pluginSkills = new Set(plugin.skills.map((s) => s.replace(/^\.\//, "")));
const readme = read("README.md");
const readmeZh = existsSync(join(repo, "README.zh-CN.md")) ? read("README.zh-CN.md") : null;
const askMatt = read("skills/engineering/ask-matt/SKILL.md");

// 1. Promoted skills: everywhere they must be.
for (const bucket of PROMOTED) {
  const bucketReadme = read(`skills/${bucket}/README.md`);
  for (const name of skillsIn(bucket)) {
    const rel = `skills/${bucket}/${name}`;
    const skillMd = read(`${rel}/SKILL.md`);
    const fm = frontmatter(skillMd);
    const userInvoked = /disable-model-invocation:\s*true/.test(fm);

    if (!pluginSkills.has(rel)) problem(`${rel}: missing from .claude-plugin/plugin.json`);
    if (!readme.includes(`(./${rel}/SKILL.md)`)) problem(`${rel}: no linked entry in README.md`);
    if (readmeZh && !readmeZh.includes(`(./${rel}/SKILL.md)`)) problem(`${rel}: no linked entry in README.zh-CN.md`);
    if (!bucketReadme.includes(`(./${name}/SKILL.md)`)) problem(`${rel}: no linked entry in skills/${bucket}/README.md`);

    const yamlPath = `${rel}/agents/openai.yaml`;
    if (!existsSync(join(repo, yamlPath))) {
      problem(`${rel}: no agents/openai.yaml`);
    } else {
      const yaml = read(yamlPath);
      const implicitFalse = /allow_implicit_invocation:\s*false/.test(yaml);
      if (userInvoked && !implicitFalse) problem(`${rel}: user-invoked (disable-model-invocation: true) but openai.yaml lacks policy.allow_implicit_invocation: false`);
      if (!userInvoked && implicitFalse) problem(`${rel}: model-invoked but openai.yaml has allow_implicit_invocation: false`);
    }

    const docPath = `docs/${bucket}/${name}.md`;
    if (!existsSync(join(repo, docPath))) {
      problem(`${rel}: no docs page at ${docPath}`);
    } else {
      const doc = read(docPath);
      for (const h of ["## What it does", "## When to reach for it", "## Common questions", "## It's working if", "## Where it fits"]) {
        if (!doc.includes(h)) problem(`${docPath}: missing section "${h}"`);
      }
      if (/^# /m.test(doc)) problem(`${docPath}: has an H1 (the published page takes its title from the slug)`);
      for (const m of doc.matchAll(/\]\(((?!https?:\/\/|#|mailto:)[^)#]+)(#[^)]*)?\)/g)) {
        const target = join(repo, `docs/${bucket}`, m[1]);
        if (!existsSync(target)) problem(`${docPath}: link ${m[1]} does not resolve`);
      }
      if (/aihero\.dev\/skills-/.test(doc)) problem(`${docPath}: links to aihero.dev/skills-<name>; docs links are repo-relative`);
      if (/^(npx skills@|\/plugin install|claude plugins install)/m.test(doc)) problem(`${docPath}: carries install commands (the site renders them)`);
    }

    if (userInvoked && !askMatt.includes(name)) problem(`${rel}: user-invoked but ask-matt/SKILL.md never names it`);
  }
}

// 2. Non-promoted skills: nowhere they must not be.
for (const bucket of NON_PROMOTED) {
  for (const name of skillsIn(bucket)) {
    const rel = `skills/${bucket}/${name}`;
    if (pluginSkills.has(rel)) problem(`${rel}: non-promoted skill listed in plugin.json`);
    if (readme.includes(`(./${rel}/SKILL.md)`)) problem(`${rel}: non-promoted skill linked from README.md`);
    if (existsSync(join(repo, `docs/${bucket}/${name}.md`))) problem(`${rel}: non-promoted skill has a docs page`);
  }
}

// 3. plugin.json entries that point nowhere.
for (const rel of pluginSkills) {
  if (!existsSync(join(repo, rel, "SKILL.md"))) problem(`plugin.json: ${rel} has no SKILL.md`);
}

// 4. Prose rules: no em-dashes, English only outside the translation.
const PROSE_EXT = new Set([".md", ".py", ".json", ".yaml", ".yml", ".html", ".sh", ".mjs"]);
const SKIP_DIRS = new Set([".git", "node_modules"]);
function walk(dir, out = []) {
  for (const entry of readdirSync(dir)) {
    if (SKIP_DIRS.has(entry)) continue;
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) walk(full, out);
    else out.push(full);
  }
  return out;
}
for (const full of walk(repo)) {
  const rel = relative(repo, full);
  const ext = rel.slice(rel.lastIndexOf("."));
  if (!PROSE_EXT.has(ext)) continue;
  const text = readFileSync(full, "utf8");
  if (rel !== "CHANGELOG.md" && text.includes("\u2014")) problem(`${rel}: contains an em-dash`);
  // The Chinese poster generator carries Chinese strings for its PNG output.
  const CJK_OK = new Set(["README.zh-CN.md", "docs/engineering/poster/build_poster_zh.py"]);
  const prose = stripConversationMarker(text);
  if (!CJK_OK.has(rel) && !/^README\.md$/.test(rel) && /[\u4e00-\u9fff]/.test(prose)) problem(`${rel}: contains non-English (CJK) text`);
  if (rel === "README.md") {
    // Apart from the fixed conversation marker, only the language switch may contain CJK.
    const stripped = prose.replace(/\u7b80\u4f53\u4e2d\u6587/g, ""); // the "Simplified Chinese" switch label
    if (/[\u4e00-\u9fff]/.test(stripped)) problem(`${rel}: contains CJK text beyond the language-switch label`);
  }
  if (/plain English/.test(text) && !/never "plain English"/.test(text)) problem(`${rel}: says "plain English" (say "plain words" or "in the user's language")`);
}

// 5. Translation drift: same set of skill links as README.md.
if (readmeZh) {
  const links = (t) => new Set(t.match(/\.\/skills\/[a-z-]+\/[a-z-]+\/SKILL\.md/g) || []);
  const a = links(readme), b = links(readmeZh);
  for (const l of a) if (!b.has(l)) problem(`README.zh-CN.md: missing ${l}`);
  for (const l of b) if (!a.has(l)) problem(`README.zh-CN.md: has ${l} which README.md lacks`);
}

// 6. Standalone-safe conversation rules and complete dispatcher coverage.
problems.push(...conversationProblems(repo), ...routeCoverageProblems(repo));

if (problems.length) {
  for (const p of problems) console.error(`✗ ${p}`);
  console.error(`\n${problems.length} problem(s).`);
  process.exit(1);
}
console.log(`check-skills: ${[...pluginSkills].length} promoted skills, all invariants hold.`);
