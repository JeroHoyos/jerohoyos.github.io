def _mobile_detect():
    return "const _mob=window.innerWidth<=768||('ontouchstart' in window);\n"


def _lang_toggle():
    return """
/* ═══ LANGUAGE TOGGLE ═══ */
function setLang(lang) {
  document.documentElement.lang = lang;
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
});
/* Email copy button */
(function() {
  const btn = document.getElementById('ct-email-copy');
  if (!btn) return;
  const span = btn.querySelector('span');
  btn.addEventListener('click', () => {
    navigator.clipboard.writeText(btn.dataset.email).then(() => {
      const prev = span.textContent;
      span.textContent = '✓ copiado';
      setTimeout(() => { span.textContent = prev; }, 2000);
    });
  });
})();"""


def _tabs():
    return """
/* ═══ TABS ═══ */
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
  const SZ = _mob?32:18, STEP=_mob?8:5; let cols, rows, grid, frame = 0;
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
    requestAnimationFrame(loop);
    if (document.hidden) return;
    frame++;
    if (frame%STEP===0) step();
    cx.clearRect(0,0,cv.width,cv.height);
    for (let x=0;x<cols;x++) for (let y=0;y<rows;y++) {
      if (grid[x][y]) { cx.fillStyle='rgba(255,255,255,0.18)'; cx.fillRect(x*SZ+1,y*SZ+1,SZ-2,SZ-2); }
    }
  })();
  let _cw=window.innerWidth;
  init();
  window.addEventListener('resize',()=>{ if(Math.abs(window.innerWidth-_cw)>30){_cw=window.innerWidth;init();} });
})();"""


def _delaunay():
    return """
/* ═══ ABOUT — Delaunay Triangulation ═══ */
(function() {
  const cv = document.getElementById('c-delaunay'), cx = cv.getContext('2d');
  let pts=[], W=0, H=0, initialized=false;
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
    const r=panel.getBoundingClientRect();
    W=r.width||panel.offsetWidth||window.innerWidth;
    H=r.height||panel.offsetHeight||window.innerHeight;
    if(W<10||H<10) return; // panel oculto, no reinicializar
    cv.width=W; cv.height=H;
    pts=Array.from({length:_mob?20:48}, () => ({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-.5)*.55,vy:(Math.random()-.5)*.55}));
  }
  let t=0;
  (function loop() {
    if (!pts.length || document.hidden) { requestAnimationFrame(loop); return; }
    t++; pts.forEach(p => { p.x+=p.vx; p.y+=p.vy; if(p.x<0||p.x>W) p.vx*=-1; if(p.y<0||p.y>H) p.vy*=-1; });
    cx.fillStyle='#f4f4ef'; cx.fillRect(0,0,W,H);
    try {
      const tris=delaunay(pts);
      tris.forEach((tr) => {
        const p0=pts[tr[0]],p1=pts[tr[1]],p2=pts[tr[2]];
        const mx=(p0.x+p1.x+p2.x)/3, my=(p0.y+p1.y+p2.y)/3;
        const pulse=Math.sin(mx*0.003+my*0.003+t*0.02)*0.5+0.5;
        cx.beginPath(); cx.moveTo(p0.x,p0.y); cx.lineTo(p1.x,p1.y); cx.lineTo(p2.x,p2.y); cx.closePath();
        cx.fillStyle=`rgba(0,0,0,${(pulse*0.03).toFixed(4)})`; cx.fill();
        cx.strokeStyle=`rgba(0,0,0,${(0.08+pulse*0.07).toFixed(3)})`; cx.lineWidth=0.7; cx.stroke();
      });
    } catch(e) {}
    pts.forEach(p => { cx.beginPath(); cx.arc(p.x,p.y,1.8,0,Math.PI*2); cx.fillStyle='rgba(0,0,0,0.18)'; cx.fill(); });
    requestAnimationFrame(loop);
  })();
  resize(); window.addEventListener('resize',resize);
  new MutationObserver(() => { if (document.getElementById('panel-about').classList.contains('active')&&!initialized){resize();initialized=true;} })
    .observe(document.getElementById('panel-about'),{attributes:true,attributeFilter:['class']});
})();"""


