def _lang_toggle():
    return """
/* ═══ LANGUAGE TOGGLE ═══ */
function setLang(lang) {
  document.querySelectorAll('.lang-btn').forEach(b => b.classList.toggle('active', b.dataset.lang === lang));
  document.querySelectorAll('[data-es]').forEach(el => {
    const txt = el.getAttribute('data-' + lang);
    if (txt !== null) el.innerHTML = txt;
  });
  document.querySelectorAll('.tab-btn').forEach(btn => {
    const t = btn.getAttribute('data-' + lang);
    if (t) btn.textContent = t;
  });
  document.querySelectorAll('.explore-btn').forEach(btn => {
    const t = btn.getAttribute('data-' + lang);
    if (t) btn.textContent = t;
  });
}
document.querySelectorAll('.lang-btn').forEach(btn => {
  btn.addEventListener('click', () => setLang(btn.dataset.lang));
});"""


def _tabs():
    return """
/* ═══ TABS ═══ */
document.getElementById('scroll-cta').addEventListener('click', () => {
  document.getElementById('shell').scrollIntoView({ behavior: 'smooth', block: 'start' });
});
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.dataset.tab;
    document.querySelectorAll('.tab-btn').forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected','false'); });
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    btn.classList.add('active'); btn.setAttribute('aria-selected','true');
    document.getElementById('panel-' + id).classList.add('active');
    const sh=document.getElementById('shell');
    window.scrollTo(0, sh.getBoundingClientRect().top + window.pageYOffset);
  });
});"""


def _conway():
    return """
/* ═══ HERO — Conway's Game of Life ═══ */
(function() {
  const cv = document.getElementById('c-conway'), cx = cv.getContext('2d');
  const SZ = 18; let cols, rows, grid, frame = 0;
  function init() {
    const r = cv.parentElement.getBoundingClientRect();
    cv.width = r.width || window.innerWidth; cv.height = r.height || window.innerHeight;
    cols = Math.ceil(cv.width/SZ); rows = Math.ceil(cv.height/SZ);
    grid = Array.from({length:cols}, () => Array.from({length:rows}, () => Math.random()>.65?1:0));
  }
  function step() {
    const n = Array.from({length:cols}, () => new Array(rows).fill(0));
    for (let x=0;x<cols;x++) for (let y=0;y<rows;y++) {
      let nb=0;
      for (let dx=-1;dx<=1;dx++) for (let dy=-1;dy<=1;dy++) { if(!dx&&!dy) continue; nb+=grid[(x+dx+cols)%cols][(y+dy+rows)%rows]; }
      const c=grid[x][y]; n[x][y]=c?(nb===2||nb===3?1:0):(nb===3?1:0);
    }
    grid=n;
  }
  (function loop() {
    frame++;
    if (frame%5===0) step();
    cx.clearRect(0,0,cv.width,cv.height);
    for (let x=0;x<cols;x++) for (let y=0;y<rows;y++) {
      if (grid[x][y]) { cx.fillStyle='rgba(255,255,255,0.18)'; cx.fillRect(x*SZ+1,y*SZ+1,SZ-2,SZ-2); }
    }
    requestAnimationFrame(loop);
  })();
  init(); window.addEventListener('resize', init);
})();"""


