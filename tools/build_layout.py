"""Full-color print layout (HTML -> PDF via Chromium).
Trim 8.5 x 11 in, 0.125 in bleed on top, bottom and outside edge (KDP)."""
import html, pathlib, re, sys, subprocess
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import recipes as R

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAY = ROOT / "layout"
BOOK = "The Complete Amish Dry Mix Pantry Cookbook"
WORDS = "One Two Three Four Five Six Seven Eight Nine Ten".split()

# ---------- typography helpers ----------
FR = {"1/2": "½", "1/3": "⅓", "2/3": "⅔", "1/4": "¼", "3/4": "¾", "1/8": "⅛"}
def frac(s):
    s = re.sub(r"(\d) (\d/\d)\b", lambda m: m.group(1) + FR.get(m.group(2), " " + m.group(2)), s)
    return re.sub(r"\b(\d/\d)\b", lambda m: FR.get(m.group(1), m.group(1)), s)
def t(s):  # escape + typographic polish
    s = html.escape(frac(s))
    s = re.sub(r"(\d) to (\d)", "\\1–\\2", s)          # 8 to 10 -> 8–10
    s = s.replace(" x ", "\u202f×\u202f")               # 9 x 13 -> 9 × 13
    s = re.sub(r"(\d)°F", "\\1\u202f°F", s)
    return s

UNITS = r"(?:cups?|tablespoons?|teaspoons?|pounds?|ounces?|quarts?|pints?|gallons?|slices?|cloves?|sticks?|cans?|jars?|bags?|batch(?:es)?|sleeves?|heads?|box(?:es)?|stalks?|large|medium|small)"
QTY = re.compile(r"^((?:\d+(?: \d/\d)?|\d/\d)(?: to \d+(?: \d/\d)?)?(?: \([^)]*\))?(?: " + UNITS + r")?(?: " + UNITS + r")?)\s+(.*)$")
def split_qty(item):
    m = QTY.match(item)
    if not m: return ("", item)
    q = m.group(1)
    for a, b in (("tablespoons", "tbsp"), ("tablespoon", "tbsp"), ("teaspoons", "tsp"), ("teaspoon", "tsp"), ("pounds", "lb"), ("pound", "lb"), ("ounces", "oz"), ("ounce", "oz")):
        q = re.sub(r"\b" + a + r"\b", b, q)
    return (q, m.group(2))

