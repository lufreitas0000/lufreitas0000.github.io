import assert from "node:assert/strict";
import test from "node:test";
import {ORIGINAL_EIGENVALUES,dampedEigenvalues,spectralRadius} from "../../site/assets/js/kitaev_jacobian_toy.mjs";
test("undamped and damped eigenvalue maps",()=>{
  assert.deepEqual(ORIGINAL_EIGENVALUES,[-1.5,.4]);
  assert.deepEqual(dampedEigenvalues(1),[-1.5,.4]);
  const atHalf=dampedEigenvalues(.5);
  assert.ok(Math.abs(atHalf[0]+.25)<1e-12);
  assert.ok(Math.abs(atHalf[1]-.7)<1e-12);
  assert.ok(Math.abs(spectralRadius(.5)-.7)<1e-12);
});
test("threshold for linear stability",()=>{
  for(const a of [.1,.25,.5,.75]) assert.ok(spectralRadius(a)<1);
  assert.ok(Math.abs(spectralRadius(.8)-1)<1e-12);
  for(const a of [.85,1]) assert.ok(spectralRadius(a)>1);
});
test("reject invalid damping",()=>{
  for(const a of [-.1,1.1,Infinity,NaN]) assert.throws(()=>dampedEigenvalues(a),RangeError);
});
