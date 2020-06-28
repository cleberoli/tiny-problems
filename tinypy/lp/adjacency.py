from typing import Dict

from gurobipy.gurobipy import Model, GRB, quicksum

from tinypy.geometry.point import Point
from tinypy.utils.file import create_folder, delete_directory, file_exists, get_full_path


class AdjacencyProblem:

    STATUS_OPTIMAL = 2
    STATUS_INFEASIBLE = 3
    STATUS_UNBOUNDED = 5

    dim: int
    name: str
    p: Dict[int, 'Point']
    log: bool
    lp_directory: str

    def __init__(self, dim: int, name: str, vertices: Dict[int, 'Point'], log: bool = True):
        self.dim = dim
        self.name = name
        self.p = vertices
        self.log = log
        self.lp_directory = get_full_path('files', 'lps', 'adjacency', name)
        create_folder(self.lp_directory)

    def clear_files(self):
        delete_directory(self.lp_directory)

    def test_edge_primal(self, i: int, j: int) -> bool:
        path = f'{self.lp_directory}/primal_{i}_{j}'

        if file_exists(f'{path}.sol'):
            with open(f'{path}.sol', 'r') as file:
                status = int(file.readline())
        else:
            model = Model()
            model.setParam('LogToConsole', 0)
            model.setParam('DualReductions', 0)
            self.__primal_model(model, i, j)

            model.update()
            model.optimize()
            status = model.status

            if self.log:
                model.write(f'{path}.lp')

            with open(f'{path}.sol', 'w+') as file:
                file.write(f'{status}')

        return True if status == AdjacencyProblem.STATUS_INFEASIBLE else False

    def test_edge_dual(self, i: int, j: int) -> bool:
        path = f'{self.lp_directory}/dual_{i}_{j}'

        if file_exists(f'{path}.sol'):
            with open(f'{path}.sol', 'r') as file:
                status = int(file.readline())
        else:
            model = Model()
            model.setParam('LogToConsole', 0)
            model.setParam('DualReductions', 0)
            self.__dual_model(model, i, j)

            model.update()
            model.optimize()
            status = model.status

            if self.log:
                model.write(f'{path}.lp')

            with open(f'{path}.sol', 'w+') as file:
                file.write(f'{status}')

        return True if status == AdjacencyProblem.STATUS_UNBOUNDED else False

    def __primal_model(self, m: Model, i: int, j: int):
        lbd = dict()

        for d in range(len(self.p)):
            lbd[d] = m.addVar(name=f'lbd_{d}', vtype=GRB.CONTINUOUS, lb=0, ub=1)

        m.setObjective(0, GRB.MINIMIZE)

        for d in range(self.dim):
            m.addConstr(quicksum(lbd[k] * self.p[k][d] for k in self.p.keys() if k != i and k != j) == lbd[i] * self.p[i][d] +
                        lbd[j] * self.p[j][d])

        for d in range(len(self.p)):
            m.addConstr(lbd[d] >= 0)

        m.addConstr(quicksum(lbd[k] for k in self.p.keys() if k != i and k != j) == 1)
        m.addConstr(lbd[i] + lbd[j] == 1)

    def __dual_model(self, m: Model, i: int, j: int):
        x = m.addVar(name='x', vtype=GRB.CONTINUOUS)
        y = m.addVar(name='y', vtype=GRB.CONTINUOUS)
        q = dict()

        for d in range(self.dim):
            q[d] = m.addVar(name=f'q_{d}', vtype=GRB.CONTINUOUS)

        m.setObjective(x - y, GRB.MAXIMIZE)

        m.addConstr(quicksum(self.p[i][d] * q[d] for d in range(self.dim)) >= x)
        m.addConstr(quicksum(self.p[j][d] * q[d] for d in range(self.dim)) >= x)

        for k in self.p.keys():
            if k != i and k != j:
                m.addConstr(quicksum(self.p[k][d] * q[d] for d in range(self.dim)) <= y)
