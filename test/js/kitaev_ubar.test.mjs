import assert from "node:assert/strict";
import test from "node:test";
import {midpointUBar, REFERENCE_U_BAR} from "../../site/assets/js/kitaev_ubar.mjs";
const refs=new Map([
  [8,0.5248951470396],[16,0.5248532247853],[32,0.5248651506310],
  [64,0.5248656070195],[128,0.5248657324414],[256,0.5248657439247]
]);
test("deterministic midpoint quadrature agrees with independent fixtures",()=>{
  for(const [N,expected] of refs) assert.ok(Math.abs(midpointUBar(N)-expected)<5e-12, "N="+N);
});
test("reference value and convergence scale",()=>{
  assert.ok(Math.abs(midpointUBar(256)-REFERENCE_U_BAR)<3e-9);
  assert.ok(Math.abs(midpointUBar(128)-REFERENCE_U_BAR)<2e-8);
});
test("invalid N rejected",()=>{
  for(const N of [0,1,257,2.5,Infinity,NaN]) assert.throws(()=>midpointUBar(N),RangeError);
});
