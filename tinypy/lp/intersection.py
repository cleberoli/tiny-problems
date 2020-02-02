from gurobipy.gurobipy import Model, GRB, quicksum

from tinypy.geometry import Hyperplane, Region


class IntersectionProblem:

    STATUS_OPTIMAL = 2
    STATUS_INFEASIBLE = 3
    STATUS_UNBOUNDED = 5

    def __init__(self, region: 'Region', hyperplane: 'Hyperplane', dim: int, name: str = None):
        self.region = region
        self.hyperplane = hyperplane
        self.dim = dim
        self.name = name if name is not None else ''
        self.epsilon = 1e-2
        pass

    def test_intersection(self):
        model = Model()
        model.setParam('LogToConsole', 0)
        model.setParam('DualReductions', 0)
        self.__model(model)

        model.update()
        model.optimize()
        model.write(f'model_{self.name}.lp')
        return 1 if model.status == IntersectionProblem.STATUS_OPTIMAL else 0

    def __model(self, m: Model):
        x = dict()
        y = dict()

        for d in range(self.dim):
            x[d] = m.addVar(name=f'x_{d}', vtype=GRB.CONTINUOUS, lb=-1, ub=1)
            y[d] = m.addVar(name=f'y_{d}', vtype=GRB.CONTINUOUS, lb=-1, ub=1)

        m.setObjective(quicksum(x[d] + y[d] for d in range(self.dim)), GRB.MAXIMIZE)

        for r in self.region.hyperplanes:
            m.addConstr(quicksum(x[d] * r[d] for d in range(self.dim)) >= 0)
            m.addConstr(quicksum(y[d] * r[d] for d in range(self.dim)) >= 0)

        m.addConstr(quicksum(x[d] * self.hyperplane[d] for d in range(self.dim)) >= self.epsilon)
        m.addConstr(quicksum(y[d] * self.hyperplane[d] for d in range(self.dim)) <= - self.epsilon)
