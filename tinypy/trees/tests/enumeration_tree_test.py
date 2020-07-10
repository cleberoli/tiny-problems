from tinypy.polytopes.hypercube_polytope import HypercubePolytope
from tinypy.trees.enumeration_tree import EnumerationTree


def test_enumeration_tree():
    polytope = HypercubePolytope(4)
    tree = EnumerationTree(polytope)

    assert tree.polytope == polytope
    assert len(tree.graph.nodes) == 0
    assert len(tree.graph.edges) == 0
    assert len(tree.queue) == 0

    tree.make_tree()
    assert tree.height == 4


def test_enumeration_bfs():
    polytope = HypercubePolytope(4)
    tree = EnumerationTree(polytope)
    tree.make_tree(bfs=True)
    
    assert tree.height == 4