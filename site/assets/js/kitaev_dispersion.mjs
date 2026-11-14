/* Exact zero-field honeycomb structure factor; only r=|f| is displayed. */
const TAU = 2 * Math.PI;
export function radialModulus(JzOverJ, k1, k2) {
  if (!Number.isFinite(JzOverJ) || JzOverJ < 0 || JzOverJ > 2) throw new RangeError("Jz/J outside [0,2]");
  const re = JzOverJ + Math.cos(TAU*k1) + Math.cos(TAU*k2);
  const im = Math.sin(TAU*k1) + Math.sin(TAU*k2);
  return Math.hypot(re, im);
}
export function zeroSet(JzOverJ) {
  if (!Number.isFinite(JzOverJ) || JzOverJ < 0 || JzOverJ > 2) throw new RangeError("Jz/J outside [0,2]");
  if (JzOverJ === 0) return {kind: "line", points: []};
  if (JzOverJ === 2) return {kind: "merged", points: [[.5,.5]]};
  const q = Math.acos(-JzOverJ / 2) / TAU;
  return {kind: "points", points: [[q,1-q],[1-q,q]]};
}
function ramp(r) {
  const t=Math.pow(Math.max(0,Math.min(1,r/4)),.62);
  const low=[0,99,154], high=[250,246,238];
  return "rgb("+low.map((v,i)=>Math.round(v*(1-t)+high[i]*t)).join(",")+")";
}
function draw(ctx, ratio) {
  const x=62,y=22,len=400,N=80,size=len/N;
  ctx.clearRect(0,0,510,495);
  ctx.fillStyle="#FAF6EE";ctx.fillRect(0,0,510,495);
  for(let row=0;row<N;row++)for(let col=0;col<N;col++){
    const k1=(col+.5)/N,k2=1-(row+.5)/N;
    ctx.fillStyle=ramp(radialModulus(ratio,k1,k2));
    ctx.fillRect(x+col*size,y+row*size,size+.25,size+.25);
  }
  ctx.strokeStyle="#2B2B2B";ctx.lineWidth=1;ctx.strokeRect(x,y,len,len);
  ctx.font="13px Georgia,serif";ctx.fillStyle="#2B2B2B";ctx.textAlign="center";
  for(const [v,label] of [[0,"0"],[.5,"0.5"],[1,"1"]]){
    ctx.fillText(label,x+v*len,y+len+18);
  }
  ctx.fillText("k₁",x+len/2,y+len+43);
  ctx.textAlign="right";
  for(const [v,label] of [[0,"0"],[.5,"0.5"],[1,"1"]]){
    ctx.fillText(label,x-8,y+(1-v)*len+4);
  }
  ctx.save();ctx.translate(17,y+len/2);ctx.rotate(-Math.PI/2);
  ctx.textAlign="center";ctx.fillText("k₂",0,0);ctx.restore();
  const zeros=zeroSet(ratio);
  if(zeros.kind==="line"){
    ctx.beginPath();ctx.moveTo(x,y+len/2);ctx.lineTo(x+len/2,y);
    ctx.moveTo(x+len/2,y+len);ctx.lineTo(x+len,y+len/2);
    ctx.strokeStyle="#E41A1C";ctx.lineWidth=2.5;ctx.stroke();
  }else{
    ctx.fillStyle="#FFCCD7";ctx.strokeStyle="#2B2B2B";ctx.lineWidth=1.7;
    for(const [k1,k2] of zeros.points){
      ctx.beginPath();ctx.arc(x+len*k1,y+len*(1-k2),5.5,0,TAU);ctx.fill();ctx.stroke();
    }
  }
}
function readout(ratio){
  const zeros=zeroSet(ratio);
  if(zeros.kind==="line") return "Jz = 0: line of zeros, k₂ = k₁ + 1/2 (mod 1).";
  if(zeros.kind==="merged") return "Jz = 2J: merged zero at (1/2, 1/2).";
  return "Two Dirac points: "+zeros.points.map(p=>"("+p[0].toFixed(3)+", "+p[1].toFixed(3)+")").join(" and ")+".";
}
function initialize(){
  const root=document.getElementById("kmf-dispersion");
  if(!root)return;
  const img=root.querySelector("img"),canvas=root.querySelector("canvas"),
    controls=root.querySelector(".kmf-controls"),slider=root.querySelector('input[type="range"]'),
    output=root.querySelector("output"),status=root.querySelector(".kmf-readout");
  const ctx=canvas?.getContext("2d");
  if(!img||!canvas||!ctx||!controls||!slider||!output||!status)return;
  const update=()=>{
    const ratio=Number(slider.value);
    draw(ctx,ratio);output.textContent=ratio.toFixed(2);status.textContent=readout(ratio);
    canvas.setAttribute("aria-label","Dimensionless r = |f|, Jz/J = "+ratio.toFixed(2)+". "+status.textContent);
  };
  update();canvas.hidden=false;img.hidden=true;controls.hidden=false;
  slider.addEventListener("input",update);
}
if(typeof document!=="undefined"){
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",initialize,{once:true});
  else initialize();
}