CSS = (LAY / "fonts" / "fonts.css").read_text() + """
@page { size: 8.625in 11.25in; margin: 0; }
:root { --ink:#22302A; --green:#33503F; --gold:#A6763A; --muted:#6F6A61; --rule:#CFC5B1; --cream:#F8F2E6; --panel:#FFFDF8; }
* { box-sizing:border-box; }
html,body { margin:0; }
body { font-family:'Jost', sans-serif; font-weight:400; color:var(--ink); font-size:9.7pt; line-height:1.5;
       font-kerning:normal; font-variant-numeric:lining-nums; text-rendering:geometricPrecision; hyphens:manual; }
.page { width:8.625in; height:11.25in; position:relative; overflow:hidden; background:#fff; page-break-after:always; }
.page:last-child { page-break-after:auto; }
.page.mix { background:var(--cream); }
/* margins from trim: inside (gutter) 0.85in, outside 0.65in; bleed 0.125in added on the outside edge */
.page.right .body, .page.right .folio { left:0.85in; right:calc(0.65in + 0.125in); }
.page.left  .body, .page.left  .folio { left:calc(0.65in + 0.125in); right:0.85in; }
.photo { position:absolute; top:0; left:0; right:0; height:calc(4.2in + 0.125in); background-size:cover; background-position:center 55%; }
.body { position:absolute; top:calc(4.2in + 0.125in + 0.32in); bottom:calc(0.95in + 0.125in); }

.kicker { font-weight:500; font-size:6.9pt; letter-spacing:.3em; text-transform:uppercase; color:var(--gold); display:flex; align-items:center; gap:10px; }
.kicker i { display:inline-block; width:5px; height:5px; background:var(--gold); transform:rotate(45deg); }
h1 { font-family:'Cormorant Garamond', serif; font-weight:600; font-size:35pt; line-height:1; letter-spacing:-.2px; color:var(--ink); margin:9px 0 7px; }
.intro { font-family:'Cormorant Garamond', serif; font-style:italic; font-weight:500; font-size:13.2pt; line-height:1.32; color:var(--muted); margin:0 0 13px; max-width:5.6in; }

.meta { display:flex; border-top:.6pt solid var(--rule); border-bottom:.6pt solid var(--rule); padding:6px 0 7px; margin-bottom:16px; }
.meta div { padding:0 18px; border-left:.6pt solid var(--rule); display:flex; align-items:baseline; gap:8px; }
.meta div:first-child { padding-left:0; border-left:0; }
.meta b { font-weight:500; font-size:6.6pt; letter-spacing:.26em; text-transform:uppercase; color:var(--gold); }
.meta span { font-family:'Cormorant Garamond', serif; font-weight:600; font-size:12.5pt; color:var(--ink); }

.grid { display:grid; grid-template-columns:2.42in 1fr; column-gap:.32in; }
.grid > .col2 { border-left:.6pt solid var(--rule); padding-left:.32in; }
h2 { font-weight:500; font-size:7.2pt; letter-spacing:.3em; text-transform:uppercase; color:var(--ink); margin:0 0 9px; }
h2::after { content:''; display:block; width:22px; height:1.2pt; background:var(--gold); margin-top:5px; }

.ing { margin:0; padding:0; list-style:none; }
.ing li { display:grid; grid-template-columns:.74in 1fr; column-gap:6px; padding:3.2px 0; border-bottom:.5pt solid #E4DCCB; font-size:9.2pt; line-height:1.32; }
.mix .ing li { border-bottom-color:#E2D8C2; }
.ing li:last-child { border-bottom:0; }
.ing .q { font-weight:500; color:var(--gold); }
.ing li.noq { grid-template-columns:1fr; }
.grp { font-family:'Cormorant Garamond', serif; font-style:italic; font-weight:600; font-size:11.5pt; color:var(--green); margin:9px 0 1px; }
.grp:first-of-type { margin-top:0; }

ol.steps { list-style:none; margin:0; padding:0; }
ol.steps li { display:grid; grid-template-columns:.34in 1fr; margin-bottom:8px; }
ol.steps li span { font-family:'Cormorant Garamond', serif; font-style:italic; font-weight:600; font-size:19pt; line-height:.9; color:var(--gold); }

.use { margin-top:16px; background:var(--panel); border-top:1.6pt solid var(--green); padding:10px 12px 9px; font-size:8.9pt; line-height:1.45; }
.use h3, .note h3 { font-family:'Cormorant Garamond', serif; font-weight:600; font-size:13pt; color:var(--green); margin:0 0 3px; }
.use p { margin:0 0 4px; } .use p:last-child { margin:0; }
.keeps { margin-top:12px; padding-top:8px; border-top:.6pt solid var(--rule); font-size:8.9pt; line-height:1.45; }
.keeps b { font-weight:500; font-size:6.6pt; letter-spacing:.26em; text-transform:uppercase; color:var(--gold); margin-right:8px; }
.note { margin-top:12px; padding-left:12px; border-left:1.2pt solid var(--gold); font-size:8.9pt; line-height:1.45; color:#3C4740; }
.note h3 { font-style:italic; font-size:12pt; }

.folio { position:absolute; bottom:calc(0.45in + 0.125in); display:flex; align-items:center; gap:10px; font-size:6.4pt; letter-spacing:.28em; text-transform:uppercase; color:var(--muted); }
.page.right .folio { justify-content:flex-end; }
.folio .n { font-family:'Cormorant Garamond', serif; font-weight:600; font-size:12.5pt; letter-spacing:0; color:var(--ink); }
.folio .r { width:.3in; height:.6pt; background:var(--gold); }
"""

