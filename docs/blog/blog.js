/* ===== The ML Diarys — scroll blog =====
   Content comes from books-data.js (generated from blog/posts/*.md by build.py).
   Each book carries an `es` and an `en` view; a language toggle flips between them. */
(function(){
  const entriesEl = document.getElementById("entries");
  const reader  = document.getElementById("reader");
  const bookEl  = document.getElementById("book");
  const titleEl = document.getElementById("booktitle");
  let current = 0;
  let spread  = 0;

  const plain = t => (t || "").replace(/-<br>/g, "").replace(/<br>/g, " ");

  /* ---------------- language ---------------- */
  let LANG = localStorage.getItem("mld-lang") === "en" ? "en" : "es";
  const UI = {
    es: { open:"Abrir este diario", posted:"publicado",
          leaf:n => (n === 1 ? "falta 1 hoja" : "faltan " + n + " hojas"), last:"última página" },
    en: { open:"Open this diary", posted:"posted",
          leaf:n => (n === 1 ? "1 leaf left" : n + " leaves left"), last:"last page" }
  };
  const L = b => b[LANG] || b.es;

  /* ---------------- homepage entries ---------------- */
  function renderFormula(el, tex){
    if(!el || !tex) return;
    if(window.katex){
      try { katex.render(tex, el, { throwOnError:false, displayMode:false }); }
      catch(e){ el.textContent = tex; }
    } else { el.textContent = tex; }
    const k = el.querySelector(".katex");
    if(k){
      const cw = el.clientWidth, kw = k.scrollWidth;
      if(kw > cw && cw > 0){
        k.style.display = "inline-block";
        k.style.transformOrigin = "center";
        k.style.transform = "scale(" + (cw/kw) + ")";
      }
    }
  }

  let io = null;
  function buildEntries(){
    entriesEl.innerHTML = "";
    BOOKS.forEach((b,i)=>{
      const d = L(b);
      const plainTitle = plain(d.title);
      const art = document.createElement("article");
      art.className = "entry rv" + (i%2 ? " flip" : "");
      art.setAttribute("data-screen-label", "Diario: " + plainTitle);
      art.innerHTML = `
        <button class="tome" style="--tome-leather:${b.leather}; --tome-gilt:${b.gilt}" aria-label="${UI[LANG].open}: ${plainTitle}">
          <span class="cover">
            <span class="gilt"></span>
            <span class="corner tl"></span><span class="corner tr"></span>
            <span class="corner bl"></span><span class="corner br"></span>
            <span class="num">${d.date}</span>
            ${b.formula ? `<span class="formula"></span>` : tomeEmblem(b.emblem)}
            <span class="ctitle">${d.title}</span>
            <span class="kind">${d.kind}</span>
          </span>
          <span class="clasp"></span>
        </button>
        <div class="scrap">
          <span class="tape-l" aria-hidden="true"></span>
          <span class="tape-r" aria-hidden="true"></span>
          <p class="meta"><span class="vol">${UI[LANG].posted} ${d.date}</span><span class="sep">·</span><span>${d.kind}</span></p>
          <h3>${plainTitle}</h3>
          <p class="teaser">${d.teaser || ""}</p>
          <button class="openlink">${UI[LANG].open} <span class="arr">→</span></button>
        </div>`;
      art.querySelector(".tome").addEventListener("click", ()=> openReader(i));
      art.querySelector(".openlink").addEventListener("click", ()=> openReader(i));
      entriesEl.appendChild(art);
      renderFormula(art.querySelector(".cover .formula"), b.formula);
    });
    if(io) io.disconnect();
    io = new IntersectionObserver((ents)=>{
      ents.forEach(e=>{ if(e.isIntersecting){ e.target.classList.add("vis"); io.unobserve(e.target); } });
    }, { threshold:0.12 });
    document.querySelectorAll(".rv").forEach(el=> io.observe(el));
  }

  /* ---------------- reader ---------------- */
  const prevBtn = document.getElementById("prevPage");
  const nextBtn = document.getElementById("nextPage");
  const indEl   = document.getElementById("pageind");

  function fillDiagrams(scope){
    scope.querySelectorAll(".figbody[data-fig]").forEach(el=>{
      const fn = FIGS[el.getAttribute("data-fig")];
      el.innerHTML = fn ? fn() : "";
    });
    scope.querySelectorAll(".figbody[data-chart]").forEach(el=>{
      const fn = (typeof CHART !== "undefined") && CHART[el.getAttribute("data-chart")];
      el.innerHTML = fn ? fn(el.getAttribute("data-cdata")) : "";
    });
  }
  function renderMath(scope){
    if(!window.katex) return;
    scope.querySelectorAll(".mathblock[data-tex], .mathinline[data-tex]").forEach(el=>{
      const tex = el.getAttribute("data-tex");
      try { katex.render(tex, el, { throwOnError:false,
              displayMode: el.classList.contains("mathblock") }); }
      catch(e){ el.textContent = tex; }
    });
  }
  function spreadCount(){ return Math.max(1, Math.ceil(L(BOOKS[current]).pages.length / 2)); }

  function renderSpread(){
    const d = L(BOOKS[current]);
    const ps = d.pages;
    const sc = Math.max(1, Math.ceil(ps.length / 2));
    if(spread > sc-1) spread = sc-1;
    if(spread < 0) spread = 0;
    const Lp = ps[spread*2], Rp = ps[spread*2+1];
    bookEl.innerHTML = `<div class="spine2"></div>
      <div class="pg left">${Lp.html}<div class="folio">${Lp.folio}</div></div>
      ${ Rp ? `<div class="pg right">${Rp.html}<div class="folio">${Rp.folio}</div></div>`
            : '<div class="pg right blankpage" aria-hidden="true"></div>' }`;
    fillDiagrams(bookEl);
    renderMath(bookEl);
    const chap = (Rp && Rp.chapter) || Lp.chapter;
    titleEl.textContent = chap ? `${d.booktitle} — ${chap}` : d.booktitle;
    prevBtn.disabled = (spread === 0);
    nextBtn.disabled = (spread === sc-1);
    const remaining = sc - 1 - spread;
    // dots scale with page count so the indicator never overflows
    const dotFs  = Math.max(7, Math.min(17, Math.round(340 / (1.55 * sc))));
    const dotGap = Math.max(3, Math.min(10, Math.round(dotFs * 0.55)));
    const dots = Array.from({length:sc}, (_,s)=>
      `<span class="d${s===spread ? " on" : ""}">✦</span>`).join("");
    const tleft = remaining > 0 ? UI[LANG].leaf(remaining) : UI[LANG].last;
    indEl.innerHTML =
      `<span class="indcount">${spread+1}<span class="indslash">/</span>${sc}</span>` +
      `<span class="inddiv"></span>` +
      `<span class="inddots" style="font-size:${dotFs}px;gap:${dotGap}px">${dots}</span>` +
      `<span class="inddiv"></span>` +
      `<span class="indleft">${tleft}</span>`;
  }
  function turn(d){
    const sc = spreadCount();
    const s = spread + d;
    if(s < 0 || s >= sc) return;
    spread = s;
    renderSpread();
  }
  /* show/hide just toggle the overlay; open/close also manage the URL hash
     (#diary-N) so each diary is shareable and the Back button closes it. */
  function showReader(i){
    current = i; spread = 0;
    renderSpread();
    reader.classList.add("open");
    reader.setAttribute("aria-hidden","false");
    document.body.classList.add("locked");
  }
  function hideReader(){
    reader.classList.remove("open");
    reader.setAttribute("aria-hidden","true");
    document.body.classList.remove("locked");
  }
  function openReader(i){
    showReader(i);
    history.pushState({ diary:i }, "", "#diary-" + (i+1));
  }
  function closeReader(){
    if(/^#diary-/.test(location.hash)) history.back();   // -> popstate -> hideReader
    else hideReader();
  }
  function syncFromHash(){
    const m = location.hash.match(/^#diary-(\d+)$/);
    if(m){
      const i = +m[1] - 1;
      if(i >= 0 && i < BOOKS.length){ showReader(i); return; }
    }
    hideReader();
  }
  window.addEventListener("popstate", syncFromHash);
  document.getElementById("closeReader").addEventListener("click", ()=>closeReader());
  prevBtn.addEventListener("click", ()=>turn(-1));
  nextBtn.addEventListener("click", ()=>turn(1));
  reader.addEventListener("click", e=>{ if(e.target===reader) closeReader(); });
  document.addEventListener("keydown", e=>{
    if(!reader.classList.contains("open")) return;
    if(e.key==="Escape") closeReader();
    else if(e.key==="ArrowLeft") turn(-1);
    else if(e.key==="ArrowRight") turn(1);
  });

  /* ---------------- language toggle ---------------- */
  function syncToggle(){
    document.querySelectorAll("#langtoggle button").forEach(btn=>{
      btn.classList.toggle("on", btn.getAttribute("data-lang") === LANG);
    });
    document.body.classList.toggle("lang-en", LANG === "en");
    document.documentElement.lang = LANG;
  }
  function setLang(lang){
    LANG = (lang === "en") ? "en" : "es";
    localStorage.setItem("mld-lang", LANG);
    syncToggle();
    buildEntries();
    if(reader.classList.contains("open")) renderSpread();
  }
  document.querySelectorAll("#langtoggle button").forEach(btn=>{
    btn.addEventListener("click", ()=> setLang(btn.getAttribute("data-lang")));
  });

  /* ---------------- init ---------------- */
  syncToggle();
  buildEntries();

  /* open a diary straight from a shared #diary-N link */
  (function initFromHash(){
    const m = location.hash.match(/^#diary-(\d+)$/);
    if(!m) return;
    const i = +m[1] - 1;
    if(i < 0 || i >= BOOKS.length) return;
    history.replaceState(null, "", "#archive");          // synthetic Back target
    history.pushState({ diary:i }, "", "#diary-" + (i+1));
    showReader(i);
  })();

  /* ---------------- ember canvas (fixed, full page) ---------------- */
  const canvas = document.getElementById("embers");
  const ctx = canvas.getContext("2d");
  let W, H, DPR;
  function resize(){
    DPR = Math.min(window.devicePixelRatio||1, 2);
    W = canvas.width = innerWidth*DPR; H = canvas.height = innerHeight*DPR;
    canvas.style.width = innerWidth+"px"; canvas.style.height = innerHeight+"px";
  }
  resize(); addEventListener("resize", resize);

  const N = 44;
  const parts = [];
  function spawn(){
    return {
      x:Math.random()*innerWidth*DPR,
      y:(innerHeight + Math.random()*60)*DPR,
      r:(Math.random()*1.8+0.6)*DPR,
      vy:-(Math.random()*0.5+0.25)*DPR,
      vx:(Math.random()-0.5)*0.3*DPR,
      tw:Math.random()*6.28,
      hot:Math.random()<0.35
    };
  }
  for(let i=0;i<N;i++){ const p=spawn(); p.y = Math.random()*H; parts.push(p); }

  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  function tick(){
    ctx.clearRect(0,0,W,H);
    ctx.globalCompositeOperation = "lighter";
    for(let i=parts.length-1;i>=0;i--){
      const p = parts[i];
      p.x += p.vx + Math.sin(p.tw)*0.25*DPR; p.y += p.vy; p.tw += 0.03; p.vy *= 0.997;
      const a = Math.max(0, Math.min(1, (p.y/H))) * (0.5 + 0.5*Math.sin(p.tw*1.3));
      const col = p.hot ? "255,150,70" : "210,70,40";
      ctx.beginPath();
      ctx.fillStyle = "rgba("+col+","+(0.55*a)+")";
      ctx.arc(p.x, p.y, p.r, 0, 6.2832); ctx.fill();
      if(p.y < -10*DPR){ Object.assign(p, spawn()); }
    }
    requestAnimationFrame(tick);
  }
  if(!reduced) tick();
})();
