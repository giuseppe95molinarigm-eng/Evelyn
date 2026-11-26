"""Parser for manuscript/content/*.md (same format used by build_manuscript.js)."""
import pathlib, re

DIR = pathlib.Path(__file__).resolve().parent.parent / "manuscript" / "content"

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def parse(path):
    chapters, ch, rec, sec = [], None, None, None
    for raw in pathlib.Path(path).read_text().splitlines():
        l = raw.rstrip()
        if not l: continue
        if l.startswith("# "):
            ch = {"title": l[2:], "blocks": [], "recipes": []}; chapters.append(ch); rec = sec = None; continue
        if l.startswith("## "):
            rec = {"title": l[3:], "slug": slug(l[3:]), "intro": "", "meta": [], "uses": [], "ingr": [], "steps": [],
                   "extra": [], "keeps": "", "tip": ""}
            ch["recipes"].append(rec); sec = None; continue
        if rec is None:
            if l.startswith("* "): ch["blocks"].append(("p", l[2:]))
            elif l.startswith("### "): ch["blocks"].append(("h3", l[4:]))
            elif l.startswith("- "): ch["blocks"].append(("li", l[2:]))
            elif l.startswith("|"):
                cells = [c.strip() for c in l.strip("|").split("|")]
                if ch["blocks"] and ch["blocks"][-1][0] == "table": ch["blocks"][-1][1].append(cells)
                else: ch["blocks"].append(("table", [cells]))
            continue
        if l.startswith("> "): rec["intro"] = l[2:]
        elif l.startswith("@ "): rec["meta"] = [tuple(m.split(": ", 1)) for m in l[2:].split(" | ")]
        elif l.startswith("U: "): rec["uses"] = l[3:].split(", ")
        elif l.startswith("K: "): rec["keeps"] = l[3:]
        elif l.startswith("T: "): rec["tip"] = l[3:]
        elif l.startswith("+ "): rec["ingr"].append(("group", l[2:]))
        elif l.startswith("- "): rec["ingr"].append(("item", l[2:]))
        elif re.match(r"^\d+\. ", l): (sec["steps"] if sec else rec["steps"]).append(re.sub(r"^\d+\. ", "", l))
        elif l.startswith("= "): sec = {"title": l[2:], "paras": [], "steps": []}; rec["extra"].append(sec)
        elif l.startswith("* "):
            (sec["paras"] if sec else rec["extra"].append({"title": "", "paras": [], "steps": []}) or rec["extra"][-1]["paras"]).append(l[2:])
    return chapters

def chapters():
    return [parse(p)[0] for p in sorted(DIR.glob("[0-9][0-9].md"))]

def front(): return parse(DIR / "00_front.md")
def back(): return parse(DIR / "99_back.md")
