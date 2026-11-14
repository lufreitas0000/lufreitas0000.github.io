/* Midpoint torus quadrature for the exact isotropic Kitaev bond benchmark. */
export const REFERENCE_U_BAR = 0.5248657458506;

export function midpointUBar(N) {
  if (!Number.isInteger(N) || N < 2 || N > 256) throw new RangeError("N must be an integer in [2,256]");
  const tau=2*Math.PI, phases=new Array(N);
  for(let i=0;i<N;i++) phases[i]=tau*(i+.5)/N;
  const cos=phases.map(Math.cos), sin=phases.map(Math.sin);
  let total=0;
  for(let a=0;a<N;a++) for(let b=0;b<N;b++) {
    total+=Math.hypot(1+cos[a]+cos[b],sin[a]+sin[b]);
  }
  return total/(3*N*N);
}

function initialize(){
  const root=document.getElementById("kmf-ubar");
  if(!root)return;
  const controls=root.querySelector(".kmf-ubar-controls");
  const select=root.querySelector("select");
  const output=root.querySelector(".kmf-ubar-result");
  if(!controls||!select||!output)return;
  const update=()=>{
    const N=Number(select.value),value=midpointUBar(N);
    const error=Math.abs(value-REFERENCE_U_BAR);
    output.textContent="N = "+N+": midpoint value "+value.toFixed(12)+"; absolute difference "+error.toExponential(3)+".";
  };
  select.addEventListener("change",update);
  update();controls.hidden=false;
}

if(typeof document!=="undefined"){
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",initialize,{once:true});
  else initialize();
}
