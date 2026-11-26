// In-browser pagination for the cookbook interior.
(async function () {
  await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
  const BOOK = 'THE COMPLETE AMISH DRY MIX PANTRY COOKBOOK';
  const report = { overflow: [], shrunk: [] };

  // 1. Expand flowing sections into as many pages as needed.
  for (const tpl of [...document.querySelectorAll('template.flowsec')]) {
    const blocks = JSON.parse(tpl.innerHTML.replace(/&quot;/g, '"').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#x27;/g, "'").replace(/&amp;/g, '&'));
    const cols = tpl.dataset.cols === '1';
    let first = true, page, content, holder;
    const newPage = () => {
      page = document.createElement('section');
      page.className = 'page flow right';
      if (first && tpl.dataset.toc === '1') page.dataset.toc = tpl.dataset.title;
      page.innerHTML = '<div class="content"></div><div class="folio"></div>';
      content = page.querySelector('.content');
      if (first) {
        content.insertAdjacentHTML('beforeend', `<div class="sec-head"><span class="kicker">${tpl.dataset.kicker}</span><h1>${tpl.dataset.title}</h1><div class="rule"></div></div>`);
      }
      holder = document.createElement('div');
      if (cols) holder.className = 'colwrap';
      content.appendChild(holder);
      tpl.parentNode.insertBefore(page, tpl);
      first = false;
    };
    const overflowing = () => {
      if (cols) { holder.style.cssText = `column-count:2;column-gap:.32in;column-fill:auto;height:${content.clientHeight - holder.offsetTop}px`; return holder.scrollWidth > holder.clientWidth + 1; }
      return content.scrollHeight > content.clientHeight + 1;
    };
    newPage();
    for (const b of blocks) {
      holder.insertAdjacentHTML('beforeend', b);
      if (overflowing()) {
        holder.lastElementChild.remove();
        newPage();
        holder.insertAdjacentHTML('beforeend', b);
        if (overflowing()) report.overflow.push(tpl.dataset.title);
      }
    }
    tpl.remove();
  }

  // 2. Number pages, set left/right sides and folios, record positions.
  const pages = [...document.querySelectorAll('.page')];
  const where = {};
  let chTitle = '';
  pages.forEach((p, i) => {
    const n = i + 1;
    p.classList.remove('left', 'right');
    p.classList.add(n % 2 ? 'right' : 'left');
    if (p.dataset.chtitle) chTitle = p.dataset.chtitle;
    if (p.dataset.toc) where[p.dataset.toc] = n;
    const slugEl = p.querySelector('.photo');
    if (slugEl) { const m = slugEl.style.backgroundImage.match(/images\/(.*)\.jpg/); if (m) where['r:' + m[1]] = n; }
    const f = p.querySelector('.folio');
    if (!f || p.dataset.nofolio || p.classList.contains('opener')) { if (f) f.innerHTML = ''; return; }
    f.innerHTML = n % 2 ? `${BOOK}<span class="n">${n}</span>` : `<span class="n">${n}</span>${(p.classList.contains('recipe') ? 'CHAPTER ' + p.dataset.ch + ' · ' + chTitle : 'THE COMPLETE AMISH DRY MIX PANTRY COOKBOOK').toUpperCase()}`;
  });

  // 3. Recipe pages: shrink the photo, then the type, until the recipe fits its page.
  for (const p of document.querySelectorAll('.page.recipe')) {
    const body = p.querySelector('.body'), photo = p.querySelector('.photo');
    const limit = () => p.clientHeight - 0.78 * 96;
    const over = () => body.offsetTop + body.offsetHeight > limit();
    let h = photo.offsetHeight, fs = 10.6, changed = false;
    // First try balancing the columns: move side boxes (How to Use / Gift Tag) under the directions.
    const [c1, c2] = p.querySelectorAll('.cols > div');
    const boxes = [...c1.querySelectorAll(':scope > .box')];
    const hgt = el => { const l = el.lastElementChild; return l ? l.offsetTop + l.offsetHeight - el.offsetTop : 0; };
    if (over() && boxes.length && hgt(c1) > hgt(c2)) {
      const before = Math.max(hgt(c1), hgt(c2));
      const anchor = c2.querySelector('.keeps, .box.tip');
      boxes.forEach(b => c2.insertBefore(b, anchor));
      if (Math.max(hgt(c1), hgt(c2)) >= before) boxes.forEach(b => c1.appendChild(b)); // no gain: undo
      else changed = true;
    }
    while (over() && h > 2.8 * 96) { h -= 8; photo.style.height = h + 'px'; changed = true; }
    while (over() && fs > 9.0) { fs -= 0.2; body.style.fontSize = fs + 'pt'; changed = true; }
    if (changed) report.shrunk.push(p.querySelector('h1').textContent);
    if (over()) report.overflow.push(p.querySelector('h1').textContent);
  }

  // 4. Contents and recipe index page numbers.
  const toc = document.getElementById('toc');
  const rows = Object.entries(where).filter(([k]) => !k.startsWith('r:'));
  toc.innerHTML = rows.map(([k, n]) => {
    const m = k.match(/^Chapter (\d+): (.*)$/);
    return m ? `<div class="toc-row ch"><span class="ttl"><small>Chapter ${m[1]}</small>${m[2]}</span><span class="pg">${n}</span></div>`
             : `<div class="toc-row"><span class="ttl">${k}</span><span class="pg">${n}</span></div>`;
  }).join('');
  document.querySelectorAll('[data-ref]').forEach(s => { s.textContent = where['r:' + s.dataset.ref] || '?'; });

  report.pages = pages.length;
  window.__report = report;
  window.__paginated = true;
})();