def recipe_page(r, ch_no, ch_title, page_no, side):
    is_mix = bool(r["keeps"])
    meta = "".join(f"<div><b>{t(k)}</b><span>{t(v)}</span></div>" for k, v in r["meta"])
    parts, cur = [], []
    def flush():
        if cur: parts.append('<ul class="ing">' + "".join(cur) + "</ul>"); cur.clear()
    for kind, v in r["ingr"]:
        if kind == "group":
            flush(); parts.append(f'<div class="grp">{t(v)}</div>')
        else:
            q, rest = split_qty(v)
            cur.append(f'<li><span class="q">{t(q)}</span><span>{t(rest)}</span></li>' if q else f'<li class="noq"><span>{t(rest)}</span></li>')
    flush()
    steps = "".join(f"<li><span>{i}</span><div>{t(s)}</div></li>" for i, s in enumerate(r["steps"], 1))
    use = "".join(f'<div class="use"><h3>{t(s["title"])}</h3>' + "".join(f"<p>{t(p)}</p>" for p in s["paras"]) + "</div>" for s in r["extra"])
    keeps = f'<div class="keeps"><b>Keeps</b>{t(r["keeps"])}</div>' if r["keeps"] else ""
    note = f'<div class="note"><h3>Pantry note</h3>{t(r["tip"])}</div>' if r["tip"] else ""
    chap = f"Chapter {WORDS[ch_no - 1]}"
    kicker = (f"<span>Pantry Mix</span><i></i><span>{chap}</span>" if is_mix
              else f"<span>{chap}</span><i></i><span>Made with {t(', '.join(r['uses']))}</span>" if r["uses"] else f"<span>{chap}</span>")
    folio = (f'<span>{t(BOOK)}</span><span class="r"></span><span class="n">{page_no}</span>' if side == "right"
             else f'<span class="n">{page_no}</span><span class="r"></span><span>{t(ch_title)}</span>')
    return f"""<section class="page {side}{' mix' if is_mix else ''}">
<div class="photo" style="background-image:url('images/{r['slug']}.jpg')"></div>
<div class="body">
<div class="kicker">{kicker}</div>
<h1>{t(r['title'])}</h1>
<p class="intro">{t(r['intro'])}</p>
<div class="meta">{meta}</div>
<div class="grid">
<div class="col1"><h2>Ingredients</h2>{''.join(parts)}{use}</div>
<div class="col2"><h2>{'Method' if is_mix else 'Directions'}</h2><ol class="steps">{steps}</ol>{keeps}{note}</div>
</div></div>
<div class="folio">{folio}</div>
</section>"""

def render(name, pages):
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(BOOK)}</title><style>{CSS}</style></head><body>{''.join(pages)}</body></html>"
    out = LAY / f"{name}.html"
    out.write_text(doc)
    js = f"""const {{ chromium }} = require('playwright');
(async () => {{ const b = await chromium.launch(); const p = await b.newPage();
await p.goto('file://{out}'); await p.waitForLoadState('networkidle'); await p.evaluate(() => document.fonts.ready);
await p.pdf({{ path: '{LAY / (name + '.pdf')}', preferCSSPageSize: true, printBackground: true }});
const ov = await p.evaluate(() => [...document.querySelectorAll('.body')].map(b => b.scrollHeight > b.clientHeight + 1));
console.log('overflow per page:', JSON.stringify(ov)); await b.close(); }})();"""
    subprocess.run(["node", "-e", js], check=True)
    print("wrote", LAY / (name + ".pdf"))

def build_sample():
    chs = R.chapters()
    sel = [(1, "All-Purpose Amish Baking Mix"), (1, "Strawberry Shortcake Biscuits")]
    pages = []
    for i, (ci, title) in enumerate(sel):
        ch = chs[ci - 1]
        r = next(x for x in ch["recipes"] if x["title"] == title)
        pages.append(recipe_page(r, ci, ch["title"], 10 + i, "left" if i % 2 == 0 else "right"))
    render("Sample_Pages", pages)

if __name__ == "__main__":
    build_sample()