def _delaunay():
    return """
/* ═══ ABOUT — Delaunay Triangulation ═══ */
(function() {
  const cv = document.getElementById('c-delaunay'), cx = cv.getContext('2d');
  let pts=[], W=0, H=0;
  function circ(ax,ay,bx,by,ex,ey) {
    const D=2*(ax*(by-ey)+bx*(ey-ay)+ex*(ay-by));
    if (Math.abs(D)<1e-10) return null;
    const ux=((ax*ax+ay*ay)*(by-ey)+(bx*bx+by*by)*(ey-ay)+(ex*ex+ey*ey)*(ay-by))/D;
    const uy=((ax*ax+ay*ay)*(ex-bx)+(bx*bx+by*by)*(ax-ex)+(ex*ex+ey*ey)*(bx-ax))/D;
    return {x:ux, y:uy, r2:(ax-ux)**2+(ay-uy)**2};
  }
  function delaunay(pts) {
    const N=pts.length, sup=[{x:-9e3,y:-9e3},{x:2e4,y:0},{x:0,y:2e4}], all=[...pts,...sup];
    let tris=[[N,N+1,N+2]];
    for (let i=0;i<N;i++) {
      const p=all[i]; let edges=[];
      tris=tris.filter(t => {
        const cc=circ(all[t[0]].x,all[t[0]].y,all[t[1]].x,all[t[1]].y,all[t[2]].x,all[t[2]].y);
        if (!cc) return true;
        if ((p.x-cc.x)**2+(p.y-cc.y)**2<cc.r2) { edges.push([t[0],t[1]],[t[1],t[2]],[t[2],t[0]]); return false; }
        return true;
      });
      edges.filter(([a,b],idx,arr) => !arr.some(([c,d],j) => idx!==j&&((a===d&&b===c)||(a===c&&b===d)))).forEach(([a,b]) => tris.push([a,b,i]));
    }
    return tris.filter(t => !t.some(v => v>=N));
  }
  function resize() {
    const panel=document.getElementById('panel-about');
    W=panel.offsetWidth||window.innerWidth; H=panel.offsetHeight||window.innerHeight;
    cv.width=W; cv.height=H;
    pts=Array.from({length:48}, () => ({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.55,vy:(Math.random()-.5)*.55}));
  }
  let t=0;
  (function loop() {
    if (!pts.length) { requestAnimationFrame(loop); return; }
    t++; pts.forEach(p => { p.x+=p.vx; p.y+=p.vy; if(p.x<0||p.x>W) p.vx*=-1; if(p.y<0||p.y>H) p.vy*=-1; });
    cx.fillStyle='#f4f4ef'; cx.fillRect(0,0,W,H);
    try {
      const tris=delaunay(pts);
      tris.forEach((tr) => {
        const p0=pts[tr[0]],p1=pts[tr[1]],p2=pts[tr[2]];
        const cx_t=(p0.x+p1.x+p2.x)/3, cy_t=(p0.y+p1.y+p2.y)/3;
        const pulse=Math.sin(cx_t*0.003+cy_t*0.003+t*0.02)*0.5+0.5;
        cx.beginPath(); cx.moveTo(p0.x,p0.y); cx.lineTo(p1.x,p1.y); cx.lineTo(p2.x,p2.y); cx.closePath();
        cx.fillStyle=`rgba(0,0,0,${(pulse*0.03).toFixed(4)})`; cx.fill();
        cx.strokeStyle=`rgba(0,0,0,${(0.08+pulse*0.07).toFixed(3)})`; cx.lineWidth=0.7; cx.stroke();
      });
    } catch(e) {}
    pts.forEach(p => { cx.beginPath(); cx.arc(p.x,p.y,1.8,0,Math.PI*2); cx.fillStyle='rgba(0,0,0,0.18)'; cx.fill(); });
    requestAnimationFrame(loop);
  })();
  resize(); window.addEventListener('resize',resize);
  new MutationObserver(() => { if (document.getElementById('panel-about').classList.contains('active')) resize(); })
    .observe(document.getElementById('panel-about'),{attributes:true,attributeFilter:['class']});
})();"""


def _flow():
    return """
/* ═══ PROJECTS — Flow Field ═══ */
(function() {
  const cv=document.getElementById('c-flow'), cx=cv.getContext('2d');
  let W,H,particles=[],t=0,active=false;
  const NP=900;
  function noise(x,y,t) { return Math.sin(x*.009+t)*Math.cos(y*.007+t*.9)+Math.sin(x*.018-t*.7)*Math.cos(y*.013+t*.4)+Math.sin((x+y)*.005+t)+Math.sin(x*.004-y*.006+t*.3)*0.5; }
  function init() {
    const panel=document.getElementById('panel-projects');
    W=panel.offsetWidth||window.innerWidth; H=panel.offsetHeight||window.innerHeight;
    cv.width=W; cv.height=H;
    particles=Array.from({length:NP}, () => ({x:Math.random()*W,y:Math.random()*H,life:Math.random()*120,maxLife:80+Math.random()*120,w:0.6+Math.random()*1.4}));
    cx.fillStyle='#f4f4ef'; cx.fillRect(0,0,W,H);
  }
  (function loop() {
    requestAnimationFrame(loop);
    if (!active) return;
    cx.fillStyle='rgba(244,244,239,0.018)'; cx.fillRect(0,0,W,H);
    particles.forEach(p => {
      const angle=noise(p.x,p.y,t)*Math.PI*2, speed=2.2;
      const nx=p.x+Math.cos(angle)*speed, ny=p.y+Math.sin(angle)*speed;
      const a=p.life/p.maxLife, fade=a<.08?a/.08:a>.85?(1-a)/.15:1;
      cx.beginPath(); cx.strokeStyle=`rgba(5,5,5,${(0.85*fade).toFixed(3)})`; cx.lineWidth=p.w;
      cx.moveTo(p.x,p.y); cx.lineTo(nx,ny); cx.stroke();
      p.x=nx; p.y=ny; p.life++;
      if (p.life>p.maxLife||p.x<-5||p.x>W+5||p.y<-5||p.y>H+5) { p.x=Math.random()*W; p.y=Math.random()*H; p.life=0; p.maxLife=80+Math.random()*120; }
    });
    t+=0.004;
  })();
  init();
  new MutationObserver(() => { const on=document.getElementById('panel-projects').classList.contains('active'); if(on&&!active){init();active=true;}else if(!on) active=false; })
    .observe(document.getElementById('panel-projects'),{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize', () => { if(active) init(); });
})();"""


