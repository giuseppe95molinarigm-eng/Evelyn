"""Builds the complete full-color interior in Style A ("Modern Clean"), the style chosen by the client.
HTML is paginated in Chromium (flowing sections split across pages, recipes auto-fit to one page),
then printed to a KDP-ready PDF: 8.5 x 11 in trim + 0.125 in bleed."""
import html, json, pathlib, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "styles"))
import recipes as R
import style_a_modern as A

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAY = ROOT / "layout"
COMPACT = "--compact" in sys.argv
OUT_NAME = "The_Complete_Amish_Dry_Mix_Pantry_Cookbook_Interior" + ("_Compact" if COMPACT else "")
e = html.escape
TITLE = "The Complete Amish Dry Mix Pantry Cookbook"
SUBTITLE = ("150 Budget-Friendly Homemade Dry Mixes and Meals from Scratch, with Baking, Soup and Seasoning Blends, "
            "Mixes in a Jar for Gifting, and a Shelf-Life Chart")
AUTHOR = "[Author Name]"
WORDS = "One Two Three Four Five Six Seven Eight Nine Ten".split()

EXTRA_CSS = """
.page { background:#fff; }
.folio:empty { display:none; }
/* ---------- flowing text pages ---------- */
.flow .content { position:absolute; top:calc(0.85in + 0.125in); bottom:calc(0.95in + 0.125in); overflow:hidden; }
.page.right .content { left:0.8in; right:calc(0.6in + 0.125in); }
.page.left  .content { left:calc(0.6in + 0.125in); right:0.8in; }
.flow .content.cols2 { column-count:2; column-gap:0.32in; column-fill:auto; }
.sec-head { margin-bottom:16px; }
.sec-head .kicker { display:block; }
.sec-head h1 { font-size:30pt; margin:4px 0 0; }
.sec-head .rule { width:56px; height:3px; background:var(--terra); margin-top:10px; border-radius:2px; }
.content p { margin:0 0 9px; font-size:10.4pt; line-height:1.55; }
.content h3 { font-family:'Playfair Display', serif; color:var(--green); font-size:13.5pt; margin:14px 0 6px; break-after:avoid; }
.content ul.bl { list-style:none; padding:0; margin:0 0 8px; }
.content ul.bl li { position:relative; padding:0 0 0 16px; margin:0 0 5px; font-size:10.2pt; line-height:1.48; break-inside:avoid; }
.content ul.bl li::before { content:''; position:absolute; left:2px; top:7px; width:6px; height:6px; border-radius:50%; background:var(--terra); }
.content ul.bl li b { color:var(--green); }
table.t { width:100%; border-collapse:separate; border-spacing:0; font-size:9.3pt; margin:0 0 14px; break-inside:avoid; border-radius:8px; overflow:hidden; border:1px solid #E6DFD0; }
table.t th { background:var(--green); color:#fff; text-align:left; font-weight:600; font-size:8pt; letter-spacing:1.4px; text-transform:uppercase; padding:6px 9px; }
table.t td { padding:5px 9px; border-top:1px solid #EEE7D8; vertical-align:top; line-height:1.35; }
table.t tr:nth-child(even) td { background:var(--cream); }
table.t td:first-child { font-weight:600; color:var(--green); }
.cap { font-family:'Playfair Display', serif; color:var(--green); font-size:12.5pt; margin:4px 0 6px; break-after:avoid; }
.note-p { background:var(--sage-l); border-radius:8px; padding:9px 12px; font-size:9.6pt !important; }
.idx { break-inside:avoid; margin:0 0 9px; font-size:9.6pt; line-height:1.4; }
.idx b { display:block; font-family:'Playfair Display', serif; color:var(--green); font-size:11.5pt; }
.ri { font-size:9.4pt; line-height:1.3; padding:2.5px 0; border-bottom:1px dotted #DDD3BF; display:flex; justify-content:space-between; gap:8px; break-inside:avoid; }
.ri span:last-child { color:var(--terra); font-weight:600; white-space:nowrap; }
.ri.letter { border:0; font-family:'Playfair Display', serif; font-weight:700; color:var(--terra); font-size:13pt; padding-top:7px; }
.shop { break-inside:avoid; margin-bottom:10px; }
/* ---------- title, copyright, contents ---------- */
.titlepage { display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; }
.titlepage .inner { width:5.6in; }
.titlepage .orn { color:var(--terra); font-size:10pt; letter-spacing:8px; margin:0 0 22px; }
.titlepage h1 { font-family:'Playfair Display', serif; font-size:40pt; line-height:1.08; color:var(--green); margin:0 0 18px; }
.titlepage .sub { font-family:'Playfair Display', serif; font-style:italic; font-weight:500; font-size:13pt; color:var(--muted); line-height:1.45; margin:0 0 40px; }
.titlepage .auth { font-size:10pt; letter-spacing:4px; text-transform:uppercase; color:var(--sage); font-weight:700; }
.copyright .content { top:auto !important; bottom:calc(1.1in + 0.125in) !important; font-size:8.6pt; color:var(--muted); }
.copyright .content p { font-size:8.6pt; line-height:1.5; }
.toc-row { display:flex; align-items:baseline; gap:8px; padding:3.4px 0; border-bottom:1px solid #EEE7D8; font-size:10.4pt; }
.toc-row .ttl { flex:1; }
.toc-row.ch .ttl { font-family:'Playfair Display', serif; font-weight:700; color:var(--green); font-size:11.5pt; }
.toc-row .ttl small { display:block; font-family:'Source Sans 3'; font-weight:400; font-size:8pt; letter-spacing:1.8px; text-transform:uppercase; color:var(--sage); }
.toc-row .pg { font-weight:700; color:var(--terra); }
/* ---------- chapter openers ---------- */
.opener .hero { position:absolute; top:0; left:0; right:0; height:calc(6.4in + 0.125in); background-size:cover; background-position:center; }
.opener .hero::after { content:''; position:absolute; left:0; right:0; bottom:0; height:0.9in; background:linear-gradient(to bottom, rgba(255,255,255,0), #fff); }
.opener .ob { position:absolute; top:calc(6.25in + 0.125in); }
.page.right .ob { left:0.8in; right:calc(0.6in + 0.125in); }
.page.left .ob { left:calc(0.6in + 0.125in); right:0.8in; }
.opener .num { font-family:'Playfair Display', serif; font-weight:700; font-size:13pt; color:var(--terra); letter-spacing:3px; text-transform:uppercase; }
.opener h1 { font-size:36pt; margin:4px 0 12px; }
.opener .lead { font-family:'Playfair Display', serif; font-style:italic; font-weight:500; font-size:12.5pt; line-height:1.5; color:var(--muted); margin:0 0 18px; }
.opener .mixes { border-top:1px solid #E3DCCD; padding-top:12px; }
.opener .mixes .kicker { margin-bottom:8px; display:block; }
.opener .chips span { display:inline-block; background:var(--cream); border:1px solid #EFE4CC; color:var(--green); font-weight:600; font-size:9.4pt; padding:4px 11px; border-radius:20px; margin:0 6px 7px 0; }
.blank { }
/* ---------- compact edition: two recipes per page ---------- */
.duo .slot { position:absolute; height:4.62in; overflow:hidden; }
.duo .slot.s1 { top:calc(0.6in + 0.125in); }
.duo .slot.s2 { top:calc(0.6in + 0.125in + 4.62in + 0.22in); }
.duo .mid { position:absolute; top:calc(0.6in + 0.125in + 4.62in + 0.11in); height:1px; background:#E3DCCD; }
.page.right .slot, .page.right .mid { left:0.8in; right:calc(0.6in + 0.125in); }
.page.left .slot, .page.left .mid { left:calc(0.6in + 0.125in); right:0.8in; }
.half .top { display:grid; grid-template-columns:2.55in 1fr; column-gap:.24in; margin-bottom:9px; align-items:start; }
.half .ph { height:1.92in; border-radius:10px; background-size:cover; background-position:center; }
.half .kicker { font-size:6.6pt; letter-spacing:1.8px; }
.half .badge { display:table; margin:4px 0 0; }
.half h1 { font-size:18.5pt; margin:5px 0 4px; line-height:1.1; }
.half .intro { font-size:9.2pt; line-height:1.35; margin:0 0 7px; }
.half .meta { margin:0; } .half .meta div { padding:3px 0; } .half .meta span { font-size:8.8pt; } .half .meta b { font-size:6.2pt; }
.half .cols { grid-template-columns:2.4in 1fr; gap:.22in; font-size:9.1pt; line-height:1.38; }
.half .ingr { padding:8px 11px 6px; } .half .ingr li { font-size:8.7pt; padding:2px 0 2px 13px; }
.half .ingr li::before { top:7px; } .half h2 { font-size:11pt; margin-bottom:4px; }
.half ol.steps li { margin-bottom:5px; padding-left:26px; } .half ol.steps li::before { width:17px; height:17px; line-height:17px; font-size:8pt; }
.half .box { margin-top:8px; padding:7px 11px; font-size:8.7pt; } .half .keeps { margin-top:7px; font-size:8.7pt; }
.duo .ohalf .banner { position:absolute; top:0; left:0; right:0; height:calc(2.75in + 0.125in); background-size:cover; background-position:center; }
.duo .ohalf .banner::after { content:''; position:absolute; left:0; right:0; bottom:0; height:.5in; background:linear-gradient(to bottom, rgba(255,255,255,0), #fff); }
.duo .ohalf .otext { position:absolute; top:calc(2.72in + 0.125in); }
.page.right .ohalf .otext { left:0.8in; right:calc(0.6in + 0.125in); } .page.left .ohalf .otext { left:calc(0.6in + 0.125in); right:0.8in; }
.ohalf .num { font-family:'Playfair Display', serif; font-weight:700; font-size:10.5pt; color:var(--terra); letter-spacing:3px; text-transform:uppercase; }
.ohalf h1 { font-size:25pt; margin:2px 0 6px; line-height:1.1; }
.ohalf .lead { font-family:'Playfair Display', serif; font-style:italic; font-weight:500; font-size:10.4pt; line-height:1.45; color:var(--muted); margin:0 0 8px; }
.ohalf .chips span { display:inline-block; background:var(--cream); border:1px solid #EFE4CC; color:var(--green); font-weight:600; font-size:8.2pt; padding:2px 9px; border-radius:20px; margin:0 5px 5px 0; }
.duo.withopener .slot.s1 { display:none; }
.duo.withopener .slot.s2 { top:calc(5.45in + 0.125in); height:4.73in; }
.duo.withopener .mid { top:calc(5.3in + 0.125in); }
#pool { display:none; }
"""

