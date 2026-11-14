import assert from "node:assert/strict";
import test from "node:test";
import {interpolateWithinSegment} from "../support/kitaev_grid_interpolation.mjs";
const samples=[
 {h:0,value:1,branch_id:"A",segment_id:"low"},
 {h:.2,value:.6,branch_id:"A",segment_id:"low"},
 {h:.8,value:7,branch_id:"A",segment_id:"high"},
 {h:1,value:8,branch_id:"A",segment_id:"high"},
 {h:0,value:3,branch_id:"B",segment_id:"low"},
 {h:.2,value:4,branch_id:"B",segment_id:"low"}
];
test("exact grid nodes and candidate linear interpolation",()=>{
 const out=interpolateWithinSegment(samples,.1,"A","low");
 assert.ok(Math.abs(out.value-.8)<1e-12);
 assert.deepEqual(out.source_h,[0,.2]);
 assert.equal(out.method,"linear-candidate");
 assert.equal(interpolateWithinSegment(samples,.8,"A","high").value,7);
});
test("disallow interpolation across phase segments, branches, extrapolation",()=>{
 for(const [h,branch,segment] of [[.5,"A","low"],[.5,"A","high"],[.1,"B","high"],[-.1,"A","low"]]){
  assert.throws(()=>interpolateWithinSegment(samples,h,branch,segment),RangeError);
 }
});
test("reject duplicated grid nodes and nonfinite data",()=>{
 assert.throws(()=>interpolateWithinSegment([...samples,samples[0]],.1,"A","low"),RangeError);
 assert.throws(()=>interpolateWithinSegment([{h:0,value:NaN,branch_id:"A",segment_id:"low"}],0,"A","low"),TypeError);
});