def _flow():
    return """
/* ═══ PROJECTS — Flow Field ═══ */
(function() {
  const cv=document.getElementById('c-flow'), cx=cv.getContext('2d');
  let W,H,particles=[],t=0,active=false,initialized=false;
  const NP=_mob?200:900;
  function noise(x,y,t) { return _mob ? Math.sin(x*.009+t)*Math.cos(y*.007+t*.9)+Math.sin((x+y)*.005+t) : Math.sin(x*.009+t)*Math.cos(y*.007+t*.9)+Math.sin(x*.018-t*.7)*Math.cos(y*.013+t*.4)+Math.sin((x+y)*.005+t)+Math.sin(x*.004-y*.006+t*.3)*0.5; }
  function init() {
    const panel=document.getElementById('panel-projects');
    W=panel.offsetWidth||window.innerWidth; H=panel.offsetHeight||window.innerHeight;
    cv.width=W; cv.height=H;
    particles=Array.from({length:NP}, () => ({x:Math.random()*W,y:Math.random()*H,life:Math.random()*120,maxLife:80+Math.random()*120,w:0.6+Math.random()*1.4}));
    cx.fillStyle='#f4f4ef'; cx.fillRect(0,0,W,H);
  }
  (function loop() {
    requestAnimationFrame(loop);
    if (!active || document.hidden) return;
    cx.fillStyle='rgba(244,244,239,0.018)'; cx.fillRect(0,0,W,H);
    particles.forEach(p => {
      const angle=noise(p.x,p.y,t)*Math.PI*2, speed=2.2;
      const nx=p.x+Math.cos(angle)*speed, ny=p.y+Math.sin(angle)*speed;
      const a=p.life/p.maxLife, fade=a<.08?a/.08:a>.85?(1-a)/.15:1;
      cx.beginPath(); cx.strokeStyle=`rgba(5,5,5,${(0.3*fade).toFixed(3)})`; cx.lineWidth=p.w;
      cx.moveTo(p.x,p.y); cx.lineTo(nx,ny); cx.stroke();
      p.x=nx; p.y=ny; p.life++;
      if (p.life>p.maxLife||p.x<-5||p.x>W+5||p.y<-5||p.y>H+5) { p.x=Math.random()*W; p.y=Math.random()*H; p.life=0; p.maxLife=80+Math.random()*120; }
    });
    t+=0.004;
  })();
  let _cw=window.innerWidth;
  init(); initialized=true;
  new MutationObserver(() => { const on=document.getElementById('panel-projects').classList.contains('active'); if(on&&!active){if(!initialized){init();initialized=true;}active=true;}else if(!on) active=false; })
    .observe(document.getElementById('panel-projects'),{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',()=>{ if(active&&Math.abs(window.innerWidth-_cw)>30){_cw=window.innerWidth;init();} });
})();"""

def _chladni():
    return """
/* ═══ CONTACT — Chladni Figures ═══ */
(function() {
  const cv=document.getElementById('c-fourier'), cx=cv.getContext('2d');
  let W,H,active=false,initialized=false,transT=0,pairIdx=0;
  const PAIRS=[[2,3],[3,2],[4,3],[3,4],[2,5],[5,2],[4,5],[5,4],[3,5],[5,3],[4,7],[7,4]];
  const TRANS=200;
  const off=document.createElement('canvas'), oc=off.getContext('2d');
  function ss(t){return t*t*(3-2*t);}
  function render(m,n) {
    const SC=_mob?10:4, cols=Math.max(1,Math.floor(W/SC)), rows=Math.max(1,Math.floor(H/SC));
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
    requestAnimationFrame(loop); if(!active || document.hidden) return;
    const nextIdx=(pairIdx+1)%PAIRS.length;
    const [m0,n0]=PAIRS[pairIdx],[m1,n1]=PAIRS[nextIdx];
    const a=ss(Math.min(1,transT/TRANS));
    render(m0+(m1-m0)*a, n0+(n1-n0)*a);
    if(++transT>=TRANS){pairIdx=nextIdx;transT=0;}
  })();
  let _cw=window.innerWidth;
  init(); initialized=true;
  new MutationObserver(()=>{const on=document.getElementById('panel-contact').classList.contains('active');if(on&&!active){if(!initialized){init();initialized=true;}active=true;}else if(!on)active=false;}).observe(document.getElementById('panel-contact'),{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',()=>{if(active&&Math.abs(window.innerWidth-_cw)>30){_cw=window.innerWidth;init();}});
})();"""


