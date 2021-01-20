from tinypy.models.tree import Tree
from tinypy.polytopes.base_polytope import Polytope
from tinypy.geometry.point import Point


class TreeRunner:

    polytope: Polytope
    tree: Tree

    def __init__(self, polytope: Polytope):
        self.polytope = polytope
        self.tree = Tree(polytope.instance.name, polytope.instance.type, 1)
        self.tree.get_doc()

    def run(self, point: Point):
        parent = self.tree.root
        node = self.tree.graph.nodes[parent]
        left = None
        right = None

        while node['hyperplane'] is not None:
            h = self.polytope.hyperplanes[node['hyperplane']]

            for child, direction in self.tree.graph[parent].items():
                if direction['direction'] == 'left':
                    left = child
                else:
                    right = child

            if h.in_halfspace(point):
                parent = right
            else:
                parent = left

            node = self.tree.graph.nodes[parent]

        print(node['solutions'][0])
