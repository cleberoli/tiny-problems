from typing import Dict

from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.geometry.cone import Cone
from tinypy.graph.delaunay import DelaunayTriangulation
from tinypy.models.cone import Cone as DBCone
from tinypy.instances.base_instance import Instance


class VoronoiDiagram:
    """Represents a Voronoi diagram with the corresponding Delaunay triangulation.

    Attributes:
        type: The instance type.
        name: The instance name.
        delaunay: The corresponding Delaunay triangulation.
        hyperplanes: The corresponding hyperplanes for each Delaunay edge.
        cones: The cones for each solution.
    """

    type: str
    name: str
    cone_file: str

    instance: Instance
    delaunay: DelaunayTriangulation
    hyperplanes: Dict[int, Hyperplane]
    cones: Dict[int, Cone]

    def __init__(self,  instance: Instance, delaunay: DelaunayTriangulation, hyperplanes: Dict[int, Hyperplane]):
        """Initializes the Voronoi diagram.

        Args:
            delaunay: The corresponding Delaunay triangulation.
            hyperplanes: The corresponding hyperplanes for each Delaunay edge.
        """
        self.type = instance.type
        self.name = instance.name

        self.instance = instance
        self.delaunay = delaunay
        self.hyperplanes = hyperplanes

    def build(self, solutions: Dict[int, Point]):
        """Builds the Voronoi diagram based on the given solutions.

        Args:
            solutions: The Voronoi vertices.
        """
        db_cone = DBCone(self.instance.name, self.instance.type, self.instance.dimension, self.instance.size)
        doc = db_cone.get_doc()

        if doc is not None:
            self.cones = dict()

            for (key, value) in db_cone.cones.items():
                self.cones[key] = Cone(key, solutions[key], value)
        else:
            self.cones = self.__generate_cones(solutions)
            cones = dict()

            for (key, value) in self.cones.items():
                cones[key] = value.hyperplanes

            db_cone.cones = cones
            db_cone.add_doc()

    def __generate_cones(self, solutions: Dict[int, Point]) -> Dict[int, Cone]:
        """Generates the Voronoi cones.

        Args:
            solutions: The Voronoi vertices.

        Returns:
            The cones for each solution.
        """
        cones = dict()

        if len(self.hyperplanes) == 0:
            return cones

        for (s, solution) in solutions.items():
            cone = Cone(s, solution)
            edges = self.delaunay.get_edges(s)
            hyperplanes = [self.delaunay.get_edge(s, e) for e in edges]

            for h in hyperplanes:
                hyperplane = self.hyperplanes[h]

                if hyperplane.in_halfspace(solution):
                    cone.add_hyperplane(h)
                else:
                    cone.add_hyperplane(-h)

            cones[s] = cone

        return cones
