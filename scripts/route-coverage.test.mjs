import test from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { routeCoverageProblems } from "./route-coverage.mjs";
const repo = join(dirname(fileURLToPath(import.meta.url)), "..");

test("every promoted skill is classified and the curated kit agrees with invocation metadata", () => {
  assert.deepEqual(routeCoverageProblems(repo), []);
});

test("a newly promoted skill cannot silently miss the dispatcher map", () => {
  const root = mkdtempSync(join(tmpdir(), "cat-routes-"));
  const put = (path, text) => {
    mkdirSync(dirname(join(root, path)), { recursive: true });
    writeFileSync(join(root, path), text);
  };
  try {
    put("skills/engineering/vibe/SKILL.md", "---\nname: vibe\ndisable-model-invocation: true\n---\n");
    put("skills/engineering/new-skill/SKILL.md", "---\nname: new-skill\n---\n");
    put("skills/engineering/vibe/ROUTES.md", "| `vibe` | kit | Route requests |\n");
    put("skills/engineering/vibe/WORKFLOW.md", "**You type these** (user-invoked):\n| `/vibe` | Route |\n**The agent reaches for these** (model-invoked):\n**Deliberately left out**\n");
    assert.ok(routeCoverageProblems(root).some((p) => p.includes("new-skill has no route classification")));
    put("skills/engineering/vibe/ROUTES.md", "| `vibe` | kit | Route requests |\n| `new-skill` | full-map | Use the full map |\n");
    assert.deepEqual(routeCoverageProblems(root), []);
    put("skills/engineering/vibe/ROUTES.md", "| `vibe` | kit | Route requests |\n| `new-skill` | kit | New work |\n");
    assert.ok(routeCoverageProblems(root).some((p) => p.includes("kit skill new-skill is missing")));
  } finally {
    rmSync(root, { recursive: true, force: true });
  }
});

test("research is not described as excluded by the full router", () => {
  const router = readFileSync(join(repo, "skills/engineering/ask-matt/SKILL.md"), "utf8");
  assert.doesNotMatch(router, /deliberately leaves out[^.\n]*`research`/);
});
