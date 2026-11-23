"""Builds the Milestone 1 client deliverable (HTML -> PDF) plus Markdown and KDP description files."""
import html, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import outline_data as d

OUT = pathlib.Path(__file__).resolve().parent.parent / "milestone-1"
OUT.mkdir(exist_ok=True)
e = html.escape

CSS = """
@page { size: Letter; margin: 0; }
* { box-sizing: border-box; }
body { margin:0; font-family: Inter, sans-serif; color:#14161b; font-size:10.5pt; line-height:1.5; }
.page { width:8.5in; height:11in; padding:0.6in 0.7in 0.75in; position:relative; page-break-after:always; overflow:hidden; }
.page:last-child { page-break-after:auto; }
.hdr { display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35in; }
.logo { font-family:'Inter Display',Inter; font-weight:800; color:#F08A24; font-size:17pt; letter-spacing:-0.5px; }
.hdr .tag { font-size:7.5pt; letter-spacing:3px; color:#555; }
.ftr { position:absolute; bottom:0.35in; left:0.7in; right:0.7in; display:flex; justify-content:space-between; font-size:7.5pt; color:#777; border-top:1px solid #e6e6e6; padding-top:6px; }
.ftr b { color:#F08A24; }
.kicker { color:#F08A24; font-weight:700; font-size:8pt; letter-spacing:3px; text-transform:uppercase; margin:0 0 6px; }
h1 { font-family:'Inter Display',Inter; font-weight:800; font-size:24pt; margin:0 0 10px; letter-spacing:-0.5px; line-height:1.15; }
h2 { font-family:'Inter Display',Inter; font-weight:800; font-size:13pt; margin:18px 0 8px; }
p { margin:0 0 9px; }
.lead { font-size:11pt; color:#333; }
/* cover */
.cover { background:#0c0e12; color:#fff; border-left:14px solid #F08A24; }
.cover .logo { font-size:26pt; margin-top:0.3in; }
.cover .kicker { margin-top:1.6in; }
.cover h1 { font-size:36pt; color:#fff; }
.cover h1 span { color:#F08A24; }
.cover .lead { color:#c9ccd3; max-width:5.6in; }
.cover .meta { position:absolute; bottom:0.8in; left:0.7in; right:0.7in; display:flex; gap:0.9in; border-top:1px solid #2a2d34; padding-top:14px; }
.cover .meta div { font-size:7.5pt; letter-spacing:2.5px; color:#8a8f99; }
.cover .meta b { display:block; color:#fff; letter-spacing:0; font-size:10pt; margin-top:6px; }
.cover .incl { margin-top:0.35in; display:grid; grid-template-columns:1fr 1fr; gap:10px; max-width:6in; }
.cover .incl div { border:1px solid #2a2d34; border-radius:8px; padding:10px 12px; font-size:9.5pt; color:#c9ccd3; }
.cover .incl b { color:#F08A24; display:block; font-size:8pt; letter-spacing:2px; }
/* title block */
.titlebox { background:#0c0e12; color:#fff; border-radius:10px; padding:22px 24px; margin:12px 0 14px; }
.titlebox .t { font-family:'Inter Display',Inter; font-weight:800; font-size:20pt; line-height:1.15; }
.titlebox .s { color:#F5B26B; font-size:11pt; margin-top:8px; line-height:1.4; }
.badge { display:inline-block; background:#F08A24; color:#fff; font-size:7pt; font-weight:700; letter-spacing:2px; padding:3px 8px; border-radius:4px; margin-bottom:10px; }
table { width:100%; border-collapse:collapse; font-size:9pt; }
th { text-align:left; font-size:7pt; letter-spacing:1.5px; text-transform:uppercase; color:#777; border-bottom:2px solid #14161b; padding:6px 6px; }
td { border-bottom:1px solid #eee; padding:6px 6px; vertical-align:top; }
td.k { font-weight:600; white-space:nowrap; }
.ok { color:#1b7f3b; font-weight:700; }
.alt { border:1px solid #e3e3e3; border-radius:8px; padding:12px 14px; margin-bottom:10px; }
.alt .t { font-weight:800; font-size:11pt; }
.alt .s { color:#444; font-size:9.5pt; margin-top:3px; }
.alt .n { font-size:7.5pt; color:#888; margin-top:5px; }
.note { background:#FFF5EA; border-left:4px solid #F08A24; padding:10px 14px; font-size:9.5pt; border-radius:0 6px 6px 0; margin:12px 0; }
/* description */
.desc { border:1px solid #e3e3e3; border-radius:10px; padding:14px 20px; font-size:9.1pt; line-height:1.42; }
.desc ul { margin:0 0 9px; padding-left:18px; } .desc li { margin-bottom:3px; }
/* outline */
.overview td.num { font-family:'Inter Display'; font-weight:800; color:#F08A24; width:34px; }
.chap { break-inside:avoid; margin-bottom:12px; }
.chap .ch { display:flex; align-items:baseline; gap:10px; border-bottom:2px solid #14161b; padding-bottom:3px; margin-bottom:4px; }
.chap .cn { font-family:'Inter Display'; font-weight:800; color:#F08A24; font-size:9pt; letter-spacing:2px; }
.chap .ct { font-family:'Inter Display'; font-weight:800; font-size:12pt; }
.chap .ci { font-size:8.5pt; color:#666; margin-bottom:5px; }
.cols { display:grid; grid-template-columns:1fr 1.35fr; gap:16px; }
.cols h4 { margin:0 0 3px; font-size:7pt; letter-spacing:2px; color:#888; text-transform:uppercase; }
ol { margin:0; padding-left:0; list-style:none; font-size:8.8pt; }
ol li { padding:1.5px 0; display:flex; gap:7px; }
ol li span { color:#F08A24; font-weight:700; min-width:24px; font-variant-numeric:tabular-nums; }
.two { columns:2; column-gap:22px; }
.steps > div { display:flex; gap:14px; padding:10px 0; border-bottom:1px solid #eee; }
.steps b.n { font-family:'Inter Display'; font-weight:800; color:#F08A24; font-size:14pt; min-width:34px; }
"""

