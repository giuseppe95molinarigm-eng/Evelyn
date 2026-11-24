// Builds the plain Word manuscript from manuscript/content/*.md
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, PageBreak,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType, LevelFormat,
  Footer, PageNumber, TabStopType, TabStopPosition,
} = require('docx');

const ROOT = path.resolve(__dirname, '..');
const DIR = path.join(ROOT, 'manuscript', 'content');
const OUT = path.join(ROOT, 'manuscript', 'The_Complete_Amish_Dry_Mix_Pantry_Cookbook_Manuscript.docx');
const TITLE = 'The Complete Amish Dry Mix Pantry Cookbook';
const SUBTITLE = '150 Budget-Friendly Homemade Dry Mixes and Meals from Scratch, with Baking, Soup and Seasoning Blends, Mixes in a Jar for Gifting, and a Shelf-Life Chart';
const FONT = 'Georgia';

// ---------- parsing ----------
function parseFile(file) {
  const lines = fs.readFileSync(file, 'utf8').split('\n');
  const chapters = [];
  let ch = null, rec = null, sec = null;
  for (const raw of lines) {
    const l = raw.replace(/\s+$/, '');
    if (!l) continue;
    if (l.startsWith('# ')) { ch = { title: l.slice(2), intro: [], blocks: [], recipes: [] }; chapters.push(ch); rec = null; sec = null; continue; }
    if (l.startsWith('## ')) { rec = { title: l.slice(3), intro: '', meta: '', uses: [], ingr: [], steps: [], extra: [], keeps: '', tip: '' }; ch.recipes.push(rec); sec = null; continue; }
    if (!rec) { // chapter-level content
      if (l.startsWith('* ')) ch.blocks.push({ t: 'p', v: l.slice(2) });
      else if (l.startsWith('### ')) ch.blocks.push({ t: 'h3', v: l.slice(4) });
      else if (l.startsWith('- ')) ch.blocks.push({ t: 'li', v: l.slice(2) });
      else if (l.startsWith('|')) {
        const cells = l.split('|').slice(1, -1).map(s => s.trim());
        const last = ch.blocks[ch.blocks.length - 1];
        if (last && last.t === 'table') last.rows.push(cells); else ch.blocks.push({ t: 'table', rows: [cells] });
      }
      continue;
    }
    if (l.startsWith('> ')) rec.intro = l.slice(2);
    else if (l.startsWith('@ ')) rec.meta = l.slice(2);
    else if (l.startsWith('U: ')) rec.uses = l.slice(3).split(', ');
    else if (l.startsWith('K: ')) rec.keeps = l.slice(3);
    else if (l.startsWith('T: ')) rec.tip = l.slice(3);
    else if (l.startsWith('+ ')) rec.ingr.push({ group: l.slice(2) });
    else if (l.startsWith('- ')) rec.ingr.push({ item: l.slice(2) });
    else if (/^\d+\. /.test(l)) { (sec ? sec.steps : rec.steps).push(l.replace(/^\d+\. /, '')); }
    else if (l.startsWith('= ')) { sec = { title: l.slice(2), paras: [], steps: [] }; rec.extra.push(sec); }
    else if (l.startsWith('* ')) { if (sec) sec.paras.push(l.slice(2)); else rec.extra.push({ title: '', paras: [l.slice(2)], steps: [] }); }
    else throw new Error(`Unparsed line in ${file}: ${l}`);
  }
  return chapters;
}

const files = fs.readdirSync(DIR).filter(f => f.endsWith('.md')).sort();
const front = parseFile(path.join(DIR, '00_front.md'));
const back = parseFile(path.join(DIR, '99_back.md'));
const recipeChapters = files.filter(f => /^\d\d\.md$/.test(f)).map(f => parseFile(path.join(DIR, f))[0]);

// ---------- helpers ----------
let numRef = 0;
const numberingConfig = [{
  reference: 'bullets',
  levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 540, hanging: 270 } } } }],
}];
function newNumbering() {
  const ref = `steps${numRef++}`;
  numberingConfig.push({ reference: ref, levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 540, hanging: 360 } } } }] });
  return ref;
}
const P = (text, opts = {}) => new Paragraph({ spacing: { after: 120, line: 288 }, ...opts, children: Array.isArray(text) ? text : [new TextRun(text)] });
const labelled = (label, text) => P([new TextRun({ text: label, bold: true }), new TextRun(text)]);
const H1 = (text, pageBreak = true) => new Paragraph({ heading: HeadingLevel.HEADING_1, pageBreakBefore: pageBreak, children: [new TextRun(text)] });
const H2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, pageBreakBefore: true, children: [new TextRun(text)] });
const H3 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [new TextRun(text)] });
const bullet = (text) => new Paragraph({ numbering: { reference: 'bullets', level: 0 }, spacing: { after: 60, line: 276 }, children: [new TextRun(text)] });

