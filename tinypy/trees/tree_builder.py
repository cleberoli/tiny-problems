from typing import Dict

from tinypy.models.tree import Tree
from tinypy.polytopes.base_polytope import Polytope
from tinypy.trees.node import Node


class TreeBuilder:

    polytope: Polytope

    def __init__(self, polytope: Polytope):
        self.polytope = polytope

    def build_tree(self, nodes: Dict[str, Node], root: Node, k: int) -> Tree:
        tree = Tree(self.polytope.instance.name, self.polytope.instance.type, k)
        tree.root = root.hash
        tree.add_node(root.hash, 0, root.solutions, root.hyperplane)
        queue = [(root, 0)]

        while len(queue) > 0:
            node, height = queue.pop(0)
            left_node = nodes[node.left]
            tree.add_node(left_node.hash, height + 1, left_node.solutions, left_node.hyperplane)
            tree.add_edge_left(node.hash, left_node.hash)

            if len(left_node.solutions) > 1:
                queue.append((left_node, height + 1))

            right_node = nodes[node.right]
            tree.add_node(right_node.hash, height + 1, right_node.solutions, right_node.hyperplane)
            tree.add_edge_right(node.hash, right_node.hash)

            if len(right_node.solutions) > 1:
                queue.append((right_node, height + 1))

        return tree
