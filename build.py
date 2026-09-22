#!/usr/bin/env python3
"""
Builds the site into ./site

  python3 build.py

Add a new piece: drop a .md file into ./posts with a front-matter block:

  ---
  title: My new piece
  date: 2026-09-01
  summary: one line shown on the Writings index (optional)
  draft: true          # optional — builds the page but hides it from the index
  ---

The filename (minus .md) becomes the URL: posts/my-piece.md -> /writings/my-piece/

Add a project: append a block to ./projects.md (blocks separated by a blank line):

  title: My project
  url: https://example.com
  description: one line shown under the title (optional)
"""
import re, shutil, html
from pathlib import Path
from datetime import date
import markdown

ROOT = Path(__file__).parent
OUT = ROOT / "site"
SITE_NAME = "Jae Chung"
SITE_URL = "https://jaechung.net"
# Footer links — edit these
LINKS = [("X", "https://x.com/_jaechung"), ("GitHub", "https://github.com/jchung00")]

def read_front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    meta = {}
    if not m:
        return meta, text
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, m.group(2)

def md(text):
    return markdown.markdown(text, extensions=["smarty", "fenced_code", "tables"])

def page(title, body, active, description="", path="/"):
    t = SITE_NAME if title == SITE_NAME else f"{title} — {SITE_NAME}"
    current = ' aria-current="page"'
    nav = "".join(
        f'<a href="{href}"{current if key == active else ""}>{label}</a>'
        for key, href, label in [("about", "/", "About"), ("writings", "/writings/", "Writings"),
                                 ("projects", "/projects/", "Projects")]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(t)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:title" content="{html.escape(t)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:type" content="website">
<link rel="stylesheet" href="/style.css">
</head>
<body>
<header>
  <a class="name" href="/">Jae Chung</a>
  <nav>{nav}</nav>
</header>
<main>
{body}
</main>
<footer>
{"".join(f'<a href="{h}">{l}</a>' for l, h in LINKS)}
</footer>
</body>
</html>
"""

def read_projects(path):
    """projects.md: one block per project, blank-line separated, `key: value` lines."""
    if not path.exists():
        return []
    projects = []
    for block in re.split(r"\n\s*\n", path.read_text().strip()):
        entry = {}
        for line in block.splitlines():
            if ":" in line and not line.lstrip().startswith("#"):
                k, v = line.split(":", 1)
                entry[k.strip()] = v.strip()
        if entry.get("title") and entry.get("url"):
            projects.append(entry)
    return projects

def fmt_date(s):
    y, m, d = (int(x) for x in s.split("-"))
    return date(y, m, d).strftime("%B %-d, %Y"), date(y, m, d)

def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copy(ROOT / "static" / "style.css", OUT / "style.css")
    for extra in (ROOT / "static").glob("*"):
        if extra.name != "style.css":
            shutil.copy(extra, OUT / extra.name)
    if (ROOT / "images").exists():
        shutil.copytree(ROOT / "images", OUT / "images")

    # About / landing
    meta, body = read_front_matter((ROOT / "about.md").read_text())
    (OUT / "index.html").write_text(page(
        SITE_NAME, f'<article class="about">{md(body)}</article>', "about",
        meta.get("description", ""), "/"))

    # Posts
    posts = []
    for f in sorted((ROOT / "posts").glob("*.md")):
        meta, body = read_front_matter(f.read_text())
        slug = f.stem
        pretty, d = fmt_date(meta["date"])
        posts.append(dict(slug=slug, title=meta["title"], date=d, pretty=pretty,
                          summary=meta.get("summary", ""),
                          draft=meta.get("draft", "").lower() == "true"))
        out_dir = OUT / "writings" / slug
        out_dir.mkdir(parents=True)
        article = f"""<article class="post">
<header class="post-header">
  <h1>{html.escape(meta["title"])}</h1>
  <time datetime="{meta["date"]}">{pretty}</time>
</header>
{md(body)}
<p class="back"><a href="/writings/">← All writings</a></p>
</article>"""
        (out_dir / "index.html").write_text(page(
            meta["title"], article, "writings", meta.get("summary", ""), f"/writings/{slug}/"))

    # Writings index (newest first, drafts hidden)
    visible = sorted((p for p in posts if not p["draft"]), key=lambda p: p["date"], reverse=True)
    items = "\n".join(
        f"""<li>
  <a href="/writings/{p["slug"]}/">{html.escape(p["title"])}</a>
  <time datetime="{p["date"].isoformat()}">{p["date"].strftime("%Y.%m")}</time>
  {f'<p>{html.escape(p["summary"])}</p>' if p["summary"] else ""}
</li>""" for p in visible)
    (OUT / "writings" / "index.html").write_text(page(
        "Writings", f'<h1>Writings</h1>\n<ul class="writings">\n{items}\n</ul>', "writings",
        "Writing by Jae Chung", "/writings/"))

    # Projects
    projects = read_projects(ROOT / "projects.md")
    items = "\n".join(
        f"""<li>
  <a href="{html.escape(p["url"])}">{html.escape(p["title"])}</a>
  <span class="host">{html.escape(re.sub(r"^https?://", "", p["url"]).rstrip("/"))}</span>
  {f'<p>{html.escape(p["description"])}</p>' if p.get("description") else ""}
</li>""" for p in projects)
    (OUT / "projects").mkdir()
    (OUT / "projects" / "index.html").write_text(page(
        "Projects", f'<h1>Projects</h1>\n<ul class="writings projects">\n{items}\n</ul>', "projects",
        "Projects by Jae Chung", "/projects/"))
    print(f"built {len(posts)} posts ({len(posts) - len(visible)} drafts), "
          f"{len(projects)} projects -> {OUT}")

if __name__ == "__main__":
    build()
