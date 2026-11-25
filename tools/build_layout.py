"""Full-color print layout (HTML -> PDF via Chromium). Usage: python3 tools/build_layout.py sample"""
import html, pathlib, sys, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import recipes as R

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAY = ROOT / "layout"
e = html.escape
BOOK = "The Complete Amish Dry Mix Pantry Cookbook"

CSS = (LAY / "fonts" / "fonts.css").read_text() + """
/* 8.5 x 11 in trim + 0.125 in bleed on top, bottom and outside edge (KDP) */
@page { size: 8.625in 11.25in; margin: 0; }
:root { --green:#2E4A3B; --sage:#7E9A7E; --sage-l:#E8EFE6; --cream:#FBF6EC; --butter:#F4E7C9; --terra:#B5582E; --ink:#2B2A27; --muted:#6F6A60; }
* { box-sizing:border-box; }
html,body { margin:0; }
body { font-family:'Source Sans 3', sans-serif; color:var(--ink); font-size:10.6pt; line-height:1.42; }
.page { width:8.625in; height:11.25in; position:relative; overflow:hidden; background:#fff; page-break-after:always; }
.page:last-child { page-break-after:auto; }
/* inner (gutter) margin 0.8in, outside 0.6in from trim */
.page.right .body { padding:0 calc(0.6in + 0.125in) 0 0.8in; }
.page.left  .body { padding:0 0.8in 0 calc(0.6in + 0.125in); }
.page.left { } .page.right { }
.photo { height:4.55in; background-size:cover; background-position:center; position:relative; }
.photo::after { content:''; position:absolute; left:0; right:0; bottom:0; height:0.5in; background:linear-gradient(to bottom, rgba(255,255,255,0), #fff); }
.body { position:relative; margin-top:0.04in; }
.kicker { font-size:7.6pt; letter-spacing:2.6px; text-transform:uppercase; color:var(--sage); font-weight:700; }
.badge { display:inline-block; font-size:7.4pt; letter-spacing:1.8px; text-transform:uppercase; font-weight:700; padding:3px 9px; border-radius:20px; margin-left:8px; vertical-align:1px; }
.badge.mix { background:var(--terra); color:#fff; }
.badge.uses { background:var(--sage-l); color:var(--green); letter-spacing:.4px; text-transform:none; font-size:8.4pt; font-weight:600; }
h1 { font-family:'Playfair Display', serif; font-weight:700; color:var(--green); font-size:27pt; line-height:1.08; margin:6px 0 6px; }
.intro { font-family:'Playfair Display', serif; font-style:italic; font-weight:500; color:var(--muted); font-size:11pt; line-height:1.4; margin:0 0 10px; }
.meta { display:flex; border-top:1px solid #E3DCCD; border-bottom:1px solid #E3DCCD; margin-bottom:14px; }
.meta div { flex:1; padding:6px 0; text-align:center; border-left:1px solid #E3DCCD; }
.meta div:first-child { border-left:0; }
.meta b { display:block; font-size:7pt; letter-spacing:2px; text-transform:uppercase; color:var(--sage); }
.meta span { font-size:10pt; font-weight:600; color:var(--green); }
.cols { display:grid; grid-template-columns: 2.55in 1fr; gap:0.28in; }
.ingr { background:var(--cream); border-radius:10px; padding:12px 14px 10px; align-self:start; }
h2 { font-family:'Playfair Display', serif; font-weight:700; color:var(--green); font-size:13pt; margin:0 0 6px; }
.ingr ul { list-style:none; padding:0; margin:0; }
.ingr li { padding:3px 0 3px 14px; position:relative; border-bottom:1px dotted #DDD3BF; font-size:9.9pt; line-height:1.3; }
.ingr li:last-child { border-bottom:0; }
.ingr li::before { content:''; position:absolute; left:0; top:9px; width:5px; height:5px; border-radius:50%; background:var(--terra); }
.ingr .grp { font-weight:700; font-size:8pt; letter-spacing:1.4px; text-transform:uppercase; color:var(--terra); margin:8px 0 1px; }
.ingr .grp:first-child { margin-top:0; }
ol.steps { list-style:none; padding:0; margin:0; counter-reset:s; }
ol.steps li { counter-increment:s; position:relative; padding-left:30px; margin-bottom:8px; }
ol.steps li::before { content:counter(s); position:absolute; left:0; top:0; width:20px; height:20px; border-radius:50%; background:var(--green); color:#fff; font-weight:700; font-size:9pt; text-align:center; line-height:20px; }
.box { border-radius:10px; padding:10px 14px; margin-top:12px; font-size:10pt; }
.box.use { background:var(--sage-l); font-size:9.6pt; }
.box.use h3, .box.tip h3 { font-family:'Playfair Display', serif; font-size:11pt; color:var(--green); margin:0 0 3px; }
.box.use p { margin:0 0 4px; } .box.use p:last-child { margin:0; }
.keeps { display:flex; gap:8px; align-items:center; margin-top:10px; font-size:9.6pt; }
.keeps b { background:var(--butter); color:var(--terra); font-size:7.4pt; letter-spacing:1.6px; text-transform:uppercase; padding:3px 8px; border-radius:4px; white-space:nowrap; }
.box.tip { border:1.5px dashed var(--sage); }
.folio { position:absolute; bottom:0.45in; font-size:7.8pt; color:var(--muted); letter-spacing:1.2px; }
.page.right .folio { right:calc(0.6in + 0.125in); text-align:right; }
.page.left .folio { left:calc(0.6in + 0.125in); }
.folio .n { font-family:'Playfair Display', serif; font-weight:700; font-size:11pt; color:var(--green); letter-spacing:0; }
.page.right .folio .n { margin-left:8px; } .page.left .folio .n { margin-right:8px; }
"""

