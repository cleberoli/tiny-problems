from hashlib import blake2b
from typing import Dict

from gurobipy.gurobipy import Model, GRB, quicksum

from tinypy.geometry.cone import Cone
from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.region import Region
from tinypy.utils.file import create_folder, delete_directory, file_exists, get_full_path


class IntersectionProblem:

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
        self.dim = dim
        self.name = name
        self.cones = cones
        self.hyperplanes = hyperplanes
        self.log = log
        self.lp_directory = get_full_path('files', 'lps', 'intersection', name)
        create_folder(self.lp_directory)

    def clear_files(self):
        delete_directory(self.lp_directory)

    def test_intersection(self, region: 'Region', cone: int, hyperplane: int) -> bool:
        path = f'{self.lp_directory}/test_{repr(region)}_{cone}_{hyperplane}'

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
