/* ===== Hand-drawn ML diagrams (sketch style) =====
   These are JavaScript drawing functions (real SVG, generated in code), so they
   live here by hand — not in the auto-generated books-data.js.
   To use one inside a diary page, write:  @fig net | fig. 1 — the caption
   where "net" is one of the keys in FIGS below. */
function netDiagram(){
  const L=[ [60,[70,120,170,220]], [230,[50,105,160,215,265]], [400,[120,195]] ];
  let s='<svg viewBox="0 0 460 300">';
  // edges
  for(let i=0;i<2;i++){ const a=L[i],b=L[i+1];
    a[1].forEach(ay=> b[1].forEach(by=>{ s+=`<line class="sk" x1="${a[0]+13}" y1="${ay}" x2="${b[0]-13}" y2="${by}" stroke-width="1.1" opacity="0.5"/>`; }));
  }
  // nodes
  L.forEach((col,ci)=> col[1].forEach(y=>{
    const cls = ci===2?'sk sk-r':'sk';
    s+=`<circle class="${cls}" cx="${col[0]}" cy="${y}" r="13" fill="oklch(0.82 0.05 80)"/>`;
  }));
  s+='<text class="lbl" x="40" y="276">inputs</text><text class="lbl" x="196" y="296">hidden layers</text><text class="lbl lbl-r" x="372" y="240">output</text>';
  s+='</svg>';
  return s;
}
function descentDiagram(){
  let s='<svg viewBox="0 0 460 300">';
  // contour ellipses
  for(let i=5;i>=1;i--){ s+=`<ellipse class="sk" cx="250" cy="160" rx="${i*38}" ry="${i*22}" stroke-width="1.4" opacity="${0.3+i*0.08}"/>`; }
  // descent path (zigzag spiraling in)
  s+='<path class="sk sk-r" stroke-width="2.4" d="M70 60 L132 120 L150 86 L196 138 L210 116 L236 152 L246 140 L250 160"/>';
  ['70,60','132,120','196,138','236,152','250,160'].forEach(p=>{ const [x,y]=p.split(','); s+=`<circle class="sk-fr" cx="${x}" cy="${y}" r="4"/>`;});
  s+='<text class="lbl lbl-r" x="40" y="50">start (high loss)</text><text class="lbl" x="262" y="166">minimum</text>';
  s+='</svg>';
  return s;
}
function attnDiagram(){
  const toks=['The','cat','sat','on','mat'], n=toks.length, x0=120,y0=40,cell=38;
  const w=[ [9,1,1,1,1],[2,8,1,2,1],[1,3,7,2,3],[1,1,2,6,2],[1,2,4,2,8] ];
  let s='<svg viewBox="0 0 460 300">';
  for(let r=0;r<n;r++)for(let c=0;c<n;c++){ const a=(w[r][c]/9); s+=`<rect x="${x0+c*cell}" y="${y0+r*cell}" width="${cell-3}" height="${cell-3}" rx="3" fill="oklch(0.5 0.19 28 / ${0.12+a*0.8})" stroke="oklch(0.4 0.06 50 / 0.5)"/>`; }
  toks.forEach((t,i)=>{ s+=`<text class="lbl" x="${x0+i*cell+2}" y="${y0-8}" font-size="14">${t}</text>`; s+=`<text class="lbl" x="${x0-12}" y="${y0+i*cell+24}" font-size="14" text-anchor="end">${t}</text>`; });
  s+='<text class="lbl lbl-r" x="120" y="262">each word stares at every other word</text>';
  s+='</svg>';
  return s;
}
function overfitDiagram(){
  let s='<svg viewBox="0 0 460 300">';
  s+='<line class="sk" x1="50" y1="250" x2="430" y2="250" stroke-width="1.6"/><line class="sk" x1="50" y1="40" x2="50" y2="250" stroke-width="1.6"/>';
  const pts=[[80,210],[110,180],[140,200],[175,150],[210,175],[245,120],[285,150],[320,110],[360,130],[400,95]];
  pts.forEach(p=>{ s+=`<circle class="sk-fill" cx="${p[0]}" cy="${p[1]}" r="4.5"/>`; });
  // smooth (good) fit
  s+='<path class="sk sk-t" stroke-width="2.6" d="M70 215 Q230 150 410 95"/>';
  // overfit wiggle through points
  s+='<path class="sk sk-r" stroke-width="2.2" stroke-dasharray="1 0" d="M80 210 L110 180 L140 200 L175 150 L210 175 L245 120 L285 150 L320 110 L360 130 L400 95"/>';
  s+='<text class="lbl lbl-r" x="300" y="86">overfit</text><text class="lbl" x="120" y="135" fill="var(--teal)">true pattern</text>';
  s+='</svg>';
  return s;
}
function backpropDiagram(){
  let s='<svg viewBox="0 0 460 300">';
  const boxes=[[40,'x'],[150,'w·x'],[260,'σ'],[370,'ŷ']];
  boxes.forEach(b=>{ s+=`<rect class="sk" x="${b[0]}" y="110" width="64" height="56" rx="6" fill="oklch(0.82 0.05 80)"/><text class="lbl" x="${b[0]+32}" y="146" text-anchor="middle" font-size="20">${b[1]}</text>`; });
  // forward arrows
  for(let i=0;i<3;i++){ const x=104+i*110; s+=`<path class="sk" stroke-width="2" d="M${x} 138 L${x+42} 138"/><path class="sk-fill" d="M${x+42} 138 l-8 -4 0 8 z"/>`; }
  s+='<text class="lbl" x="160" y="96">forward →</text>';
  // backward dashed arrows
  for(let i=0;i<3;i++){ const x=146+i*110; s+=`<path class="sk sk-r" stroke-width="2" stroke-dasharray="6 5" d="M${x} 182 L${x-42} 182"/><path class="sk-fr" d="M${x-42} 182 l8 -4 0 8 z"/>`; }
  s+='<text class="lbl lbl-r" x="150" y="212">← blame flows back</text>';
  s+='</svg>';
  return s;
}
function hallucDiagram(){
  let s='<svg viewBox="0 0 460 300">';
  // prompt box
  s+='<rect class="sk" x="40" y="60" width="150" height="180" rx="8" fill="oklch(0.82 0.05 80)"/><text class="lbl" x="58" y="92">prompt:</text><text class="lbl" x="58" y="120" font-size="15">"who wrote</text><text class="lbl" x="58" y="142" font-size="15">the Diarys?"</text>';
  s+='<path class="sk sk-r" stroke-width="2" d="M196 150 L250 150"/><path class="sk-fr" d="M250 150 l-9 -4 0 8 z"/>';
  // probability bars
  const bars=[['Stanford',0.42],['??? 7th',0.31,true],['unknown',0.18],['the Author',0.09]];
  let y=80;
  bars.forEach(b=>{ const w=b[1]*180; const col=b[2]?'oklch(0.55 0.215 30)':'oklch(0.45 0.07 215)';
    s+=`<rect x="270" y="${y}" width="${w}" height="22" rx="3" fill="${col}"/><text class="lbl" x="${276}" y="${y+16}" font-size="13" fill="oklch(0.96 0.02 80)">${b[0]}</text>`; y+=40; });
  s+='<text class="lbl lbl-r" x="270" y="262">it picks the confident lie</text>';
  s+='</svg>';
  return s;
}

