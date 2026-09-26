import { readFileSync } from "node:fs";
import { join } from "node:path";
import { skillFiles } from "./sync-conversation-style.mjs";

export function routeCoverageProblems(repo) {
  const problems = [];
  const read = (path) => readFileSync(join(repo, path), "utf8");
  try {
    const skills = skillFiles(repo).filter(({ bucket }) => ["engineering", "productivity"].includes(bucket));
    const promoted = new Map(skills.map((skill) => [skill.name, skill]));
    const routes = read("skills/engineering/vibe/ROUTES.md");
    const entries = [...routes.matchAll(/^\| `([a-z0-9-]+)` \| (kit|bring-back|full-map) \| ([^|]+) \|$/gm)];
    const seen = new Map();
    for (const [, name, place, reason] of entries) {
      if (seen.has(name)) problems.push(`vibe/ROUTES.md: duplicate route for ${name}`);
      seen.set(name, place);
      if (!promoted.has(name)) problems.push(`vibe/ROUTES.md: ${name} is not a promoted skill`);
      if (!reason.trim()) problems.push(`vibe/ROUTES.md: ${name} has no routing reason`);
    }
    for (const name of promoted.keys()) {
      if (!seen.has(name)) problems.push(`vibe/ROUTES.md: promoted skill ${name} has no route classification`);
    }
    const handbook = read("skills/engineering/vibe/WORKFLOW.md");
    const sections = handbook.match(/\*\*You type these\*\*[^\n]*\n([\s\S]*?)\*\*The agent reaches for these\*\*[^\n]*\n([\s\S]*?)\*\*Deliberately left out\*\*/);
    if (!sections) {
      problems.push("vibe/WORKFLOW.md: cannot find both curated-kit tables");
    } else {
      const inKit = new Set();
      for (const [index, section] of [sections[1], sections[2]].entries()) {
        for (const [, name] of section.matchAll(/^\| `\/?([a-z0-9-]+)` \|/gm)) {
          if (inKit.has(name)) problems.push(`vibe/WORKFLOW.md: duplicate kit entry ${name}`);
          inKit.add(name);
          if (seen.get(name) !== "kit") problems.push(`vibe/ROUTES.md: ${name} is in the handbook kit but not classified as kit`);
          const skill = promoted.get(name);
          if (skill) {
            const fm = read(skill.path).match(/^---\n([\s\S]*?)\n---/)?.[1] || "";
            const userInvoked = /disable-model-invocation:\s*true/.test(fm);
            if (userInvoked !== (index === 0)) problems.push(`vibe/WORKFLOW.md: ${name} is in the wrong invocation table`);
          }
        }
      }
      for (const [name, place] of seen) {
        if (place === "kit" && !inKit.has(name)) problems.push(`vibe/WORKFLOW.md: kit skill ${name} is missing`);
      }
    }
  } catch (error) {
    problems.push(`Vibe route coverage: ${error.message}`);
  }
  return problems;
}
