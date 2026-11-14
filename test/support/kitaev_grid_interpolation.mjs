/* Unpublished, solver-independent candidate for branch-safe scalar interpolation. */
export function interpolateWithinSegment(records, h, branchId, segmentId) {
  if (!Number.isFinite(h)) throw new RangeError("finite h required");
  if (!branchId || !segmentId) throw new TypeError("branch and segment required");
  if (!Array.isArray(records)) throw new TypeError("records must be an array");
  const points=records.filter(x=>x.branch_id===branchId && x.segment_id===segmentId)
    .slice().sort((a,b)=>a.h-b.h);
  if (!points.length) throw new RangeError("no data for the selected branch/segment");
  if (points.some(p=>!Number.isFinite(p.h)||!Number.isFinite(p.value))) {
    throw new TypeError("nonfinite source values");
  }
  for(let i=1;i<points.length;i++) if(points[i].h<=points[i-1].h) {
    throw new RangeError("duplicate or nonascending h nodes");
  }
  const low=points[0], high=points[points.length-1];
  if(h<low.h||h>high.h) throw new RangeError("extrapolation or cross-segment evaluation forbidden");
  const exact=points.find(p=>p.h===h);
  if(exact) return {value:exact.value,method:"exact-grid",source_h:[h,h],branch_id:branchId,segment_id:segmentId};
  const index=points.findIndex(p=>p.h>h);
  if(index<1) throw new RangeError("missing interpolation bracket");
  const a=points[index-1],b=points[index];
  const weight=(h-a.h)/(b.h-a.h);
  return {value:(1-weight)*a.value+weight*b.value,method:"linear-candidate",source_h:[a.h,b.h],branch_id:branchId,segment_id:segmentId};
}