# ---------------- page builders ----------------
def recipe_page(r, ci, ch_title):
    html_ = A.recipe_page(r, ci, ch_title, 0, "right", bool(r["keeps"]))
    html_ = html_.replace('<section class="page right">', f'<section class="page recipe" data-ch="{ci}" data-chtitle="{e(ch_title)}">')
    return html_.split('<div class="folio">')[0] + '<div class="folio"></div>\n</section>'

def half_recipe(r, ci, ch_title):
    """Compact half-page version of a recipe (smaller photo beside the title)."""
    full = A.recipe_page(r, ci, ch_title, 0, "right", bool(r["keeps"]))
    body = full.split('<div class="body">', 1)[1].rsplit('<div class="folio">', 1)[0]
    body = body.rsplit("</div>", 1)[0]            # drop closing tag of .body
    head, rest = body.split('<div class="meta">', 1)
    meta, cols = rest.split("</div>\n<div class=\"cols\">", 1)
    return (f'<div class="half" data-slug="{r["slug"]}"><div class="top"><div class="ph" style="background-image:url(\'images/{r["slug"]}.jpg\')"></div>'
            f'<div class="hd">{head}<div class="meta">{meta}</div></div></div><div class="cols">{cols}</div>')

def half_opener(ci, ch):
    mixes = [r["title"] for r in ch["recipes"] if r["keeps"]]
    lead = ch["blocks"][0][1] if ch["blocks"] else ""
    chips = "".join(f"<span>{e(m)}</span>" for m in mixes)
    return (f'<div class="ohalf" data-ch="{ci}" data-chtitle="{e(ch["title"])}" data-toc="Chapter {ci}: {e(ch["title"])}">'
            f'<div class="banner" style="background-image:url(\'images/chapter-{ci:02d}.jpg\')"></div>'
            f'<div class="otext"><div class="num">Chapter {WORDS[ci-1]}</div><h1>{e(ch["title"])}</h1><p class="lead">{e(lead)}</p>'
            + (f'<div class="chips">{chips}</div>' if mixes else '') + '</div></div>')