def _particles():
    return """
/* ═══ ARTE — Campo de partículas con atractores ═══ */
(function(){
  const cv=document.getElementById('c-dp'),cx=cv.getContext('2d');
  let W,H,active=false,initialized=false,t=0,pts=[];
  const N=_mob?200:900;

  function init(){
    const p=document.getElementById('panel-arte');
    W=p.offsetWidth||window.innerWidth;H=p.offsetHeight||window.innerHeight;
    cv.width=W;cv.height=H;
    pts=Array.from({length:N},()=>({
      x:Math.random()*W,y:Math.random()*H,
      vx:0,vy:0,
      life:Math.floor(Math.random()*200),
      max:120+Math.random()*180,
      w:0.4+Math.random()*1.1
    }));
    cx.fillStyle='#f4f4ef';cx.fillRect(0,0,W,H);
  }

  function noise(x,y,t){
    return Math.sin(x*0.0055+t)*Math.cos(y*0.0048+t*0.79)
          +Math.sin(x*0.012-t*0.63)*Math.cos(y*0.0095+t*0.31)
          +Math.sin((x-y)*0.0038+t*0.47)*0.55
          +Math.sin(x*0.0021+y*0.003-t*0.19)*0.3;
  }

  function forces(px,py,t){
    const a1x=W*0.5+Math.cos(t*0.37)*W*0.28,a1y=H*0.5+Math.sin(t*0.37)*H*0.23;
    const a2x=W*0.5+Math.cos(t*0.23+2.1)*W*0.21,a2y=H*0.5+Math.sin(t*0.29+1.0)*H*0.26;
    const a3x=W*0.5+Math.cos(t*0.51+4.2)*W*0.14,a3y=H*0.5+Math.sin(t*0.44+3.1)*H*0.14;
    let fx=0,fy=0;
    for(const [ax,ay,str] of [[a1x,a1y,14000],[a2x,a2y,10000],[a3x,a3y,7000]]){
      const dx=ax-px,dy=ay-py,d2=dx*dx+dy*dy+600;
      fx+=dx/d2*str;fy+=dy/d2*str;
    }
    return [fx,fy];
  }

  (function loop(){
    requestAnimationFrame(loop);if(!active||document.hidden)return;
    t+=0.005;
    cx.fillStyle='rgba(244,244,239,0.028)';cx.fillRect(0,0,W,H);
    for(const p of pts){
      const angle=noise(p.x,p.y,t)*Math.PI*2;
      const [fx,fy]=forces(p.x,p.y,t);
      p.vx=p.vx*0.91+Math.cos(angle)*1.6+fx*0.014;
      p.vy=p.vy*0.91+Math.sin(angle)*1.6+fy*0.014;
      const spd=Math.sqrt(p.vx*p.vx+p.vy*p.vy);
      if(spd>4.5){p.vx=p.vx/spd*4.5;p.vy=p.vy/spd*4.5;}
      const nx=p.x+p.vx,ny=p.y+p.vy;
      p.life++;
      const age=p.life/p.max,fade=age<0.08?age/0.08:age>0.82?(1-age)/0.18:1;
      cx.beginPath();cx.moveTo(p.x,p.y);cx.lineTo(nx,ny);
      cx.strokeStyle=`rgba(5,5,5,${(0.62*fade).toFixed(3)})`;
      cx.lineWidth=p.w;cx.stroke();
      p.x=nx;p.y=ny;
      if(p.life>p.max||nx<-8||nx>W+8||ny<-8||ny>H+8){
        p.x=Math.random()*W;p.y=Math.random()*H;
        p.vx=0;p.vy=0;p.life=0;p.max=120+Math.random()*180;
      }
    }
  })();

  let _cw=window.innerWidth;
  init(); initialized=true;
  new MutationObserver(()=>{const on=document.getElementById('panel-arte').classList.contains('active');if(on&&!active){if(!initialized){init();initialized=true;}active=true;}else if(!on)active=false;}).observe(document.getElementById('panel-arte'),{attributes:true,attributeFilter:['class']});
  window.addEventListener('resize',()=>{if(active&&Math.abs(window.innerWidth-_cw)>30){_cw=window.innerWidth;init();}});
})();"""