def recipe_page(r, ch_no, ch_title, page_no, side, is_mix):
    meta = "".join(f"<div><b>{e(k)}</b><span>{e(v)}</span></div>" for k, v in r["meta"])
    ingr = "".join(f'<div class="grp">{e(v)}</div>' if t == "group" else f"<li>{e(v)}</li>" for t, v in r["ingr"])
    ingr = ingr.replace("</div><li>", "</div><ul><li>")  # crude list grouping
    ingr_html = "<ul>" + ingr + "</ul>" if not r["ingr"] or r["ingr"][0][0] == "item" else ingr
    # rebuild cleanly: wrap consecutive items into <ul>
    parts, cur = [], []
    for t, v in r["ingr"]:
        if t == "group":
            if cur: parts.append("<ul>" + "".join(cur) + "</ul>"); cur = []
            parts.append(f'<div class="grp">{e(v)}</div>')
        else: cur.append(f"<li>{e(v)}</li>")
    if cur: parts.append("<ul>" + "".join(cur) + "</ul>")
    steps = "".join(f"<li>{e(s)}</li>" for s in r["steps"])
    extra = ""
    for s in r["extra"]:
        extra += f'<div class="box use"><h3>{e(s["title"])}</h3>' + "".join(f"<p>{e(p)}</p>" for p in s["paras"]) + "</div>"
    keeps = f'<div class="keeps"><b>Keeps</b><span>{e(r["keeps"])}</span></div>' if r["keeps"] else ""
    tip = f'<div class="box tip"><h3>Pantry Tip</h3>{e(r["tip"])}</div>' if r["tip"] else ""
    badge = '<span class="badge mix">Pantry Mix</span>' if is_mix else (
        f'<span class="badge uses">Made with: {e(", ".join(r["uses"]))}</span>' if r["uses"] else "")
    folio = (f'{e(BOOK.upper())}<span class="n">{page_no}</span>' if side == "right"
             else f'<span class="n">{page_no}</span>{e(("Chapter %d · %s" % (ch_no, ch_title)).upper())}')
    img = f"images/{r['slug']}.jpg"
    return f"""<section class="page {side}">
<div class="photo" style="background-image:url('{img}')"></div>
<div class="body">
<div class="kicker">Chapter {ch_no} · {e(ch_title)}{badge}</div>
<h1>{e(r['title'])}</h1>
<p class="intro">{e(r['intro'])}</p>
<div class="meta">{meta}</div>
<div class="cols">
<div><div class="ingr"><h2>Ingredients</h2>{''.join(parts)}</div>{extra}</div>
<div><h2>Directions</h2><ol class="steps">{steps}</ol>{keeps}{tip}</div>
</div></div>
<div class="folio">{folio}</div>
</section>"""

def build(selection, name):
    chs = R.chapters()
    pages = []
    for i, (ci, title) in enumerate(selection):
        ch = chs[ci - 1]
        r = next(x for x in ch["recipes"] if x["title"] == title)
        side = "left" if i % 2 == 0 else "right"
        pages.append(recipe_page(r, ci, ch["title"], 10 + i, side, bool(r["keeps"])))
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>{e(BOOK)}</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    out = LAY / f"{name}.html"
    out.write_text(doc)
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
await p.goto('file://{out}'); await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready);
await p.pdf({{ path: '{LAY / (name + '.pdf')}', preferCSSPageSize: true, printBackground: true }});
const ov = await p.evaluate(() => [...document.querySelectorAll('.page')].map(pg => {{ const b = pg.querySelector('.body'); return b.offsetTop + b.offsetHeight > pg.clientHeight - 0.75*96; }}));
console.log('overflow per page:', ov); await b.close(); }})();"""
    subprocess.run(["node", "-e", js], check=True)
    print("wrote", LAY / (name + ".pdf"))

if __name__ == "__main__":
    build([(1, "All-Purpose Amish Baking Mix"), (1, "Strawberry Shortcake Biscuits")], "Sample_Pages")