def page(body, tag="MILESTONE 1 · TITLE & OUTLINE", n=None, cls=""):
    hdr = f'<div class="hdr"><div class="logo">Elite</div><div class="tag">{tag}</div></div>' if not cls else ""
    ftr = f'<div class="ftr"><span><b>Elite Publishing</b> · Professional self-publishing services</span><span>{n}</span></div>' if n else ""
    return f'<section class="page {cls}">{hdr}{body}{ftr}</section>'

pages = []
# Cover
pages.append(page(f"""
<div class="logo">Elite</div>
<p class="kicker">Milestone 1 · For your review</p>
<h1>Title, Subtitle &amp;<br><span>150-Recipe Outline</span></h1>
<p class="lead">The SEO title and subtitle, the Amazon book description and the chapter-by-chapter recipe outline for
<i>{e(d.TITLE)}</i>, built on the keyword research from your niche report.</p>
<div class="incl">
<div><b>01</b>SEO title &amp; subtitle, with two alternatives</div>
<div><b>02</b>Amazon book description</div>
<div><b>03</b>Chapter-by-chapter outline: 150 recipes</div>
<div><b>04</b>Front &amp; back matter extras</div>
</div>
<div class="meta"><div>PREPARED FOR<b>Evelyn</b></div><div>MARKETPLACE<b>Amazon.com (US)</b></div><div>DATE<b>November 2026</b></div></div>
""", cls="cover"))