function outlierDiagram(){
  let s='<svg viewBox="0 0 460 300">';
  // axes
  s+='<line class="sk" x1="50" y1="250" x2="430" y2="250" stroke-width="1.6"/><line class="sk" x1="50" y1="40" x2="50" y2="250" stroke-width="1.6"/>';
  // the well-behaved crowd, climbing along a trend
  const cloud=[[80,235],[104,224],[122,214],[140,206],[160,199],[178,189],[196,183],[214,171],[232,166],[250,151],[270,149],[288,133],[306,129],[326,119],[346,109],[362,101],[382,93],[402,87]];
  cloud.forEach(p=>{ s+=`<circle class="sk-fill" cx="${p[0]}" cy="${p[1]}" r="3.6"/>`; });
  // the strays, far from the herd
  [[150,78],[372,212]].forEach(p=>{ s+=`<circle class="sk-fr" cx="${p[0]}" cy="${p[1]}" r="6"/>`; });
  s+='<text class="lbl lbl-r" x="120" y="70">the stray</text>';
  s+='<text class="lbl lbl-r" x="300" y="236">and another</text>';
  s+='<text class="lbl" x="232" y="206">the well-behaved crowd</text>';
  s+='</svg>';
  return s;
}
function boxplotDiagram(){
  const y=150, h=46;
  let s='<svg viewBox="0 0 460 300">';
  // number line
  s+='<line class="sk" x1="40" y1="250" x2="430" y2="250" stroke-width="1.4"/>';
  for(let i=0;i<=8;i++){ const x=40+i*48; s+=`<line class="sk" x1="${x}" y1="246" x2="${x}" y2="254" stroke-width="1.2"/>`; }
  // whiskers + caps
  s+=`<line class="sk" x1="120" y1="${y}" x2="180" y2="${y}" stroke-width="1.6"/>`;
  s+=`<line class="sk" x1="120" y1="${y-14}" x2="120" y2="${y+14}" stroke-width="1.6"/>`;
  s+=`<line class="sk" x1="320" y1="${y}" x2="360" y2="${y}" stroke-width="1.6"/>`;
  s+=`<line class="sk" x1="360" y1="${y-14}" x2="360" y2="${y+14}" stroke-width="1.6"/>`;
  // the box (Q1..Q3)
  s+=`<rect class="sk" x="180" y="${y-h/2}" width="140" height="${h}" rx="4" fill="oklch(0.82 0.05 80)"/>`;
  // median
  s+=`<line class="sk sk-r" x1="248" y1="${y-h/2}" x2="248" y2="${y+h/2}" stroke-width="2.4"/>`;
  // strays beyond the fence
  [70,395,409].forEach(x=>{ s+=`<circle class="sk-fr" cx="${x}" cy="${y}" r="5"/>`; });
  s+=`<text class="lbl" x="166" y="${y-32}">Q1</text>`;
  s+=`<text class="lbl" x="306" y="${y-32}">Q3</text>`;
  s+=`<text class="lbl lbl-r" x="222" y="${y+58}">median</text>`;
  s+='<text class="lbl lbl-r" x="356" y="118">beyond 1.5·IQR</text>';
  s+='</svg>';
  return s;
}

/* ===== Custom diagrams for the data-mining diaries ===== */

/* curse — same handful of points, emptier as dimension grows (1D → 2D → 3D) */
function curseDiagram(){
  let s='<svg viewBox="0 0 460 300">';
  // 1D
  s+='<text class="lbl" x="68" y="40" text-anchor="middle">1D</text>';
  s+='<line class="sk" x1="22" y1="120" x2="118" y2="120" stroke-width="1.8"/>';
  [30,44,57,69,80,94,108].forEach(x=> s+=`<circle class="sk-fill" cx="${x}" cy="120" r="4"/>`);
  // 2D
  s+='<text class="lbl" x="228" y="40" text-anchor="middle">2D</text>';
  s+='<rect class="sk" x="168" y="58" width="120" height="120" stroke-width="1.8" fill="none"/>';
  [[185,150],[212,92],[250,160],[270,78],[228,120],[196,72],[266,138]].forEach(p=> s+=`<circle class="sk-fill" cx="${p[0]}" cy="${p[1]}" r="4"/>`);
  // 3D cube
  s+='<text class="lbl lbl-r" x="388" y="40" text-anchor="middle">3D</text>';
  const fx=330,fy=66,sz=92,off=26;
  s+=`<rect class="sk" x="${fx}" y="${fy+off}" width="${sz}" height="${sz}" stroke-width="1.6" fill="none"/>`;
  s+=`<rect class="sk" x="${fx+off}" y="${fy}" width="${sz}" height="${sz}" stroke-width="1.5" fill="none" opacity="0.55"/>`;
  s+=`<line class="sk" x1="${fx}" y1="${fy+off}" x2="${fx+off}" y2="${fy}" stroke-width="1.4" opacity="0.55"/>`;
  s+=`<line class="sk" x1="${fx+sz}" y1="${fy+off}" x2="${fx+off+sz}" y2="${fy}" stroke-width="1.4" opacity="0.55"/>`;
  s+=`<line class="sk" x1="${fx}" y1="${fy+off+sz}" x2="${fx+off}" y2="${fy+sz}" stroke-width="1.4" opacity="0.55"/>`;
  s+=`<line class="sk" x1="${fx+sz}" y1="${fy+off+sz}" x2="${fx+off+sz}" y2="${fy+sz}" stroke-width="1.4" opacity="0.55"/>`;
  [[362,150],[404,108],[382,182]].forEach(p=> s+=`<circle class="sk-fr" cx="${p[0]}" cy="${p[1]}" r="4"/>`);
  // arrows between panels
  s+='<text class="lbl" x="143" y="124" font-size="20">→</text><text class="lbl" x="303" y="124" font-size="20">→</text>';
  return s+'</svg>';
}

