from ast import literal_eval as make_tuple
from datetime import datetime
from typing import Dict, List

from tinypy.geometry.bisection import Bisection
from tinypy.geometry.cone import Cone
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.region import Region
from tinypy.lp.intersection import IntersectionProblem
from tinypy.polytopes.base_polytope import Polytope
from tinypy.utils.file import create_directory, delete_directory, delete_directory_files, file_exists, get_full_path


class Intersections:
    """Computes the intersections of hyperplanes and solution cones.

    The files are stored in order to speed up the process in case of any kind
    of interruptions.


    Attributes:
        type: The instance type.
        name: The instance name.
        intersection_file: The path where the intersections should be stored.
        polytope: The polytope.
        hyperplanes: The polytope's set of hyperplanes.
        cones: The polytope's solution cones.
        intersection_lp: Instance of the intersection linear program model.
    """

    type: str
    name: str
    intersection_file: str

    polytope: Polytope
    hyperplanes: Dict[int, 'Hyperplane']
    cones: Dict[int, 'Cone']
    intersection_lp: IntersectionProblem

    def __init__(self, polytope: Polytope):
        """Initializes the intersections.

        Args:
            polytope: The polytope.
        """
        self.type = polytope.instance.type
        self.name = polytope.instance.name

        self.polytope = polytope
        self.hyperplanes = polytope.H
        self.hyperplanes.update(polytope.extended_H)
        self.cones = polytope.voronoi.cones
        self.intersection_lp = IntersectionProblem(polytope.dimension, polytope.instance.name, self.cones, self.hyperplanes,
                                                   polytope.instance.get_triangles(), True)

    def clear_files(self):
        """Deletes the files used to stored previous results.
        """
        delete_directory(get_full_path('files', 'intersections', self.type, self.name))

    def clear_lp_files(self):
        """Deletes the files used by the linear program.
        """
        self.intersection_lp.clear_files()

    def get_positions(self, region: 'Region', cones: List[int]) -> Dict[int, 'Bisection']:
        """Returns the the positions of cones with respect to hyperplanes.

        Computes the positions of cones relative to all possible hyperplanes
        that do not delimit the given region.

        Args:
            region: The region to be considered.
            cones: The cones to be considered.

        Returns:
            The bisections of the given cones for each hyperplane.
        """
        self.intersection_file = get_full_path('files', 'intersections', self.type, self.name, f'{repr(region)}.tptf')
        create_directory(get_full_path('files', 'intersections', self.type, self.name))

        hyperplanes = [h for h in self.hyperplanes.keys() if h not in region.hyperplanes and -h not in region.hyperplanes]

        if file_exists(self.intersection_file):
            positions = self.__read_intersection_file(len(hyperplanes))
        else:
            positions = self.__compute_positions(region, cones, hyperplanes)
            self.__write_intersection_file(region, cones, hyperplanes, positions)
            self.intersection_lp.clear_files(region)

        return positions

    def __compute_positions(self, region: 'Region', reference_cones: List[int], reference_hyperplanes: List[int]) -> Dict[int, 'Bisection']:
        """Returns the the positions of cones with respect to hyperplanes.

        Args:
            region: The region to be considered.
            reference_cones: The cones to be considered.
            reference_hyperplanes: The hyperplanes whose bisections we want.

        Returns:
            The bisections of the given cones for each hyperplane.
        """
        intersections = self.__compute_intersections(region, reference_cones, reference_hyperplanes)
        positions = dict()

        for h in reference_hyperplanes:
            positions[h] = Bisection()
            cones = [c for (c, value) in intersections[h].items() if value is False]

            for c in cones:
                if self.hyperplanes[h].in_halfspace(self.cones[c].solution):
                    positions[h].add_right(c)
                else:
                    positions[h].add_left(c)

        return positions

    def __compute_intersections(self, region: 'Region', reference_cones: List[int], reference_hyperplanes: List[int]) -> Dict[int, Dict[int, bool]]:
        """Computes the intersections of each hyperplane with each cone.

        Args:
            region: The region to be considered.
            reference_cones: The cones to be considered.
            reference_hyperplanes: The hyperplanes whose bisections we want.

        Returns:
            The intersections of the hyperplanes with cones.
        """
        intersections = dict()

        for h in reference_hyperplanes:
            intersections[h] = dict()

            for c in reference_cones:
                intersections[h][c] = self.intersection_lp.test_intersection(region, c, h)

        return intersections

    def __read_intersection_file(self, p_size: int) -> Dict[int, 'Bisection']:
        """Reads the intersection file.

        Args:
            p_size: The number of hyperplanes.

        Returns:
            The bisections of the given cones for each hyperplane.
        """
        positions = dict()

        with open(self.intersection_file, 'r') as file:
            file.readline()     # name
            file.readline()     # type
            file.readline()     # generated
            file.readline()     # region
            file.readline()     # hash
            file.readline()     # hyperplanes
            file.readline()     # solutions
            file.readline()

            file.readline()     # POSITION SECTION
            for _ in range(p_size):
                line = file.readline().split(':')
                key = int(line[0].strip())
                bisection_tuple = make_tuple(line[1].strip())
                bisection = Bisection(bisection_tuple[0], bisection_tuple[1])
                positions[key] = bisection

        return positions

    def __write_intersection_file(self, region: 'Region', reference_cones: List[int],
                                  reference_hyperplanes: List[int], positions: Dict[int, 'Bisection']):
        """Writes the intersection file.

        Args:
            region: The region to be considered.
            reference_cones: The cones to be considered.
            reference_hyperplanes: The hyperplanes whose bisections we want.
            positions: The bisections of the given cones for each hyperplane.
        """
        now = datetime.now()

        with open(self.intersection_file, 'w+') as file:
            file.write(f'NAME: {self.name}\n')
            file.write(f'TYPE: {self.type.upper()}\n')
            file.write(f'GENERATED: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            file.write(f'REGION: {str(region)}\n')
            file.write(f'HASH: {repr(region)}\n')
            file.write(f'HYPERPLANES: {reference_hyperplanes}\n')
            file.write(f'SOLUTIONS: {reference_cones}\n\n')

            file.write(f'POSITION SECTION\n')
            for (index, bisection) in positions.items():
                file.write(f'{index}: {repr(bisection)}\n')