def _strange_attractor():
    return """
/* ═══ ARTE — de Jong Attractor ═══ */
(function() {
  const cv=document.getElementById('c-dp'), cx=cv.getContext('2d');
  const offCv=document.createElement('canvas'), offCx=offCv.getContext('2d');
  let W,H,active=false,x,y,a,b,c,d,frames=0;
  function pick() {
    let ok=false;
    while(!ok) {
      a=Math.random()*5-2.5; b=Math.random()*5-2.5;
      c=Math.random()*5-2.5; d=Math.random()*5-2.5;
      let tx=0.1,ty=0.1,rx=0,ry=0;
      for(let i=0;i<600;i++){
        const nx=Math.sin(a*ty)-Math.cos(b*tx),ny=Math.sin(c*tx)-Math.cos(d*ty);
        tx=nx; ty=ny; if(i>300){rx=Math.max(rx,Math.abs(tx));ry=Math.max(ry,Math.abs(ty));}
      }
      if(rx>0.7&&ry>0.7){x=tx;y=ty;ok=true;}
    }
    frames=0;
    const SC=2, gW=Math.ceil(W/SC), gH=Math.ceil(H/SC);
    if(offCv.width!==gW||offCv.height!==gH){offCv.width=gW;offCv.height=gH;}
    const cts=new Float32Array(gW*gH);
    let lx=x,ly=y;
    for(let i=0;i<200000;i++){
      const nx=Math.sin(a*ly)-Math.cos(b*lx),ny=Math.sin(c*lx)-Math.cos(d*ly);
      lx=nx; ly=ny;
      if(i<100) continue;
      const px=Math.floor((lx/2.4+0.5)*gW), py=Math.floor((ly/2.4+0.5)*gH);
      if(px>=0&&px<gW&&py>=0&&py<gH) cts[py*gW+px]++;
    }
    x=lx; y=ly;
    let maxC=1;
    for(let i=0;i<cts.length;i++) if(cts[i]>maxC) maxC=cts[i];
    const im=offCx.createImageData(gW,gH), dd=im.data;
    for(let i=0;i<gW*gH;i++){
      const t2=cts[i]>0?Math.min(1,Math.log(1+cts[i])/Math.log(1+maxC)*1.7):0;
      const col=Math.round(244*(1-t2*0.80));
      dd[i*4]=col; dd[i*4+1]=col; dd[i*4+2]=col; dd[i*4+3]=255;
    }
    offCx.putImageData(im,0,0);
    cx.fillStyle='#f4f4ef'; cx.fillRect(0,0,W,H);
    cx.drawImage(offCv,0,0,W,H);
  }
  function init() {
    W=window.innerWidth; H=window.innerHeight;
    cv.width=W; cv.height=H; pick();
  }
  init();
  (function loop() {
    requestAnimationFrame(loop); if(!active) return;
    cx.fillStyle='rgba(5,5,5,0.025)';
    for(let i=0;i<150;i++){
      const nx=Math.sin(a*y)-Math.cos(b*x),ny=Math.sin(c*x)-Math.cos(d*y);
      x=nx; y=ny; cx.fillRect((x/2.4+0.5)*W-0.75,(y/2.4+0.5)*H-0.75,1.5,1.5);
    }
    if(++frames>1200) pick();
  })();
  new MutationObserver(()=>{
    const on=document.getElementById('panel-arte').classList.contains('active');
    if(on&&!active){
      if(Math.abs(window.innerWidth-W)>80||Math.abs(window.innerHeight-H)>80) init();
      active=true;
    } else if(!on) active=false;
  }).observe(document.getElementById('panel-arte'),{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',()=>{if(active)init();});
})();"""