/* corrmatrix — correlation heatmap; highlight a redundant pair to drop */
function corrMatrixDiagram(){
  const vars=['MPG','Cyl','Disp','HP','Wt'];
  const M=[[1,-.78,-.81,-.78,-.83],[-.78,1,.95,.84,.9],[-.81,.95,1,.9,.93],[-.78,.84,.9,1,.86],[-.83,.9,.93,.86,1]];
  const x0=150,y0=42,cell=42;
  let s='<svg viewBox="0 0 460 300">';
  for(let r=0;r<5;r++)for(let c=0;c<5;c++){
    const v=M[r][c], a=Math.min(Math.abs(v),1);
    const col=v>=0?`oklch(0.52 0.205 28 / ${(0.14+a*0.78).toFixed(2)})`:`oklch(0.45 0.10 232 / ${(0.14+a*0.78).toFixed(2)})`;
    s+=`<rect x="${x0+c*cell}" y="${y0+r*cell}" width="${cell-3}" height="${cell-3}" rx="3" fill="${col}" stroke="oklch(0.4 0.05 60 / 0.4)"/>`;
    s+=`<text x="${x0+c*cell+(cell-3)/2}" y="${y0+r*cell+24}" text-anchor="middle" font-family="Caveat,cursive" font-size="13" fill="${a>0.6?'oklch(0.96 0.02 80)':'oklch(0.26 0.03 52)'}">${v===1?'1':v.toFixed(2)}</text>`;
  }
  vars.forEach((v,i)=>{
    s+=`<text class="lbl" x="${x0-8}" y="${y0+i*cell+25}" text-anchor="end" font-size="14">${v}</text>`;
    s+=`<text class="lbl" x="${x0+i*cell+(cell-3)/2}" y="${y0-8}" text-anchor="middle" font-size="14">${v}</text>`;
  });
  // ring the redundant Disp×Cyl pair (col 2, row 1)
  s+=`<rect x="${x0+2*cell-2}" y="${y0+cell-2}" width="${cell+1}" height="${cell+1}" rx="3" fill="none" stroke="oklch(0.26 0.03 52)" stroke-width="2.6"/>`;
  s+=`<text class="lbl lbl-r" x="${x0+2.5*cell}" y="${y0+5*cell+20}" text-anchor="middle">Disp ≈ Cyl (0.95) → drop one</text>`;
  return s+'</svg>';
}

/* varimp — random-forest variable importance bars */
function varImpDiagram(){
  const data=[['Displacement',62],['Weight',46],['Horsepower',38],['MPG',30],['Acceleration',22],['Cylinders',15],['Year',11]];
  const x0=152,y0=34,bw=240,rowH=30,max=66;
  let s='<svg viewBox="0 0 460 300">';
  s+=`<line class="sk" x1="${x0}" y1="24" x2="${x0}" y2="${y0+data.length*rowH-6}" stroke-width="1.4"/>`;
  data.forEach((d,i)=>{
    const w=d[1]/max*bw, y=y0+i*rowH, top=i===0;
    s+=`<rect x="${x0}" y="${y}" width="${w.toFixed(1)}" height="${rowH-12}" rx="3" fill="oklch(0.52 0.10 150 / ${top?0.9:0.7})" stroke="oklch(0.4 0.06 150 / 0.7)"/>`;
    s+=`<text class="lbl" x="${x0-8}" y="${y+15}" text-anchor="end" font-size="14">${d[0]}</text>`;
    s+=`<circle class="sk-fr" cx="${(x0+w).toFixed(1)}" cy="${y+(rowH-12)/2}" r="3.4"/>`;
  });
  s+=`<text class="lbl" x="${x0+bw/2}" y="${y0+data.length*rowH+12}" text-anchor="middle">MeanDecreaseGini →</text>`;
  return s+'</svg>';
}

/* featsel — forward (grow from empty) vs backward (shrink from full) */
function featSelDiagram(){
  const bw=26,gap=7,x0=150;
  let s='<svg viewBox="0 0 460 300">';
  const row=(y,states,fill)=> states.forEach((on,i)=>{
    s+=`<rect class="sk" x="${x0+i*(bw+gap)}" y="${y}" width="${bw}" height="${bw}" rx="3" fill="${on?fill:'none'}"/>`;
  });
  s+='<text class="lbl" x="24" y="48">Forward →</text>';
  row(30,[0,0,0,0,0]); row(64,[1,0,0,0,0],'oklch(0.52 0.10 150 / 0.85)'); row(98,[1,1,0,0,0],'oklch(0.52 0.10 150 / 0.85)');
  s+='<text class="lbl" x="305" y="78" font-size="20">⋯</text>';
  s+='<line class="sk" x1="30" y1="150" x2="430" y2="150" stroke-width="1" opacity="0.3" stroke-dasharray="4 5"/>';
  s+='<text class="lbl lbl-r" x="24" y="190">Backward ←</text>';
  const red='oklch(0.52 0.205 28 / 0.8)';
  row(172,[1,1,1,1,1],red); row(206,[1,0,1,1,1],red); row(240,[1,0,1,0,1],red);
  s+='<text class="lbl" x="305" y="220" font-size="20">⋯</text>';
  return s+'</svg>';
}

