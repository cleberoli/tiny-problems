from typing import Dict, List, Tuple

from tinypy.geometry.bisection import Bisection
from tinypy.geometry.cone import Cone
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.region import Region
from tinypy.lp.intersection import IntersectionProblem
from tinypy.polytopes.base_polytope import Polytope


class Intersections:
    """Computes the intersections of hyperplanes and solution cones.

    The files are stored in order to speed up the process in case of any kind
    of interruptions.


    Attributes:
        type: The instance type.
        name: The instance name.
        polytope: The polytope.
        hyperplanes: The polytope's set of hyperplanes.
        cones: The polytope's solution cones.
        intersection_lp: Instance of the intersection linear program model.
    """

    EPSILON = 1E-4
    LEFT = 0
    RIGHT = 1

    type: str
    name: str
    intersection_file: str

    polytope: Polytope
    hyperplanes: Dict[int, 'Hyperplane']
    cones: Dict[int, 'Cone']
    intersection_lp: IntersectionProblem
    positions: Dict[str, Dict[int, Bisection]]

    def __init__(self, polytope: Polytope):
        """Initializes the intersections.

        Args:
            polytope: The polytope.
        """
        self.type = polytope.instance.type
        self.name = polytope.instance.name
        self.positions = dict()

        self.polytope = polytope
        self.hyperplanes = polytope.hyperplanes
        self.cones = polytope.voronoi.cones
        self.intersection_lp = IntersectionProblem(polytope.dimension, polytope.instance.name, self.cones, self.hyperplanes,
                                                   polytope.instance.get_triangles())

    def get_positions(self, region: 'Region', cones: List[int], hyperplanes: List[int] = None) -> Dict[int, 'Bisection']:
        """Returns the the positions of cones with respect to hyperplanes.

        Computes the positions of cones relative to all possible hyperplanes
        that do not delimit the given region.

        Args:
            region: The region to be considered.
            cones: The cones to be considered.
            hyperplanes: List of hyperplanes to be considered.
        Returns:
            The bisections of the given cones for each hyperplane.
        """
        if hyperplanes is None:
            hyperplanes = [h for h in self.hyperplanes.keys() if h not in region.hyperplanes and -h not in region.hyperplanes]

        if hash(region) in self.positions:
            hyperplanes = [h for h in hyperplanes if h not in self.positions[repr(region)].keys()]

            if len(hyperplanes) > 0:
                self.__compute_positions(region, cones, hyperplanes)
        else:
            self.positions[repr(region)] = dict()
            self.__compute_positions(region, cones, hyperplanes)

        return self.positions[repr(region)]

    def __compute_positions(self, region: 'Region', reference_cones: List[int], reference_hyperplanes: List[int]):
        """Returns the the positions of cones with respect to hyperplanes.

        Args:
            region: The region to be considered.
            reference_cones: The cones to be considered.
            reference_hyperplanes: The hyperplanes whose bisections we want.

        Returns:
            The bisections of the given cones for each hyperplane.
        """
        intersections = self.__compute_intersections(region, reference_cones, reference_hyperplanes)

        for h in reference_hyperplanes:
            self.positions[repr(region)][h] = Bisection()
            cones = [c for (c, value) in intersections[h].items() if value[0] is False or value[1] is False]

            for c in cones:
                if intersections[h][c][self.RIGHT] is True:
                    self.positions[repr(region)][h].add_right(c)
                else:
                    self.positions[repr(region)][h].add_left(c)

    def __compute_intersections(self, region: 'Region', cones: List[int], hyperplanes: List[int]) -> Dict[int, Dict[int, Tuple[bool, bool]]]:
        """Computes the intersections of each hyperplane with each cone.

        Args:
            region: The region to be considered.
            cones: The cones to be considered.
            hyperplanes: The hyperplanes whose bisections we want.

        Returns:
            The intersections of the hyperplanes with cones.
        """
        intersections = dict()

        for h in hyperplanes:
            intersections[h] = dict()

            for c in cones:
                intersections[h][c] = self.intersection_lp.test_intersection(region, c, h)

        return intersections