def _chladni():
    return """
/* ═══ CONTACT — Chladni Figures ═══ */
(function() {
  const cv=document.getElementById('c-fourier'), cx=cv.getContext('2d');
  let W,H,active=false,transT=0,pairIdx=0;
  const PAIRS=[[2,3],[3,2],[4,3],[3,4],[2,5],[5,2],[4,5],[5,4],[3,5],[5,3],[4,7],[7,4]];
  const TRANS=200;
  const off=document.createElement('canvas'), oc=off.getContext('2d');
  function ss(t){return t*t*(3-2*t);}
  function render(m,n) {
    const SC=4, cols=Math.max(1,Math.floor(W/SC)), rows=Math.max(1,Math.floor(H/SC));
    if(off.width!==cols||off.height!==rows){off.width=cols;off.height=rows;}
    const img=oc.createImageData(cols,rows), d=img.data;
    for(let i=0;i<rows;i++){
      const yn=i/rows;
      for(let j=0;j<cols;j++){
        const xn=j/cols;
        const v=Math.sin(m*Math.PI*xn)*Math.sin(n*Math.PI*yn)+Math.sin(n*Math.PI*xn)*Math.sin(m*Math.PI*yn);
        const dark=Math.exp(-v*v*9);
        const col=Math.round(244*(1-dark*0.92));
        const idx=(i*cols+j)*4;
        d[idx]=col;d[idx+1]=col;d[idx+2]=Math.round(col*0.99);d[idx+3]=255;
      }
    }
    oc.putImageData(img,0,0);
    cx.drawImage(off,0,0,W,H);
  }
  function init() {
    const p=document.getElementById('panel-contact');
    W=p.offsetWidth||window.innerWidth; H=p.offsetHeight||window.innerHeight;
    cv.width=W; cv.height=H; transT=0;
  }
  (function loop() {
    requestAnimationFrame(loop); if(!active) return;
    const nextIdx=(pairIdx+1)%PAIRS.length;
    const [m0,n0]=PAIRS[pairIdx],[m1,n1]=PAIRS[nextIdx];
    const a=ss(Math.min(1,transT/TRANS));
    render(m0+(m1-m0)*a, n0+(n1-n0)*a);
    if(++transT>=TRANS){pairIdx=nextIdx;transT=0;}
  })();
  init();
  new MutationObserver(()=>{const on=document.getElementById('panel-contact').classList.contains('active');if(on&&!active){init();active=true;}else if(!on)active=false;}).observe(document.getElementById('panel-contact'),{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',()=>{if(active)init();});
})();"""


def _harmonograph():
    return """
/* ═══ ARTE — Harmonograph ═══ */
(function() {
  const cv=document.getElementById('c-dp'), cx=cv.getContext('2d');
  let W,H,active=false,t,f1,f2,f3,f4,p1,p2,p3,p4,d,prevX,prevY;
  const RATIOS=[[2,3],[3,4],[4,5],[3,5],[5,6],[5,7],[4,7],[2,5],[3,7]];
  const DT=0.03, STEPS=10;
  function newCurve() {
    const [m,n]=RATIOS[Math.floor(Math.random()*RATIOS.length)];
    const e1=0.006+Math.random()*0.028, e2=0.006+Math.random()*0.028;
    f1=m; f2=m+e1; f3=n; f4=n+e2;
    p1=Math.random()*Math.PI*2; p2=Math.random()*Math.PI*2;
    p3=Math.random()*Math.PI*2; p4=Math.random()*Math.PI*2;
    d=0.00020+Math.random()*0.00032; t=0;
    const A=Math.min(W,H)*0.43;
    prevX=W/2+A*(Math.sin(p1)+Math.sin(p2))*0.5;
    prevY=H/2+A*(Math.sin(p3)+Math.sin(p4))*0.5;
    cx.fillStyle='#f4f4ef'; cx.fillRect(0,0,W,H);
  }
  function init() {
    const p=document.getElementById('panel-arte');
    W=p.offsetWidth||window.innerWidth; H=p.offsetHeight||window.innerHeight;
    cv.width=W; cv.height=H; newCurve();
  }
  (function loop() {
    requestAnimationFrame(loop); if(!active) return;
    const A=Math.min(W,H)*0.43;
    for(let s=0;s<STEPS;s++) {
      const e=Math.exp(-d*t); if(e<0.004){newCurve();return;}
      const nx=W/2+A*e*(Math.sin(f1*t+p1)+Math.sin(f2*t+p2))*0.5;
      const ny=H/2+A*e*(Math.sin(f3*t+p3)+Math.sin(f4*t+p4))*0.5;
      cx.beginPath(); cx.moveTo(prevX,prevY); cx.lineTo(nx,ny);
      cx.strokeStyle=`rgba(5,5,5,${(e*0.65).toFixed(3)})`; cx.lineWidth=1.2; cx.stroke();
      prevX=nx; prevY=ny; t+=DT;
    }
  })();
  init();
  new MutationObserver(()=>{const on=document.getElementById('panel-arte').classList.contains('active');if(on&&!active){init();active=true;}else if(!on)active=false;}).observe(document.getElementById('panel-arte'),{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',()=>{if(active)init();});
})();"""