def blocks_html(blocks):
    out, ul = [], []
    def flush():
        if ul: out.append('<ul class="bl">' + "".join(ul) + "</ul>"); ul.clear()
    for kind, v in blocks:
        if kind == "li":
            ul.append(f"<li>{bold_lead(v)}</li>"); continue
        flush()
        if kind == "p": out.append(f"<p>{e(v)}</p>")
        elif kind == "h3": out.append(f"<h3>{e(v)}</h3>")
        elif kind == "table": out.append(table(v))
    flush()
    return out

def bold_lead(v):
    # "Save money. A homemade..." -> bold lead-in up to the first period/colon when short
    for sep in (". ", ": "):
        if sep in v and len(v.split(sep)[0]) < 40 and v.split(sep)[0][0].isupper():
            a, b = v.split(sep, 1); return f"<b>{e(a)}{sep.strip()}</b> {e(b)}"
    return e(v)

def table(rows):
    head = "".join(f"<th>{e(c)}</th>" for c in rows[0])
    body = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
    return f'<table class="t"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'

def flow(title, kicker, blocks, cols2=False, toc=True):
    """A flowing section: blocks are distributed over as many pages as needed by the browser."""
    data = json.dumps(blocks)
    return (f'<template class="flowsec" data-title="{e(title)}" data-kicker="{e(kicker)}" data-cols="{int(cols2)}" data-toc="{int(toc)}">'
            f'{e(data)}</template>')