# Title page
kw_rows = [
    ("amish dry mix pantry cookbook", "Main keyword", "Title (exact phrase)"),
    ("dry mix pantry cookbook", "Core variant", "Title"),
    ("homemade dry mixes", "Core variant", "Subtitle"),
    ("mixes in a jar", "Secondary · gift angle", "Subtitle"),
    ("budget friendly", "Buyer motivation", "Subtitle"),
    ("meals from scratch", "Supporting", "Subtitle"),
    ("baking / soup / seasoning mixes", "Long-tail", "Subtitle"),
    ("shelf-life chart", "Differentiator", "Subtitle"),
]
rows = "".join(f'<tr><td class="k">{a}</td><td>{b}</td><td>{c}</td><td class="ok">✓</td></tr>' for a, b, c in kw_rows)
alts = "".join(f'<div class="alt"><div class="t">{e(t)}</div><div class="s">{e(s)}</div><div class="n">{len(t)+len(s)} characters (title + subtitle)</div></div>' for t, s in d.ALTERNATES)
pages.append(page(f"""
<p class="kicker">01 · Title &amp; subtitle</p>
<h1>Our recommended title</h1>
<div class="titlebox"><span class="badge">RECOMMENDED</span>
<div class="t">{e(d.TITLE)}</div><div class="s">{e(d.SUBTITLE)}</div></div>
<p><b>Why this title works.</b> It contains the exact main keyword, <i>“amish dry mix pantry cookbook”</i>, so Amazon matches the book to the
search buyers actually type. <b>“Complete”</b> sets it apart from the four page-one titles (“Everyday”, “Big”, “Small-Batch”, “One-Mix”)
and tells shoppers that this is the one book they need. The subtitle covers the second-tier keywords and the selling points from the report:
the 150-recipe count, budget, homemade, the three main mix types, the gift angle and the shelf-life chart that competitors don’t offer.</p>
<table><thead><tr><th>Keyword</th><th>Role</th><th>Placed in</th><th></th></tr></thead><tbody>{rows}</tbody></table>
<div class="note">Title + subtitle: <b>{len(d.TITLE)+len(d.SUBTITLE)} characters</b>, within Amazon KDP’s 200-character limit. The remaining keywords from the report
(“amish pantry cookbook”, “make ahead pantry mixes”, “homestead pantry cookbook” and others) will go into the 7 backend keyword slots so that no words are repeated.</div>
""", n=2))
comp = [("The Amish Dry Mix Pantry Cookbook","Molly Danvers","Generic, no differentiator in the title"),
        ("The Everyday Amish Dry Mix Pantry Cookbook","Loretta Pemberton","Angle: everyday use"),
        ("The Big Amish Dry Mix Pantry Cookbook for Beginners","Madison R. Blake","Angle: size / beginners"),
        ("The Small-Batch Amish Dry Mix Pantry Cookbook","CJ Hammond","Angle: small households"),
        ("The Amish One-Mix Dry Pantry Cookbook","Ingrid Schumacher","Angle: single base mix")]
crow = "".join(f'<tr><td class="k" style="white-space:normal">{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>' for a,b,c in comp)
pages.append(page(f"""
<p class="kicker">01 · Title &amp; subtitle</p>
<h1>Two alternatives</h1>
<p class="lead">If you prefer a different tone, both options below keep the main keyword in the title and stay within the 200-character limit.</p>
{alts}
<h2>How the title stands out on page one</h2>
<p>Every organic page-one competitor already uses a one-word angle in front of the main keyword. Ours claims the broadest one,
<b>“Complete”</b>, and backs it up in the subtitle with 150 recipes, gift jars and a shelf-life chart.</p>
<table><thead><tr><th>Page-one title</th><th>Author</th><th>Positioning</th></tr></thead><tbody>{crow}
<tr><td class="k" style="white-space:normal;color:#F08A24">The Complete Amish Dry Mix Pantry Cookbook</td><td><b>Your book</b></td><td><b>Angle: everything in one book, mixes + meals + gifts</b></td></tr></tbody></table>
""", n=3))

# Description
pages.append(page(f"""
<p class="kicker">02 · Amazon description</p>
<h1>Book description</h1>
<p>This is how the description will look on Amazon. It opens with the reader’s problem, lists what’s inside, and works in the secondary keywords naturally.</p>
<div class="desc">{d.DESCRIPTION_HTML}</div>
<p style="font-size:8pt;color:#777;margin-top:8px">{len(d.DESCRIPTION_HTML)} of 4,000 characters, including formatting. We will send the ready-to-paste KDP HTML version with the listing.</p>
""", n=4))

# Outline overview
ov = []
num = 1
ranges = []
for i, (t, intro, mixes, uses) in enumerate(d.CHAPTERS, 1):
    cnt = len(mixes) + len(uses)
    ranges.append((num, num + cnt - 1))
    detail = f"{len(mixes)} mixes · {len(uses)} recipes" if mixes else f"{len(uses)} gift jars"
    ov.append(f'<tr><td class="num">{i:02d}</td><td class="k">{e(t)}</td><td>{detail}</td><td>{num}–{num+cnt-1}</td></tr>')
    num += cnt
fm = "".join(f"<li><span>·</span><div><b>{e(a)}</b>: {e(b)}</div></li>" for a, b in d.FRONT_MATTER)
bm = "".join(f"<li><span>·</span><div><b>{e(a)}</b>: {e(b)}</div></li>" for a, b in d.BACK_MATTER)
pages.append(page(f"""
<p class="kicker">03 · Recipe outline</p>
<h1>How the book is organised</h1>
<p class="lead">150 recipes in 10 chapters, all built on the “one mix, many meals” idea from the report. In chapters 1–9, five pantry
mixes are each followed by the recipes you make with them. Chapter 10 is a holiday-ready collection of gifts in a jar.</p>
<table class="overview"><thead><tr><th></th><th>Chapter</th><th>Content</th><th>Recipes</th></tr></thead><tbody>{''.join(ov)}
<tr><td></td><td class="k">Total</td><td>45 mixes · 90 recipes · 15 gift jars</td><td><b>150</b></td></tr></tbody></table>
<h2>Front matter</h2><ol>{fm}</ol>
<h2>Bonus back matter</h2><ol>{bm}</ol>
""", n=5))