def _fourier_epicycles():
    return """
/* ═══ BLOG — Fourier Epicycles ═══ */
(function() {
  const cv=document.getElementById('c-scatter'), cx=cv.getContext('2d');
  let W,H,active=false,grps=[];
  function mkGrp(){
    const nh=3+Math.floor(Math.random()*4);
    const harms=Array.from({length:nh},(_,i)=>({k:i+1,r:1/(i+1),phi:Math.random()*Math.PI*2}));
    const phase=Math.random()*Math.PI*2;
    const sp=(Math.random()>0.5?1:-1)*(0.003+Math.random()*0.004);
    const R=Math.min(W,H)*(0.07+Math.random()*0.12);
    const gx=W*(0.08+Math.random()*0.84), gy=H*(0.1+Math.random()*0.8);
    let px=gx,py=gy;
    for(const{k,r,phi}of harms){px+=R*r*Math.cos(k*phase+phi);py+=R*r*Math.sin(k*phase+phi);}
    return{gx,gy,R,harms,phase,sp,px,py};
  }
  function tip(g,ph){
    let px=g.gx,py=g.gy;
    for(const{k,r,phi}of g.harms){px+=g.R*r*Math.cos(k*ph+phi);py+=g.R*r*Math.sin(k*ph+phi);}
    return[px,py];
  }
  function init(){
    const p=document.getElementById('panel-blog');
    W=p.offsetWidth||window.innerWidth; H=window.innerHeight;
    cv.width=W; cv.height=H;
    cx.fillStyle='#f4f4ef'; cx.fillRect(0,0,W,H);
    grps=Array.from({length:8},mkGrp);
    cx.lineWidth=1.3; cx.strokeStyle='rgba(5,5,5,0.09)';
    grps.forEach(g=>{
      for(let pass=0;pass<12;pass++){
        cx.beginPath();
        for(let i=0;i<=900;i++){
          const ph=(i/900)*Math.PI*2+pass*0.22;
          const[px,py]=tip(g,ph);
          i===0?cx.moveTo(px,py):cx.lineTo(px,py);
        }
        cx.stroke();
      }
    });
  }
  (function loop(){
    requestAnimationFrame(loop); if(!active) return;
    cx.fillStyle='rgba(244,244,239,0.004)'; cx.fillRect(0,0,W,H);
    cx.lineWidth=1.3;
    grps.forEach(g=>{
      g.phase+=g.sp;
      const[nx,ny]=tip(g,g.phase);
      cx.beginPath(); cx.moveTo(g.px,g.py); cx.lineTo(nx,ny);
      cx.strokeStyle='rgba(5,5,5,0.18)'; cx.stroke();
      g.px=nx; g.py=ny;
    });
  })();
  init();
  new MutationObserver(()=>{const on=document.getElementById('panel-blog').classList.contains('active');if(on&&!active){init();active=true;}else if(!on)active=false;}).observe(document.getElementById('panel-blog'),{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',()=>{if(active)init();});
})();"""


def build_js():
    return (
        "<script>"
        + _lang_toggle()
        + _tabs()
        + _conway()
        + _delaunay()
        + _flow()
        + _fourier_epicycles()
        + _chladni()
        + _strange_attractor()
        + "\n</script>"
    )
