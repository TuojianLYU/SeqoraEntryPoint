const SECTION_MAP = [
  { id: "skills", heading: "Skills", grid: "skills-grid", badge: "Skill" },
  { id: "tools", heading: "工具 Tools", grid: "tools-grid", badge: "Tool" },
  { id: "websites", heading: "网站 Websites", grid: "websites-grid", badge: "Link" },
  { id: "learning", heading: "学习资源 Learning", grid: "learning-grid", badge: "Learn" },
  { id: "others", heading: "其他 Others", grid: "others-grid", badge: "Other" }
];

const PLACEHOLDER_RE = /^_?(待添加|示例)_?$/i;

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function markdownInline(value) {
  let html = escapeHtml(value || "");
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_match, label, url) => {
    const href = escapeHtml(url);
    const target = /^https?:\/\//i.test(url) ? ' target="_blank" rel="noreferrer"' : "";
    return `<a href="${href}"${target}>${label}</a>`;
  });
  html = html.replace(/\bhttps?:\/\/[^\s<")]+/g, (url) => {
    if (html.includes(`href="${url}"`)) return url;
    const href = escapeHtml(url);
    return `<a href="${href}" target="_blank" rel="noreferrer">${url}</a>`;
  });
  html = html.replace(/_([^_]+)_/g, "<em>$1</em>");
  return html;
}

function normalizeHeading(line) {
  return line.replace(/^##+\s+/, "").trim();
}

function getSection(readme, heading) {
  const lines = readme.split(/\r?\n/);
  const start = lines.findIndex((line) => normalizeHeading(line) === heading);
  if (start === -1) return "";

  const sectionLines = [];
  for (let index = start + 1; index < lines.length; index += 1) {
    if (/^##\s+/.test(lines[index])) break;
    sectionLines.push(lines[index]);
  }
  return sectionLines.join("\n");
}

function parseTable(section) {
  const rows = section
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.startsWith("|") && line.endsWith("|"));

  if (rows.length < 3) return [];

  const headers = splitRow(rows[0]);
  return rows.slice(2).map((row) => {
    const cells = splitRow(row);
    return headers.reduce((entry, header, index) => {
      entry[header] = cells[index] || "";
      return entry;
    }, {});
  }).filter((entry) => !PLACEHOLDER_RE.test(stripMarkdown(entry["名称"] || "")));
}

function splitRow(row) {
  return row
    .slice(1, -1)
    .split("|")
    .map((cell) => cell.trim());
}

function stripMarkdown(value) {
  return String(value || "")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1")
    .replace(/_/g, "")
    .trim();
}

function parseNotes(section) {
  return section
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => /^[-*]\s+/.test(line))
    .map((line) => line.replace(/^[-*]\s+/, ""))
    .filter((line) => !PLACEHOLDER_RE.test(stripMarkdown(line)));
}

function getIntro(readme) {
  const lines = readme.split(/\r?\n/);
  const firstHeading = lines.findIndex((line) => /^##\s+/.test(line));
  return lines
    .slice(1, firstHeading === -1 ? lines.length : firstHeading)
    .map((line) => line.trim())
    .filter(Boolean)
    .join(" ");
}

function getLastUpdated(readme) {
  const match = readme.match(/_最后更新：([^_]+)_/);
  return match ? match[1].trim() : "";
}

function cardFor(entry, section) {
  const name = entry["名称"] || "Untitled";
  const description = entry["用途"] || entry["说明"] || "";
  const path = entry["路径"] || "";
  const link = entry["链接"] || entry["下载"] || "";
  const searchText = [name, description, path, link, section.badge].join(" ").toLowerCase();

  const card = document.createElement("article");
  card.className = "resource-card";
  card.dataset.search = stripMarkdown(searchText).toLowerCase();
  card.innerHTML = `
    <div class="card-top">
      <h3 class="card-title">${markdownInline(name)}</h3>
      <span class="badge">${section.badge}</span>
    </div>
    <p class="description">${markdownInline(description)}</p>
    <div class="meta">
      ${path ? markdownInline(path) : ""}
      ${link ? markdownInline(link) : ""}
    </div>
  `;
  return card;
}

function renderSection(section, entries) {
  const grid = document.getElementById(section.grid);
  grid.innerHTML = "";

  if (!entries.length) {
    const empty = document.createElement("div");
    empty.className = "empty";
    empty.textContent = "README 里还没有正式条目。";
    grid.append(empty);
    return;
  }

  entries.forEach((entry) => grid.append(cardFor(entry, section)));
}

function renderNotes(notes) {
  const list = document.getElementById("notes-list");
  list.innerHTML = "";

  if (!notes.length) {
    const empty = document.createElement("li");
    empty.className = "empty";
    empty.textContent = "README 里还没有正式笔记。";
    list.append(empty);
    return;
  }

  notes.forEach((note) => {
    const item = document.createElement("li");
    item.innerHTML = markdownInline(note);
    list.append(item);
  });
}

function applySearch(query) {
  const normalized = query.trim().toLowerCase();
  const cards = Array.from(document.querySelectorAll(".resource-card"));
  let visible = 0;

  cards.forEach((card) => {
    const matched = !normalized || card.dataset.search.includes(normalized);
    card.hidden = !matched;
    if (matched) visible += 1;
  });

  document.getElementById("resource-count").textContent =
    `${visible} resource${visible === 1 ? "" : "s"}`;
}

async function boot() {
  const response = await fetch("README.md", { cache: "no-store" });
  if (!response.ok) throw new Error(`README fetch failed: ${response.status}`);

  const readme = await response.text();
  document.getElementById("intro-copy").textContent = getIntro(readme);

  const lastUpdated = getLastUpdated(readme);
  document.getElementById("sync-status").textContent =
    lastUpdated ? `Last updated ${lastUpdated}` : "README synced";

  SECTION_MAP.forEach((section) => {
    renderSection(section, parseTable(getSection(readme, section.heading)));
  });
  renderNotes(parseNotes(getSection(readme, "灵感 / 笔记 Notes")));

  const search = document.getElementById("resource-search");
  search.addEventListener("input", (event) => applySearch(event.target.value));
  applySearch("");
}

boot().catch((error) => {
  document.getElementById("sync-status").textContent = "README sync failed";
  document.getElementById("intro-copy").textContent =
    "Could not load README.md. Serve this repository from a static web server or GitHub Pages.";
  console.error(error);
});
