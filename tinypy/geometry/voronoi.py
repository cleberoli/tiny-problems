from datetime import datetime
from typing import Dict

from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.geometry.cone import Cone
from tinypy.graph.delaunay import DelaunayTriangulation
from tinypy.utils.file import create_folder, file_exists, get_full_path


class VoronoiDiagram:
    """Represents a Voronoi diagram with the corresponding Delaunay triangulation.

    Attributes:
        type: The instance type.
        name: The instance name.
        cone_file: The path where the cones should be stored.
        delaunay: The corresponding Delaunay triangulation.
        hyperplanes: The corresponding hyperplanes for each Delaunay edge.
        cones: The cones for each solution.
    """

    type: str
    name: str
    cone_file: str

    delaunay: DelaunayTriangulation
    hyperplanes: Dict[int, 'Hyperplane']
    cones: Dict[int, 'Cone']

    def __init__(self, delaunay: DelaunayTriangulation, hyperplanes: Dict[int, 'Hyperplane'], instance_type: str, instance_name: str):
        """Initializes the Voronoi diagram.

        Args:
            delaunay: The corresponding Delaunay triangulation.
            hyperplanes: The corresponding hyperplanes for each Delaunay edge.
            instance_type: The instance type.
            instance_name: The instance name.
        """
        self.type = instance_type
        self.name = instance_name
        self.cone_file = get_full_path('files', 'cones', instance_type, f'{instance_name}.tpcf')
        create_folder(get_full_path('files', 'cones', instance_type))

        self.delaunay = delaunay
        self.hyperplanes = hyperplanes

    def build(self, solutions: Dict[int, 'Point']):
        """Builds the Voronoi diagram based on the given solutions.

        Args:
            solutions: The Voronoi vertices.
        """
        if file_exists(self.cone_file):
            self.cones = self.__read_cone_file(solutions)
        else:
            self.cones = self.__generate_cones(solutions)
            self.__write_cone_file(solutions[1].dim, len(solutions))

    def __generate_cones(self, solutions: Dict[int, 'Point']) -> Dict[int, 'Cone']:
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
            hyperplanes = [self.delaunay.get_edge(s, e, 'h') for e in edges]

            for h in hyperplanes:
                hyperplane = self.hyperplanes[h]

                if hyperplane.in_halfspace(solution):
                    cone.add_hyperplane(h)
                else:
                    cone.add_hyperplane(-h)

            cones[s] = cone

        return cones

    def __read_cone_file(self, solutions: Dict[int, 'Point']) -> Dict[int, 'Cone']:
        """Reads the cone file.

        Args:
            solutions: The Voronoi vertices.

        Returns:
            The cones for each solution.
        """
        cones = dict()

        with open(self.cone_file, 'r') as file:
            file.readline()     # name
            file.readline()     # type
            file.readline()     # generated
            file.readline()     # dimension
            c_size = int(file.readline().split()[1])
            h_size = int(file.readline().split()[1])
            file.readline()

            file.readline()     # HYPERPLANES SECTION
            for _ in range(h_size):
                file.readline()
            file.readline()

            file.readline()     # CONES SECTION

            if c_size <= 1:
                return cones

            for _ in range(c_size):
                line = file.readline().split(':')
                key = int(line[0].strip())
                hyperplanes_list = list(map(int, line[1].split()))
                cone = Cone(key, solutions[key], hyperplanes_list)
                cones[key] = cone

        return cones

    def __write_cone_file(self, dim: int, size: int):
        """Writes the cone file.

        Args:
            dim: The dimension of the polytope.
            size: The size of the polytope.
        """
        now = datetime.now()

        with open(self.cone_file, 'w+') as file:
            file.write(f'NAME: {self.name}\n')
            file.write(f'TYPE: {self.type.upper()}\n')
            file.write(f'GENERATED: {now.strftime("%d/%m/%Y %H:%M:%S")}\n')
            file.write(f'DIMENSION: {dim}\n')
            file.write(f'SOLUTIONS: {size}\n')
            file.write(f'HYPERPLANES: {len(self.hyperplanes)}\n\n')

            file.write(f'HYPERPLANES SECTION\n')
            for (index, hyperplane) in self.hyperplanes.items():
                file.write(f'{index}: {" ".join(map(str, hyperplane.normal))} {hyperplane.d}\n')
            file.write('\n')

            file.write(f'CONES SECTION\n')
            for (index, cone) in self.cones.items():
                file.write(f'{index}: {" ".join(map(str, cone.hyperplanes))}\n')
            file.write('\n')