def opener(ci, ch):
    mixes = [r["title"] for r in ch["recipes"] if r["keeps"]]
    chips = "".join(f"<span>{e(m)}</span>" for m in mixes)
    lead = ch["blocks"][0][1] if ch["blocks"] else ""
    label = "In this chapter" if mixes else "Gifts in this chapter"
    if not mixes:
        chips = "".join(f"<span>{e(r['title'].replace(' in a Jar', ''))}</span>" for r in ch["recipes"][:8]) + "<span>and more</span>"
    return f"""<section class="page opener" data-toc="Chapter {ci}: {e(ch['title'])}" data-ch="{ci}" data-chtitle="{e(ch['title'])}">
<div class="hero" style="background-image:url('images/chapter-{ci:02d}.jpg')"></div>
<div class="ob"><div class="num">Chapter {WORDS[ci-1]}</div><h1>{e(ch['title'])}</h1><p class="lead">{e(lead)}</p>
<div class="mixes"><span class="kicker">{'The pantry mixes' if mixes else label}</span><div class="chips">{chips}</div></div></div>
<div class="folio"></div></section>"""

def build():
    chs = R.chapters(); front = R.front(); back = {c["title"]: c for c in R.back()}
    all_r = [(ci, ch, r) for ci, ch in enumerate(chs, 1) for r in ch["recipes"]]
    pages = []
    # Title page, copyright, contents
    pages.append(f"""<section class="page titlepage" data-nofolio="1"><div class="inner"><div class="orn">✦ ✦ ✦</div>
<h1>{e(TITLE)}</h1><p class="sub">{e(SUBTITLE)}</p><div class="auth">{e(AUTHOR)}</div></div></section>""")
    cp = [f"Copyright © 2026 {AUTHOR}. All rights reserved.",
          "No part of this book may be reproduced, stored in a retrieval system or transmitted in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without the prior written permission of the author, except for brief quotations in reviews.",
          "Disclaimer: The recipes and information in this book are provided for general home-cooking use. Storage times are guidelines for best quality and depend on your ingredients, containers and storage conditions. Always check mixes before use and discard any that smell stale or show signs of moisture or spoilage. Readers with food allergies or dietary restrictions should check every ingredient label. The author and publisher are not responsible for any adverse effects resulting from the use of the information in this book.",
          "This book is inspired by the traditional, frugal cooking of Amish communities. It is not affiliated with or endorsed by any Amish community or organization."]
    pages.append('<section class="page flow copyright" data-nofolio="1"><div class="content">' + "".join(f"<p>{e(p)}</p>" for p in cp) + "</div></section>")
    pages.append('<section class="page flow tocpage" data-nofolio="1"><div class="content"><div class="sec-head"><span class="kicker">Inside this book</span><h1>Contents</h1><div class="rule"></div></div><div id="toc"></div></div></section>')
    # Front matter
    for c in front:
        pages.append(flow(c["title"], "Getting started", blocks_html(c["blocks"])))
    # Chapters
    if COMPACT:
        pool = []
        for ci, ch in enumerate(chs, 1):
            pool.append(f'<div class="item" data-kind="opener" data-ch="{ci}">{opener(ci, ch)}{half_opener(ci, ch)}</div>')
            for r in ch["recipes"]:
                pool.append(f'<div class="item" data-kind="recipe" data-ch="{ci}">{recipe_page(r, ci, ch["title"])}{half_recipe(r, ci, ch["title"])}</div>')
        pages.append('<div id="pool">' + "".join(pool) + "</div>")
    else:
        for ci, ch in enumerate(chs, 1):
            pages.append(opener(ci, ch))
            for r in ch["recipes"]:
                pages.append(recipe_page(r, ci, ch["title"]))
    # Back matter: shelf-life chart
    b = ['<p>Use this chart to check how long each mix keeps. Times are for best quality when the mix is stored in an airtight container in a cool, dry, dark place. Mixes that contain fat, whole grains or dairy powders keep longer when refrigerated or frozen.</p>']
    for ci, ch in enumerate(chs, 1):
        mixes = [r for r in ch["recipes"] if r["keeps"]]
        if mixes:
            b.append(f'<div style="break-inside:avoid"><div class="cap">Chapter {ci}: {e(ch["title"])}</div>' + table([["Mix", "Keeps"]] + [[m["title"], m["keeps"]] for m in mixes]) + "</div>")
    pages.append(flow("Master Shelf-Life Chart", "Bonus", b))
    # One mix, many meals index
    b = ["<p>Find every recipe you can make from the mixes already on your shelf.</p>"]
    for ci, ch, r in all_r:
        if not r["keeps"]: continue
        made = [x["title"] for _, _, x in all_r if r["title"] in x["uses"]]
        if made: b.append(f'<div class="idx"><b>{e(r["title"])}</b>{" · ".join(e(m) for m in made)}</div>')
    pages.append(flow("One Mix, Many Meals Index", "Bonus", b, cols2=True))
    # Meal plan: keep each week's table together
    mp = back["4-Week Pantry Meal Plan"]["blocks"]
    b = []
    for kind, v in mp:
        if kind == "p" and v.startswith("This plan"): b.append(f"<p>{e(v)}</p>")
        elif kind == "table": b.append(f'<div style="break-inside:avoid">{table(v)}')
        elif kind == "p": b[-1] += f'<p class="note-p">{e(v)}</p></div>'
    pages.append(flow("4-Week Pantry Meal Plan", "Bonus", b))
    # Shopping list in two columns, one group per block
    sl = back["Pantry Shopping List"]["blocks"]; b = []; cur = None
    for kind, v in sl:
        if kind == "p": b.append(f"<p>{e(v)}</p>")
        elif kind == "h3": cur = f'<div class="shop"><h3>{e(v)}</h3><ul class="bl">'; b.append(cur)
        elif kind == "li": b[-1] += f"<li>{e(v)}</li>"
    b = [x + "</ul></div>" if x.startswith('<div class="shop">') else x for x in b]
    pages.append(flow("Pantry Shopping List", "Bonus", b, cols2=True))
    # Conversions
    cv = back["Kitchen Conversion Chart"]["blocks"]; b = []
    for kind, v in cv:
        if kind == "h3": b.append(f'<div style="break-inside:avoid"><div class="cap">{e(v)}</div>')
        elif kind == "table": b[-1] += table(v) + "</div>"
    pages.append(flow("Kitchen Conversion Chart", "Bonus", b))
    # Recipe index (page numbers filled in by the paginator)
    items = sorted(((r["title"], r["slug"]) for _, _, r in all_r), key=lambda x: x[0].lower())
    b, letter = [], ""
    for t_, s_ in items:
        if t_[0].upper() != letter:
            letter = t_[0].upper()
            b.append(f'<div style="break-inside:avoid"><div class="ri letter">{letter}</div><div class="ri"><span>{e(t_)}</span><span data-ref="{s_}"></span></div></div>')
            continue
        b.append(f'<div class="ri"><span>{e(t_)}</span><span data-ref="{s_}"></span></div>')
    pages.append(flow("Recipe Index", "Index", b, cols2=True))

    css = A.CSS + EXTRA_CSS
    js = (LAY / "paginate.js").read_text()
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>{e(TITLE)}</title><style>{css}</style></head><body>{''.join(pages)}<script>{js}</script></body></html>"
    out = LAY / f"{OUT_NAME}.html"
    out.write_text(doc)
    run = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
p.on('console', m => console.log('[page]', m.text()));
await p.goto('file://{out}', {{ waitUntil: 'networkidle', timeout: 0 }});
await p.waitForFunction(() => window.__paginated === true, null, {{ timeout: 0 }});
const report = await p.evaluate(() => window.__report);
console.log(JSON.stringify(report));
await p.pdf({{ path: '{LAY / (OUT_NAME + '.pdf')}', preferCSSPageSize: true, printBackground: true, timeout: 0 }});
await b.close(); }})();"""
    subprocess.run(["node", "-e", run], check=True)
    print("wrote", LAY / (OUT_NAME + ".pdf"))

if __name__ == "__main__":
    build()
