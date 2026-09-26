import test from "node:test";
import assert from "node:assert/strict";
import vm from "node:vm";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { parseHTML } from "linkedom";
import { LABELS, validateGuide, renderGuide, safeSourceLink } from "../skills/productivity/askcat/scripts/build-page.mjs";

const repo = join(dirname(fileURLToPath(import.meta.url)), "..");
const template = readFileSync(join(repo, "skills/productivity/askcat/template.html"), "utf8");
const MARKER = "喵！";

function fixture() {
  const names = ["vibe", "tell-a-story", "cattytest", "verify", "test-audit", "research"];
  const skills = names.map((name, index) => ({
    name, invoke: index < 3 ? "you" : "agent", beta: false,
    oneLiner: `We can explore ${name} together.`, when: "When you need a comfortable starting point.",
    see: "A clear next step, with the evidence kept visible.",
    example: index < 3 ? `/${name}` : `Please help with ${name}.`,
    tip: "You can correct the explanation before moving on.",
    working: "You can recognize your intended outcome.", broken: "The explanation makes an unsupported promise.",
    file: `skills/engineering/${name}/SKILL.md`,
  }));
  const inventory = { scope: "installed", skills: skills.map(({ name, invoke, beta }) => ({ name, invoke, beta })) };
  const labels = Object.fromEntries(LABELS.map((name) => [name, name]));
  labels.installedScope = "Verified installed skills";
  labels.repositoryScope = "Repository catalog; commands may need installing";
  const data = {
    scope: "installed", lang: "en", title: "Test guide", subtitle: "Let's find a gentle starting point.",
    source: "test-fixture", generated: "2026-09-27", cat: { name: "Mimi", moods: { storyteller: "Calico storyteller" } }, labels,
    intro: { heading: "Welcome", paragraphs: ["One small step is enough to start.", "We can go at your pace."], bubble: "What would you like to explore first?" },
    chapters: [{ id: "build", title: "Build", blurb: "Here are your options.", mood: "builder", bubble: "We can choose one together.", skills }],
    picker: { start: "q1", questions: [{ id: "q1", text: "What would help you most?", options: skills.map((skill) => ({ label: skill.name, skill: skill.name, prompt: skill.example })) }] },
    firstRun: [{ type: "/vibe", watch: "One clear recommendation." }],
    glossary: [{ term: "spec", plain: "The agreed description of the work." }], footer: "You can regenerate this guide after updating the kit.",
  };
  return { data, inventory };
}

function mount(data, inventory, { hash = "", store = new Map(), unavailableStorage = false, html } = {}) {
  const page = html || renderGuide(template, data, inventory);
  const { window, document } = parseHTML(page);
  window.HTMLElement.prototype.scrollIntoView = function () { this.setAttribute("data-scrolled", "true"); };
  const localStorage = {
    getItem(key) { if (unavailableStorage) throw new Error("blocked"); return store.get(key) ?? null; },
    setItem(key, value) { if (unavailableStorage) throw new Error("blocked"); store.set(key, value); },
    removeItem(key) { if (unavailableStorage) throw new Error("blocked"); store.delete(key); },
  };
  const context = vm.createContext({ window, document, localStorage, location: { hash }, URL, setTimeout: (fn) => fn() });
  for (const script of document.querySelectorAll("script")) vm.runInContext(script.textContent, context);
  return { document, window, store, context };
}

test("a complete inventory produces one offline guide with exact card count", () => {
  const { data, inventory } = fixture();
  assert.deepEqual(validateGuide(data, inventory), []);
  const { document } = mount(data, inventory);
  assert.equal(document.querySelectorAll(".card").length, inventory.skills.length);
  assert.equal(document.querySelector(".scope").textContent, data.labels.installedScope);
  assert.equal(document.querySelectorAll("script[src],link[rel=stylesheet],img[src]").length, 0);
});