/* pca — data cloud rotated onto its principal axes PC1 / PC2 */
function pcaDiagram(){
  const cx=240,cy=158,ang=-28*Math.PI/180,ca=Math.cos(ang),sa=Math.sin(ang);
  const rot=(px,py)=>[cx+px*ca-py*sa, cy+px*sa+py*ca];
  let s='<svg viewBox="0 0 460 300">';
  s+=`<line class="sk" x1="55" y1="${cy}" x2="430" y2="${cy}" stroke-width="1.3" opacity="0.4"/>`;
  s+=`<line class="sk" x1="${cx}" y1="36" x2="${cx}" y2="268" stroke-width="1.3" opacity="0.4"/>`;
  s+=`<text class="lbl" x="420" y="${cy-8}" opacity="0.6">X</text><text class="lbl" x="${cx+8}" y="48" opacity="0.6">Y</text>`;
  s+=`<g transform="rotate(-28 ${cx} ${cy})"><ellipse class="sk-t" cx="${cx}" cy="${cy}" rx="132" ry="40" stroke-width="2" fill="oklch(0.45 0.08 215 / 0.10)"/></g>`;
  [[-118,12],[-96,-14],[-72,7],[-54,-17],[-32,5],[-12,-9],[8,13],[28,-7],[50,9],[72,-13],[96,5],[116,-11]]
    .forEach(p=>{ const [X,Y]=rot(p[0],p[1]); s+=`<circle class="sk-fill" cx="${X.toFixed(1)}" cy="${Y.toFixed(1)}" r="3.6"/>`; });
  const [a1x,a1y]=rot(-150,0),[a2x,a2y]=rot(152,0);
  s+=`<line class="sk-r" x1="${a1x.toFixed(1)}" y1="${a1y.toFixed(1)}" x2="${a2x.toFixed(1)}" y2="${a2y.toFixed(1)}" stroke-width="2.6"/>`;
  s+=`<circle class="sk-fr" cx="${a2x.toFixed(1)}" cy="${a2y.toFixed(1)}" r="4.6"/>`;
  const [b1x,b1y]=rot(0,-58),[b2x,b2y]=rot(0,58);
  s+=`<line class="sk-r" x1="${b1x.toFixed(1)}" y1="${b1y.toFixed(1)}" x2="${b2x.toFixed(1)}" y2="${b2y.toFixed(1)}" stroke-width="1.8" stroke-dasharray="5 4" opacity="0.85"/>`;
  s+=`<text class="lbl lbl-r" x="${(a2x-2).toFixed(1)}" y="${(a2y-10).toFixed(1)}">PC1</text>`;
  s+=`<text class="lbl lbl-r" x="${(b1x+8).toFixed(1)}" y="${(b1y+2).toFixed(1)}">PC2</text>`;
  return s+'</svg>';
}

/* scaling — one shape, three scales (original / min-max / z-score) */
function scalingDiagram(){
  const bars=[6,14,23,27,22,18,7,5],max=28;
  let s='<svg viewBox="0 0 460 300">';
  const hist=(x0,label,t0,t1)=>{
    const bw=14,base=212;
    bars.forEach((b,i)=>{ const h=b/max*120; s+=`<rect class="sk" x="${x0+i*bw}" y="${(base-h).toFixed(1)}" width="${bw-2}" height="${h.toFixed(1)}" fill="oklch(0.82 0.05 80)"/>`; });
    s+=`<line class="sk" x1="${x0}" y1="${base}" x2="${x0+bars.length*bw}" y2="${base}" stroke-width="1.4"/>`;
    s+=`<text class="lbl" x="${x0+bars.length*bw/2}" y="${base+22}" text-anchor="middle">${label}</text>`;
    s+=`<text class="lbl" x="${x0}" y="${base+40}" font-size="12" opacity="0.7">${t0}</text>`;
    s+=`<text class="lbl" x="${x0+bars.length*bw-8}" y="${base+40}" font-size="12" opacity="0.7" text-anchor="end">${t1}</text>`;
  };
  hist(40,'Original','4.3','7.9');
  hist(190,'Min-Max','0','1');
  hist(340,'Z-Score','-2','2');
  s+='<text class="lbl lbl-r" x="230" y="40" text-anchor="middle">same shape · new scale</text>';
  return s+'</svg>';
}

/* binning — equal-width bins over a number line with stacked duplicates */
function binningDiagram(){
  const x0=40,x1=430,y=146,vmax=45;
  const X=v=> x0+v/vmax*(x1-x0);
  let s='<svg viewBox="0 0 460 300">';
  s+=`<line class="sk" x1="${x0}" y1="${y}" x2="${x1}" y2="${y}" stroke-width="1.6"/>`;
  for(let t=0;t<=45;t+=5){ const xx=X(t); s+=`<line class="sk" x1="${xx.toFixed(1)}" y1="${y-5}" x2="${xx.toFixed(1)}" y2="${y+5}" stroke-width="1.2"/><text class="lbl" x="${xx.toFixed(1)}" y="${y+22}" text-anchor="middle" font-size="11" opacity="0.65">${t}</text>`; }
  const data=[1,1,1,1,1,2,2,11,11,12,12,44],seen={};
  data.forEach(v=>{ const k=(seen[v]=(seen[v]||0)+1)-1; s+=`<circle class="sk-fill" cx="${X(v).toFixed(1)}" cy="${y-12-k*11}" r="4"/>`; });
  [[0,15,'Low'],[15,30,'Mid'],[30,45,'High']].forEach(b=>{ const xa=X(b[0]),xb=X(b[1]);
    s+=`<path class="sk-r" d="M${(xa+3).toFixed(1)} ${y+32} L${(xa+3).toFixed(1)} ${y+42} L${(xb-3).toFixed(1)} ${y+42} L${(xb-3).toFixed(1)} ${y+32}" stroke-width="1.8" fill="none"/>`;
    s+=`<text class="lbl lbl-r" x="${((xa+xb)/2).toFixed(1)}" y="${y+62}" text-anchor="middle">${b[2]}</text>`;
  });
  return s+'</svg>';
}

