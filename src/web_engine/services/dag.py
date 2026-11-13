"""Pure Directed Acyclic Graph (DAG) navigation service (zero HTML, zero I/O)."""

from __future__ import annotations

from typing import Iterable

from ..domain.contracts import ContractViolationError
from ..domain.models import SiteGraph, SiteNode, SitemapBranch


PRIMARY_NODE_IDS: tuple[str, ...] = ("home", "research", "about", "notes")


def build_and_verify_site_dag(nodes: Iterable[SiteNode]) -> SiteGraph:
    """Pure constructor validating parent pointers and proving the navigation graph is acyclic."""
    node_map: dict[str, SiteNode] = {}
    for n in nodes:
        if n.node_id in node_map:
            raise ContractViolationError(f"Duplicate DAG node_id: {n.node_id!r}")
        node_map[n.node_id] = n

    children_lists: dict[str, list[str]] = {nid: [] for nid in node_map}
    for n in node_map.values():
        if n.parent_id is not None:
            if n.parent_id not in node_map:
                raise ContractViolationError(
                    f"DAG node {n.node_id!r} references non-existent parent_id {n.parent_id!r}"
                )
            children_lists[n.parent_id].append(n.node_id)

    state: dict[str, int] = {nid: 0 for nid in node_map}

    def _dfs(cur: str) -> None:
        state[cur] = 1
        for child_id in children_lists[cur]:
            if state[child_id] == 1:
                raise ContractViolationError(f"Cycle detected in SiteGraph involving node {child_id!r}")
            if state[child_id] == 0:
                _dfs(child_id)
        state[cur] = 2

    for nid in node_map:
        if state[nid] == 0:
            _dfs(nid)

    return SiteGraph(
        nodes=node_map,
        children_map={k: tuple(v) for k, v in children_lists.items()},
    )


def compute_breadcrumb_trail(graph: SiteGraph, node_id: str) -> tuple[SiteNode, ...]:
    """Pure function returning the ordered ancestor path `(root, ..., current_node)` for `node_id`."""
    if node_id not in graph.nodes:
        return ()
    trail: list[SiteNode] = []
    cur: SiteNode | None = graph.nodes[node_id]
    while cur is not None:
        trail.append(cur)
        cur = graph.nodes.get(cur.parent_id) if cur.parent_id else None
    trail.reverse()
    return tuple(trail)


def get_visible_sitemap_branches(graph: SiteGraph) -> tuple[SitemapBranch, ...]:
    """Pure function returning visible primary nodes and their visible non-primary children."""
    branches: list[SitemapBranch] = []
    for pid in PRIMARY_NODE_IDS:
        pnode = graph.nodes.get(pid)
        if not pnode or not pnode.visible:
            continue
        child_ids = graph.children_map.get(pid, ())
        visible_children = tuple(
            graph.nodes[cid]
            for cid in child_ids
            if cid != pid and cid not in PRIMARY_NODE_IDS and graph.nodes[cid].visible
        )
        branches.append(SitemapBranch(root=pnode, children=visible_children))
    return tuple(branches)
