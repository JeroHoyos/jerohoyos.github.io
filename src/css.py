def build_css():
    return """<style>
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
:root{--black:#050505;--white:#f4f4ef;--gray:#666;--accent:#76ff7a}
body{background:#f4f4ef;color:var(--black);font-family:'Space Mono',monospace;overflow-x:hidden}

/* LANG TOGGLE */
.lang-toggle{position:fixed;top:1.2rem;right:1.5rem;z-index:200;display:flex;gap:.3rem}
.lang-btn{font-family:'Space Mono',monospace;font-size:.46rem;letter-spacing:2.5px;text-transform:uppercase;padding:.38rem .7rem;background:none;border:1px solid #ccc;color:#999;cursor:pointer;transition:all .2s}
.lang-btn.active{border-color:#555;color:var(--black)}
.lang-btn:hover{border-color:#888;color:#555}

/* HERO */
#hero{height:65vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;position:relative;overflow:hidden;background:var(--black)}
#hero canvas{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0;pointer-events:none}
.hero-inner{position:relative;z-index:2}
.hero-name{font-family:'Bebas Neue',sans-serif;font-size:clamp(4rem,12vw,13rem);line-height:.88;letter-spacing:-3px;color:var(--white);animation:fadeUp .8s .1s ease both}
.hero-sub{font-family:'DM Serif Display',serif;font-style:italic;font-size:clamp(1.1rem,3.5vw,1.7rem);color:var(--gray);margin-top:2rem;line-height:1.6;animation:fadeUp .8s .2s ease both}
.hero-bottom{position:absolute;bottom:2.5rem;left:0;right:0;display:flex;justify-content:space-between;align-items:flex-end;padding:0 4rem;z-index:2;animation:fadeIn 1.2s .5s ease both}
.hero-socials{display:flex;gap:.8rem;flex-wrap:wrap;justify-content:center}
.hero-socials a{display:inline-flex;align-items:center;gap:.6rem;font-size:.75rem;letter-spacing:2.5px;text-transform:uppercase;color:#ccc;text-decoration:none;padding:.85rem 1.6rem;border:1px solid #333;background:rgba(255,255,255,0.06);backdrop-filter:blur(6px);transition:all .25s;position:relative;overflow:hidden}
.hero-socials a::before{content:'';position:absolute;inset:0;background:var(--white);transform:scaleX(0);transform-origin:left;transition:transform .3s cubic-bezier(.76,0,.24,1);z-index:0}
.hero-socials a:hover::before{transform:scaleX(1)}
.hero-socials a:hover{color:var(--black);border-color:var(--white)}
.hero-socials a svg,.hero-socials a span{position:relative;z-index:1}
.hero-socials a svg{width:18px;height:18px;fill:currentColor;flex-shrink:0}
.hero-scroll{font-size:.52rem;letter-spacing:2px;text-transform:uppercase;color:var(--gray);writing-mode:vertical-rl;cursor:pointer;background:none;border:none;font-family:inherit;transition:color .2s}
.hero-scroll:hover{color:var(--white)}

/* SHELL / TABS */
#shell{display:flex;flex-direction:column}
#tab-bar{position:sticky;top:0;z-index:50;background:var(--black);border-bottom:1px solid #222;display:flex;align-items:stretch;flex-wrap:wrap;touch-action:pan-x}
.tab-btn{font-family:'Space Mono',monospace;font-size:.75rem;letter-spacing:3px;text-transform:uppercase;padding:1.6rem 2.4rem;background:none;border:none;color:#555;cursor:pointer;border-right:1px solid #222;transition:color .2s;position:relative}
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
.sec-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,7vw,7rem);letter-spacing:1px;line-height:.9;margin-bottom:3.5rem}

/* ABOUT */
.about-grid{display:grid;grid-template-columns:1fr;gap:5rem;align-items:start}
.about-bio p{font-size:.82rem;line-height:2.3;color:#3a3a3a;margin-bottom:1.1rem}
.about-bio strong{color:var(--black)}

/* STACK */
.stack-section{margin-top:2.8rem}
.stack-header{font-size:.82rem;letter-spacing:3px;text-transform:uppercase;color:#111;margin-bottom:1.4rem;padding-bottom:.6rem;border-bottom:2px solid #222;display:flex;align-items:center;gap:.8rem;font-weight:700}
.stack-tier{margin-bottom:2.2rem}
.stack-tier-label{font-size:.58rem;letter-spacing:3px;text-transform:uppercase;color:#555;margin-bottom:1rem;display:flex;align-items:center;gap:.5rem}
.stack-tier-label span{flex:1;height:1px;background:#aaa}
.stack-chips{display:flex;flex-wrap:wrap;gap:.5rem}
.chip{font-size:.54rem;letter-spacing:1.5px;text-transform:uppercase;padding:.38rem .9rem;border:1px solid;transition:all .2s;cursor:default}
.chip-gpu{border-color:#76b900;color:#4a7a00;background:rgba(118,185,0,.06)}.chip-gpu:hover{background:rgba(118,185,0,.15)}
.chip-ml{border-color:#5588cc;color:#2255aa;background:rgba(85,136,204,.06)}.chip-ml:hover{background:rgba(85,136,204,.15)}
.chip-data{border-color:#cc7700;color:#995500;background:rgba(204,119,0,.06)}.chip-data:hover{background:rgba(204,119,0,.15)}
.chip-lang{border-color:#555;color:#222}.chip-lang:hover{background:rgba(0,0,0,.05)}
.chip-viz{border-color:#9955cc;color:#7733aa;background:rgba(153,85,204,.06)}.chip-viz:hover{background:rgba(153,85,204,.15)}
.chip-ops{border-color:#cc3344;color:#aa2233;background:rgba(204,51,68,.06)}.chip-ops:hover{background:rgba(204,51,68,.15)}
.nvidia-note{font-size:.44rem;letter-spacing:1px;color:#888;line-height:1.8;margin-top:1.2rem;padding:.8rem 1rem;border-left:2px solid #ddd;background:rgba(0,0,0,.02)}
.nvidia-note strong{color:#76b900}

/* SKILLS */
.skills-section{margin-top:2rem}
.skills-group{margin-bottom:2rem}
.skills-group-label{font-size:.46rem;letter-spacing:3px;text-transform:uppercase;color:#999;margin-bottom:.9rem;padding-bottom:.4rem;border-bottom:1px solid #ddd}
.skill-row{display:flex;align-items:center;gap:.8rem;margin-bottom:.7rem}
.skill-name{font-size:.56rem;letter-spacing:1px;color:#333;min-width:130px}
.skill-bar-wrap{flex:1;height:1px;background:#ddd;position:relative}
.skill-bar{height:1px;background:#333}
.skill-years{font-size:.44rem;letter-spacing:1px;color:#bbb;min-width:50px;text-align:right;white-space:nowrap}

/* EDUCATION */
.edu-strip{margin-top:2.8rem;border-top:1px solid #e5e5e5;padding-top:2rem}
.edu-strip-label{font-size:.82rem;letter-spacing:3px;text-transform:uppercase;color:#111;margin-bottom:1.4rem;font-weight:700}
.edu-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem}
.edu-item{border-left:2px solid #e5e5e5;padding-left:1rem}
.edu-year{font-size:.54rem;letter-spacing:2px;color:#555;margin-bottom:.3rem}
.edu-name{font-family:'DM Serif Display',serif;font-size:1.1rem;color:var(--black);margin-bottom:.2rem}
.edu-inst{font-size:.62rem;color:#444}
.explore-btn{font-family:'Space Mono',monospace;font-size:.6rem;letter-spacing:2.5px;text-transform:uppercase;padding:.9rem 2rem;background:none;border:1px solid #222;color:#111;cursor:pointer;transition:all .2s;position:relative;overflow:hidden}
.explore-btn::after{content:'';position:absolute;inset:0;background:#111;transform:scaleX(0);transform-origin:left;transition:transform .3s cubic-bezier(.76,0,.24,1);z-index:0}
.explore-btn:hover::after{transform:scaleX(1)}
.explore-btn:hover{color:#f4f4ef}
.explore-btn span,.explore-btn{position:relative;z-index:1}
.about-item{border-top:1px solid #ddd;padding:1.7rem 0}
.a-num{font-size:.44rem;letter-spacing:3px;text-transform:uppercase;color:#ccc;margin-bottom:.5rem}
.a-title{font-family:'DM Serif Display',serif;font-size:1.15rem;margin-bottom:.6rem;color:var(--black)}
.a-desc{font-size:.58rem;color:#666;line-height:1.9}
.a-tools{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.7rem}
.a-tool{font-size:.4rem;letter-spacing:1.5px;text-transform:uppercase;padding:.18rem .48rem;border:1px solid #ddd;color:#aaa}

/* PROJECTS */
.proj-grid{display:grid;grid-template-columns:1fr 1fr;gap:1px;border:1px solid #ddd}
.proj-card{padding:2.5rem 2rem;border:1px solid #ddd;text-decoration:none;color:inherit;position:relative;overflow:hidden;display:block}
.proj-card::after{content:'';position:absolute;inset:0;background:var(--black);transform:scaleY(0);transform-origin:bottom;transition:transform .45s cubic-bezier(.76,0,.24,1);z-index:0}
.proj-card:hover::after{transform:scaleY(1)}
.proj-card:hover .p-lang,.proj-card:hover .p-title,.proj-card:hover .p-desc,.proj-card:hover .p-meta,.proj-card:hover .p-arrow{color:var(--white)!important}
.proj-card:hover .p-badge{border-color:#555;color:#aaa}
.p-lang{font-size:.46rem;letter-spacing:3px;text-transform:uppercase;color:var(--gray);margin-bottom:1.2rem;position:relative;z-index:1;transition:color .3s}
.p-title{font-family:'DM Serif Display',serif;font-size:1.15rem;margin-bottom:.8rem;position:relative;z-index:1;transition:color .3s}
.p-desc{font-size:.58rem;color:#555;line-height:1.9;position:relative;z-index:1;transition:color .3s}
.p-badges{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:1rem;position:relative;z-index:1}
.p-badge{font-size:.41rem;letter-spacing:1.5px;text-transform:uppercase;padding:.22rem .55rem;border:1px solid #ccc;color:#888;transition:all .3s}
.p-meta{margin-top:1.2rem;font-size:.5rem;color:#3a3a3a;position:relative;z-index:1;transition:color .3s;display:flex;align-items:center;gap:.8rem}
.p-metric{font-size:.46rem;color:#666;font-style:italic}
.p-arrow{position:absolute;top:1.8rem;right:1.8rem;font-size:1rem;color:#222;transition:transform .3s,color .3s;z-index:1}
.proj-card:hover .p-arrow{transform:translate(3px,-3px)}
.proj-star{grid-column:1/-1;border:1px solid #ddd;padding:3rem 2.5rem;position:relative;overflow:hidden;text-decoration:none;color:inherit;display:block}
.proj-star::before{content:'FEATURED';position:absolute;top:1.2rem;right:1.8rem;font-size:.41rem;letter-spacing:3px;color:#aaa}
.proj-star::after{content:'';position:absolute;inset:0;background:var(--black);transform:scaleY(0);transform-origin:bottom;transition:transform .5s cubic-bezier(.76,0,.24,1);z-index:0}
.proj-star:hover::after{transform:scaleY(1)}
.proj-star:hover .p-lang,.proj-star:hover .p-title,.proj-star:hover .proj-star-body,.proj-star:hover .p-meta,.proj-star:hover .p-arrow{color:var(--white)!important}
.proj-star:hover .p-badge{border-color:#555;color:#aaa}
.proj-star:hover .proj-star-stat-label{color:#aaa}
.proj-star:hover .proj-star-stat-val{color:var(--white)}
.proj-star:hover .proj-star-details{border-left-color:#444}
.proj-star:hover .proj-star-stat{border-top-color:#333}
.proj-star-inner{position:relative;z-index:1;display:grid;grid-template-columns:1fr 1.2fr;gap:3rem;align-items:start}
.proj-star-body{font-size:.62rem;line-height:2.1;color:#666;margin-top:1rem;transition:color .3s}
.proj-star-details{border-left:1px solid #ddd;padding-left:2rem}
.proj-star-stat{border-top:1px solid #ddd;padding:1rem 0;display:flex;justify-content:space-between;align-items:center}
.proj-star-stat-label{font-size:.46rem;letter-spacing:2px;text-transform:uppercase;color:#444}
.proj-star-stat-val{font-family:'DM Serif Display',serif;font-size:1rem;color:var(--black)}

/* BLOG */
.blog-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;border:1px solid #ddd}
.blog-article{padding:2.5rem 2rem;border:1px solid #e5e5e5;text-decoration:none;color:inherit;position:relative;overflow:hidden;display:block}
.blog-article::after{content:'';position:absolute;inset:0;background:var(--black);transform:scaleY(0);transform-origin:bottom;transition:transform .45s cubic-bezier(.76,0,.24,1);z-index:0}
.blog-article:hover::after{transform:scaleY(1)}
.blog-article:hover .ba-date,.blog-article:hover .ba-title,.blog-article:hover .ba-excerpt,.blog-article:hover .ba-read{color:var(--white)!important}
.blog-article:hover .ba-tag{border-color:#555!important;color:#aaa!important}
.ba-date{font-size:.46rem;letter-spacing:3px;text-transform:uppercase;color:var(--gray);margin-bottom:1rem;position:relative;z-index:1;transition:color .3s}
.ba-tags{display:flex;gap:.4rem;flex-wrap:wrap;margin-bottom:1rem;position:relative;z-index:1}
.ba-tag{font-size:.41rem;letter-spacing:2px;text-transform:uppercase;padding:.22rem .55rem;border:1px solid #ccc;color:#888;transition:all .3s}
.ba-title{font-family:'DM Serif Display',serif;font-size:1.1rem;line-height:1.35;color:var(--black);margin-bottom:1.2rem;position:relative;z-index:1;transition:color .3s}
.ba-excerpt{font-size:.56rem;line-height:1.95;color:#555;position:relative;z-index:1;transition:color .3s;margin-bottom:1.8rem}
.ba-read{font-size:.46rem;letter-spacing:2px;text-transform:uppercase;color:#444;position:relative;z-index:1;transition:color .3s}
.ba-num{position:absolute;bottom:1rem;right:1.5rem;font-family:'Bebas Neue',sans-serif;font-size:5rem;color:rgba(0,0,0,.04);line-height:1;z-index:0;pointer-events:none}
.blog-article:hover .ba-num{color:rgba(255,255,255,.04)}

/* ARTE */
.arte-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(480px,1fr));gap:3rem}
.arte-empty{font-size:.62rem;letter-spacing:3px;text-transform:uppercase;color:#bbb;padding:4rem 0;border:1px dashed #ddd;text-align:center}
.arte-piece{border:1px solid #e5e5e5;overflow:hidden;background:#f7f7f2}
.arte-img-wrap{width:100%;overflow:hidden;min-height:320px}
.arte-img-wrap img{display:block;width:100%;height:100%;min-height:320px;object-fit:cover}
.arte-caption{padding:.9rem 1.2rem;display:flex;align-items:baseline;gap:1rem}
.arte-caption-year{font-size:.4rem;letter-spacing:3px;text-transform:uppercase;color:#bbb;white-space:nowrap}
.arte-caption-title{font-family:'DM Serif Display',serif;font-size:1rem;color:var(--black)}

/* CONTACT */
.contact-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:4rem 0}
.contact-big{font-family:'Bebas Neue',sans-serif;font-size:clamp(3rem,10vw,11rem);letter-spacing:-2px;color:var(--black);margin-bottom:1.5rem;line-height:.9}
.contact-email{font-family:'DM Serif Display',serif;font-style:italic;font-size:clamp(.9rem,2vw,1.4rem);color:var(--gray);text-decoration:none;display:block;margin-bottom:2rem;transition:color .2s}
.contact-email:hover{color:var(--black)}
.contact-cv{display:inline-block;margin-bottom:3rem;font-size:.52rem;letter-spacing:3px;text-transform:uppercase;padding:1rem 2.5rem;border:1px solid #ccc;color:#777;text-decoration:none;transition:all .3s}
.contact-cv:hover{border-color:var(--black);color:var(--black)}
.c-links{display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;margin-top:.5rem}
.c-link{display:inline-flex;align-items:center;gap:.7rem;font-size:.75rem;letter-spacing:2.5px;text-transform:uppercase;padding:1.1rem 2.2rem;border:1px solid #ccc;color:#555;text-decoration:none;background:rgba(0,0,0,0.03);transition:all .3s;position:relative;overflow:hidden}
.c-link::before{content:'';position:absolute;inset:0;background:var(--black);transform:scaleY(0);transform-origin:bottom;transition:transform .35s cubic-bezier(.76,0,.24,1);z-index:0}
.c-link:hover::before{transform:scaleY(1)}
.c-link:hover{color:var(--white);border-color:var(--black)}
.c-link svg,.c-link span{position:relative;z-index:1}
.c-link svg{width:20px;height:20px;fill:currentColor;flex-shrink:0}
.c-link.gh:hover{color:#f4f4ef}.c-link.li:hover{color:#90bce8}.c-link.kg:hover{color:#7adeff}.c-link.em:hover{color:#ddd}

/* KAGGLE */
.kaggle-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;border:1px solid #ddd;margin-bottom:3.5rem}
.kstat{padding:1.8rem 1.5rem;border:1px solid #e5e5e5;text-align:center}
.kstat-val{font-family:'Bebas Neue',sans-serif;font-size:clamp(2rem,4vw,3.5rem);color:var(--black);line-height:1}
.kstat-label{font-size:.44rem;letter-spacing:3px;text-transform:uppercase;color:var(--gray);margin-top:.5rem}
.k-section-label{font-size:.48rem;letter-spacing:4px;text-transform:uppercase;color:var(--gray);margin-bottom:1.2rem;border-bottom:1px solid #ddd;padding-bottom:.8rem}
.k-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1px;border:1px solid #ddd}
.k-card{padding:2rem 1.8rem;border:1px solid #e5e5e5;transition:background .25s}
.k-card:hover{background:#f0f0eb}
.k-card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem;gap:1rem}
.k-card-title{font-family:'DM Serif Display',serif;font-size:1rem;color:var(--black);line-height:1.35}
.k-card-badge{font-size:.41rem;letter-spacing:2px;text-transform:uppercase;padding:.28rem .65rem;border:1px solid;white-space:nowrap}
.k-badge-gold{border-color:#7a5f00;color:#c9a227}.k-badge-silver{border-color:#444;color:#aaa}.k-badge-bronze{border-color:#5a3a1a;color:#b87333}
.k-card-desc{font-size:.57rem;line-height:1.9;color:#555;margin-bottom:1rem}
.k-card-meta{display:flex;justify-content:space-between;font-size:.44rem;letter-spacing:1.5px;text-transform:uppercase;color:#333;margin-bottom:.8rem}
.k-tags{display:flex;flex-wrap:wrap;gap:.3rem}
.k-tag{font-size:.4rem;letter-spacing:1.5px;text-transform:uppercase;padding:.18rem .5rem;border:1px solid #ddd;color:#999}

/* FOOTER */
footer{padding:1.2rem 4rem;border-top:1px solid #e5e5e5;display:flex;justify-content:space-between;font-size:.46rem;letter-spacing:2px;text-transform:uppercase;color:#aaa}

@keyframes fadeUp{from{opacity:0;transform:translateY(28px)}to{opacity:1;transform:none}}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}

/* TABLET */
@media(max-width:900px){
  .lang-toggle{top:.8rem;right:.8rem}
  .tab-btn{padding:1rem 1.2rem;font-size:.6rem;letter-spacing:2px}
  .dark-panel,.light-panel{padding:3rem 1.5rem 4rem}
  .about-grid,.edu-grid,.proj-star-inner{grid-template-columns:1fr}
  .proj-grid{grid-template-columns:1fr}
  .proj-star-details{border-left:none;padding-left:0;border-top:1px solid #ddd;padding-top:1.5rem}
  .blog-grid{grid-template-columns:1fr 1fr}
  .kaggle-stats{grid-template-columns:1fr 1fr}
  .k-grid{grid-template-columns:1fr}
  .hero-bottom{padding:0 1.5rem}
  .arte-grid{grid-template-columns:1fr}
  footer{flex-direction:column;gap:.5rem}
}
@media(max-width:600px){
  .lang-toggle{top:.6rem;right:.6rem;gap:.2rem}
  .lang-btn{font-size:.55rem;padding:.32rem .55rem}
  #hero{height:100svh}
  .hero-name{font-size:clamp(3.2rem,18vw,6rem);letter-spacing:-1px;line-height:.9}
  .hero-sub{font-size:clamp(1rem,4vw,1.3rem);margin-top:1.2rem}
  .hero-bottom{flex-direction:column;align-items:center;gap:1.2rem;bottom:2rem;padding:0 1.2rem}
  .hero-socials a{font-size:.6rem;padding:.65rem 1rem}
  .tab-btn{padding:.8rem .9rem;font-size:.5rem}
  .dark-panel,.light-panel{padding:2.5rem 1.2rem 3.5rem}
  .sec-title{font-size:clamp(2.8rem,12vw,5rem)}
  .blog-grid{grid-template-columns:1fr}
  .kaggle-stats{grid-template-columns:1fr 1fr}
  .contact-big{font-size:clamp(2.8rem,16vw,5rem);letter-spacing:-1px}
  footer{flex-direction:column;gap:.5rem;padding:1rem 1.2rem;font-size:.52rem}
}
</style>"""