def _euler_helix():
    return """
/* ═══ BLOG — Lorenz Attractor (estilo Manim, fondo negro) ═══ */
(function() {
  const cv=document.getElementById('c-scatter'), cx=cv.getContext('2d');
  let W,H,active=false,initialized=false,animId=null;

  // Parámetros clásicos de Lorenz
  const SIGMA=10, RHO=28, BETA=8/3;
  const DT=0.006;
  // Vista 3D fija — ángulo similar al del video (desde arriba-derecha)
  const ROT_Y=2.42, ROT_X=0.38;

  // Dos trayectorias con condiciones iniciales casi idénticas
  const TRAILS=2, MAX_PTS=_mob?500:1800;
  const inits=[[0.1,0.1,20],[0.1+0.001,0.1,20]];
  let states, histories;

  function lorenz(x,y,z){
    return [SIGMA*(y-x), x*(RHO-z)-y, x*y-BETA*z];
  }
  function rk4(x,y,z){
    const [k1x,k1y,k1z]=lorenz(x,y,z);
    const [k2x,k2y,k2z]=lorenz(x+k1x*DT/2,y+k1y*DT/2,z+k1z*DT/2);
    const [k3x,k3y,k3z]=lorenz(x+k2x*DT/2,y+k2y*DT/2,z+k2z*DT/2);
    const [k4x,k4y,k4z]=lorenz(x+k3x*DT,y+k3y*DT,z+k3z*DT);
    return [
      x+(k1x+2*k2x+2*k3x+k4x)*DT/6,
      y+(k1y+2*k2y+2*k3y+k4y)*DT/6,
      z+(k1z+2*k2z+2*k3z+k4z)*DT/6
    ];
  }

  // Proyección 3D → 2D con rotación fija
  function proj(x,y,z){
    // Centrar en el atractor (~0,0,25)
    const cx0=0, cy0=0, cz0=25;
    const rx=x-cx0, ry=y-cy0, rz=z-cz0;
    // Rotación Y
    const cosY=Math.cos(ROT_Y), sinY=Math.sin(ROT_Y);
    const x1=rx*cosY+rz*sinY, z1=-rx*sinY+rz*cosY;
    // Rotación X
    const cosX=Math.cos(ROT_X), sinX=Math.sin(ROT_X);
    const y2=ry*cosX-z1*sinX, z2=ry*sinX+z1*cosX;
    const sc=W*0.014, d=8/(8+z2*0.04);
    return [W/2+x1*sc*d, H/2-y2*sc*d];
  }

  function colorAt(t){
    // t ∈ [0,1] — gris claro → gris muy oscuro
    const v=Math.round(180-t*160);
    return `rgb(${v},${v},${v})`;
  }

  function init(){
    const p=document.getElementById('panel-blog');
    W=p.offsetWidth||window.innerWidth; H=p.offsetHeight||window.innerHeight;
    cv.width=W; cv.height=H;
    states=inits.map(([x,y,z])=>({x,y,z}));
    histories=inits.map(()=>[]);
    // Pre-calcular un tramo para que no empiece vacío
    for(let i=0;i<400;i++){
      states.forEach((s,idx)=>{
        const [nx,ny,nz]=rk4(s.x,s.y,s.z);
        s.x=nx;s.y=ny;s.z=nz;
        histories[idx].push([nx,ny,nz]);
        if(histories[idx].length>MAX_PTS) histories[idx].shift();
      });
    }
  }

  // Dibuja ejes tenues estilo Manim
  function drawAxes(){
    const axLen=22;
    const axes=[
      [[-axLen,0,25],[axLen,0,25]],
      [[0,-axLen,25],[0,axLen,25]],
      [[0,0,25-axLen],[0,0,25+axLen]],
    ];
    axes.forEach(([a,b])=>{
      const [x0,y0]=proj(...a),[x1,y1]=proj(...b);
      cx.beginPath(); cx.moveTo(x0,y0); cx.lineTo(x1,y1);
      cx.strokeStyle='rgba(10,10,10,0.20)'; cx.lineWidth=0.8;
      cx.setLineDash([4,8]); cx.stroke(); cx.setLineDash([]);
    });
    // Marcas de tick
    for(let v=-20;v<=20;v+=10){
      [[[v,0,25],[v,0.6,25]],[[0,v,25],[0.6,v,25]]].forEach(([a,b])=>{
        const [x0,y0]=proj(...a),[x1,y1]=proj(...b);
        cx.beginPath();cx.moveTo(x0,y0);cx.lineTo(x1,y1);
        cx.strokeStyle='rgba(10,10,10,0.25)';cx.lineWidth=0.7;cx.stroke();
      });
    }
  }

  function frame(){
    if(!active||document.hidden){animId=null;return;}

    // Avanzar pasos por frame
    for(let s=0;s<(_mob?1:4);s++){
      states.forEach((st,idx)=>{
        const [nx,ny,nz]=rk4(st.x,st.y,st.z);
        st.x=nx;st.y=ny;st.z=nz;
        histories[idx].push([nx,ny,nz]);
        if(histories[idx].length>MAX_PTS) histories[idx].shift();
      });
    }

    // Fondo del sitio
    cx.fillStyle='#f4f4ef'; cx.fillRect(0,0,W,H);

    drawAxes();

    // Dibujar cada trayectoria
    histories.forEach((hist,ti)=>{
      const n=hist.length;
      if(n<2) return;
      for(let i=1;i<n;i++){
        const age=i/n;
        const t=ti===0?age:1-age; // segunda trayectoria va en dirección inversa del gradiente
        cx.beginPath();
        const [x0,y0]=proj(...hist[i-1]);
        const [x1,y1]=proj(...hist[i]);
        cx.moveTo(x0,y0); cx.lineTo(x1,y1);
        // Opacidad crece hacia el extremo reciente
        const alpha=(0.08+age*0.92).toFixed(3);
        const col=colorAt(t);
        cx.strokeStyle=col.replace('rgb(','rgba(').replace(')',`,${alpha})`);
        cx.lineWidth=0.5+age*1.8; cx.stroke();
      }
    });

    // Puntos brillantes (GlowDot)
    states.forEach((st,ti)=>{
      const [px,py]=proj(st.x,st.y,st.z);
      const col=ti===0?'rgba(30,30,30,':'rgba(90,90,90,';
      // Halo exterior
      cx.beginPath(); cx.arc(px,py,9,0,Math.PI*2);
      cx.fillStyle=col+'0.12)'; cx.fill();
      cx.beginPath(); cx.arc(px,py,5.5,0,Math.PI*2);
      cx.fillStyle=col+'0.35)'; cx.fill();
      // Núcleo
      cx.beginPath(); cx.arc(px,py,3,0,Math.PI*2);
      cx.fillStyle=col+'1)'; cx.fill();
    });

    animId=requestAnimationFrame(frame);
  }

  let _cw=window.innerWidth;
  init(); initialized=true;
  new MutationObserver(()=>{
    const on=document.getElementById('panel-blog').classList.contains('active');
    if(on&&!active){if(!initialized){init();initialized=true;} active=true; if(!animId) frame();}
    else if(!on) active=false;
  }).observe(document.getElementById('panel-blog'),{attributes:true,attributeFilter:['class']});
  document.addEventListener('visibilitychange',()=>{ if(!document.hidden&&active&&!animId) frame(); });
  window.addEventListener('resize',()=>{if(active&&Math.abs(window.innerWidth-_cw)>30){_cw=window.innerWidth;init();}});
})();"""


def build_js():
    return (
        "<script>"
        + _mobile_detect()
        + _lang_toggle()
        + _tabs()
        + _conway()
        + _delaunay()
        + _flow()
        + _chladni()
        + _euler_helix()
        + _particles()
        + "\n</script>"
    )

