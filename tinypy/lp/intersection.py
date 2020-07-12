from typing import Dict

from gurobipy.gurobipy import Model, GRB, quicksum

from tinypy.geometry.cone import Cone
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.region import Region
from tinypy.utils.file import create_directory, delete_directory, file_exists, get_full_path


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
    EPSILON = 1E-2

    dim: int
    name: str
    log: bool
    lp_directory: str

    cones: Dict[int, 'Cone']
    hyperplanes: Dict[int, 'Hyperplane']

    def __init__(self, dim: int, name: str, cones: Dict[int, 'Cone'], hyperplanes: Dict[int, 'Hyperplane'], log: bool = False):
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
        self.log = log
        self.lp_directory = get_full_path('files', 'lps', 'intersection', name)
        create_directory(self.lp_directory)

    def clear_files(self):
        """Deletes the files used to stored the models and results.
        """
        delete_directory(self.lp_directory)

    def test_intersection(self, region: 'Region', cone: int, hyperplane: int) -> bool:
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
                status = int(file.readline())
        else:
            model = Model()
            model.setParam('LogToConsole', 0)
            model.setParam('DualReductions', 0)
            self.__model(model, region, cone, hyperplane)

            model.update()
            model.optimize()
            status = model.status

            if self.log:
                model.write(f'{path}.lp')

            with open(f'{path}.sol', 'w+') as file:
                file.write(f'{status}')

        return True if status == IntersectionProblem.STATUS_OPTIMAL else False

    def __model(self, m: Model, region: 'Region', c: int, h: int):
        """Defines the model.

        Args:
            m: The gurobi model.
            region: Restriction of the space.
            c: The cone index.
            h: The hyperplane index.
        """
        delimiters = region.hyperplanes + self.cones[c].hyperplanes
        x = dict()
        y = dict()

        for d in range(self.dim):
            x[d] = m.addVar(name=f'x_{d}', vtype=GRB.CONTINUOUS, lb=-1, ub=1)
            y[d] = m.addVar(name=f'y_{d}', vtype=GRB.CONTINUOUS, lb=-1, ub=1)

        m.setObjective(0, GRB.MINIMIZE)

        for index in delimiters:
            hyperplane = self.hyperplanes[index] if index > 0 else -self.hyperplanes[-index]
            m.addConstr(quicksum(x[d] * hyperplane[d] for d in range(self.dim)) >= 0)
            m.addConstr(quicksum(y[d] * hyperplane[d] for d in range(self.dim)) >= 0)

        m.addConstr(quicksum(x[d] * self.hyperplanes[h][d] for d in range(self.dim)) >= self.hyperplanes[h].d + self.EPSILON)
        m.addConstr(quicksum(y[d] * self.hyperplanes[h][d] for d in range(self.dim)) <= self.hyperplanes[h].d - self.EPSILON)
