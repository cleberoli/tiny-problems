from typing import Dict, List, Tuple

from gurobipy.gurobipy import Model, GRB, quicksum

from tinypy.geometry.cone import Cone
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.geometry.region import Region
from tinypy.utils.file import create_directory, delete_directory, delete_directory_files, file_exists, get_full_path


class IntersectionProblem:
    """Linear program model to determine the intersections.

    Attributes:
        dim: The space dimension.
        name: The instance name.
        log: A boolean representing whether the model files should be saved.
        lp_directory: The path where the lp solutions should be stored.
        cones: Set of cones.
        hyperplanes: Set of hyperplanes.
    """

    STATUS_OPTIMAL = 2
    STATUS_INFEASIBLE = 3
    STATUS_UNBOUNDED = 5
    EPSILON = 1E-4

    dim: int
    name: str
    log: bool
    lp_directory: str

    cones: Dict[int, 'Cone']
    hyperplanes: Dict[int, 'Hyperplane']
    euclidean_hyperplanes: List['Hyperplane']

    def __init__(self, dim: int, name: str, cones: Dict[int, 'Cone'], hyperplanes: Dict[int, 'Hyperplane'], triangles: List[List[int]],
                 log: bool = False):
        """Initializes the intersection model.

        Args:
            dim: The space dimension.
            name: The instance name.
            cones: Set of cones.
            hyperplanes: Set of hyperplanes.
            log: A boolean representing whether the model files should be saved.
        """
        self.dim = dim
        self.name = name
        self.cones = cones
        self.hyperplanes = hyperplanes
        self.euclidean_hyperplanes = self.__get_euclidean_hyperplanes(triangles)
        self.log = log
        self.lp_directory = get_full_path('files', 'lps', 'intersection', name)
        create_directory(self.lp_directory)

    def clear_files(self, region: Region = None):
        """Deletes the files used to stored the models and results for the region.

        If no region is provided then all intersection lp files will be deleted.

        Args:
            region: The region whose files will be deleted.
        """
        if region is None:
            delete_directory(self.lp_directory)
        else:
            delete_directory_files(self.lp_directory, repr(region))

    def test_intersection(self, region: 'Region', cone: int, hyperplane: int) -> Tuple[bool, bool]:
        """Checks whether the hyperplane intercepts the given cone.

        Args:
            region: Restriction of the space.
            cone: The cone index.
            hyperplane: The hyperplane index.

        Returns:
            Whether the hyperplane intercepts the cone.
        """
        path = f'{self.lp_directory}/{repr(region)}_{cone}_{hyperplane}'

        if file_exists(f'{path}.sol'):
            with open(f'{path}.sol', 'r') as file:
                line = file.readline().split()
                left_status, right_status = int(line[0]), int(line[1])
        else:
            right_model = Model()
            left_model = Model()
            right_model.setParam('LogToConsole', 0)
            left_model.setParam('LogToConsole', 0)
            right_model.setParam('DualReductions', 0)
            left_model.setParam('DualReductions', 0)
            self.__model(right_model, region, cone, hyperplane, True)
            self.__model(left_model, region, cone, hyperplane, False)

            right_model.update()
            left_model.update()
            right_model.optimize()
            left_model.optimize()
            right_status = right_model.status
            left_status = left_model.status

            if self.log:
                right_model.write(f'{path}+.lp')
                left_model.write(f'{path}-.lp')

            with open(f'{path}.sol', 'w+') as file:
                file.write(f'{left_status} {right_status}')

        left_status = True if left_status == IntersectionProblem.STATUS_OPTIMAL else False
        right_status = True if right_status == IntersectionProblem.STATUS_OPTIMAL else False

        return left_status, right_status

    def __get_euclidean_hyperplanes(self, triangles: List[List[int]]) -> List[Hyperplane]:
        hyperplanes = []

        if len(triangles) > 0:
            for i in range(self.dim):
                point = Point([0] * i + [1] + [0] * (self.dim - i - 1))
                hyperplanes.append(Hyperplane(point, d=0))

            for triangle in triangles:
                pairs = [[triangle[0], triangle[1]], [triangle[0], triangle[2]], [triangle[1], triangle[2]]]

                for pair in pairs:
                    point = Point([1 if i in pair else 0 for i in range(self.dim)])
                    hyperplanes.append(Hyperplane(point, d=0))

        return hyperplanes

    def __model(self, m: Model, region: 'Region', c: int, h: int, right: bool = True):
        """Defines the model.

        Args:
            m: The gurobi model.
            region: Restriction of the space.
            c: The cone index.
            h: The hyperplane index.
        """
        delimiters = region.hyperplanes + self.cones[c].hyperplanes
        x = dict()

        for d in range(self.dim):
            x[d] = m.addVar(name=f'x_{d}', vtype=GRB.CONTINUOUS)

        m.setObjective(0, GRB.MINIMIZE)

        for euclidean in self.euclidean_hyperplanes:
            m.addConstr(quicksum(x[d] * euclidean[d] for d in range(self.dim)) >= euclidean.d)

        for index in delimiters:
            hyperplane = self.hyperplanes[index] if index > 0 else -self.hyperplanes[-index]
            m.addConstr(quicksum(x[d] * hyperplane[d] for d in range(self.dim)) >= hyperplane.d)

        if right is True:
            m.addConstr(quicksum(x[d] * self.hyperplanes[h][d] for d in range(self.dim)) >= self.hyperplanes[h].d + self.EPSILON)
        else:
            m.addConstr(quicksum(x[d] * self.hyperplanes[h][d] for d in range(self.dim)) <= self.hyperplanes[h].d - self.EPSILON)