/* skew — right-skewed histogram → log(x) → roughly symmetric */
function skewDiagram(){
  let s='<svg viewBox="0 0 460 300">';
  const hist=(x0,vals)=>{ const bw=15,base=212,max=Math.max(...vals); vals.forEach((b,i)=>{ const h=b/max*132; s+=`<rect class="sk" x="${x0+i*bw}" y="${(base-h).toFixed(1)}" width="${bw-2}" height="${h.toFixed(1)}" fill="oklch(0.82 0.05 80)"/>`; }); s+=`<line class="sk" x1="${x0}" y1="${base}" x2="${x0+vals.length*bw}" y2="${base}" stroke-width="1.4"/>`; };
  hist(38,[28,22,14,9,6,4,3,2]);
  s+='<text class="lbl" x="98" y="248" text-anchor="middle">right-skew</text>';
  s+='<path class="sk-r" stroke-width="2.2" d="M214 150 L272 150"/><path class="sk-fr" d="M272 150 l-9 -4 0 8 z"/>';
  s+='<text class="lbl lbl-r" x="243" y="138" text-anchor="middle">log(x)</text>';
  hist(292,[4,10,18,24,24,18,10,4]);
  s+='<text class="lbl" x="352" y="248" text-anchor="middle">≈ normal</text>';
  return s+'</svg>';
}

/* entropy — supervised split-point that minimizes class entropy */
function entropyDiagram(){
  const x0=42,x1=428,y=140,vmin=18,vmax=58;
  const X=v=> x0+(v-vmin)/(vmax-vmin)*(x1-x0);
  let s='<svg viewBox="0 0 460 300">';
  s+=`<line class="sk" x1="${x0}" y1="${y}" x2="${x1}" y2="${y}" stroke-width="1.6"/>`;
  [[22,0],[25,0],[30,1],[35,1],[40,0],[45,1],[50,1],[55,0]].forEach(d=>{ const xx=X(d[0]);
    s+= d[1] ? `<circle class="sk-fr" cx="${xx.toFixed(1)}" cy="${y-16}" r="6"/>`
             : `<circle class="sk" cx="${xx.toFixed(1)}" cy="${y-16}" r="6" fill="none" stroke-width="2"/>`;
    s+=`<text class="lbl" x="${xx.toFixed(1)}" y="${y+20}" text-anchor="middle" font-size="11" opacity="0.65">${d[0]}</text>`;
  });
  const xs=X(32.5);
  s+=`<line class="sk-r" x1="${xs.toFixed(1)}" y1="${y-62}" x2="${xs.toFixed(1)}" y2="${y+38}" stroke-width="2.2" stroke-dasharray="6 4"/>`;
  s+=`<text class="lbl lbl-r" x="${xs.toFixed(1)}" y="${y-68}" text-anchor="middle">split t = 30</text>`;
  s+=`<text class="lbl" x="${X(24).toFixed(1)}" y="${y-40}" text-anchor="middle">≤30 · H=0.918</text>`;
  s+=`<text class="lbl" x="${X(47).toFixed(1)}" y="${y-40}" text-anchor="middle">&gt;30 · H=0.971</text>`;
  s+=`<circle class="sk-fr" cx="62" cy="246" r="5"/><text class="lbl" x="74" y="251" font-size="13">Premium</text>`;
  s+=`<circle class="sk" cx="178" cy="246" r="5" fill="none" stroke-width="2"/><text class="lbl" x="190" y="251" font-size="13">No Premium</text>`;
  return s+'</svg>';
}

/* onehot — a category column exploded into binary indicator columns */
function oneHotDiagram(){
  const rows=['north','east','south'],cols=['north','east','south'];
  const M=[[1,0,0],[0,1,0],[0,0,1]];
  const y0=72,rh=44,mx=210,cw=72;
  let s='<svg viewBox="0 0 460 300">';
  s+='<text class="lbl" x="80" y="52" text-anchor="middle">region</text>';
  rows.forEach((r,i)=>{ const y=y0+i*rh; s+=`<rect class="sk" x="30" y="${y}" width="100" height="${rh-8}" rx="3" fill="oklch(0.82 0.05 80)"/><text class="lbl" x="80" y="${y+24}" text-anchor="middle">${r}</text>`; });
  s+='<path class="sk-r" stroke-width="2.2" d="M140 150 L186 150"/><path class="sk-fr" d="M186 150 l-9 -4 0 8 z"/>';
  cols.forEach((c,j)=> s+=`<text class="lbl" x="${mx+j*cw+(cw-8)/2}" y="52" text-anchor="middle" font-size="13">${c}</text>`);
  rows.forEach((r,i)=>{ const y=y0+i*rh; cols.forEach((c,j)=>{ const v=M[i][j],x=mx+j*cw;
    s+=`<rect class="sk" x="${x}" y="${y}" width="${cw-8}" height="${rh-8}" rx="3" fill="${v?'oklch(0.52 0.205 28 / 0.8)':'none'}"/>`;
    s+=`<text x="${x+(cw-8)/2}" y="${y+24}" text-anchor="middle" font-family="Caveat,cursive" font-size="16" fill="${v?'oklch(0.96 0.02 80)':'oklch(0.26 0.03 52)'}">${v}</text>`;
  }); });
  return s+'</svg>';
}