for (const [name, mutate, expected] of [
  ["new skill omitted", (d, i) => i.skills.push({ name: "new-skill", invoke: "you", beta: false }), /Missing card: new-skill/],
  ["duplicate installs become duplicate cards", (d) => d.chapters[0].skills.push(d.chapters[0].skills[0]), /Duplicate card: vibe/],
  ["wrong invocation", (d) => { d.chapters[0].skills[1].invoke = "agent"; }, /Invocation mismatch/],
  ["beta flag lost", (d, i) => { i.skills[1].beta = true; }, /Beta flag mismatch/],
  ["catalog called installed", (d, i) => { i.scope = "repository"; }, /scope must match/],
  ["missing UI translation", (d) => { delete d.labels.restart; }, /Missing label: restart/],
  ["uninstalled picker leaf", (d) => { d.picker.questions[0].options[0].skill = "not-installed"; }, /unavailable skill/],
  ["omitted story route", (d) => { d.picker.questions[0].options[1] = d.picker.questions[0].options[0]; }, /important installed route: tell-a-story/],
  ["missing graph target", (d) => d.picker.questions[0].options.push({ label: "Next", next: "missing" }), /Missing picker target/],
  ["cycle", (d) => d.picker.questions[0].options.push({ label: "Again", next: "q1" }), /Picker cycle/],
  ["unreachable question", (d) => d.picker.questions.push({ id: "unused", text: "Unused?", options: d.picker.questions[0].options }), /Unreachable picker question/],
  ["unsafe source URL", (d) => { d.chapters[0].skills[0].file = "javascript:alert(1)"; }, /Unsafe source link/],
  ["uncopyable user command", (d) => { d.chapters[0].skills[1].example = "Please tell me a story"; }, /must begin with \/tell-a-story/],
  ["unavailable first-run command", (d) => d.firstRun.push({ type: "/uninstalled-setup", watch: "A setup file" }), /unavailable command/],
]) {
  test(`guide validation rejects ${name}`, () => {
    const { data, inventory } = fixture();
    mutate(data, inventory);
    assert.match(validateGuide(data, inventory).join("\n"), expected);
    assert.throws(() => renderGuide(template, data, inventory));
  });
}

test("picker depth is bounded", () => {
  const { data, inventory } = fixture();
  for (let n = 1; n <= 5; n++) {
    const q = n === 1 ? data.picker.questions[0] : { id: `q${n}`, text: "Another choice?", options: [data.picker.questions[0].options[0]] };
    if (n < 5) q.options.push({ label: "More", next: `q${n + 1}` });
    else q.options.push(data.picker.questions[0].options[1]);
    if (n > 1) data.picker.questions.push(q);
  }
  assert.match(validateGuide(data, inventory).join("\n"), /exceeds four questions/);
});

test("source links permit encoded local paths and reject executable schemes and controls", () => {
  for (const value of ["../My%20Project/skills/sample/SKILL.md", "https://example.test/SKILL.md", "file:///tmp/SKILL.md"]) assert.equal(safeSourceLink(value), true);
  for (const value of ["javascript:alert(1)", "data:text/html,hello", "//outside.test/page", "java\nscript:alert(1)"]) assert.equal(safeSourceLink(value), false);
});

test("narration has one marker per paragraph while commands and labels stay unchanged", () => {
  const { data, inventory } = fixture();
  data.intro.paragraphs = [`We can take our time. ${MARKER}\n\nOne small step next. ${MARKER} ${MARKER}`];
  const { document } = mount(data, inventory);
  const prose = [...document.querySelectorAll(".one,.tip > div,.tells > div,.chapter .blurb,dd")];
  for (const node of prose) assert.ok(node.textContent.endsWith(MARKER), node.textContent);
  const intro = [...document.querySelectorAll("section.block > p")].find((p) => p.textContent.includes("One small step next"));
  assert.equal(intro.textContent.split(MARKER).length - 1, 2);
  assert.equal(document.querySelector("#skill-tell-a-story .ex").textContent, "/tell-a-story");
  assert.equal(document.querySelector(".steps .t").textContent, "/vibe");
  assert.equal(document.querySelector("#q").getAttribute("placeholder"), data.labels.search);
});

test("the fixed marker has a tiny embedded font and its redistribution license", () => {
  const match = template.match(/data:font\/woff2;base64,([A-Za-z0-9+/=]+)/);
  assert.ok(match);
  const font = Buffer.from(match[1], "base64");
  assert.equal(font.toString("ascii", 0, 4), "wOF2");
  assert.ok(font.length < 8 * 1024);
  assert.ok(template.includes("SIL OPEN FONT LICENSE Version 1.1"));
  const { data, inventory } = fixture();
  const { document } = mount(data, inventory);
  assert.ok(document.querySelectorAll(".miao").length > 0);
  assert.equal(document.querySelector(".ex .miao"), null);
});

test("the calico storyteller is used on the story card and its picker result", () => {
  const { data, inventory } = fixture();
  const { document, window } = mount(data, inventory);
  assert.ok(document.querySelector('#skill-tell-a-story .cat[data-mood="storyteller"]'));
  document.querySelector('#pk button[data-i="1"]').dispatchEvent(new window.Event("click"));
  assert.ok(document.querySelector('.picker .result .cat[data-mood="storyteller"]'));
  assert.equal(document.querySelector(".picker .result .ex").textContent, "/tell-a-story");
  document.querySelector("#pk [data-restart]").dispatchEvent(new window.Event("click"));
  assert.equal(document.querySelectorAll("#pk button[data-i]").length, 6);
});

test("role-specific SVG groups are in the mascot DOM where their CSS can reach them", () => {
  const { data, inventory } = fixture();
  const { document } = mount(data, inventory);
  const cat = document.querySelector('#skill-tell-a-story .cat');
  assert.ok(cat.querySelector('.acc-book'));
  assert.ok(cat.querySelector('.coat-calico'));
  assert.equal(cat.querySelector('use'), null);
});

