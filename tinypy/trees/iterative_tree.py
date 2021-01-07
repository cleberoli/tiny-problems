import time
from math import ceil, log2
from typing import Dict, List

from tinypy.geometry.bisection import Bisection
from tinypy.geometry.intersections import Intersections
from tinypy.geometry.region import Region
from tinypy.polytopes.base_polytope import Polytope
from tinypy.trees.node import Node
from tinypy.trees.tree_builder import TreeBuilder
from tinypy.utils.constants import INFINITY


class IterativeTree:

    polytope: Polytope
    intersections: Intersections

    threshold: int
    lb: int
    ub: int

    table: Dict[int, List[List[int]]]
    nodes: Dict[str, Node]
    tree_builder: TreeBuilder

    def __init__(self, polytope: Polytope):
        self.polytope = polytope
        self.intersections = Intersections(polytope)
        self.threshold = INFINITY
        self.lb = ceil(log2(len(self.polytope.vertices)))
        self.ub = len(self.polytope.vertices) - 1
        self.table = self.get_ordering_table()
        self.nodes = dict()
        self.tree_builder = TreeBuilder(polytope)

    def build_tree(self, threshold: int = INFINITY):
        region = Region()
        solutions = list(self.polytope.vertices.keys())
        hyperplanes = list(self.polytope.hyperplanes.keys())
        positions = self.intersections.get_positions(region, solutions)
        hyperplanes = self.process_hyperplanes(hyperplanes, positions, len(solutions))
        node = Node(region, solutions, hyperplanes)
        self.threshold = min(threshold, len(hyperplanes))
        self.lb = self.get_lower_bound(node)

        start_time = time.time()

        for k in range(1, self.threshold + 1):
            root = self.explore_node(node, k, self.lb)
            self.ub = root.height
            tree = self.tree_builder.build_tree(self.nodes, root, k)
            tree.add_doc()
            e = int(time.time() - start_time)
            print(k, root.height, '{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

            if root.threshold == -1:
                print('OPTIMAL SOLUTION FOUND')
                break

    def explore_node(self, node: Node, k: int, lb: int) -> Node:
        if node.hash in self.nodes:
            node = self.nodes[node.hash]

        if node.threshold == -1:                                                # node calculated to optimality
            return node
        else:
            if node.hash not in self.nodes:                                     # first time calculation
                min_height = INFINITY
                node.hyperplane = None
                node.left = None
                node.right = None
                node.height = INFINITY
                valid_tree = False
            else:                                                               # node previous calculated
                min_height = node.height
                valid_tree = True

            optimal_tree = False

            # run computations for k hyperplanes in each level
            # a previous calculated node stores how many hyperplanes as threshold
            for i in range(min(k, len(node.hyperplanes))):
                h = node.hyperplanes[i]

                if len(node.region) >= self.ub:
                    break

                new_hyperplanes = node.hyperplanes.copy()
                new_hyperplanes.remove(h)

                left_solutions = [item for item in node.solutions if item not in self.intersections.positions[node.hash][h].right]

                if len(left_solutions) == 1:
                    left_subtree = self.case_1(node, left_solutions, new_hyperplanes, -h)
                elif len(left_solutions) == 2:
                    left_subtree = self.case_2(node, left_solutions, new_hyperplanes, -h)
                else:
                    left_node = self.case_default(node, left_solutions, new_hyperplanes, -h)
                    left_subtree = self.explore_node(left_node, k, self.get_lower_bound(left_node))

                if left_subtree.height <= min_height:
                    right_solutions = [item for item in node.solutions if item not in self.intersections.positions[node.hash][h].left]
                    right_region = Region(node.region)
                    right_region.add_hyperplane(h)

                    if len(right_solutions) == 1:
                        right_subtree = self.case_1(node, right_solutions, new_hyperplanes, h)
                    elif len(right_solutions) == 2:
                        right_subtree = self.case_2(node, right_solutions, new_hyperplanes, h)
                    else:
                        right_node = self.case_default(node, right_solutions, new_hyperplanes, h)
                        right_subtree = self.explore_node(right_node, k, self.get_lower_bound(right_node))

                    height = max(left_subtree.height, right_subtree.height)

                    if height < min_height - 1:
                        min_height = height + 1
                        node.hyperplane = h
                        node.height = height + 1
                        node.left = left_subtree.hash
                        node.right = right_subtree.hash
                        valid_tree = True

                if i >= node.threshold:
                    node.threshold = node.threshold + 1

                if node.height == lb or k >= len(node.hyperplanes):
                    optimal_tree = True
                    break

            if optimal_tree or len(node.hyperplanes) == 0:
                node.threshold = -1
                node.hyperplanes = []

            if node.hash not in self.nodes or valid_tree:
                self.nodes[node.hash] = node

            return node

    def process_hyperplanes(self, hyperplanes: List[int], positions: Dict[int, Bisection], s: int) -> List[int]:
        ordered_hyperplanes = []

        for h in hyperplanes:
            s_l = s - len(positions[h].right)
            s_r = s - len(positions[h].left)
            order = self.table[s][s_l][s_r]

            if s_l + s_r > s or s_l > 0 and s_r > 0:
                ordered_hyperplanes.append((h, order))

        ordered_hyperplanes.sort(key=lambda x: x[1])

        return [h[0] for h in ordered_hyperplanes]

    def get_ordering_table(self) -> Dict[int, List[List[int]]]:
        table = dict()

        for s in range(2, self.polytope.instance.size + 1):
            table[s] = [[0 for _ in range(s + 1)] for _ in range(s + 1)]
            half = ceil(s / 2)
            order = 1

            for i in range(half, s + 1):
                for j in range(s - i, i + 1):
                    table[s][i][j] = table[s][j][i] = order
                    order = order + 1

        return table

    def get_lower_bound(self, node: Node) -> int:
        best_l = len(node.solutions) - len(self.intersections.positions[node.hash][node.hyperplanes[0]].left)
        best_r = len(node.solutions) - len(self.intersections.positions[node.hash][node.hyperplanes[0]].right)
        return ceil(log2(max(best_l, best_r))) + 1

    def case_1(self, node: Node, solutions: List[int], hyperplanes: List[int], hyperplane: int) -> Node:
        region = Region(node.region)
        region.add_hyperplane(hyperplane)
        new_node = Node(region, solutions, hyperplanes)
        new_node.set_leaf()

        self.nodes[new_node.hash] = new_node
        return new_node

    def case_2(self, node: Node, solutions: List[int], hyperplanes: List[int], hyperplane: int) -> Node:
        region = Region(node.region)
        region.add_hyperplane(hyperplane)
        new_node = Node(region, solutions, hyperplanes)
        h = self.polytope.get_bisector(solutions[0], solutions[1])

        left_region = Region(new_node.region)
        left_region.add_hyperplane(-h)
        left_node = Node(left_region, [solutions[1]], hyperplanes)
        left_node.set_leaf()
        self.nodes[left_node.hash] = left_node

        right_region = Region(new_node.region)
        right_region.add_hyperplane(h)
        right_node = Node(right_region, [solutions[0]], hyperplanes)
        right_node.set_leaf()
        self.nodes[right_node.hash] = right_node

        new_node.set_node(1, -1, self.polytope.get_bisector(solutions[0], solutions[1]), left_node.hash, right_node.hash)
        new_node.hyperplanes = []

        self.nodes[new_node.hash] = new_node
        return new_node

    def case_default(self, node: Node, solutions: List[int], hyperplanes: List[int], hyperplane: int) -> Node:
        region = Region(node.region)
        region.add_hyperplane(hyperplane)
        positions = self.intersections.get_positions(region, solutions)
        new_hyperplanes = self.process_hyperplanes(hyperplanes, positions, len(solutions))
        new_node = Node(region, solutions, new_hyperplanes)

        return new_node