/* tree — a decision tree (the slides' Age/Income buy-or-not example) */
function treeDiagram(){
  let s='<svg viewBox="0 0 460 300">';
  const box=(x,y,w,txt,cls)=>{
    s+=`<rect class="${cls||'sk'}" x="${(x-w/2).toFixed(1)}" y="${y-14}" width="${w}" height="28" rx="6" fill="oklch(0.82 0.05 80)"/>`;
    s+=`<text class="lbl" x="${x}" y="${y+5}" text-anchor="middle" font-size="13">${txt}</text>`;
  };
  const edge=(x1,y1,x2,y2,lab)=>{
    s+=`<line class="sk" x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke-width="1.6"/>`;
    s+=`<text class="lbl lbl-r" x="${((x1+x2)/2).toFixed(1)}" y="${((y1+y2)/2-3).toFixed(1)}" text-anchor="middle" font-size="12">${lab}</text>`;
  };
  edge(200,52,128,98,'yes'); edge(262,52,330,98,'no');
  edge(98,126,72,184,'yes'); edge(150,126,182,184,'no');
  box(230,38,120,'Age ≤ 30');
  box(330,112,74,'No buy','sk sk-r');
  box(122,112,128,'Income ≤ 50k');
  box(72,198,74,'Buy','sk sk-t');
  box(184,198,74,'No buy','sk sk-r');
  s+='<text class="lbl" x="300" y="206" font-size="12">root → leaves</text>';
  return s+'</svg>';
}

/* scree — PCA variance explained (bars) + cumulative line (Iris values) */
function screeDiagram(){
  const ev=[72.96,22.85,3.67,0.52], cum=[72.96,95.81,99.48,100];
  const x0=72,y0=44,base=240,bw=64,maxh=base-y0;
  let s='<svg viewBox="0 0 460 300">';
  s+=`<line class="sk" x1="${x0-16}" y1="${base}" x2="430" y2="${base}" stroke-width="1.5"/>`;
  s+=`<line class="sk" x1="${x0-16}" y1="${y0-8}" x2="${x0-16}" y2="${base}" stroke-width="1.5"/>`;
  ev.forEach((v,i)=>{ const h=v/100*maxh, x=x0+i*90;
    s+=`<rect class="sk" x="${x}" y="${(base-h).toFixed(1)}" width="${bw}" height="${h.toFixed(1)}" fill="oklch(0.55 0.09 230 / .5)"/>`;
    s+=`<text class="lbl" x="${x+bw/2}" y="${base+18}" text-anchor="middle" font-size="12">PC${i+1}</text>`;
    s+=`<text class="lbl" x="${x+bw/2}" y="${(base-h-6).toFixed(1)}" text-anchor="middle" font-size="11">${v}%</text>`;
  });
  const pts=cum.map((v,i)=>`${x0+i*90+bw/2},${(base-v/100*maxh).toFixed(1)}`).join(' ');
  s+=`<polyline class="sk-r" points="${pts}" fill="none" stroke-width="2.2"/>`;
  cum.forEach((v,i)=>{ s+=`<circle class="sk-fr" cx="${x0+i*90+bw/2}" cy="${(base-v/100*maxh).toFixed(1)}" r="3.6"/>`; });
  const y95=base-95/100*maxh;
  s+=`<line class="sk" x1="${x0-16}" y1="${y95.toFixed(1)}" x2="430" y2="${y95.toFixed(1)}" stroke-width="1.2" stroke-dasharray="5 4" opacity=".7"/>`;
  s+=`<text class="lbl lbl-r" x="424" y="${(y95-5).toFixed(1)}" text-anchor="end" font-size="11">95%</text>`;
  s+=`<text class="lbl" x="${x0+90+bw/2}" y="${(base-cum[1]/100*maxh-10).toFixed(1)}" text-anchor="middle" font-size="11">acum.</text>`;
  return s+'</svg>';
}

/* iv — the Information Value interpretation scale (from the notebook) */
function ivDiagram(){
  const x0=44,x1=430,y=150;
  const bands=[[0,0.02,'oklch(0.62 0.015 60)','useless'],[0.02,0.10,'oklch(0.66 0.11 95)','weak'],
               [0.10,0.30,'oklch(0.60 0.12 150)','medium'],[0.30,0.50,'oklch(0.58 0.13 45)','strong'],
               [0.50,0.62,'oklch(0.52 0.20 28)','suspicious']];
  const X=v=> x0+(v/0.62)*(x1-x0);
  let s='<svg viewBox="0 0 460 300">';
  bands.forEach(b=>{
    s+=`<rect x="${X(b[0]).toFixed(1)}" y="${y-24}" width="${(X(b[1])-X(b[0])).toFixed(1)}" height="48" fill="${b[2]}" opacity=".55" stroke="oklch(0.4 0.04 60 / .4)"/>`;
    s+=`<text class="lbl" x="${((X(b[0])+X(b[1]))/2).toFixed(1)}" y="${y+42}" text-anchor="middle" font-size="11">${b[3]}</text>`;
  });
  [0,0.02,0.10,0.30,0.50].forEach(t=>{ s+=`<text class="lbl" x="${X(t).toFixed(1)}" y="${y-32}" text-anchor="middle" font-size="11" opacity=".7">${t}</text>`; });
  s+=`<text class="lbl lbl-r" x="${x0}" y="${y-48}" font-size="12">Information Value →</text>`;
  return s+'</svg>';
}

/* the in-page diagrams, keyed by the name you use in  @fig <name> | caption */
const FIGS = {
  tree:treeDiagram, scree:screeDiagram, iv:ivDiagram,
  net:netDiagram, descent:descentDiagram, attn:attnDiagram, overfit:overfitDiagram,
  backprop:backpropDiagram, halluc:hallucDiagram, outlier:outlierDiagram, boxplot:boxplotDiagram,
  curse:curseDiagram, corrmatrix:corrMatrixDiagram, varimp:varImpDiagram, featsel:featSelDiagram,
  pca:pcaDiagram, scaling:scalingDiagram, binning:binningDiagram, skew:skewDiagram,
  entropy:entropyDiagram, onehot:oneHotDiagram,
};

/* ===== Per-topic cover emblems (the gilt sigil on each book cover) =====
   Choose one in a post's frontmatter with:  emblem: net   (any key below). */
