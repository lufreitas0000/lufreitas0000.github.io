/* Illustrative 2x2 linear fixed point, not the Kitaev solver Jacobian. */
export const ORIGINAL_EIGENVALUES = [-1.5, 0.4];

export function dampedEigenvalues(alpha) {
  if (!Number.isFinite(alpha) || alpha < 0 || alpha > 1) {
    throw new RangeError("alpha must be in [0,1]");
  }
  return ORIGINAL_EIGENVALUES.map(lambda => 1 - alpha + alpha * lambda);
}
export function spectralRadius(alpha) {
  return Math.max(...dampedEigenvalues(alpha).map(Math.abs));
}

function draw(ctx,alpha){
  const values=dampedEigenvalues(alpha);
  ctx.clearRect(0,0,440,370);
  ctx.fillStyle="#FAF6EE";ctx.fillRect(0,0,440,370);
  const ox=225,oy=165,s=105;
  ctx.strokeStyle="#B8AD9D";ctx.lineWidth=1;
  ctx.beginPath();ctx.moveTo(20,oy);ctx.lineTo(430,oy);ctx.moveTo(ox,10);ctx.lineTo(ox,330);ctx.stroke();
  ctx.strokeStyle="#00639A";ctx.lineWidth=1.8;
  ctx.beginPath();ctx.arc(ox,oy,s,0,Math.PI*2);ctx.stroke();
  ctx.fillStyle="#2B2B2B";ctx.font="13px Georgia,serif";ctx.textAlign="center";
  ctx.fillText("Re λ",415,oy-8);
  ctx.fillText("Im λ",ox+28,18);
  ctx.fillText("−1",ox-s,oy+17);ctx.fillText("0",ox,oy+17);ctx.fillText("1",ox+s,oy+17);
  ctx.font="14px Georgia,serif";
  values.forEach((v,i)=>{
    ctx.beginPath();ctx.fillStyle=i===0?"#E41A1C":"#3B8E38";
    ctx.strokeStyle="#2B2B2B";ctx.lineWidth=1;
    ctx.arc(ox+v*s,oy,6,0,Math.PI*2);ctx.fill();ctx.stroke();
    ctx.fillStyle="#2B2B2B";
    ctx.fillText("λ"+(i+1),ox+v*s,oy-14);
  });
}
function initialize(){
  const root=document.getElementById("kmf-jacobian");if(!root)return;
  const controls=root.querySelector(".kmf-controls"),input=root.querySelector('input[type="range"]'),
    output=root.querySelector("output"),status=root.querySelector(".kmf-readout"),
    image=root.querySelector("img"),canvas=root.querySelector("canvas");
  const ctx=canvas?.getContext("2d");
  if(!controls||!input||!output||!status||!image||!canvas||!ctx)return;
  const update=()=>{
    const alpha=Number(input.value),vals=dampedEigenvalues(alpha),rho=spectralRadius(alpha);
    draw(ctx,alpha);output.textContent=alpha.toFixed(2);
    status.textContent="Eigenvalues: "+vals.map(x=>x.toFixed(3)).join(", ")+
      "; spectral radius "+rho.toFixed(3)+". "+(rho<1?"Convergent linear iteration.":rho>1?"Divergent linear iteration.":"Borderline: not asymptotically convergent.");
    canvas.setAttribute("aria-label",status.textContent);
  };
  update();image.hidden=true;canvas.hidden=false;controls.hidden=false;
  input.addEventListener("input",update);
}
if(typeof document!=="undefined"){
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",initialize,{once:true});
  else initialize();
}