test("search, progress and stored ticks survive regeneration", () => {
  const { data, inventory } = fixture();
  const { document, window, store } = mount(data, inventory);
  const search = document.querySelector("#q");
  search.value = "tell-a-story";
  search.dispatchEvent(new window.Event("input"));
  assert.equal(document.querySelectorAll(".card:not(.hidden)").length, 1);
  const box = document.querySelector('#skill-tell-a-story input[type="checkbox"]');
  box.checked = true;
  box.dispatchEvent(new window.Event("change", { bubbles: true }));
  assert.equal(document.querySelector("#cnt").textContent, "1 / 6");
  assert.ok(document.querySelector("#skill-tell-a-story").classList.contains("done"));
  const regenerated = mount(data, inventory, { store });
  assert.ok(regenerated.document.querySelector('#skill-tell-a-story input').hasAttribute("checked"));
});

test("deep links work and malformed hashes do not crash the guide", () => {
  const { data, inventory } = fixture();
  for (const hash of ["#[", "#%zz", "#missing"]) assert.doesNotThrow(() => mount(data, inventory, { hash }));
  const { document } = mount(data, inventory, { hash: "#skill-tell-a-story" });
  assert.equal(document.querySelector("#skill-tell-a-story").getAttribute("data-scrolled"), "true");
});

test("closing script tags and HTML in source text stay literal", () => {
  const { data, inventory } = fixture();
  const payload = '</script><script>window.PWNED=true</script><img src=x onerror=alert(1)>';
  data.intro.bubble = payload;
  const page = renderGuide(template, data, inventory);
  assert.ok(page.includes("\\u003c/script>"));
  const { document, window } = mount(data, inventory, { html: page });
  assert.equal(document.querySelectorAll("script").length, 2);
  assert.equal(window.PWNED, undefined);
  assert.equal(document.querySelectorAll("img[onerror]").length, 0);
  assert.ok(document.querySelector("header .bubble").textContent.startsWith(payload));
});

test("decorative markers are rejected in copyable prompts and first-run commands", () => {
  for (const field of ["example", "prompt", "type"]) {
    const { data, inventory } = fixture();
    if (field === "example") data.chapters[0].skills[1].example += ` ${MARKER}`;
    if (field === "prompt") data.picker.questions[0].options[1].prompt += ` ${MARKER}`;
    if (field === "type") data.firstRun[0].type += ` ${MARKER}`;
    assert.match(validateGuide(data, inventory).join("\n"), /decorative marker/);
  }
});

test("malformed collections fail validation without throwing a renderer exception", () => {
  for (const mutate of [
    (d) => { d.chapters = [null]; },
    (d) => { d.picker.questions = {}; },
    (d) => { d.picker.questions[0].options = {}; },
    (d) => { d.firstRun = {}; },
    (d, i) => { i.skills = [null]; },
  ]) {
    const { data, inventory } = fixture();
    mutate(data, inventory);
    assert.doesNotThrow(() => validateGuide(data, inventory));
    assert.ok(validateGuide(data, inventory).length > 0);
  }
});

test("progress still works for this page when browser storage is unavailable", () => {
  const { data, inventory } = fixture();
  const { document, window } = mount(data, inventory, { unavailableStorage: true });
  const box = document.querySelector('#skill-tell-a-story input[type="checkbox"]');
  box.checked = true;
  box.dispatchEvent(new window.Event("change", { bubbles: true }));
  assert.equal(document.querySelector("#cnt").textContent, "1 / 6");
});

test("builder refuses an existing output unless replacement is explicitly requested", () => {
  const { data, inventory } = fixture();
  const folder = mkdtempSync(join(tmpdir(), "askcat-page-"));
  try {
    const guidePath = join(folder, "guide.json"), inventoryPath = join(folder, "inventory.json"), out = join(folder, "askcat.html");
    writeFileSync(guidePath, JSON.stringify(data));
    writeFileSync(inventoryPath, JSON.stringify(inventory));
    writeFileSync(out, "Keep this file.");
    const args = [join(repo, "skills/productivity/askcat/scripts/build-page.mjs"), "--data", guidePath, "--inventory", inventoryPath, "--out", out];
    const refused = spawnSync(process.execPath, args, { encoding: "utf8" });
    assert.equal(refused.status, 1);
    assert.equal(readFileSync(out, "utf8"), "Keep this file.");
    assert.equal(spawnSync(process.execPath, [...args, "--force"], { encoding: "utf8" }).status, 0);
    assert.match(readFileSync(out, "utf8"), /window\.ASKCAT = /);
  } finally {
    rmSync(folder, { recursive: true, force: true });
  }
});
