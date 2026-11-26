"""Style C, "Heritage Farmhouse": arched photo window, Amish-quilt palette, warm serif typography."""
import html, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import recipes as R
from build_layout import t, split_qty, render, WORDS, BOOK, LAY

CSS = (LAY / "fonts" / "fonts.css").read_text() + """
@page { size: 8.625in 11.25in; margin: 0; }
:root { --ink:#2A2622; --red:#8C3B2E; --indigo:#2F3E5C; --mustard:#C3923A; --muted:#756C62; --rule:#D8CDBB; --paper:#FCF9F3; --wash:#F3ECDF; }
* { box-sizing:border-box; }
html,body { margin:0; }
body { font-family:'Lora','Jost',serif; color:var(--ink); font-size:9.9pt; line-height:1.52; font-variant-numeric:lining-nums; }
.page { width:8.625in; height:11.25in; position:relative; overflow:hidden; background:var(--paper); page-break-after:always; }
.page:last-child { page-break-after:auto; }
.page { --acc:var(--red); } .page.mix { --acc:var(--indigo); }
/* quilt-stripe band on the outside edge (bleeds) */
.band { position:absolute; top:0; bottom:0; width:calc(0.16in + 0.125in); background:var(--acc); }
.band::after { content:''; position:absolute; top:0; bottom:0; width:1.2pt; background:var(--mustard); }
.page.left .band { left:0; } .page.right .band { right:0; }
.page.left .band::after { right:-4pt; } .page.right .band::after { left:-4pt; }
.page.right .area, .page.right .folio { left:.85in; right:calc(.7in + .125in); }
.page.left  .area, .page.left  .folio { left:calc(.7in + .125in); right:.85in; }
.area { position:absolute; top:calc(.6in + .125in); bottom:calc(.95in + .125in); display:grid; grid-template-columns:2.85in 1fr; column-gap:.34in; grid-template-rows:auto 1fr; }
.arch { width:2.85in; height:4.15in; border-radius:1.425in 1.425in 6px 6px; background-size:cover; background-position:center; box-shadow:0 0 0 1pt var(--paper), 0 0 0 2pt var(--acc); }
.head { display:flex; flex-direction:column; justify-content:flex-end; padding-bottom:4px; position:relative; }
.seal { position:absolute; top:0; right:0; width:.95in; height:.95in; border-radius:50%; border:1.2pt solid var(--acc); display:flex; align-items:center; justify-content:center; text-align:center;
  font-weight:700; font-size:6.4pt; letter-spacing:.22em; text-transform:uppercase; color:var(--acc); line-height:1.5; }
.seal::before { content:''; position:absolute; inset:3px; border-radius:50%; border:.6pt solid var(--acc); }
.seal b { display:block; font-family:'DM Serif Display',serif; font-weight:400; font-size:17pt; letter-spacing:0; line-height:1; }
.chap { font-weight:600; font-size:7pt; letter-spacing:.24em; text-transform:uppercase; color:var(--acc); }
h1 { font-family:'DM Serif Display',serif; font-weight:400; font-size:32pt; line-height:1.04; margin:8px 0 10px; color:var(--ink); }
.orn { display:flex; align-items:center; gap:8px; margin:0 0 10px; color:var(--mustard); }
.orn::before, .orn::after { content:''; height:.7pt; background:var(--mustard); flex:0 0 .45in; }
.orn span { font-size:8pt; }
.intro { font-style:italic; font-size:11pt; line-height:1.45; color:var(--muted); margin:0 0 12px; }
.facts { display:grid; grid-auto-flow:column; grid-auto-columns:1fr; border-top:.7pt solid var(--rule); border-bottom:.7pt solid var(--rule); }
.facts div { padding:6px 0 6px 10px; border-left:.7pt solid var(--rule); }
.facts div:first-child { border-left:0; padding-left:0; }
.facts b { display:block; font-weight:600; font-size:6.4pt; letter-spacing:.22em; text-transform:uppercase; color:var(--acc); }
.facts span { font-family:'DM Serif Display',serif; font-size:12pt; }
.made { margin-top:9px; font-size:8.6pt; color:var(--muted); font-style:italic; }
.made b { font-style:normal; font-weight:600; color:var(--acc); }

.side { grid-row:2; margin-top:.36in; }
.main { grid-row:2; margin-top:.36in; }
h2 { font-family:'DM Serif Display',serif; font-weight:400; font-size:15pt; color:var(--acc); margin:0 0 6px; display:flex; align-items:center; gap:10px; }
h2::after { content:''; flex:1; height:.7pt; background:var(--rule); }
.ingbox { background:var(--wash); padding:12px 14px 10px; border-radius:2px; }
.ing { list-style:none; margin:0; padding:0; }
.ing li { padding:3.2px 0; font-size:9.3pt; line-height:1.35; border-bottom:.5pt dashed #CDBFA8; }
.ing li:last-child { border-bottom:0; }
.ing .q { font-weight:700; color:var(--ink); margin-right:4px; }
.grp { font-weight:600; font-size:6.8pt; letter-spacing:.2em; text-transform:uppercase; color:var(--acc); margin:8px 0 1px; }
.grp:first-child { margin-top:0; }
ol.steps { margin:0; padding:0; list-style:none; }
ol.steps li { position:relative; padding-left:.4in; margin-bottom:10px; }
ol.steps li span { position:absolute; left:0; top:-1px; width:.25in; height:.25in; border:1pt solid var(--acc); transform:rotate(45deg) scale(.82); display:flex; align-items:center; justify-content:center; }
ol.steps li span i { transform:rotate(-45deg); font-style:normal; font-family:'DM Serif Display',serif; font-size:11pt; color:var(--acc); }
.use { margin-top:12px; border:1pt solid var(--acc); padding:9px 12px; font-size:8.8pt; line-height:1.45; position:relative; }
.use h3 { position:absolute; top:-8px; left:10px; background:var(--paper); padding:0 6px; margin:0; font-weight:600; font-size:6.8pt; letter-spacing:.22em; text-transform:uppercase; color:var(--acc); }
.use p { margin:0 0 4px; } .use p:last-child { margin:0; }
.keeps { margin-top:10px; font-size:8.8pt; } .keeps b { font-weight:600; font-size:6.6pt; letter-spacing:.22em; text-transform:uppercase; color:var(--mustard); margin-right:6px; }
.note { margin-top:10px; font-size:8.8pt; font-style:italic; color:var(--muted); }
.note b { font-style:normal; font-weight:600; font-size:6.6pt; letter-spacing:.22em; text-transform:uppercase; color:var(--mustard); margin-right:6px; }
.folio { position:absolute; bottom:calc(.5in + .125in); display:flex; justify-content:space-between; align-items:center; font-size:6.6pt; letter-spacing:.22em; text-transform:uppercase; color:var(--muted); }
.folio .n { font-family:'DM Serif Display',serif; font-size:12pt; letter-spacing:0; color:var(--acc); }
"""

