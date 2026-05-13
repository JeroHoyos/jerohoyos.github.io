def build_css():
    return """<style>
*{margin:0;padding:0;box-sizing:border-box}
html{font-size:20px;scroll-behavior:smooth;overflow-x:hidden}
:root{--black:#050505;--white:#f4f4ef;--gray:#666}
body{background:#f4f4ef;color:var(--black);font-family:'Space Mono',monospace;overflow-x:hidden;-webkit-text-size-adjust:100%}

/* LANG TOGGLE */
.lang-toggle{position:fixed;top:1.2rem;right:1.5rem;z-index:200;display:flex;gap:.3rem}
.lang-btn{font-family:'Space Mono',monospace;font-size:.46rem;letter-spacing:2.5px;text-transform:uppercase;padding:.38rem .7rem;background:none;border:1px solid #ccc;color:#999;cursor:pointer;transition:all .2s}
.lang-btn.active{border-color:#555;color:var(--black)}
.lang-btn:hover{border-color:#888;color:#555}

/* HERO */
#hero{height:65vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;position:relative;overflow:hidden;background:var(--black)}
#hero canvas{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none}
.hero-inner{position:relative;z-index:2}
.hero-name{font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,8vw,8rem);line-height:.88;letter-spacing:-3px;color:var(--white);animation:fadeUp .8s .1s ease both}
.hero-sub{font-family:'DM Serif Display',serif;font-style:italic;font-size:clamp(1.1rem,3.5vw,1.7rem);color:var(--gray);margin-top:2rem;line-height:1.6;animation:fadeUp .8s .2s ease both}
.hero-bottom{position:absolute;bottom:2.5rem;left:0;right:0;display:flex;justify-content:space-between;align-items:flex-end;padding:0 4rem;z-index:2;animation:fadeIn 1.2s .5s ease both}
.hero-socials{display:flex;gap:.8rem;flex-wrap:wrap;justify-content:center}
.hero-socials a{display:inline-flex;align-items:center;gap:.6rem;font-size:.75rem;letter-spacing:2.5px;text-transform:uppercase;color:#ccc;text-decoration:none;padding:.85rem 1.6rem;border:1px solid #333;background:rgba(255,255,255,0.06);backdrop-filter:blur(6px);transition:all .25s;position:relative;overflow:hidden}
.hero-socials a::before{content:'';position:absolute;inset:0;background:var(--white);transform:scaleX(0);transform-origin:left;transition:transform .3s cubic-bezier(.76,0,.24,1);z-index:0}
.hero-socials a:hover::before{transform:scaleX(1)}
.hero-socials a:hover{color:var(--black);border-color:var(--white)}
.hero-socials a svg,.hero-socials a span{position:relative;z-index:1}
.hero-socials a svg{width:18px;height:18px;fill:currentColor;flex-shrink:0}

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
.tab-panel.active{display:block}
.tab-panel>canvas{position:absolute;inset:0;z-index:0;pointer-events:none;display:block;width:100%;height:100%}
.panel-content{position:relative;z-index:2}
.dark-panel{background:rgba(244,244,239,0.78);padding:5rem 4rem 6rem}
.light-panel{background:rgba(244,244,239,0.62);color:var(--black);padding:5rem 4rem 6rem}
.sec-label{font-size:.52rem;letter-spacing:4px;text-transform:uppercase;color:var(--gray);margin-bottom:.8rem}
.sec-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,7vw,7rem);letter-spacing:1px;line-height:.9;margin-bottom:.8rem}
.sec-sub{font-size:.65rem;color:#666;max-width:52rem;line-height:1.9;margin-bottom:3rem}
#panel-projects .panel-content{background:rgba(244,244,239,0.38)}
#panel-projects .sec-title,#panel-blog .sec-title,#panel-arte .sec-title{text-align:center}
#panel-projects .sec-sub,#panel-blog .sec-sub,#panel-arte .sec-sub{text-align:center;margin-left:auto;margin-right:auto}

/* ABOUT */
.about-layout{display:grid;grid-template-columns:1fr 1.15fr;gap:1.5rem 5rem;align-items:start}
.about-bottom{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:3rem;padding-top:1.2rem;border-top:2px solid #999;align-items:start}
.idioma-item{display:flex;justify-content:space-between;align-items:baseline;padding:.45rem 0;border-bottom:1px solid #eee}
.idioma-item:last-child{border-bottom:none}
.idioma-name{font-size:.65rem;color:#222}
.idioma-level{font-size:.48rem;letter-spacing:2px;text-transform:uppercase;color:#888}
.about-preview{grid-column:1/-1;padding-top:1.2rem;border-top:2px solid #999}
.apm-row{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-top:.8rem}
.apm-tags{display:flex;flex-wrap:wrap;gap:.3rem}
.apm-ver-mas{display:block;margin-top:1.2rem;text-align:center;padding:.9rem;border:1px solid #ccc;font-size:.48rem;letter-spacing:2.5px;text-transform:uppercase;color:#666;cursor:pointer;background:none;font-family:'Space Mono',monospace;width:100%;transition:border-color .2s,color .2s,background .2s}
.apm-ver-mas:hover{border-color:#555;color:#111;background:rgba(0,0,0,.04)}
.about-contact{grid-column:1/-1;padding-top:1.2rem;border-top:2px solid #999}
.ac-socials{display:flex;gap:.6rem;flex-wrap:wrap;margin-bottom:1.2rem}
.ac-soc{display:inline-flex;align-items:center;gap:.5rem;font-size:.5rem;letter-spacing:2px;text-transform:uppercase;color:#666;text-decoration:none;padding:.75rem 1.3rem;border:1px solid #ddd;transition:border-color .2s,color .2s,background .2s}
.ac-soc:hover{border-color:#888;color:#111;background:rgba(0,0,0,.03)}
.ac-soc svg{width:14px;height:14px;fill:currentColor;flex-shrink:0}
.ac-label{font-size:.36rem;letter-spacing:3px;text-transform:uppercase;color:#bbb}
.ac-name{font-family:'DM Serif Display',serif;font-size:1rem;color:#111;margin:.2rem 0}
.ac-val{font-size:.46rem;color:#888;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.ac-arrow{font-size:.85rem;color:#ccc;margin-top:auto;padding-top:.9rem;transition:color .2s}
.ac-card:hover .ac-arrow{color:#111}
.about-sub-label{font-size:.7rem;letter-spacing:4px;text-transform:uppercase;color:#555;margin-bottom:1.4rem}
.about-bio p{font-size:.85rem;line-height:2.4;color:#2a2a2a;margin-bottom:1.2rem}
.about-bio strong{color:var(--black)}

/* STACK */
.stack-tier{margin-bottom:1.8rem}
.stack-tier-label{font-size:.5rem;letter-spacing:3px;text-transform:uppercase;color:#888;margin-bottom:.8rem;display:flex;align-items:center;gap:.5rem}
.stack-tier-label span{flex:1;height:1px;background:#ddd}
.stack-chips{display:flex;flex-wrap:wrap;gap:.4rem}
.chip{font-size:.52rem;letter-spacing:1.5px;text-transform:uppercase;padding:.35rem .85rem;border:1px solid;transition:background .2s;cursor:default}
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
.explore-btn{font-family:'Space Mono',monospace;font-size:.58rem;letter-spacing:2.5px;text-transform:uppercase;padding:.85rem 1.8rem;background:none;border:1px solid #222;color:#111;cursor:pointer;transition:all .2s;position:relative;overflow:hidden}
.explore-btn::after{content:'';position:absolute;inset:0;background:#111;transform:scaleX(0);transform-origin:left;transition:transform .3s cubic-bezier(.76,0,.24,1);z-index:0}
.explore-btn:hover::after{transform:scaleX(1)}
.explore-btn:hover{color:#f4f4ef}
.explore-btn span,.explore-btn{position:relative;z-index:1}

/* PROJECTS */
.proj-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4rem}
.proj-card{display:flex;flex-direction:column;gap:.5rem;padding:1.3rem 1.5rem;border:1px solid #ddd;text-decoration:none;color:inherit;transition:border-color .2s,background .2s}
#panel-projects .proj-card{border-color:#ccc;background:rgba(232,232,228,0.72)}
#panel-projects .proj-c-name{color:#000}
#panel-projects .proj-c-desc{color:#1a1a1a}
#panel-projects .proj-c-cta{color:#333;border-color:#aaa}
.proj-card--featured{grid-column:span 2}
.proj-card:hover{border-color:#999;background:rgba(0,0,0,.025)}
.proj-c-name{font-family:'DM Serif Display',serif;font-size:1.3rem;color:#111;line-height:1.2}
.proj-card--featured .proj-c-name{font-size:1.55rem}
.proj-c-desc{font-size:.63rem;color:#555;line-height:1.85;flex:1}
.proj-c-tags{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.1rem}
.proj-c-tag{font-size:.46rem;letter-spacing:1.5px;text-transform:uppercase;padding:.28rem .7rem;border:1px solid;background:transparent;white-space:nowrap}
.proj-c-cta{margin-top:.5rem;padding:.6rem 1rem;border:1px solid #ddd;font-size:.46rem;letter-spacing:2.5px;text-transform:uppercase;color:#888;text-align:center;transition:background .2s,color .2s,border-color .2s}
.proj-card:hover .proj-c-cta{background:rgba(0,0,0,.03);border-color:#888;color:#333}

/* BLOG */
.blog-list{display:flex;flex-direction:column}
.blog-row{display:grid;grid-template-columns:5.5rem 1fr;gap:2rem;padding:2.5rem 0;border-bottom:1px solid #ebebeb;text-decoration:none;color:inherit;transition:background .2s}
.blog-row:first-child{border-top:1px solid #ebebeb}
.blog-row:hover{background:rgba(0,0,0,.018)}
.br-left{padding-top:.2rem}
.br-num{font-family:'Bebas Neue',sans-serif;font-size:2.8rem;color:#e0e0db;line-height:1;margin-bottom:.4rem}
.br-date{font-size:.52rem;letter-spacing:2.5px;text-transform:uppercase;color:#888}
.br-tags{display:flex;gap:.35rem;flex-wrap:wrap;margin-bottom:.9rem}
.br-tag{font-size:.5rem;letter-spacing:2px;text-transform:uppercase;padding:.22rem .55rem;border:1px solid #ccc;color:#555}
.br-title{font-family:'DM Serif Display',serif;font-size:1.4rem;line-height:1.3;color:var(--black);margin-bottom:.7rem;transition:color .2s}
.blog-row:hover .br-title{color:#333}
.br-excerpt{font-size:.7rem;line-height:2;color:#444;margin-bottom:1rem}
.br-read{font-size:.52rem;letter-spacing:2px;text-transform:uppercase;color:#888;transition:color .2s}
.blog-row:hover .br-read{color:var(--black)}

/* ARTE */
.arte-grid{columns:3 280px;column-gap:1.8rem}
.arte-empty{font-size:.62rem;letter-spacing:3px;text-transform:uppercase;color:#bbb;padding:4rem 0;border:1px dashed #ddd;text-align:center}
.arte-piece{break-inside:avoid;margin-bottom:1.8rem;overflow:hidden;border:1px solid #e5e5e5;background:#f7f7f2}
.arte-img-wrap{width:100%;overflow:hidden}
.arte-img-wrap img{display:block;width:100%;height:auto;object-fit:cover}

/* CONTACT */
.ct-header{text-align:center;margin-bottom:1.6rem}
.ct-big{color:#0a0a0a;margin-bottom:.8rem}
.ct-sub{font-size:.58rem;color:#444;max-width:44rem;margin:0 auto;line-height:1.8}
.ct-form-wrap{max-width:42rem;margin:0 auto}
.cf-wrap{background:transparent;border:none;padding:0}
.cf-label{display:flex;flex-direction:column;gap:.3rem;font-size:.44rem;letter-spacing:2px;text-transform:uppercase;color:#333;margin-bottom:.65rem}
.cf-label input,.cf-label textarea{background:transparent;border:1px solid #888;color:#0a0a0a;padding:.65rem .9rem;font-family:'Space Mono',monospace;font-size:.53rem;outline:none;transition:border-color .2s;resize:vertical}
.cf-label input:focus,.cf-label textarea:focus{border-color:#111}
.cf-btn{width:100%;padding:.85rem;background:transparent;color:#0a0a0a;border:1px solid #888;font-family:'Space Mono',monospace;font-size:.48rem;letter-spacing:2.5px;text-transform:uppercase;cursor:pointer;transition:border-color .2s,color .2s,background .2s;margin-top:.2rem}
.cf-btn:hover{border-color:#111;color:#0a0a0a;background:rgba(0,0,0,.04)}
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
  .proj-grid{grid-template-columns:1fr 1fr}
  .proj-card--featured{grid-column:span 2}
  .blog-row{grid-template-columns:4rem 1fr;gap:1.2rem}
  .hero-bottom{padding:0 1.5rem}
  .arte-grid{columns:2 240px}
  .ct-form-wrap{max-width:100%}
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
  .tab-btn{padding:.85rem 1rem;font-size:.55rem;letter-spacing:2px;white-space:nowrap;flex-shrink:0}
  .dark-panel,.light-panel{padding:2.5rem 1.2rem 3.5rem}
  .sec-title{font-size:clamp(2.5rem,12vw,5rem)}
  .about-bottom{grid-template-columns:1fr}
  .apm-row{grid-template-columns:1fr}
  .apm-row .proj-card--featured{grid-column:span 1}
  .proj-grid{grid-template-columns:1fr}
  .proj-card--featured{grid-column:span 1}
  .blog-row{grid-template-columns:1fr;gap:.6rem}
  .br-left{display:flex;align-items:baseline;gap:1rem;margin-bottom:.5rem}
  .br-num{font-size:2rem}
  .arte-grid{columns:1}
  .ct-socials{gap:.5rem}
  .ct-soc{padding:.75rem 1.2rem;font-size:.5rem}
  footer{flex-direction:column;gap:.5rem;padding:1rem 1.2rem;text-align:center}
}

/* SMALL MOBILE ≤380px */
@media(max-width:380px){
  html{font-size:14px}
  .tab-btn{padding:.75rem .85rem;font-size:.55rem}
  .hero-socials a{padding:.6rem .8rem;gap:.4rem}
}
</style>"""
