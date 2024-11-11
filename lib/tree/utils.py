from .node import TreeNode
from enum import Enum


class TraversalMode(Enum):
    DEPTH_FIRST = 0
    BREADTH_FIRST = 1


def traverse(v: TreeNode, mode: TraversalMode = TraversalMode.DEPTH_FIRST):
    # generator
    yield v
    queue = [c for c in v.children]
    while queue:
        yield queue[0]
        next_nodes = [c for c in queue[0].children]
        if mode == TraversalMode.DEPTH_FIRST:
            queue = next_nodes + queue[1:]
        else:
            queue = queue[1:] + next_nodes


def size(v: TreeNode):
    return len([v for v in traverse(v)])

def render(v: TreeNode):
    # TODO: pretty print the tree
    pass