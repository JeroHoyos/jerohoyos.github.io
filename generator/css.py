def build_css():
    return """<style>
*{margin:0;padding:0;box-sizing:border-box}
html{font-size:20px;scroll-behavior:smooth;overflow-x:hidden}
:root{--black:#050505;--white:#f4f4ef;--gray:#666}
body{background:#f4f4ef;color:var(--black);font-family:'Space Mono',monospace;overflow-x:hidden;-webkit-text-size-adjust:100%}

.lang-toggle{position:fixed;top:1.2rem;right:1.5rem;z-index:200;display:flex;gap:.3rem}
.lang-btn{font-family:'Space Mono',monospace;font-size:.46rem;letter-spacing:2.5px;text-transform:uppercase;padding:.38rem .7rem;background:rgba(30,30,30,0.35);border:1px solid rgba(160,160,160,0.35);color:#888;cursor:pointer;transition:all .2s;backdrop-filter:blur(6px)}
.lang-btn.active{border-color:rgba(180,180,180,0.65);color:#bbb}
.lang-btn:hover{border-color:rgba(160,160,160,0.55);color:#aaa}

#hero{height:65vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;position:relative;overflow:hidden;background:var(--black)}
#hero canvas{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none}
.hero-inner{position:relative;z-index:2}
.hero-name{font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,8vw,8rem);line-height:.88;letter-spacing:-3px;color:var(--white);animation:fadeUp .8s .1s ease both}

#shell{display:flex;flex-direction:column}
#tab-bar{position:sticky;top:0;z-index:50;background:var(--black);border-bottom:1px solid #222;display:flex;align-items:stretch;flex-wrap:nowrap;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none}
#tab-bar::-webkit-scrollbar{display:none}
.tab-btn:first-child{margin-left:auto;border-left:1px solid #222}
.tab-btn:last-child{margin-right:auto}
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
#panel-projects .sec-title,#panel-arte .sec-title{text-align:center}
#panel-projects .sec-sub,#panel-arte .sec-sub{text-align:center;margin-left:auto;margin-right:auto}

.about-layout{display:grid;grid-template-columns:1fr 1.35fr;gap:1.5rem 5rem;align-items:start}
.about-bottom{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:3rem;padding-top:1.2rem;border-top:2px solid #999;align-items:start}
.idioma-item{display:flex;justify-content:space-between;align-items:baseline;padding:.45rem 0;border-bottom:1px solid #eee}
.idioma-item:last-child{border-bottom:none}
.idioma-name{font-size:.65rem;color:#222}
.idioma-level{font-size:.48rem;letter-spacing:2px;text-transform:uppercase;color:#888}
.about-preview{grid-column:1/-1;padding-top:1.2rem;border-top:2px solid #999}
.apm-row{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-top:.8rem}
.apm-tags{display:flex;flex-wrap:wrap;gap:.3rem}
.apm-ver-mas{display:block;width:max-content;max-width:100%;margin:2.4rem auto 0;text-align:center;padding:.9rem 2.6rem;border:1px solid #1a1a1a;border-radius:999px;font-size:.6rem;letter-spacing:2.5px;text-transform:uppercase;color:#111;cursor:pointer;background:none;font-family:'Space Mono',monospace;font-weight:700;transition:background .2s,color .2s,transform .2s}
.apm-ver-mas:hover{background:#1a1a1a;color:#f4f4ef;transform:translateY(-1px)}
.apm-ver-mas span{pointer-events:none}
.about-sub-label{font-size:.85rem;letter-spacing:4px;text-transform:uppercase;color:#111;margin-bottom:1.4rem;font-weight:700}
.about-bio p{font-size:.85rem;line-height:2.4;color:#2a2a2a;margin-bottom:1.2rem}
.about-bio strong{color:var(--black)}
.bio-talk{border-radius:12px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,.08)}
.bio-talk img{width:100%;height:auto;display:block}
.bio-talk figcaption{font-size:.5rem;letter-spacing:1.5px;color:#888;padding:.7rem 1rem;text-align:center;background:#fafaf8}

.edu-item{margin-bottom:1.5rem}
.edu-item:last-child{margin-bottom:0}
.edu-year{font-size:.5rem;letter-spacing:2px;color:#bbb;margin-bottom:.35rem}
.edu-name{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--black);margin-bottom:.25rem;line-height:1.3}
.edu-inst{font-size:.62rem;color:#555}

.proj-paper{max-width:60rem;margin:0 auto;text-align:left}

.proj-kicker{font-size:.46rem;letter-spacing:3px;text-transform:uppercase;color:#666;font-weight:700;margin-bottom:.75rem}
.proj-tags{display:flex;flex-wrap:wrap;justify-content:center;gap:.4rem}
.proj-tag{font-size:.44rem;letter-spacing:1.5px;text-transform:uppercase;padding:.32rem .78rem;border:1px solid;border-radius:999px;background:transparent;white-space:nowrap;font-weight:700}

.proj-lead{display:grid;grid-template-columns:1.05fr 1fr;gap:2.4rem;align-items:center;padding-bottom:2.6rem;margin-bottom:.5rem;border-bottom:2px solid #1a1a1a}
.proj-lead-media{display:block;background:#ecece8;border-radius:16px;overflow:hidden;aspect-ratio:4/3;box-shadow:0 12px 34px rgba(0,0,0,.11)}
.proj-lead-media img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.proj-lead-media:hover img{transform:scale(1.02)}
.proj-lead-body{display:flex;flex-direction:column}
.proj-lead-badge{align-self:center;display:inline-flex;align-items:center;gap:.3rem;font-size:.44rem;letter-spacing:2.5px;text-transform:uppercase;font-weight:700;color:#f4f4ef;background:#1a1a1a;border-radius:999px;padding:.38rem .9rem;margin-bottom:1.1rem}
.proj-lead-title{font-family:'DM Serif Display',serif;font-size:clamp(1.8rem,3.4vw,2.7rem);line-height:1.08;color:#0a0a0a;text-decoration:none;text-align:center;margin-bottom:1rem;transition:color .2s}
.proj-lead-title:hover{color:#555}
.proj-lead-deck{font-size:.72rem;line-height:2;color:#3a3a3a;margin-bottom:1.3rem}
.proj-lead-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem;padding:1.1rem 0;margin-bottom:1.3rem;border-top:1px solid #d8d8d2;border-bottom:1px solid #d8d8d2}
.proj-stat{display:flex;flex-direction:column;gap:.25rem}
.proj-stat-val{font-family:'DM Serif Display',serif;font-size:.92rem;color:#0a0a0a;line-height:1.05}
.proj-stat-label{font-size:.4rem;letter-spacing:1.5px;text-transform:uppercase;color:#555}
.proj-lead .proj-tags{margin-bottom:1.4rem}
.proj-readmore{align-self:center;padding:.72rem 1.7rem;border:1px solid #1a1a1a;border-radius:999px;font-size:.46rem;letter-spacing:2.5px;text-transform:uppercase;color:#111;text-decoration:none;background:none;transition:background .2s,color .2s,transform .2s}
.proj-readmore:hover{background:#1a1a1a;color:#f4f4ef;transform:translateY(-1px)}
.proj-post:hover .proj-readmore{background:#1a1a1a;color:#f4f4ef}
.proj-post-cta{margin-top:1.3rem}

.proj-feed-head{display:flex;align-items:center;gap:1rem;margin:2.6rem 0 1.4rem}
.proj-feed-label{font-size:.5rem;letter-spacing:3.5px;text-transform:uppercase;color:#111;font-weight:700;white-space:nowrap}
.proj-feed-rule{flex:1;height:1px;background:#ccc}

.proj-feed{display:flex;flex-direction:column}
.proj-post{display:grid;grid-template-columns:1fr 1fr;gap:2.2rem;align-items:center;padding:1.9rem 0;border-top:1px solid #d8d8d2;text-decoration:none;color:inherit;transition:opacity .2s}
.proj-post:first-child{border-top:none}
.proj-post-media{aspect-ratio:16/10;background:#ecece8;border-radius:14px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.09)}
.proj-post-media img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.proj-post:hover .proj-post-media img{transform:scale(1.04)}
.proj-post-body{display:flex;flex-direction:column;min-width:0}
.proj-post-title{font-family:'DM Serif Display',serif;font-size:1.4rem;line-height:1.18;color:#0a0a0a;text-align:center;margin-bottom:.6rem;transition:color .2s}
.proj-post:hover .proj-post-title{color:#555}
.proj-post-excerpt{font-size:.72rem;line-height:2;color:#3a3a3a;margin-bottom:1rem}
.proj-post-foot{display:flex;flex-wrap:wrap;justify-content:center;align-items:center;gap:.7rem 1rem;margin-top:auto}

.proj-card{display:flex;flex-direction:column;gap:.55rem;text-decoration:none;color:inherit}
.proj-c-img{aspect-ratio:16/9;background:#ecece8;border-radius:14px;overflow:hidden;box-shadow:0 8px 22px rgba(0,0,0,.10);transition:box-shadow .3s,transform .3s cubic-bezier(.2,.7,.2,1)}
.proj-c-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.proj-card:hover .proj-c-img{box-shadow:0 14px 32px rgba(0,0,0,.16);transform:translateY(-3px)}
.proj-card:hover .proj-c-img img{transform:scale(1.05)}
.proj-c-name{font-family:'DM Serif Display',serif;font-size:1.4rem;color:#111;line-height:1.2;text-align:center;margin-top:.4rem;transition:color .2s}
.proj-card:hover .proj-c-name{color:#555}
.proj-c-desc{font-size:.72rem;line-height:2;color:#3a3a3a;flex:1}
.proj-c-tags{display:flex;flex-wrap:wrap;justify-content:center;gap:.3rem;margin-top:.15rem}
.proj-c-tag{font-size:.44rem;letter-spacing:1.5px;text-transform:uppercase;padding:.3rem .72rem;border:1px solid;border-radius:999px;background:transparent;white-space:nowrap;font-weight:700}
.proj-c-cta{align-self:center;margin-top:.9rem;padding:.65rem 1.5rem;border:1px solid #1a1a1a;border-radius:999px;font-size:.44rem;letter-spacing:2.5px;text-transform:uppercase;color:#111;background:none;transition:background .2s,color .2s,transform .2s}
.proj-card:hover .proj-c-cta{background:#1a1a1a;color:#f4f4ef}

.arte-grid{columns:3 280px;column-gap:1.8rem}
.arte-empty{font-size:.62rem;letter-spacing:3px;text-transform:uppercase;color:#bbb;padding:4rem 0;border:1px dashed #ddd;text-align:center}
.arte-piece{break-inside:avoid;margin-bottom:1.8rem;overflow:hidden;border:1px solid #e5e5e5;background:#f7f7f2}
.arte-img-wrap{width:100%;overflow:hidden}
.arte-img-wrap img{display:block;width:100%;height:auto;object-fit:cover}
img.lb-trigger{cursor:zoom-in;transition:opacity .2s}
img.lb-trigger:hover{opacity:.88}

#lightbox{position:fixed;inset:0;z-index:9000;background:rgba(0,0,0,.93);display:none;align-items:center;justify-content:center;cursor:zoom-out}
#lightbox.open{display:flex;animation:lbIn .18s ease}
@keyframes lbIn{from{opacity:0}to{opacity:1}}
#lightbox img{max-width:90vw;max-height:90vh;object-fit:contain;display:block;cursor:default;box-shadow:0 8px 40px rgba(0,0,0,.6)}
#lb-close{position:absolute;top:1.2rem;right:1.4rem;background:none;border:1px solid rgba(255,255,255,.18);color:rgba(255,255,255,.6);font-size:1.1rem;line-height:1;padding:.5rem .7rem;cursor:pointer;transition:all .18s;font-family:'Space Mono',monospace}
#lb-close:hover{color:#fff;border-color:rgba(255,255,255,.55)}

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

footer{padding:1.2rem 4rem;border-top:1px solid #e5e5e5;display:flex;justify-content:space-between;font-size:.46rem;letter-spacing:2px;text-transform:uppercase;color:#aaa}

@keyframes fadeUp{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}

@media(max-width:900px){
  .lang-toggle{top:.8rem;right:.8rem}
  .tab-btn{padding:1rem 1.2rem;font-size:.6rem;letter-spacing:2px;white-space:nowrap;flex-shrink:0}
  .dark-panel,.light-panel{padding:3rem 2rem 4rem}
  .about-layout{grid-template-columns:1fr}
  .about-bottom{grid-template-columns:1fr 1fr}
  .apm-row{grid-template-columns:1fr 1fr}
  .proj-lead{grid-template-columns:1fr;gap:1.6rem}
  .proj-post{grid-template-columns:10rem 1fr;gap:1.3rem}
  .arte-grid{columns:2 240px}
  .ct-socials{gap:.55rem}
  footer{flex-direction:column;gap:.5rem;text-align:center}
}

@media(max-width:600px){
  html{font-size:16px}
  .lang-toggle{top:.6rem;right:.6rem;gap:.2rem}
  .lang-btn{font-size:.6rem;padding:.35rem .6rem}
  #hero{height:100svh}
  .hero-name{font-size:clamp(3.5rem,18vw,7rem);letter-spacing:-1px;line-height:.9}
  .tab-btn{padding:1.1rem 1.4rem;font-size:.7rem;letter-spacing:2px;white-space:nowrap;flex-shrink:0}
  .dark-panel,.light-panel{padding:2.5rem 1.2rem 3.5rem}
  .sec-title{font-size:clamp(2.5rem,12vw,5rem)}
  .about-bottom{grid-template-columns:1fr}
  .apm-row{grid-template-columns:1fr}
  .apm-row .proj-card--featured{grid-column:span 1}
  .proj-lead-stats{grid-template-columns:repeat(2,1fr)}
  .proj-post{grid-template-columns:1fr;gap:1rem}
  .proj-post-media{aspect-ratio:16/9}
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

@media(max-width:380px){
  html{font-size:14px}
  .tab-btn{padding:1rem 1.2rem;font-size:.65rem}
}
</style>"""
