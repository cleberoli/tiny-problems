from copy import deepcopy
from typing import List

from networkx import DiGraph

from tinypy.geometry.intersections import Intersections
from tinypy.geometry.region import Region
from tinypy.polytopes.base_polytope import Polytope


class EnumerationTree:

    polytope: Polytope
    graph: DiGraph
    queue: List[int]
    height: int
    root: int

    def __init__(self, polytope: Polytope):
        self.graph = DiGraph()
        self.polytope = polytope
        self.intersections = Intersections(polytope)
        self.queue = []
        self.next_node = 0
        self.height = 0
        self.root = 1

    def make_tree(self):
        root_node = self.__add_node(0, list(self.polytope.vertices.keys()), Region())
        self.queue.append(root_node)
        self.dfs()

    def __add_node(self, height: int, solutions: List[int], region: Region) -> int:
        self.graph.add_node(self.__get_next_node(), height=height, solutions=solutions, region=region)
        self.height = max(self.height, height)

        return self.next_node

    def __get_next_node(self):
        self.next_node = self.next_node + 1
        return self.next_node

    def bfs(self):
        height: int
        solutions: List[int]
        hyperplanes: List[int]
        region: Region

        while len(self.queue) > 0:
            parent_node = self.queue.pop(0)
            node = self.graph.nodes[parent_node]
            height, solutions, region = node['height'], node['solutions'].copy(), deepcopy(node['region'])
            sol_i, sol_j = solutions[0], solutions[1]
            if self.polytope.voronoi.delaunay.skeleton.graph.has_edge(sol_i, sol_j):
                hyperplane = self.polytope.voronoi.delaunay.get_edge(sol_i, sol_j, 'h')
            else:
                hyperplane = self.polytope.extended_skeleton.get_edge(sol_i, sol_j, 'h')
            # i, j = 0, 1
            #
            # while not self.polytope.voronoi.delaunay.skeleton.graph.has_edge(sol_i, sol_j):
            #     j = j + 1
            #
            #     if j >= len(solutions):
            #         i = i + 1
            #         j = i + 2
            #         sol_i = solutions[i]
            #
            #     sol_j = solutions[j]

            # hyperplane = self.polytope.voronoi.delaunay.get_edge(sol_i, sol_j, 'h')
            node['hyperplane'] = hyperplane
            positions = self.intersections.get_positions(region, solutions, [hyperplane])

            left_solutions = [item for item in solutions if item not in positions[hyperplane].right]
            right_solutions = [item for item in solutions if item not in positions[hyperplane].left]
            # print(height, len(solutions), solutions, left_solutions, right_solutions)

            left_region = deepcopy(region)
            right_region = deepcopy(region)
            left_region.add_hyperplane(-hyperplane)
            right_region.add_hyperplane(hyperplane)

            # children_hyperplanes = hyperplanes.copy()
            # children_hyperplanes.remove(hyperplane)

            left_node = self.__add_node(height + 1, left_solutions, left_region)
            self.graph.add_edge(parent_node, left_node, direction='left')

            if len(left_solutions) > 1:
                self.queue.append(left_node)
            else:
                print(left_node)

            right_node = self.__add_node(height + 1, right_solutions, right_region)
            self.graph.add_edge(parent_node, right_node, direction='right')

            if len(right_solutions) > 1:
                self.queue.append(right_node)
            else:
                print(right_node)

    def dfs(self):
        height: int
        solutions: List[int]
        hyperplanes: List[int]
        region: Region

        while len(self.queue) > 0:
            parent_node = self.queue.pop()
            node = self.graph.nodes[parent_node]
            height, solutions, region = node['height'], node['solutions'].copy(), deepcopy(node['region'])
            sol_i, sol_j = solutions[0], solutions[1]
            if self.polytope.voronoi.delaunay.skeleton.graph.has_edge(sol_i, sol_j):
                hyperplane = self.polytope.voronoi.delaunay.get_edge(sol_i, sol_j, 'h')
            else:
                hyperplane = self.polytope.extended_skeleton.get_edge(sol_i, sol_j, 'h')
            # i, j = 0, 1
            #
            # while not self.polytope.voronoi.delaunay.skeleton.graph.has_edge(sol_i, sol_j):
            #     j = j + 1
            #
            #     if j >= len(solutions):
            #         i = i + 1
            #         j = i + 2
            #         sol_i = solutions[i]
            #
            #     sol_j = solutions[j]

            # hyperplane = self.polytope.voronoi.delaunay.get_edge(sol_i, sol_j, 'h')
            node['hyperplane'] = hyperplane
            positions = self.intersections.get_positions(region, solutions, [hyperplane])

            left_solutions = [item for item in solutions if item not in positions[hyperplane].right]
            right_solutions = [item for item in solutions if item not in positions[hyperplane].left]
            # print(height, len(solutions), solutions, left_solutions, right_solutions)

            left_region = deepcopy(region)
            right_region = deepcopy(region)
            left_region.add_hyperplane(-hyperplane)
            right_region.add_hyperplane(hyperplane)

            # children_hyperplanes = hyperplanes.copy()
            # children_hyperplanes.remove(hyperplane)

            left_node = self.__add_node(height + 1, left_solutions, left_region)
            self.graph.add_edge(parent_node, left_node, direction='left')

            if len(left_solutions) > 1:
                self.queue.append(left_node)
            # else:
            #     print(self.graph.nodes[left_node]['height'], self.graph.nodes[left_node]['solutions'])

            right_node = self.__add_node(height + 1, right_solutions, right_region)
            self.graph.add_edge(parent_node, right_node, direction='right')

            if len(right_solutions) > 1:
                self.queue.append(right_node)
            # else:
            #     print(self.graph.nodes[right_node]['height'], self.graph.nodes[right_node]['solutions'])
