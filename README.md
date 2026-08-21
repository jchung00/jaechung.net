# jaechung.net

Static site. No framework, no dependencies beyond Python + `markdown`.

    pip install markdown
    python3 build.py        # writes ./site
    python3 -m http.server -d site 8000   # preview at localhost:8000

## Editing

- `about.md` — landing page
- `posts/*.md` — one file per piece. Front matter:

      ---
      title: Title of the piece
      date: 2026-09-01
      summary: optional one-liner for the index
      draft: true         # optional: builds the page but hides it from /writings/
      ---

  The filename becomes the URL (`posts/inner-voices.md` → `/writings/inner-voices/`).
- `images/` — anything here is copied to `/images/`. Reference as `![caption](/images/foo.png)`.
- `static/style.css` — all styling.
- Footer links live at the top of `build.py` (`LINKS`).

## Deploying

Point Cloudflare Pages / Netlify / Vercel at this repo with:

- build command: `pip install markdown && python3 build.py`
- output directory: `site`

Then add `jaechung.net` as a custom domain. Or just upload the `site/` folder anywhere that serves static files.
