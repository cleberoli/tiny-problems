from ast import literal_eval as make_tuple
from datetime import datetime
from typing import Dict, List

from tinypy.geometry.bisection import Bisection
from tinypy.geometry.cone import Cone
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.region import Region
from tinypy.lp.intersection import IntersectionProblem
from tinypy.polytopes.base_polytope import Polytope
from tinypy.utils.file import create_folder, delete_directory, file_exists, get_full_path


class Intersections:

    type: str
    name: str
    intersection_file: str

    polytope: Polytope
    hyperplanes: Dict[int, 'Hyperplane']
    cones: Dict[int, 'Cone']
    intersection_lp: IntersectionProblem

    def __init__(self, polytope: Polytope):
        self.type = polytope.instance.type
        self.name = polytope.instance.name

        self.polytope = polytope
        self.hyperplanes = polytope.H
        self.hyperplanes.update(polytope.extended_H)
        self.cones = polytope.voronoi.cones
        self.intersection_lp = IntersectionProblem(polytope.dimension, polytope.instance.name, polytope.voronoi.cones, polytope.H, True)

    def clear_files(self):
        delete_directory(get_full_path('files', 'intersections', self.type))

    def clear_lp_files(self):
        self.intersection_lp.clear_files()

    def get_positions(self, region: 'Region', cones: List[int], hyperplanes: List[int]) -> Dict[int, 'Bisection']:
        self.intersection_file = get_full_path('files', 'intersections', self.type, self.name, f'{self.name}-{repr(region)}.tptf')
        create_folder(get_full_path('files', 'intersections', self.type, self.name))

        if file_exists(self.intersection_file):
            positions = self.__read_intersection_file(len(hyperplanes))
        else:
            positions = self.__compute_positions(region, cones, hyperplanes)
            self.__write_intersection_file(region, cones, hyperplanes, positions)

        return positions

    def __compute_positions(self, region: 'Region', reference_cones: List[int], reference_hyperplanes: List[int]) -> Dict[int, 'Bisection']:
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
        intersections = dict()

        for h in reference_hyperplanes:
            intersections[h] = dict()

            for c in reference_cones:
                intersections[h][c] = self.intersection_lp.test_intersection(region, c, h)

        return intersections

    def __read_intersection_file(self, p_size: int) -> Dict[int, 'Bisection']:
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
