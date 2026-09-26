import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import {
  START, END, DOC_START, DOC_END, PROJECT_START, PROJECT_END, MARKER,
  extractBlock, upsertBlock, conversationUpdates, conversationProblems,
  stripConversationMarker, skillFiles,
} from "./sync-conversation-style.mjs";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const canonical = readFileSync(join(repo, ".agents/conversation-style.md"), "utf8");
const block = extractBlock(canonical, START, END);

test("portable block is canonical and does not change existing commands or frontmatter", () => {
  const source = "---\nname: sample\ndisable-model-invocation: true\n---\n\nRun `/sample --json`.\n";
  const result = upsertBlock(source, block, START, END);
  assert.ok(result.startsWith(source));
  assert.equal(upsertBlock(result, block, START, END), result);
  assert.equal(extractBlock(result, START, END), block);
});

test("malformed and duplicated blocks fail rather than silently losing instructions", () => {
  assert.throws(() => extractBlock(`${START}\nMissing end`, START, END), /Malformed/);
  assert.throws(() => extractBlock(`${block}\n${block}`, START, END), /duplicated/);
  assert.throws(() => extractBlock(`${END}\n${START}`, START, END), /Malformed/);
});

test("only the exact conversational marker is exempt from the CJK prose check", () => {
  assert.equal(stripConversationMarker(`A paragraph. ${MARKER}`), "A paragraph. ");
  assert.match(stripConversationMarker("\u55b5!"), /[\u4e00-\u9fff]/);
  assert.match(stripConversationMarker(`${MARKER} \u4f60\u597d`), /[\u4e00-\u9fff]/);
});

test("sync covers all buckets, promoted docs, and the emitted setup block without duplicate writes", () => {
  const root = mkdtempSync(join(tmpdir(), "cat-style-"));
  const put = (path, text) => {
    mkdirSync(dirname(join(root, path)), { recursive: true });
    writeFileSync(join(root, path), text);
  };
  try {
    put(".agents/conversation-style.md", canonical);
    for (const bucket of ["engineering", "productivity", "in-progress", "misc", "deprecated"]) {
      const name = bucket === "engineering" ? "setup-matt-pocock-skills" : `${bucket}-example`;
      const setup = bucket === "engineering" ? "\n```markdown\n## Agent skills\n\n### Language\nPreserve commands.\n```\n" : "";
      put(`skills/${bucket}/${name}/SKILL.md`, `---\nname: ${name}\n---\n\nAn instruction.\n${setup}`);
      if (["engineering", "productivity"].includes(bucket)) {
        put(`docs/${bucket}/${name}.md`, "## What it does\n\nAn explanation.\n\n## When to reach for it\n\nWhenever needed.\n");
      }
    }
    const updates = conversationUpdates(root);
    assert.equal(updates.length, 7);
    assert.equal(skillFiles(root).length, 5);
    for (const { path, updated } of updates) put(path, updated);
    assert.deepEqual(conversationUpdates(root), []);
    const setup = readFileSync(join(root, "skills/engineering/setup-matt-pocock-skills/SKILL.md"), "utf8");
    const emitted = extractBlock(setup, PROJECT_START, PROJECT_END);
    assert.ok(emitted.includes("### Conversation style"));
    assert.ok(emitted.includes(MARKER));
    assert.ok(setup.indexOf(PROJECT_START) > setup.indexOf("```markdown"));
    assert.ok(setup.indexOf(PROJECT_END) < setup.indexOf("### Language"));
    const doc = readFileSync(join(root, "docs/productivity/productivity-example.md"), "utf8");
    assert.equal(extractBlock(doc, DOC_START, DOC_END), extractBlock(canonical, DOC_START, DOC_END));
    put("skills/misc/misc-example/SKILL.md", readFileSync(join(root, "skills/misc/misc-example/SKILL.md"), "utf8").replace(MARKER, "meow"));
    assert.equal(conversationProblems(root).length, 1);
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("all real skills and promoted docs have the portable style, including direct-before-setup usage", () => {
  assert.ok(skillFiles(repo).length > 0);
  assert.deepEqual(conversationProblems(repo), []);
});
