def build_css():
    return """<style>
*{margin:0;padding:0;box-sizing:border-box}
html{font-size:20px;scroll-behavior:smooth;overflow-x:hidden}
:root{--black:#050505;--white:#f4f4ef;--gray:#666}
body{background:#f4f4ef;color:var(--black);font-family:'Space Mono',monospace;overflow-x:hidden;-webkit-text-size-adjust:100%}

/* LANG TOGGLE */
.lang-toggle{position:fixed;top:1.2rem;right:1.5rem;z-index:200;display:flex;gap:.3rem}
.lang-btn{font-family:'Space Mono',monospace;font-size:.46rem;letter-spacing:2.5px;text-transform:uppercase;padding:.38rem .7rem;background:rgba(30,30,30,0.35);border:1px solid rgba(160,160,160,0.35);color:#888;cursor:pointer;transition:all .2s;backdrop-filter:blur(6px)}
.lang-btn.active{border-color:rgba(180,180,180,0.65);color:#bbb}
.lang-btn:hover{border-color:rgba(160,160,160,0.55);color:#aaa}

/* HERO */
#hero{height:65vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;position:relative;overflow:hidden;background:var(--black)}
#hero canvas{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none}
.hero-inner{position:relative;z-index:2}
.hero-name{font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,8vw,8rem);line-height:.88;letter-spacing:-3px;color:var(--white);animation:fadeUp .8s .1s ease both}
.hero-sub{font-family:'DM Serif Display',serif;font-style:italic;font-size:clamp(1.1rem,3.5vw,1.7rem);color:var(--gray);margin-top:2rem;line-height:1.6;animation:fadeUp .8s .2s ease both}
.hero-bottom{position:absolute;bottom:2.5rem;left:0;right:0;display:flex;justify-content:space-between;align-items:flex-end;padding:0 4rem;z-index:2;animation:fadeIn 1.2s .5s ease both}
.hero-socials{display:flex;gap:.8rem;flex-wrap:wrap;justify-content:center}
.hero-socials a{display:inline-flex;align-items:center;gap:.4rem;font-size:.52rem;letter-spacing:2px;text-transform:uppercase;color:#ccc;text-decoration:none;padding:.55rem 1rem;border:1px solid #333;background:rgba(255,255,255,0.06);backdrop-filter:blur(6px);transition:all .25s;position:relative;overflow:hidden}
.hero-socials a::before{content:'';position:absolute;inset:0;background:var(--white);transform:scaleX(0);transform-origin:left;transition:transform .3s cubic-bezier(.76,0,.24,1);z-index:0}
.hero-socials a:hover::before{transform:scaleX(1)}
.hero-socials a:hover{color:var(--black);border-color:var(--white)}
.hero-socials a svg,.hero-socials a span{position:relative;z-index:1}
.hero-socials a svg{width:14px;height:14px;fill:currentColor;flex-shrink:0}

/* SHELL / TABS */
#shell{display:flex;flex-direction:column}
#tab-bar{position:sticky;top:0;z-index:50;background:var(--black);border-bottom:1px solid #222;display:flex;align-items:stretch;flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
#tab-bar::-webkit-scrollbar{display:none}
.tab-btn{font-family:'Space Mono',monospace;font-size:.75rem;letter-spacing:3px;text-transform:uppercase;padding:1.6rem 2.4rem;background:none;border:none;color:#555;cursor:pointer;border-right:1px solid #222;transition:color .2s;position:relative;white-space:nowrap;flex-shrink:0}
.tab-btn::after{content:'';position:absolute;bottom:0;left:0;right:0;height:3px;background:var(--white);transform:scaleX(0);transition:transform .25s}
.tab-btn:hover{color:#bbb}
.tab-btn.active{color:var(--white)}
.tab-btn.active::after{transform:scaleX(1)}
.tab-panel{display:none;position:relative;background:#f4f4ef}
.tab-panel.active{display:block;animation:tabIn .3s ease both}
@keyframes tabIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.tab-panel>canvas{position:absolute;inset:0;z-index:0;pointer-events:none;display:block;width:100%;height:100%}
.panel-content{position:relative;z-index:2}
.dark-panel{background:rgba(244,244,239,0.78);padding:5rem 4rem 6rem}
.light-panel{background:rgba(244,244,239,0.62);color:var(--black);padding:5rem 4rem 6rem}
.sec-label{font-size:.52rem;letter-spacing:4px;text-transform:uppercase;color:var(--gray);margin-bottom:.8rem}
.sec-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,7vw,7rem);letter-spacing:1px;line-height:.9;margin-bottom:.8rem}
.sec-sub{font-size:.85rem;color:#2a2a2a;max-width:52rem;line-height:2.4;margin-bottom:3rem}
#panel-projects .panel-content{background:rgba(244,244,239,0.38)}
#panel-projects .sec-title,#panel-blog .sec-title,#panel-arte .sec-title{text-align:center}
#panel-projects .sec-sub,#panel-blog .sec-sub,#panel-arte .sec-sub{text-align:center;margin-left:auto;margin-right:auto}

/* ABOUT */
.about-layout{display:grid;grid-template-columns:1fr 1.35fr;gap:1.5rem 5rem;align-items:start}
.about-bottom{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:3rem;padding-top:1.2rem;border-top:2px solid #999;align-items:start}
.idioma-item{display:flex;justify-content:space-between;align-items:baseline;padding:.45rem 0;border-bottom:1px solid #eee}
.idioma-item:last-child{border-bottom:none}
.idioma-name{font-size:.65rem;color:#222}
.idioma-level{font-size:.48rem;letter-spacing:2px;text-transform:uppercase;color:#888}
.about-preview{grid-column:1/-1;padding-top:1.2rem;border-top:2px solid #999}
.apm-row{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-top:.8rem}
.apm-tags{display:flex;flex-wrap:wrap;gap:.3rem}
.apm-ver-mas{display:block;margin-top:1.8rem;text-align:center;padding:1.15rem;border:2px solid #1a1a1a;font-size:1rem;letter-spacing:2.5px;text-transform:uppercase;color:#111;cursor:pointer;background:none;font-family:'Space Mono',monospace;font-weight:700;width:100%;transition:background .2s,letter-spacing .2s}
.apm-ver-mas:hover{background:rgba(0,0,0,.05);letter-spacing:3.5px}
.about-sub-label{font-size:.85rem;letter-spacing:4px;text-transform:uppercase;color:#111;margin-bottom:1.4rem;font-weight:700}
.about-bio p{font-size:.85rem;line-height:2.4;color:#2a2a2a;margin-bottom:1.2rem}
.about-bio strong{color:var(--black)}
.bio-talk{margin-top:2rem;border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)}
.bio-talk img{width:100%;height:auto;display:block}
.bio-talk figcaption{font-size:.5rem;letter-spacing:1.5px;color:#888;padding:.7rem 1rem;text-align:center;background:#fafaf8}

/* STACK */
.stack-tier{margin-bottom:2.2rem}
.stack-tier-label{font-size:.65rem;letter-spacing:2.5px;text-transform:uppercase;color:#333;margin-bottom:.9rem;font-weight:700;display:flex;align-items:center;gap:.6rem}
.stack-tier-label span{flex:1;height:1px;background:#ccc}
.stack-chips{display:flex;flex-wrap:wrap;gap:.55rem}
.chip{font-size:.6rem;letter-spacing:1.5px;text-transform:uppercase;padding:.45rem 1.05rem;border:1px solid;transition:background .2s,transform .15s;cursor:default}
.chip:hover{transform:translateY(-1px)}
.chip-gpu{border-color:#76b900;color:#4a7a00;background:rgba(118,185,0,.06)}.chip-gpu:hover{background:rgba(118,185,0,.15)}
.chip-ml{border-color:#5588cc;color:#2255aa;background:rgba(85,136,204,.06)}.chip-ml:hover{background:rgba(85,136,204,.15)}
.chip-data{border-color:#cc7700;color:#995500;background:rgba(204,119,0,.06)}.chip-data:hover{background:rgba(204,119,0,.15)}
.chip-lang{border-color:#555;color:#222}.chip-lang:hover{background:rgba(0,0,0,.05)}
.chip-viz{border-color:#9955cc;color:#7733aa;background:rgba(153,85,204,.06)}.chip-viz:hover{background:rgba(153,85,204,.15)}
.chip-ops{border-color:#cc3344;color:#aa2233;background:rgba(204,51,68,.06)}.chip-ops:hover{background:rgba(204,51,68,.15)}

/* EDUCATION */
.edu-item{margin-bottom:1.5rem}
.edu-item:last-child{margin-bottom:0}
.edu-year{font-size:.5rem;letter-spacing:2px;color:#bbb;margin-bottom:.35rem}
.edu-name{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--black);margin-bottom:.25rem;line-height:1.3}
.edu-inst{font-size:.62rem;color:#555}

/* PROJECTS — editorial layout (La Silla Vacía inspired) */
.proj-paper{max-width:60rem;margin:0 auto;text-align:left}

/* shared editorial bits */
.proj-kicker{font-size:.46rem;letter-spacing:3px;text-transform:uppercase;color:#666;font-weight:700;margin-bottom:.75rem}
.proj-tags{display:flex;flex-wrap:wrap;gap:.35rem}
.proj-tag{font-size:.44rem;letter-spacing:1.5px;text-transform:uppercase;padding:.26rem .65rem;border:1px solid;background:transparent;white-space:nowrap}

/* lead story */
.proj-lead{display:grid;grid-template-columns:1.05fr 1fr;gap:2.4rem;align-items:center;padding-bottom:2.6rem;margin-bottom:.5rem;border-bottom:2px solid #1a1a1a}
.proj-lead-media{display:block;background:#e8e8e5;border:1px solid #ddd;overflow:hidden;aspect-ratio:4/3}
.proj-lead-media img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.proj-lead-media:hover img{transform:scale(1.02)}
.proj-lead-body{display:flex;flex-direction:column}
.proj-lead-title{font-family:'DM Serif Display',serif;font-size:clamp(1.8rem,3.4vw,2.7rem);line-height:1.08;color:#0a0a0a;text-decoration:none;margin-bottom:1rem;transition:color .2s}
.proj-lead-title:hover{color:#555}
.proj-lead-deck{font-size:.72rem;line-height:2;color:#3a3a3a;margin-bottom:1.3rem}
.proj-lead-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem;padding:1.1rem 0;margin-bottom:1.3rem;border-top:1px solid #d8d8d2;border-bottom:1px solid #d8d8d2}
.proj-stat{display:flex;flex-direction:column;gap:.25rem}
.proj-stat-val{font-family:'DM Serif Display',serif;font-size:.92rem;color:#0a0a0a;line-height:1.05}
.proj-stat-label{font-size:.4rem;letter-spacing:1.5px;text-transform:uppercase;color:#555}
.proj-lead .proj-tags{margin-bottom:1.4rem}
.proj-readmore{align-self:flex-start;padding:.7rem 1.6rem;border:1px solid #1a1a1a;font-size:.46rem;letter-spacing:2.5px;text-transform:uppercase;color:#111;text-decoration:none;background:none;transition:background .2s,color .2s}
.proj-readmore:hover{background:#1a1a1a;color:#f4f4ef}

/* feed masthead */
.proj-feed-head{display:flex;align-items:center;gap:1rem;margin:2.6rem 0 1.4rem}
.proj-feed-label{font-size:.5rem;letter-spacing:3.5px;text-transform:uppercase;color:#111;font-weight:700;white-space:nowrap}
.proj-feed-rule{flex:1;height:1px;background:#ccc}

/* feed rows */
.proj-feed{display:flex;flex-direction:column}
.proj-post{display:grid;grid-template-columns:1fr 1fr;gap:2.2rem;align-items:center;padding:1.9rem 0;border-top:1px solid #d8d8d2;text-decoration:none;color:inherit;transition:opacity .2s}
.proj-post:first-child{border-top:none}
.proj-post-media{aspect-ratio:16/10;background:#e8e8e5;border:1px solid #ddd;overflow:hidden}
.proj-post-media img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.proj-post:hover .proj-post-media img{transform:scale(1.04)}
.proj-post-body{display:flex;flex-direction:column;min-width:0}
.proj-post-title{font-family:'DM Serif Display',serif;font-size:1.4rem;line-height:1.18;color:#0a0a0a;margin-bottom:.6rem;transition:color .2s}
.proj-post:hover .proj-post-title{color:#555}
.proj-post-excerpt{font-size:.72rem;line-height:2;color:#3a3a3a;margin-bottom:1rem}
.proj-post-foot{display:flex;flex-wrap:wrap;align-items:center;gap:.7rem 1rem;margin-top:auto}
.proj-byline{font-size:.44rem;letter-spacing:2px;text-transform:uppercase;color:#777;white-space:nowrap}
.proj-post-foot .proj-tags{margin-left:auto}

/* About-panel projects preview — open image cards (no box) */
.proj-card{display:flex;flex-direction:column;gap:.55rem;text-decoration:none;color:inherit}
.proj-c-img{aspect-ratio:16/9;background:#e8e8e5;border:1px solid #ddd;border-radius:8px;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,.10);transition:box-shadow .3s,transform .3s cubic-bezier(.2,.7,.2,1)}
.proj-c-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.proj-card:hover .proj-c-img{box-shadow:0 14px 32px rgba(0,0,0,.16);transform:translateY(-3px)}
.proj-card:hover .proj-c-img img{transform:scale(1.05)}
.proj-c-name{font-family:'DM Serif Display',serif;font-size:1.4rem;color:#111;line-height:1.2;margin-top:.4rem;transition:color .2s}
.proj-card:hover .proj-c-name{color:#555}
.proj-c-desc{font-size:.72rem;line-height:2;color:#3a3a3a;flex:1}
.proj-c-tags{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.15rem}
.proj-c-tag{font-size:.44rem;letter-spacing:1.5px;text-transform:uppercase;padding:.24rem .6rem;border:1px solid;background:transparent;white-space:nowrap}
.proj-c-cta{margin-top:.3rem;font-size:.48rem;letter-spacing:2.5px;text-transform:uppercase;color:#555;transition:color .2s}
.proj-card:hover .proj-c-cta{color:#111}

/* BLOG PORTAL → The ML Diarys (clickable summon doorway) */
#panel-blog .blog-void{background:rgba(244,244,239,0.62)}
.blog-portal{display:flex;justify-content:center;width:100%}
/* "venom" corruption: a dark, organic aura that only clings to the book
   (stacked drop-shadows render outside the clipped book, so the panel stays white) */
.summon{position:relative;display:grid;grid-template-columns:1.04fr .96fr;width:100%;max-width:62rem;
  text-decoration:none;color:oklch(0.26 0.030 52);overflow:hidden;
  background:linear-gradient(150deg,oklch(0.96 0.018 82) 0%,oklch(0.94 0.022 85) 45%,oklch(0.90 0.030 80) 100%);
  border:14px solid oklch(0.17 0.03 40);border-radius:6px;
  box-shadow:
    0 0 18px 1px rgba(8,7,7,.9),
    0 0 50px 5px rgba(12,9,9,.5),
    0 20px 52px rgba(0,0,0,.5),
    inset 0 0 70px oklch(0.62 0.05 55 / 0.25);
  transition:transform .4s cubic-bezier(.2,.7,.2,1),box-shadow .4s}
.summon::after{content:"";position:absolute;top:0;bottom:0;left:50%;width:2px;transform:translateX(-50%);
  background:linear-gradient(180deg,transparent,oklch(0.20 0.03 35 / 0.5) 12%,oklch(0.10 0.02 30 / 0.7) 50%,oklch(0.20 0.03 35 / 0.5) 88%,transparent);pointer-events:none}
.summon:hover{transform:translateY(-5px);
  box-shadow:
    0 0 26px 3px rgba(6,6,6,.98),
    0 0 72px 12px rgba(14,9,9,.55),
    0 26px 62px rgba(0,0,0,.55),
    inset 0 0 70px oklch(0.62 0.05 55 / 0.28)}
.summon-page{position:relative;display:flex;flex-direction:column;align-items:center;padding:2.8rem 2.4rem}
.summon-left{justify-content:flex-start}
.summon-title{font-family:'Rye',serif;font-size:clamp(2.2rem,5vw,3.6rem);line-height:.92;text-align:center;color:oklch(0.27 0.06 48);
  text-shadow:1px 1px 0 oklch(0.97 0.02 80),2px 3px 0 oklch(0.40 0.170 27),4px 7px 14px oklch(0.20 0.08 30 / 0.38);margin-bottom:.6rem}
.summon-sub{font-family:'EB Garamond',serif;font-style:italic;font-size:.8rem;line-height:1.45;text-align:center;color:oklch(0.38 0.035 54);max-width:24rem;margin-bottom:1.8rem}
.summon-ritual{width:100%;max-width:24rem;border:1.5px solid oklch(0.52 0.06 50 / 0.45);padding:1.2rem 1.4rem 1.3rem;
  background:oklch(0.89 0.028 76 / 0.55);box-shadow:inset 0 0 30px oklch(0.62 0.05 55 / 0.22),0 2px 0 rgba(255,255,255,.3)}
.summon-h2{display:block;font-family:'Nosifer',system-ui,sans-serif;font-size:1.5rem;line-height:1.18;text-transform:uppercase;text-align:center;color:oklch(0.52 0.205 28);margin-bottom:1rem;transform:rotate(-1.4deg);text-shadow:1px 1px 0 oklch(0.30 0.12 28),3px 4px 6px oklch(0.20 0.10 28 / 0.5)}
.summon-steps{display:flex;flex-direction:column;gap:.6rem}
.summon-step{display:grid;grid-template-columns:1.2rem 1fr;gap:.6rem;align-items:baseline;font-size:.72rem;color:oklch(0.38 0.035 54);line-height:1.3}
.summon-step i{font-family:'EB Garamond',serif;font-style:italic;color:oklch(0.52 0.205 28);font-size:.8rem}
.summon-incant{display:block;text-align:center;margin-top:1rem;font-family:'Rye',serif;font-size:1.1rem;color:oklch(0.61 0.225 30);
  text-shadow:0 0 18px oklch(0.55 0.2 32 / 0.45),1px 1px 0 oklch(0.30 0.10 30 / 0.4);animation:summonBreathe 3.8s ease-in-out infinite}
@keyframes summonBreathe{0%,100%{opacity:.82}50%{opacity:1;text-shadow:0 0 28px oklch(0.6 0.22 34 / 0.6)}}
.summon-descend{display:flex;flex-direction:column;align-items:center;gap:.15rem;margin-top:1.6rem}
.summon-pre{font-family:'Caveat',cursive;font-weight:600;font-size:1.05rem;color:oklch(0.38 0.035 54);transform:rotate(-1deg);transition:.25s ease}
.summon-enter{font-family:'Caveat',cursive;font-weight:700;font-size:1.55rem;line-height:1.1;color:oklch(0.52 0.205 28);transform:rotate(-2deg);transition:.25s ease}
.summon:hover .summon-enter{color:oklch(0.61 0.225 30);transform:rotate(-2deg) scale(1.05);text-shadow:0 0 14px oklch(0.55 0.2 32 / 0.4)}
.summon:hover .summon-pre{color:oklch(0.26 0.030 52)}
.summon-chevs{display:flex;gap:.1rem;margin-top:.4rem;font-size:1.2rem;color:oklch(0.52 0.205 28)}
.summon-chevs span{animation:summonDrip 1.9s ease-in-out infinite}
.summon-chevs span:nth-child(2){animation-delay:.22s;opacity:.7}
.summon-chevs span:nth-child(3){animation-delay:.44s;opacity:.45}
@keyframes summonDrip{0%,100%{transform:translateX(0);opacity:.35}50%{transform:translateX(4px);opacity:1}}
.summon-glyphs{margin-top:1.4rem;font-size:.6rem;letter-spacing:.18em;text-align:center;line-height:1.6;color:oklch(0.52 0.04 55 / 0.55);word-break:break-all}
.summon-right{justify-content:center}
.summon-glow{position:absolute;width:80%;height:78%;left:50%;top:50%;transform:translate(-50%,-50%);
  background:radial-gradient(closest-side,oklch(0.42 0.20 27 / 0.4),oklch(0.40 0.18 26 / 0.10) 58%,transparent 74%);
  filter:blur(10px);mix-blend-mode:multiply;animation:summonBleed 6s ease-in-out infinite}
@keyframes summonBleed{0%,100%{transform:translate(-50%,-50%) scale(1);opacity:.85}50%{transform:translate(-50%,-50%) scale(1.05);opacity:1}}
.summon-hand{position:relative;z-index:2;width:100%;max-width:22rem;height:auto;object-fit:contain;transform:scaleX(-1);
  mix-blend-mode:multiply;filter:drop-shadow(2px 6px 5px oklch(0.25 0.12 28 / 0.35)) saturate(1.2) contrast(1.08);
  animation:summonBreath 6.5s ease-in-out infinite}
@keyframes summonBreath{0%,100%{transform:scaleX(-1) translateY(0)}50%{transform:scaleX(-1) translateY(-5px)}}

/* ARTE */
.arte-grid{columns:3 280px;column-gap:1.8rem}
.arte-empty{font-size:.62rem;letter-spacing:3px;text-transform:uppercase;color:#bbb;padding:4rem 0;border:1px dashed #ddd;text-align:center}
.arte-piece{break-inside:avoid;margin-bottom:1.8rem;overflow:hidden;border:1px solid #e5e5e5;background:#f7f7f2}
.arte-img-wrap{width:100%;overflow:hidden}
.arte-img-wrap img{display:block;width:100%;height:auto;object-fit:cover}
img.lb-trigger{cursor:zoom-in;transition:opacity .2s}
img.lb-trigger:hover{opacity:.88}

/* LIGHTBOX */
#lightbox{position:fixed;inset:0;z-index:9000;background:rgba(0,0,0,.93);display:none;align-items:center;justify-content:center;cursor:zoom-out}
#lightbox.open{display:flex;animation:lbIn .18s ease}
@keyframes lbIn{from{opacity:0}to{opacity:1}}
#lightbox img{max-width:90vw;max-height:90vh;object-fit:contain;display:block;cursor:default;box-shadow:0 8px 40px rgba(0,0,0,.6)}
#lb-close{position:absolute;top:1.2rem;right:1.4rem;background:none;border:1px solid rgba(255,255,255,.18);color:rgba(255,255,255,.6);font-size:1.1rem;line-height:1;padding:.5rem .7rem;cursor:pointer;transition:all .18s;font-family:'Space Mono',monospace}
#lb-close:hover{color:#fff;border-color:rgba(255,255,255,.55)}

/* CONTACT */
.ct-header{text-align:center;margin-bottom:1.6rem}
.ct-big{color:#0a0a0a;margin-bottom:.8rem}
.ct-sub{font-size:.58rem;color:#444;max-width:44rem;margin:0 auto;line-height:1.8}
.ct-email-wrap{text-align:center;margin:3rem 0 2.5rem}
.ct-email-btn{font-family:'Space Mono',monospace;font-size:clamp(.55rem,2vw,.85rem);color:#111;background:none;border:1px solid rgba(0,0,0,.28);padding:1.1rem 2.5rem;cursor:pointer;letter-spacing:1.5px;transition:border-color .2s,background .2s}
.ct-email-btn:hover{border-color:#111;background:rgba(0,0,0,.04)}
.ct-email-hint{font-size:.44rem;letter-spacing:2px;text-transform:uppercase;color:#888;margin-top:.7rem}
.ct-socials{display:flex;gap:.8rem;flex-wrap:wrap;justify-content:center;margin-top:1.8rem}
.ct-soc{display:inline-flex;align-items:center;gap:.7rem;font-size:.55rem;letter-spacing:2.5px;text-transform:uppercase;color:#555;text-decoration:none;padding:1rem 2rem;border:1px solid #ccc;transition:border-color .2s,color .2s,background .2s}
.ct-soc:hover{border-color:#555;color:#0a0a0a;background:rgba(0,0,0,.04)}
.ct-soc svg{width:16px;height:16px;fill:currentColor;flex-shrink:0}

/* FOOTER */
footer{padding:1.2rem 4rem;border-top:1px solid #e5e5e5;display:flex;justify-content:space-between;font-size:.46rem;letter-spacing:2px;text-transform:uppercase;color:#aaa}

@keyframes fadeUp{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}

/* TABLET ≤900px */
@media(max-width:900px){
  .lang-toggle{top:.8rem;right:.8rem}
  .tab-btn{padding:1rem 1.2rem;font-size:.6rem;letter-spacing:2px;white-space:nowrap;flex-shrink:0}
  .dark-panel,.light-panel{padding:3rem 2rem 4rem}
  .about-layout{grid-template-columns:1fr}
  .about-bottom{grid-template-columns:1fr 1fr}
  .apm-row{grid-template-columns:1fr 1fr}
  .proj-lead{grid-template-columns:1fr;gap:1.6rem}
  .proj-post{grid-template-columns:10rem 1fr;gap:1.3rem}
  .hero-bottom{padding:0 1.5rem}
  .arte-grid{columns:2 240px}
  .ct-socials{gap:.55rem}
  footer{flex-direction:column;gap:.5rem;text-align:center}
}

/* MOBILE ≤600px */
@media(max-width:600px){
  html{font-size:16px}
  .lang-toggle{top:.6rem;right:.6rem;gap:.2rem}
  .lang-btn{font-size:.6rem;padding:.35rem .6rem}
  #hero{height:100svh}
  .hero-name{font-size:clamp(3.5rem,18vw,7rem);letter-spacing:-1px;line-height:.9}
  .hero-sub{margin-top:1.2rem}
  .hero-bottom{flex-direction:column;align-items:center;gap:1rem;bottom:1.8rem;padding:0 1.2rem}
  .hero-socials{gap:.5rem}
  .hero-socials a{font-size:.65rem;padding:.7rem 1rem}
  .tab-btn{padding:1.1rem 1.4rem;font-size:.7rem;letter-spacing:2px;white-space:nowrap;flex-shrink:0}
  .dark-panel,.light-panel{padding:2.5rem 1.2rem 3.5rem}
  .sec-title{font-size:clamp(2.5rem,12vw,5rem)}
  .about-bottom{grid-template-columns:1fr}
  .apm-row{grid-template-columns:1fr}
  .apm-row .proj-card--featured{grid-column:span 1}
  .proj-lead-stats{grid-template-columns:repeat(2,1fr)}
  .proj-post{grid-template-columns:1fr;gap:1rem}
  .proj-post-media{aspect-ratio:16/9}
  .proj-post-foot .proj-tags{margin-left:0}
  .summon{grid-template-columns:1fr;max-width:30rem;border-width:10px}
  .summon::after{display:none}
  .summon-right{padding-top:0}
  .summon-hand{max-width:15rem}
  .summon-page{padding:2rem 1.5rem}
  .arte-grid{columns:1}
  .ct-socials{gap:.5rem}
  .ct-soc{padding:.75rem 1.2rem;font-size:.5rem}
  footer{flex-direction:column;gap:.5rem;padding:1rem 1.2rem;text-align:center}
}

/* SMALL MOBILE ≤380px */
@media(max-width:380px){
  html{font-size:14px}
  .tab-btn{padding:1rem 1.2rem;font-size:.65rem}
  .hero-socials a{padding:.6rem .8rem;gap:.4rem}
}
</style>"""
