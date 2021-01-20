from abc import ABC
from typing import Dict, Tuple

from tinypy.geometry.point import Point
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.voronoi import VoronoiDiagram
from tinypy.graph.skeleton import Skeleton
from tinypy.instances.base_instance import Instance
from tinypy.lp.adjacency import AdjacencyProblem
from tinypy.models.skeleton import Skeleton as DBSkeleton
from tinypy.models.polytope import Polytope as DBPolytope


class Polytope(ABC):
    """Base class that build the polytopes for different instances.

    Attributes:
        full_name: The polytope full name.
        name: The instance name.
        dimension: The instance dimension.
        size: The instance size.
        n: The instance main parameter.
        instance: The instance.
        skeleton: The skeleton graph.
        complement: The extended skeleton graph.
        hyperplanes: The set of hyperplanes.'
        voronoi: The Voronoi diagram.
        vertices: The polytope vertices.
    """

    full_name: str
    name: str
    dimension: int
    size: int
    n: int

    instance: Instance
    skeleton: Skeleton
    complement: Skeleton
    hyperplanes: Dict[int, Hyperplane]
    n_skeleton_hyperplanes: int
    n_complement_hyperplanes: int
    voronoi: VoronoiDiagram
    vertices: Dict[int, Point]

    def __init__(self, instance: Instance, full_name: str, save: bool = True):
        """Initializes the polytope with the given instance and name.

        Args:
            instance: The instance.
            full_name: The polytope full name.
        """
        self.instance = instance
        self.full_name = full_name
        self.name = self.instance.type
        self.dimension = self.instance.dimension
        self.size = self.instance.size
        self.n = self.instance.n

        self.vertices = self.instance.get_solution_dict().copy()
        self.vertices = dict((key, Point([1] * self.dimension) - 2 * point) for (key, point) in self.vertices.items())

        self.build_skeleton(save)
        self.voronoi = VoronoiDiagram(self.instance, self.skeleton, self.hyperplanes)
        self.voronoi.build(self.vertices, save)

        db_polytope = DBPolytope(instance.name, instance.type, instance.dimension, instance.size,
                                 self.n_skeleton_hyperplanes + self.n_complement_hyperplanes, len(self.skeleton.edges), self.skeleton.degree)

        if db_polytope.get_doc() is None and save:
            db_polytope.add_doc()

    def build_skeleton(self, save: bool = True):
        """Build the polytope skeleton.

        If the skeleton has been previously computed it is loaded from the file.
        Otherwise it is generated and saved.
        """
        db_skeleton = DBSkeleton(self.instance.name, self.instance.type, self.instance.dimension, self.instance.size, list(self.vertices.keys()))
        doc = db_skeleton.get_doc()

        if doc is not None:
            self.hyperplanes = db_skeleton.hyperplanes
            self.n_skeleton_hyperplanes = db_skeleton.n_skeleton_hyperplanes
            self.n_complement_hyperplanes = db_skeleton.n_complement_hyperplanes
            self.skeleton = Skeleton()
            self.complement = Skeleton()

            for s_edge in db_skeleton.skeleton_edges:
                self.skeleton.add_edge(s_edge[0], s_edge[1], s_edge[2])

            for c_edge in db_skeleton.complement_edges:
                self.complement.add_edge(c_edge[0], c_edge[1], c_edge[2])
        else:
            self.hyperplanes, self.skeleton, self.complement, self.n_skeleton_hyperplanes, self.n_complement_hyperplanes = self.__generate_skeleton()
            db_skeleton.hyperplanes = self.hyperplanes
            db_skeleton.n_skeleton_hyperplanes = self.n_skeleton_hyperplanes
            db_skeleton.n_complement_hyperplanes = self.n_complement_hyperplanes
            db_skeleton.skeleton_edges = self.skeleton.graph.edges.data('h')
            db_skeleton.complement_edges = self.complement.graph.edges.data('h')

            if save:
                db_skeleton.add_doc()

    def get_bisector(self, i: int, j: int) -> int:
        """Returns the bisector of two points.

        Args:
            i: First node.
            j: Second node.

        Returns:
            The index of the bisector hyperplane, chosen from the skeleton or
            the extended skeleton.
        """
        if self.skeleton.has_edge(i, j):
            return self.skeleton.get_edge(i, j, 'h')
        else:
            return self.complement.get_edge(i, j, 'h')

    def get_hyperplane(self, h: int) -> Hyperplane:
        return self.hyperplanes[h]

    def __generate_skeleton(self) -> Tuple[Dict[int, Hyperplane], Skeleton, Skeleton, int, int]:
        """Generates the skeleton along with the hyperplanes.

        Returns:
            The skeleton graph.
            The set of hyperplanes.
            The extended skeleton graph.
            The extended set of hyperplanes.
        """
        skeleton = Skeleton()
        extended_skeleton = Skeleton()
        adjacency_lp = AdjacencyProblem(self.dimension, self.instance.name, self.vertices)
        hyperplanes = set()
        extended_hyperplanes = set()
        vertices = self.instance.get_solution_dict()

        for i in range(1, self.size + 1):
            for j in range(i + 1, self.size + 1):
                h = Hyperplane(vertices[j] - vertices[i], d=0)

                if adjacency_lp.test_edge_primal(i, j):
                    hyperplanes.add(h)
                    skeleton.add_edge(i, j, h=hash(h))
                else:
                    extended_hyperplanes.add(h)
                    extended_skeleton.add_edge(i, j, h=hash(h))

        hyperplanes = list(hyperplanes)
        hyperplanes.sort()
        hyperplanes = dict((key + 1, hyperplanes[key]) for key in range(len(hyperplanes)))

        extended_hyperplanes = list(extended_hyperplanes)
        extended_hyperplanes.sort()
        extended_hyperplanes = dict((key + len(hyperplanes) + 1, extended_hyperplanes[key]) for key in range(len(extended_hyperplanes)))

        map_dict = {hash(hyperplanes[i]): i for i in hyperplanes.keys()}
        extended_map_dict = {hash(extended_hyperplanes[i]): i for i in extended_hyperplanes.keys()}

        for edge in skeleton.edges:
            skeleton.add_edge(edge[0], edge[1], h=map_dict[skeleton.get_edge(edge[0], edge[1], 'h')])

        for edge in extended_skeleton.edges:
            extended_skeleton.add_edge(edge[0], edge[1], h=extended_map_dict[extended_skeleton.get_edge(edge[0], edge[1], 'h')])

        return {**hyperplanes, **extended_hyperplanes}, skeleton, extended_skeleton, len(hyperplanes), len(extended_hyperplanes)

    def __repr__(self):  # pragma: no cover
        return f'NAME: {self.instance.name}\n' \
               f'TYPE: {self.instance.type.upper()}\n' \
               f'DIMENSION: {self.dimension}\n' \
               f'SOLUTIONS: {self.size}\n' \
               f'HYPERPLANES: {self.n_skeleton_hyperplanes + self.n_complement_hyperplanes}\n' \
               f'EDGES: {len(self.skeleton.edges)}\n' \
               f'AVERAGE DEGREE: {self.skeleton.degree}\n'