const TABLE_W = 9360;
function table(rows) {
  const n = rows[0].length;
  const w = Math.floor(TABLE_W / n);
  const widths = Array(n).fill(w); widths[n - 1] = TABLE_W - w * (n - 1);
  const border = { style: BorderStyle.SINGLE, size: 4, color: '999999' };
  const borders = { top: border, bottom: border, left: border, right: border };
  return new Table({
    width: { size: TABLE_W, type: WidthType.DXA }, columnWidths: widths,
    rows: rows.map((r, i) => new TableRow({
      tableHeader: i === 0,
      children: r.map((c, j) => new TableCell({
        width: { size: widths[j], type: WidthType.DXA }, borders,
        shading: i === 0 ? { fill: 'E7E7E7', type: ShadingType.CLEAR, color: 'auto' } : undefined,
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({ children: [new TextRun({ text: c, bold: i === 0, size: 19 })] })],
      })),
    })),
  });
}

function blocks(list) {
  const out = [];
  for (const b of list) {
    if (b.t === 'p') out.push(P(b.v));
    else if (b.t === 'h3') out.push(H3(b.v));
    else if (b.t === 'li') out.push(bullet(b.v));
    else if (b.t === 'table') { out.push(table(b.rows)); out.push(P('')); }
  }
  return out;
}

function recipe(r, isGift) {
  const out = [H2(r.title)];
  if (r.intro) out.push(P([new TextRun({ text: r.intro, italics: true })]));
  if (r.meta) out.push(P(r.meta.split(' | ').map((m, i) => {
    const [k, ...v] = m.split(': ');
    return [new TextRun({ text: (i ? '     ' : '') + k + ': ', bold: true }), new TextRun(v.join(': '))];
  }).flat()));
  if (r.uses.length) out.push(labelled(r.uses.length > 1 ? 'Uses: ' : 'Uses: ', r.uses.join('; ')));
  out.push(H3(isGift ? 'What You Need' : 'Ingredients'));
  for (const i of r.ingr) {
    if (i.group) out.push(new Paragraph({ spacing: { before: 120, after: 60 }, keepNext: true, children: [new TextRun({ text: i.group, bold: true, italics: true })] }));
    else out.push(bullet(i.item));
  }
  if (r.steps.length) {
    out.push(H3(isGift ? 'Filling the Jar' : 'Directions'));
    const ref = newNumbering();
    r.steps.forEach(s => out.push(new Paragraph({ numbering: { reference: ref, level: 0 }, spacing: { after: 100, line: 288 }, children: [new TextRun(s)] })));
  }
  for (const s of r.extra) {
    if (s.title) out.push(H3(s.title));
    const boxed = s.title === 'Gift Tag';
    const bd = { style: BorderStyle.SINGLE, size: 6, color: '000000', space: 6 };
    s.paras.forEach(p => out.push(P(p, boxed ? { border: { top: bd, bottom: bd, left: bd, right: bd }, indent: { left: 144, right: 144 } } : {})));
  }
  if (r.keeps) out.push(labelled('Keeps: ', r.keeps + '.'));
  if (r.tip) out.push(labelled('Tip: ', r.tip));
  return out;
}

// ---------- build ----------
const children = [];
// Title page
children.push(new Paragraph({ spacing: { before: 3600, after: 360 }, alignment: AlignmentType.CENTER, children: [new TextRun({ text: TITLE, bold: true, size: 52, font: FONT })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 1200 }, children: [new TextRun({ text: SUBTITLE, italics: true, size: 26 })] }));
children.push(new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: '[Author Name]', size: 28 })] }));
// Copyright page
children.push(new Paragraph({ children: [new PageBreak()] }));
children.push(P('Copyright © 2026 [Author Name]. All rights reserved.', { spacing: { before: 4800, after: 120 } }));
children.push(P('No part of this book may be reproduced, stored in a retrieval system or transmitted in any form or by any means, electronic, mechanical, photocopying, recording or otherwise, without the prior written permission of the author, except for brief quotations in reviews.'));
children.push(P('Disclaimer: The recipes and information in this book are provided for general home-cooking use. Storage times are guidelines for best quality and depend on your ingredients, containers and storage conditions. Always check mixes before use and discard any that smell stale or show signs of moisture or spoilage. Readers with food allergies or dietary restrictions should check every ingredient label. The author and publisher are not responsible for any adverse effects resulting from the use of the information in this book.'));
children.push(P('This book is inspired by the traditional, frugal cooking of Amish communities. It is not affiliated with or endorsed by any Amish community or organization.'));
// TOC
children.push(H1('Contents'));
const PAGES = fs.existsSync(path.join(ROOT, 'manuscript', '.pages.json')) ? JSON.parse(fs.readFileSync(path.join(ROOT, 'manuscript', '.pages.json'), 'utf8')) : {};
const tocTitles = [...front.map(c => c.title), ...recipeChapters.map((c, i) => `Chapter ${i + 1}: ${c.title}`),
  'Master Shelf-Life Chart', 'One Mix, Many Meals Index', ...back.map(c => c.title), 'Recipe Index'];