const EMBLEM_ORDER = ["net","descent","attn","overfit","backprop","halluc"];
function tomeEmblem(key){
  const symbols = [
    /* net — neural network: little constellation of neurons */
    `<line class="palm" x1="18" y1="22" x2="50" y2="12" stroke-width="2" opacity="0.7"></line>
     <line class="palm" x1="18" y1="22" x2="50" y2="36" stroke-width="2" opacity="0.7"></line>
     <line class="palm" x1="18" y1="50" x2="50" y2="36" stroke-width="2" opacity="0.7"></line>
     <line class="palm" x1="18" y1="50" x2="50" y2="60" stroke-width="2" opacity="0.7"></line>
     <line class="palm" x1="50" y1="12" x2="82" y2="36" stroke-width="2" opacity="0.7"></line>
     <line class="palm" x1="50" y1="36" x2="82" y2="36" stroke-width="2" opacity="0.7"></line>
     <line class="palm" x1="50" y1="60" x2="82" y2="36" stroke-width="2" opacity="0.7"></line>
     <circle class="palm" cx="18" cy="22" r="6"></circle>
     <circle class="palm" cx="18" cy="50" r="6"></circle>
     <circle class="palm" cx="50" cy="12" r="6"></circle>
     <circle class="palm" cx="50" cy="36" r="6"></circle>
     <circle class="palm" cx="50" cy="60" r="6"></circle>
     <circle class="palmfill" cx="82" cy="36" r="6.5"></circle>`,
    /* descent — gradient descent: contour rings + path falling in */
    `<ellipse class="palm" cx="50" cy="38" rx="34" ry="21" stroke-width="2" opacity="0.55"></ellipse>
     <ellipse class="palm" cx="50" cy="38" rx="22" ry="13.5" stroke-width="2" opacity="0.75"></ellipse>
     <ellipse class="palm" cx="50" cy="38" rx="11" ry="6.5" stroke-width="2"></ellipse>
     <path class="palm" d="M14 8 L30 22 L36 14 L46 32" stroke-width="2.5"></path>
     <circle class="palmfill" cx="50" cy="38" r="3.2"></circle>`,
    /* attn — transformer: attention matrix */
    `<rect class="palmfill" x="25" y="8" width="14" height="14" rx="2"></rect>
     <rect class="palmfill" x="43" y="8" width="14" height="14" rx="2" opacity="0.4"></rect>
     <rect class="palmfill" x="61" y="8" width="14" height="14" rx="2" opacity="0.4"></rect>
     <rect class="palmfill" x="25" y="26" width="14" height="14" rx="2" opacity="0.4"></rect>
     <rect class="palmfill" x="43" y="26" width="14" height="14" rx="2"></rect>
     <rect class="palmfill" x="61" y="26" width="14" height="14" rx="2" opacity="0.4"></rect>
     <rect class="palmfill" x="25" y="44" width="14" height="14" rx="2" opacity="0.4"></rect>
     <rect class="palmfill" x="43" y="44" width="14" height="14" rx="2" opacity="0.4"></rect>
     <rect class="palmfill" x="61" y="44" width="14" height="14" rx="2"></rect>`,
    /* overfit — jagged liar's line through the dots vs smooth truth */
    `<path class="palm" d="M12 54 Q50 22 88 28" stroke-width="2" stroke-dasharray="5 4" opacity="0.6"></path>
     <path class="palm" d="M16 50 L33 26 L50 44 L67 16 L84 34" stroke-width="2.6"></path>
     <circle class="palmfill" cx="16" cy="50" r="3.4"></circle>
     <circle class="palmfill" cx="33" cy="26" r="3.4"></circle>
     <circle class="palmfill" cx="50" cy="44" r="3.4"></circle>
     <circle class="palmfill" cx="67" cy="16" r="3.4"></circle>
     <circle class="palmfill" cx="84" cy="34" r="3.4"></circle>`,
    /* backprop — chain forward, blame flowing back */
    `<rect class="palm" x="12" y="20" width="17" height="17" rx="3" stroke-width="2.5"></rect>
     <rect class="palm" x="41" y="20" width="17" height="17" rx="3" stroke-width="2.5"></rect>
     <rect class="palm" x="70" y="20" width="17" height="17" rx="3" stroke-width="2.5"></rect>
     <line class="palm" x1="29" y1="28" x2="38" y2="28" stroke-width="2"></line>
     <path class="palmfill" d="M41 28 l-7 -3.5 0 7 z"></path>
     <line class="palm" x1="58" y1="28" x2="67" y2="28" stroke-width="2"></line>
     <path class="palmfill" d="M70 28 l-7 -3.5 0 7 z"></path>
     <path class="palm" d="M82 50 L26 50" stroke-width="2.5" stroke-dasharray="5 4"></path>
     <path class="palmfill" d="M18 50 l8 -4 0 8 z"></path>`,
    /* halluc — the eye that sees what isn't there */
    `<path class="palm" d="M14 36 Q50 6 86 36 Q50 66 14 36 Z" stroke-width="2.8"></path>
     <circle class="palm" cx="50" cy="36" r="11" stroke-width="2.5"></circle>
     <circle class="palmfill" cx="50" cy="36" r="4"></circle>
     <line class="palm" x1="50" y1="58" x2="50" y2="66" stroke-width="2" opacity="0.6"></line>
     <line class="palm" x1="32" y1="54" x2="28" y2="61" stroke-width="2" opacity="0.6"></line>
     <line class="palm" x1="68" y1="54" x2="72" y2="61" stroke-width="2" opacity="0.6"></line>`
  ];
  let i = typeof key === "number" ? key : EMBLEM_ORDER.indexOf(key);
  if(i < 0) i = 0;
  return `<svg class="sigil" viewBox="0 0 100 100" aria-hidden="true">
    ${symbols[i % symbols.length]}
  </svg>`;
}


/* ===== Chart toolkit — data-driven figures in the current sketch style =====
   Write charts straight from a diary (.md), no hand-coded SVG needed:

     @chart bars    | Displacement: 62, Weight: 46, MPG: 30        | fig. 1 — …
     @chart line    | x: e10 e11 e12 e13 ; cuBLAS: 40 55 68 82 ; CPU: 8 12 15 18 | …
     @chart scatter | 1,2  2,3.5  3,3  4,5  5,4.5                  | …

   To add a new kind, add a function to the CHART map below; it receives the
   raw data string and returns an <svg>. Reuse the .sk / .sk-r / .sk-t / .lbl
   classes so it matches the grimoire diagrams. */
