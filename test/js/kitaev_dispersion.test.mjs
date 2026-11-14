import assert from "node:assert/strict";
import test from "node:test";
import { radialModulus, zeroSet } from "../../site/assets/js/kitaev_dispersion.mjs";
const tol=2e-12;
test("isotropic spectral landmarks",()=>{
  assert.ok(Math.abs(radialModulus(1,0,0)-3)<tol);
  for(const [a,b] of [[.5,0],[0,.5],[.5,.5]]) assert.ok(Math.abs(radialModulus(1,a,b)-1)<tol);
  for(const [a,b] of [[1/3,2/3],[2/3,1/3]]) assert.ok(radialModulus(1,a,b)<tol);
});
test("line, pair and merger of exact zeros",()=>{
  for(const t of [0,.02,.5,1,1.5,1.98,2]){
    const z=zeroSet(t);
    if(t===0){
      assert.equal(z.kind,"line");
      for(const a of [0,.18,.5,.79]) assert.ok(radialModulus(0,a,(a+.5)%1)<tol);
    }else if(t===2){
      assert.equal(z.kind,"merged");
      assert.deepEqual(z.points,[[.5,.5]]);
      assert.ok(radialModulus(2,.5,.5)<tol);
    }else{
      assert.equal(z.kind,"points");assert.equal(z.points.length,2);
      for(const p of z.points) assert.ok(radialModulus(t,...p)<tol);
    }
  }
});
test("torus periodicity and domain",()=>{
  for(const t of [0,.5,1,1.5,2]) for(const [a,b] of [[.12,.45],[.3,.7],[.8,.1]]){
    const v=radialModulus(t,a,b);
    assert.ok(v>=0 && v<=2+t+tol);
    assert.ok(Math.abs(v-radialModulus(t,a+1,b-1))<tol);
  }
  for(const bad of [-.1,2.1,NaN,Infinity]){
    assert.throws(()=>radialModulus(bad,.3,.7),RangeError);
    assert.throws(()=>zeroSet(bad),RangeError);
  }
});