tocTitles.forEach(t => children.push(new Paragraph({ spacing: { after: 100 },
  tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX, leader: 'dot' }], children: [
  new TextRun({ text: t, bold: t.startsWith('Chapter') }),
  new TextRun({ text: '\t' + String(PAGES[t] || '') }),
] })));
fs.writeFileSync(path.join(ROOT, 'manuscript', '.toc.json'), JSON.stringify(tocTitles));

// Front matter
for (const c of front) { children.push(H1(c.title)); children.push(...blocks(c.blocks)); }

// Recipe chapters
const allRecipes = [];
recipeChapters.forEach((c, idx) => {
  children.push(H1(`Chapter ${idx + 1}: ${c.title}`));
  children.push(...blocks(c.intro.length ? c.intro : c.blocks));
  const isGift = idx === recipeChapters.length - 1;
  for (const r of c.recipes) { children.push(...recipe(r, isGift)); allRecipes.push({ ...r, chapter: idx + 1, chapterTitle: c.title, isGift }); }
});

// Back matter
const [mealPlan, shopping, conversions] = back;
// Master shelf-life chart
children.push(H1('Master Shelf-Life Chart'));
children.push(P('Use this chart to check how long each mix keeps. Times are for best quality when the mix is stored in an airtight container in a cool, dry, dark place. Mixes that contain fat, whole grains or dairy powders keep longer when refrigerated or frozen.'));
recipeChapters.forEach((c, idx) => {
  const mixes = allRecipes.filter(r => r.chapter === idx + 1 && r.keeps);
  if (!mixes.length) return;
  children.push(H3(`Chapter ${idx + 1}: ${c.title}`));
  children.push(table([['Mix', 'Keeps'], ...mixes.map(m => [m.title, m.keeps])]));
  children.push(P(''));
});
// One mix many meals index
children.push(H1('One Mix, Many Meals Index'));
children.push(P('Find every recipe you can make from the mixes already on your shelf.'));
const mixNames = allRecipes.filter(r => r.keeps).map(r => r.title);
for (const m of mixNames) {
  const made = allRecipes.filter(r => r.uses.includes(m)).map(r => r.title);
  if (!made.length) continue;
  children.push(new Paragraph({ spacing: { before: 160, after: 60 }, keepNext: true, children: [new TextRun({ text: m, bold: true })] }));
  made.forEach(t => children.push(bullet(t)));
}
// Meal plan, shopping list, conversions
for (const c of [mealPlan, shopping, conversions]) { children.push(H1(c.title)); children.push(...blocks(c.blocks)); }
// Recipe index
children.push(H1('Recipe Index'));
children.push(P('All 150 recipes in alphabetical order, with the chapter where each one appears.'));
[...allRecipes].sort((a, b) => a.title.localeCompare(b.title)).forEach(r =>
  children.push(new Paragraph({ spacing: { after: 40 }, children: [new TextRun(r.title), new TextRun({ text: `  (Chapter ${r.chapter})`, color: '555555' })] })));

const doc = new Document({
  creator: 'Elite Publishing', title: TITLE,
    styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 40, bold: true }, paragraph: { spacing: { before: 240, after: 240 }, keepNext: true, outlineLevel: 0 } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 32, bold: true }, paragraph: { spacing: { before: 0, after: 160 }, keepNext: true, outlineLevel: 1 } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 24, bold: true }, paragraph: { spacing: { before: 200, after: 80 }, keepNext: true, outlineLevel: 2 } },
    ],
  },
  numbering: { config: numberingConfig },
  sections: [{
    properties: { page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then(buf => { fs.writeFileSync(OUT, buf); console.log('wrote', OUT, 'recipes', allRecipes.length); });
