from tinypy.polytopes.hypercube_polytope import HypercubePolytope
from tinypy.trees.enumeration_tree import EnumerationTree
from tinypy.trees.tree_writer import TreeWriter
from tinypy.utils.file import delete_file, file_exists, get_full_path


def test_tree_writer():
    polytope = HypercubePolytope(4)
    tree = EnumerationTree(polytope)
    tree.make_tree()
    tree_file = get_full_path('tinypy', 'generated', 'trees', 'cub', 'CUB_n4.py')
    assert not file_exists(tree_file)

    writer = TreeWriter(tree)
    writer.write_tree()
    assert file_exists(tree_file)

    delete_file(tree_file)
    assert not file_exists(tree_file)
