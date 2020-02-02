from typing import List

from gurobipy.gurobipy import Model, GRB, quicksum

from tinypy.geometry import Point


class AdjacencyProblem:

    STATUS_OPTIMAL = 2
    STATUS_INFEASIBLE = 3
    STATUS_UNBOUNDED = 5

    def __init__(self, dim: int, name: str, vertices: List[Point]):
        self.dim = dim
        self.name = name
        self.p = vertices

    def test_edge_primal(self, i: int, j: int) -> bool:
        model = Model()
        model.setParam('LogToConsole', 0)
        model.setParam('DualReductions', 0)
        self.__primal_model(model, i, j)

        model.update()
        model.optimize()
        # model.write(f'{self.name}_edge_primal_{i}_{j}.lp')
        return True if model.status == AdjacencyProblem.STATUS_INFEASIBLE else False

    def test_edge_dual(self, i: int, j: int) -> bool:
        model = Model()
        model.setParam('LogToConsole', 0)
        model.setParam('DualReductions', 0)
        self.__dual_model(model, i, j)

        model.update()
        model.optimize()
        # model.write(f'{self.name}_edge_dual_{i}_{j}.lp')
        return True if model.status == AdjacencyProblem.STATUS_UNBOUNDED else False

    def __primal_model(self, m: Model, i: int, j: int):
        lbd = dict()

        for d in range(len(self.p)):
            lbd[d] = m.addVar(name=f'lbd_{d}', vtype=GRB.CONTINUOUS, lb=0, ub=1)

        m.setObjective(0, GRB.MINIMIZE)

        for d in range(self.dim):
            m.addConstr(quicksum(lbd[k] * self.p[k][d] for k in range(len(self.p)) if k != i and k != j) == lbd[i] * self.p[i][d] +
                        lbd[j] * self.p[j][d])

        for d in range(len(self.p)):
            m.addConstr(lbd[d] >= 0)

        m.addConstr(quicksum(lbd[k] for k in range(len(self.p)) if k != i and k != j) == 1)
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

        for k in range(len(self.p)):
            if k != i and k != j:
                m.addConstr(quicksum(self.p[k][d] * q[d] for d in range(self.dim)) <= y)