def page(r, ch_no, ch_title, n, side, mix_no):
    is_mix = bool(r["keeps"])
    facts = "".join(f"<div><b>{t(k)}</b><span>{t(v)}</span></div>" for k, v in r["meta"])
    parts, cur = [], []
    def flush():
        if cur: parts.append('<ul class="ing">' + "".join(cur) + "</ul>"); cur.clear()
    for kind, v in r["ingr"]:
        if kind == "group": flush(); parts.append(f'<div class="grp">{t(v)}</div>')
        else:
            q, rest = split_qty(v)
            cur.append(f'<li><span class="q">{t(q)}</span>{t(rest)}</li>' if q else f"<li>{t(rest)}</li>")
    flush()
    steps = "".join(f"<li><span><i>{i}</i></span>{t(s)}</li>" for i, s in enumerate(r["steps"], 1))
    use = "".join(f'<div class="use"><h3>{t(s["title"])}</h3>' + "".join(f"<p>{t(p)}</p>" for p in s["paras"]) + "</div>" for s in r["extra"])
    keeps = f'<div class="keeps"><b>Keeps</b>{t(r["keeps"])}</div>' if r["keeps"] else ""
    note = f'<div class="note"><b>Pantry note</b>{t(r["tip"])}</div>' if r["tip"] else ""
    seal = ""
    made = f'<div class="made"><b>Made with</b> {t(", ".join(r["uses"]))}</div>' if r["uses"] else ""
    left = f'<span class="n">{n}</span><span>{t(ch_title)}</span>'
    right = f'<span>{t(BOOK)}</span><span class="n">{n}</span>'
    return f"""<section class="page {side}{' mix' if is_mix else ''}"><div class="band"></div>
<div class="area">
<div class="arch" style="background-image:url('images/{r['slug']}.jpg')"></div>
<div class="head">{seal}
<div class="chap">{'Pantry Mix &nbsp;·&nbsp; ' if is_mix else ''}Chapter {WORDS[ch_no-1]}</div>
<h1>{t(r['title'])}</h1>
<div class="orn"><span>✦</span></div>
<p class="intro">{t(r['intro'])}</p>
<div class="facts">{facts}</div>{made}
</div>
<div class="side"><div class="ingbox"><h2>Ingredients</h2>{''.join(parts)}</div>{use}</div>
<div class="main"><h2>{'Method' if is_mix else 'Directions'}</h2><ol class="steps">{steps}</ol>{keeps}{note}</div>
</div>
<div class="folio">{left if side == 'left' else right}</div>
</section>"""

def build(name):
    chs = R.chapters(); ch = chs[0]
    sel = ["All-Purpose Amish Baking Mix", "Strawberry Shortcake Biscuits"]
    pages = [page(next(x for x in ch["recipes"] if x["title"] == s), 1, ch["title"], 10 + i, "left" if i == 0 else "right", 1) for i, s in enumerate(sel)]
    render(name, pages, CSS)

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "Style_C_Heritage")
