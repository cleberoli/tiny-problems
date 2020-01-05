from gurobipy.gurobipy import Model, GRB, quicksum

from tinypy.polytopes import Polytope


class EdgeProblem:

    def __init__(self, polytope: Polytope):
        self.dim = polytope.dim
        self.name = polytope.name
        self.p = polytope.vertices

    def test_edge_primal(self, i: int, j: int):
        model = Model()
        model.setParam('LogToConsole', 0)
        model.setParam('DualReductions', 0)
        self.__primal_model(model, i, j)

        model.update()
        model.optimize()
        model.write(f'{self.name}_edge_primal_{i}_{j}.lp')
        print(i, j, model.status)

    def test_edge_dual(self, i: int, j: int):
        model = Model()
        model.setParam('LogToConsole', 0)
        model.setParam('DualReductions', 0)
        self.__dual_model(model, i, j)

        model.update()
        model.optimize()
        model.write(f'{self.name}_edge_dual_{i}_{j}.lp')
        print(i, j, model.status)

    def __primal_model(self, m: Model, i: int, j: int):
        lbd = dict()

        for d in range(len(self.p)):
            lbd[d] = m.addVar(name=f'lbd_{d}', vtype=GRB.CONTINUOUS, lb=0)

        m.setObjective(0, GRB.MINIMIZE)

        for d in range(self.dim):
            m.addConstr(quicksum(lbd[k] * self.p[k].coords[d] for k in range(len(self.p)) if k != i and k != j) == lbd[i] * self.p[i].coords[d] +
                        lbd[j] * self.p[j].coords[d])

        m.addConstr(quicksum(lbd[k] for k in range(len(self.p)) if k != i and k != j) == 1)
        m.addConstr(lbd[i] + lbd[j] == 1)

    def __dual_model(self, m: Model, i: int, j: int):
        x = m.addVar(name='x', vtype=GRB.CONTINUOUS)
        y = m.addVar(name='y', vtype=GRB.CONTINUOUS)
        q = dict()

        for d in range(self.dim):
            q[d] = m.addVar(name=f'q_{d}', vtype=GRB.CONTINUOUS)

        m.setObjective(x - y, GRB.MAXIMIZE)

        m.addConstr(quicksum(self.p[i].coords[d] * q[d] for d in range(self.dim)) >= x)
        m.addConstr(quicksum(self.p[j].coords[d] * q[d] for d in range(self.dim)) >= x)

        for k in range(len(self.p)):
            if k != i and k != j:
                m.addConstr(quicksum(self.p[k].coords[d] * q[d] for d in range(self.dim)) <= y)