# Chapter pages: 2 chapters per page
chap_html = []
for i, (t, intro, mixes, uses) in enumerate(d.CHAPTERS, 1):
    start = ranges[i-1][0]
    if mixes:
        ml = "".join(f"<li><span>{start+j}</span>{e(m)}</li>" for j, m in enumerate(mixes))
        ul = "".join(f"<li><span>{start+len(mixes)+j}</span>{e(u)}</li>" for j, u in enumerate(uses))
        body = f'<div class="cols"><div><h4>The mixes</h4><ol>{ml}</ol></div><div><h4>Made with the mixes</h4><ol>{ul}</ol></div></div>'
    else:
        ul = "".join(f"<li><span>{start+j}</span>{e(u)}</li>" for j, u in enumerate(uses))
        body = f'<h4 style="margin:0 0 3px;font-size:7pt;letter-spacing:2px;color:#888">GIFT JARS · EACH WITH A GIFT TAG</h4><ol class="two">{ul}</ol>'
    chap_html.append(f'<div class="chap"><div class="ch"><span class="cn">CHAPTER {i:02d}</span><span class="ct">{e(t)}</span></div><div class="ci">{e(intro)}</div>{body}</div>')

n = 6
for k in range(0, 10, 2):
    group = chap_html[k:k+2]
    head = '<p class="kicker">03 · Recipe outline</p><h1>Chapter by chapter</h1>' if k == 0 else ""
    pages.append(page(head + "".join(group), n=n)); n += 1

# Next steps
pages.append(page(f"""
<p class="kicker">04 · Next steps</p>
<h1>What happens next</h1>
<div class="steps">
<div><b class="n">01</b><div><b>Your review.</b> Please let us know which title you prefer (the recommended one or an alternative) and whether you’d like to
add, remove or swap any recipes. Milestone 1 includes up to 3 revisions.</div></div>
<div><b class="n">02</b><div><b>Writing the cookbook (Milestone 2).</b> Once you approve the outline, we write all 150 recipes with ingredient lists, yields,
step-by-step instructions and storage notes, plus the front and back matter listed on page 5. Each recipe gets one image.</div></div>
<div><b class="n">03</b><div><b>Cover design (Milestone 3).</b> Kindle and paperback covers built around the approved title, with a look that stands out from
the mason-jar covers on page one.</div></div>
</div>
<div class="note"><b>Every recipe has its own image.</b> For the mix recipes, the photo shows the finished mix in its jar or container. For the other recipes,
the photo shows the finished dish, so the book looks varied from start to finish.</div>
""", n=n))

doc = f'<!doctype html><html><head><meta charset="utf-8"><title>Milestone 1 · Amish Dry Mix Pantry Cookbook</title><style>{CSS}</style></head><body>{"".join(pages)}</body></html>'
(OUT / "Milestone_1_Title_Description_Outline.html").write_text(doc)
(OUT / "KDP_Description.html").write_text(d.DESCRIPTION_HTML + "\n")

# Markdown copy
md = [f"# Milestone 1: Title, Description & Outline\n", "## Recommended title\n", f"**{d.TITLE}**  \n*{d.SUBTITLE}*\n",
      f"({len(d.TITLE)+len(d.SUBTITLE)} characters)\n", "### Alternatives\n"]
md += [f"- **{t}**: {s} ({len(t)+len(s)} chars)" for t, s in d.ALTERNATES]
md += ["\n## Outline\n"]
num = 1
for i, (t, intro, mixes, uses) in enumerate(d.CHAPTERS, 1):
    md.append(f"### Chapter {i}: {t}\n_{intro}_\n")
    for label, items in (("Mixes", mixes), ("Recipes", uses)):
        if not items: continue
        md.append(f"**{label}**\n")
        for it in items:
            md.append(f"{num}. {it}"); num += 1
        md.append("")
md += ["## Front matter\n"] + [f"- {a}: {b}" for a, b in d.FRONT_MATTER]
md += ["\n## Back matter\n"] + [f"- {a}: {b}" for a, b in d.BACK_MATTER]
(OUT / "Milestone_1_Outline.md").write_text("\n".join(md) + "\n")
print("ok")