const _CW = 460, _CH = 300;
const _chartSvg = inner => '<svg viewBox="0 0 ' + _CW + ' ' + _CH + '">' + inner + '</svg>';
const _SERIES = [["sk", "sk-fill", ""], ["sk-r", "sk-fr", " lbl-r"], ["sk-t", "sk-fill", ""]];

const CHART = {
  /* horizontal labelled bars:  "label: value, label: value, …" */
  bars(data){
    const items = String(data).split(",").map(s => {
      const i = s.indexOf(":");
      return [s.slice(0, i).trim(), parseFloat(s.slice(i + 1))];
    }).filter(d => d[0] && !isNaN(d[1]));
    if(!items.length) return _chartSvg("");
    const max = Math.max(...items.map(d => Math.abs(d[1]))) || 1;
    const x0 = 150, y0 = 30, bw = 250, rowH = Math.min(38, (258 - y0) / items.length);
    let s = `<line class="sk" x1="${x0}" y1="${y0 - 6}" x2="${x0}" y2="${(y0 + items.length * rowH).toFixed(1)}" stroke-width="1.4"/>`;
    items.forEach((d, i) => {
      const w = Math.max(0, d[1]) / max * bw, y = y0 + i * rowH;
      s += `<rect class="sk" x="${x0}" y="${(y + 3).toFixed(1)}" width="${w.toFixed(1)}" height="${(rowH - 10).toFixed(1)}" rx="3" fill="oklch(0.55 0.09 230 / .5)"/>`;
      s += `<text class="lbl" x="${x0 - 9}" y="${(y + rowH / 2 + 1).toFixed(1)}" text-anchor="end" font-size="14">${d[0]}</text>`;
      s += `<text class="lbl" x="${(x0 + w + 7).toFixed(1)}" y="${(y + rowH / 2 + 1).toFixed(1)}" font-size="12">${d[1]}</text>`;
    });
    return _chartSvg(s);
  },

  /* multi-series line chart:  "x: a b c ; Name: v v v ; Name2: v v v" */
  line(data){
    const segs = String(data).split(";").map(s => s.trim()).filter(Boolean);
    let xlabels = null; const series = [];
    segs.forEach(seg => {
      const i = seg.indexOf(":"), name = seg.slice(0, i).trim();
      const vals = seg.slice(i + 1).trim().split(/\s+/);
      if(name.toLowerCase() === "x") xlabels = vals;
      else series.push([name, vals.map(parseFloat)]);
    });
    if(!series.length) return _chartSvg("");
    const n = Math.max(...series.map(s => s[1].length));
    let lo = Infinity, hi = -Infinity;
    series.forEach(([, v]) => v.forEach(y => { if(y < lo) lo = y; if(y > hi) hi = y; }));
    if(lo === hi){ hi = lo + 1; lo -= 1; }
    const x0 = 54, x1 = 410, base = 246, top = 40;
    const X = i => x0 + (n <= 1 ? 0 : i / (n - 1)) * (x1 - x0);
    const Y = y => base - (y - lo) / (hi - lo) * (base - top);
    let s = `<line class="sk" x1="${x0}" y1="${base}" x2="${x1}" y2="${base}" stroke-width="1.4"/>`;
    s += `<line class="sk" x1="${x0}" y1="${top - 6}" x2="${x0}" y2="${base}" stroke-width="1.4"/>`;
    if(xlabels) xlabels.forEach((lb, i) => {
      s += `<text class="lbl" x="${X(i).toFixed(1)}" y="${base + 18}" text-anchor="middle" font-size="11" opacity=".7">${lb}</text>`;
    });
    series.forEach(([name, vals], si) => {
      const [stroke, dot, lblc] = _SERIES[si % _SERIES.length];
      const pts = vals.map((y, i) => `${X(i).toFixed(1)},${Y(y).toFixed(1)}`).join(" ");
      s += `<polyline class="${stroke}" points="${pts}" fill="none" stroke-width="2.2"/>`;
      vals.forEach((y, i) => { s += `<circle class="${dot}" cx="${X(i).toFixed(1)}" cy="${Y(y).toFixed(1)}" r="3"/>`; });
      s += `<text class="lbl${lblc}" x="${(x1 + 5).toFixed(1)}" y="${(Y(vals[vals.length - 1]) + 3).toFixed(1)}" font-size="11">${name}</text>`;
    });
    return _chartSvg(s);
  },

  /* scatter plot:  "x,y  x,y  x,y" */
  scatter(data){
    const pts = String(data).trim().split(/\s+/).map(p => p.split(",").map(parseFloat))
      .filter(p => p.length === 2 && !isNaN(p[0]) && !isNaN(p[1]));
    if(!pts.length) return _chartSvg("");
    let xlo = Infinity, xhi = -Infinity, ylo = Infinity, yhi = -Infinity;
    pts.forEach(([x, y]) => { if(x < xlo) xlo = x; if(x > xhi) xhi = x; if(y < ylo) ylo = y; if(y > yhi) yhi = y; });
    if(xlo === xhi){ xhi = xlo + 1; xlo -= 1; } if(ylo === yhi){ yhi = ylo + 1; ylo -= 1; }
    const x0 = 50, x1 = 430, base = 250, top = 38;
    const X = x => x0 + (x - xlo) / (xhi - xlo) * (x1 - x0);
    const Y = y => base - (y - ylo) / (yhi - ylo) * (base - top);
    let s = `<line class="sk" x1="${x0}" y1="${base}" x2="${x1}" y2="${base}" stroke-width="1.4"/>`;
    s += `<line class="sk" x1="${x0}" y1="${top - 6}" x2="${x0}" y2="${base}" stroke-width="1.4"/>`;
    pts.forEach(([x, y]) => { s += `<circle class="sk-fill" cx="${X(x).toFixed(1)}" cy="${Y(y).toFixed(1)}" r="4"/>`; });
    return _chartSvg(s);
  },
};
