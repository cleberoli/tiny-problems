import itertools
import json
import os
import random
import time
from abc import ABC, abstractmethod
from bisect import insort
from functools import total_ordering
from hashlib import blake2b
from math import sqrt, ceil, floor, factorial, log2
from sys import maxsize
from typing import Dict, List, Union, Tuple

from gurobipy.gurobipy import Model, GRB, quicksum
from networkx import Graph, DiGraph

EPSILON = 1e-4
INFINITY = maxsize
MAIN_DIRECTORY = os.path.abspath(os.path.join(os.path.dirname(__file__)))

CONES = 'cones'
INSTANCES = 'instances'
POLYTOPES = 'polytopes'
SKELETONS = 'skeletons'
TREES = 'trees'


def create_directory(path: str):
    """Creates the directory if it doesn't exist.

    Args:
        path: The directory path.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def get_full_path(*path):
    """Returns the given path joined by the MAIN_DIRECTORY.

    Args:
        *path: The path.
    """
    return os.path.join(MAIN_DIRECTORY, *path)


def file_exists(path: str):
    """Checks whether a file exists.

    Args:
        path: The path.
    """
    return os.path.exists(path)


def get_combinations(x: List, r: int) -> List:
    """Returns all possible combinations with r elements.

    Args:
        x: The original set.
        r: Number of elements in a combinations.
    """
    return list(itertools.combinations(x, r))


def get_permutations(x: List, repeat: int = None) -> List:
    """Returns all permutations.

    Args:
        x: The original set.
        repeat: Number of possible repetitions.
    """
    x.sort()

    if repeat is None:
        return list(itertools.permutations(x))
    else:
        return list(itertools.product(x, repeat=repeat))


@total_ordering
class Point:
    """Represents a geometrical point in the euclidean space.

    Attributes:
        coords: The point's coordinates.
        dim: The space dimension.
    """

    coords: tuple
    dim: int

    def __init__(self, *args):
        """Initializes the point.

        Args:
            *args: The arguments to initialize the point. It can be a tuple,
                a list, or individual elements (integers or real numbers).
        """
        if type(args[0]) is list or type(args[0]) is tuple:
            args = tuple(args[0])

        if all(isinstance(x, int) for x in args) or all(isinstance(x, float) for x in args):
            self.coords = args
            self.dim = len(self.coords)
        else:
            raise ValueError('Invalid parameter.')

    @classmethod
    def origin(cls, dim: int) -> 'Point':
        """A point of all zeros in the space of given dimension.

        Args:
            dim: The space dimension.

        Returns:
            A point of all zeros in the given dimension.
        """
        return cls([0] * dim)

    @classmethod
    def random(cls, dim: int, a: int = 0, b: int = 1, decimals: int = 0, norm: int = None) -> 'Point':
        """A random point following the given parameters.

        Args:
            dim: The space dimension.
            a: The lower possible value.
            b: The upper possible value.
            decimals: Number of decimal values.
            norm: The desired norm, if any.

        Returns:
            A random point in the given dimension.
        """
        args = [random.randint(a, b) for _ in range(dim)] if decimals == 0 else [round(random.uniform(a, b), decimals) for _ in range(dim)]
        point = cls(args)

        if norm is not None:
            while point.norm <= 0:
                args = [random.randint(a, b) for _ in range(dim)] if decimals == 0 else [round(random.uniform(a, b), decimals) for _ in range(dim)]
                point = cls(args)

            unitary_point = point * (norm / point.norm)
            point = cls([round(i, max(decimals, 4)) for i in unitary_point.coords])

        return point

    @classmethod
    def random_triangle(cls, dim: int, triangles: List[List[int]], a: int = 0, b: int = 1, decimals: int = 4, norm: int = 1) -> 'Point':
        """A random point that respects the triangle inequality constraints.

        Args:
            dim: The space dimension.
            triangles: A list containing the triangles with each triangle being
                represented by a list of three vertices.
            a: The lower possible value.
            b: The upper possible value.
            decimals: Number of decimal values.
            norm: The desired norm, if any.

        Returns:
            A random point in the given dimension that respects the triangle
            inequality.
        """
        point = cls.random(dim, a, b, decimals)

        while not point.respects_triangle_inequality(triangles):
            point = cls.random(dim, a, b, decimals)

        unitary_point = point * (norm / point.norm)
        unitary_point = cls([round(i, max(decimals, 4)) for i in unitary_point.coords])

        return unitary_point

    @property
    def homogeneous_coords(self) -> tuple:
        """Returns the homogeneous coordinates for the point.
        """
        return self.coords + (1, )

    @property
    def norm(self) -> float:
        """Returns the norm for the point.
        """
        return self.distance(self.origin(self.dim))

    def distance(self, other: 'Point') -> float:
        """Returns the distance between two points.

        Args:
            other: The other point.

        Returns:
            The distance between the current point and the given one.
        """
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return sqrt(sum(list(map(lambda x: x * x, (self - other).coords))))

    def respects_triangle_inequality(self, triangles: List[List[int]]):
        """Returns whether the current point respects the triangle inequality.

        Args:
            triangles: A list containing the triangles with each triangle being
                represented by a list of three vertices.
        """
        for triangle in triangles:
            if self.coords[triangle[0]] + self.coords[triangle[1]] <= self.coords[triangle[2]]:
                return False
            if self.coords[triangle[0]] + self.coords[triangle[2]] <= self.coords[triangle[1]]:
                return False
            if self.coords[triangle[1]] + self.coords[triangle[2]] <= self.coords[triangle[0]]:
                return False

        return True

    def __add__(self, other: 'Point') -> 'Point':
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(list(map(lambda x, y: x + y, self.coords, other.coords)))

    def __sub__(self, other: 'Point') -> 'Point':
        if self.dim != other.dim:
            raise ValueError('The dimensions are not compatible.')

        return Point(list(map(lambda x, y: x - y, self.coords, other.coords)))

    def __rmul__(self, other: Union['Point', int, float]) -> Union['Point', int, float]:
        # dot product
        if isinstance(other, Point):
            if self.dim != other.dim:
                raise ValueError('The dimensions are not compatible.')

            return sum(list(map(lambda x, y: x * y, self.coords, other.coords)))

        # multiplication by a scalar
        elif isinstance(other, int) or isinstance(other, float):
            return Point(list(map(lambda x: x * other, self.coords)))

        else:
            raise ValueError('Invalid operation.')

    __mul__ = __rmul__

    def __neg__(self):
        return -1 * self

    def __getitem__(self, item: int):
        return self.coords[item]

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other: 'Point'):
        return self.coords < other.coords

    def __gt__(self, other: 'Point'):
        return not (self <= other)

    def __eq__(self, other: 'Point'):
        return self.coords == other.coords

    def __ne__(self, other: 'Point'):
        return not (self == other)

    def __str__(self):
        return str(self.coords)

    def __repr__(self):
        return str(self.coords)


@total_ordering
class Hyperplane:
    """Represents a hyperplane.

    Attributes:
        normal: normal vector.
        d: offset in the form n.x = d
    """

    normal: 'Point'
    d: int

    def __init__(self, normal: 'Point', **kwargs):
        """Initializes the hyperplane.

        Args:
            normal: A point representing the normal vector.
            **kwargs: Contains either a point on the hyperplane (p)
                or the offset (d).
        """
        if 'd' not in kwargs and 'p' not in kwargs:
            raise ValueError('Invalid parameters.')

        if 'd' in kwargs and not (isinstance(kwargs['d'], int) or isinstance(kwargs['d'], float)):
            raise ValueError('Invalid parameters.')

        if 'p' in kwargs and not isinstance(kwargs['p'], Point):
            raise ValueError('Invalid parameters.')

        self.normal = normal
        self.d = kwargs.get('d') if 'd' in kwargs else - normal * kwargs.get('p')

    def position(self, p: 'Point'):
        """Returns the dor product of p with normal vector.

        Args:
            p: Point to be compared.
        """
        return self.normal * p

    def in_halfspace(self, p: 'Point'):
        """Returns whether the position of p in relation to the offset.

        Args:
            p: Point to be compared.
        """
        return self.position(p) >= self.d

    def __neg__(self):
        return Hyperplane(-self.normal, d=-self.d)

    def __getitem__(self, item: int):
        return self.normal[item]

    def __hash__(self):
        return hash(repr(self))

    def __lt__(self, other: 'Hyperplane'):
        return self.normal < other.normal or self.normal <= other.normal and self.d < other.d

    def __gt__(self, other: 'Hyperplane'):
        return not (self <= other)

    def __eq__(self, other: 'Hyperplane'):
        return self.normal == other.normal and self.d == other.d

    def __ne__(self, other: 'Hyperplane'):
        return not (self == other)

    def __str__(self):
        terms = self.__get_terms()
        equation = ' + '.join(terms).replace('+ -', '- ')
        return f'{equation} = {self.d}'

    def __repr__(self):
        return str(self.normal.coords + (self.d, ))

    def __get_terms(self) -> List[str]:
        """Returns a list of the terms.
        """
        terms = []

        for d in range(self.normal.dim):
            coefficient = self.normal[d]

            if coefficient != 0:
                if coefficient == 1:
                    terms.append(f'x{d + 1}')
                elif coefficient == -1:
                    terms.append(f'-x{d + 1}')
                else:
                    terms.append(f'{coefficient}x{d + 1}')

        return terms


class DBModel(ABC):

    @classmethod
    @abstractmethod
    def from_doc(cls, doc: dict) -> 'DBModel':
        pass

    @classmethod
    @abstractmethod
    def get_collection(cls) -> str:
        pass

    @abstractmethod
    def get_file_name(self) -> str:
        pass

    @abstractmethod
    def load_doc(self, doc: dict):
        pass

    @abstractmethod
    def get_repr(self) -> dict:
        pass

    def get_file_path(self) -> str:
        return get_full_path('files', self.get_collection(), f'{self.get_file_name()}.json')

    def add_doc(self):
        with open(self.get_file_path(), 'w') as file:
            json.dump(self.get_repr(), file)

    def get_doc(self):
        doc = None

        if file_exists(self.get_file_path()):
            with open(self.get_file_path()) as file:
                doc = json.load(file)
                self.load_doc(doc)

        return doc


class Region:
    """Represents a region of the euclidean space delimited by hyperplanes.

    The region consists of all points p, such that the p is in the half-space
    of all delimiting hyperplanes.

    Attributes:
        hyperplanes: Delimiters of the region.

    """

    hyperplanes: List[int]

    def __init__(self, hyperplanes: List[int] = None):
        """Initializes the region.

        The region can be initialized with no hyperplanes (no restrictions).
        The hyperplanes can be added later.

        Args:
            hyperplanes: List of hyperplane indices.
        """
        self.hyperplanes = hyperplanes if hyperplanes is not None else []
        self.hyperplanes = sorted(self.hyperplanes, key=abs)

    def add_hyperplane(self, hyperplane: int):
        """Adds a new hyperplane delimiter, keeping the list sorted.

        Args:
            hyperplane: The hyperplane index.
        """
        self.hyperplanes.append(hyperplane)
        self.hyperplanes = sorted(self.hyperplanes, key=abs)

    def union(self, region: 'Region'):
        """Merges to regions together.

        Args:
            region: The region to be added.

        Returns:
            A new region whose hyperplanes are the union of the current ones and
            the new ones.
        """
        hyperplane_set = set(self.hyperplanes).union(set(region.hyperplanes))
        return Region(sorted(list(hyperplane_set), key=abs))

    def __str__(self):
        return str(self.hyperplanes)

    def __repr__(self):
        h = blake2b(digest_size=20)
        h.update(str.encode(str(self)))
        return h.hexdigest()


class DBCone(DBModel):

    name: str
    type: str
    dimension: int
    size: int
    cones: Dict[int, List[int]]

    def __init__(self, name: str, type: str, dimension: int, size: int, cones: Dict[int, List[int]] = None):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.size = size
        self.cones = dict() if cones is None else cones

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        cone = DBCone(doc['name'], doc['type'], doc['dimension'], doc['size'])
        cone.load_doc(doc)

        return cone

    @classmethod
    def get_collection(cls) -> str:
        return CONES

    def get_file_name(self) -> str:
        return self.name

    def load_doc(self, doc: dict):
        for (key, value) in doc['cones'].items():
            self.cones[int(key)] = value

    def get_repr(self) -> dict:
        cones = dict()

        for (key, value) in self.cones.items():
            cones[f'{key}'] = value

        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'size': self.size,
                'cones': cones}


class Cone(Region):
    """Special case of a region.

    Each cone corresponds to a solution, and the points in this region follows
    the standard definition of a cone.

    Attributes:
        tag: Integer tag identifying the cone.
        solution: Corresponding solution.
    """

    tag: int
    solution: 'Point'

    def __init__(self, tag: int, solution: 'Point', hyperplanes: List[int] = None):
        """Initializes the cone.

        Args:
            tag: Integer tag identifying the cone.
            solution: Corresponding solution.
            hyperplanes: List of hyperplane indices.
        """
        self.tag = tag
        self.solution = solution

        Region.__init__(self, hyperplanes)


class AdjacencyProblem:
    """Linear program model to determine the adjacency in polytopes.

    Attributes:
        dim: The space dimension.
        name: The instance name.
        p: The polytope vertices.
    """

    STATUS_OPTIMAL = 2
    STATUS_INFEASIBLE = 3
    STATUS_UNBOUNDED = 5

    dim: int
    name: str
    log: bool
    lp_directory: str

    p: Dict[int, 'Point']

    def __init__(self, dim: int, name: str, vertices: Dict[int, 'Point']):
        """Initializes the adjacency model.

        Args:
            dim: The space dimension.
            name: The instance name.
            vertices: The polytope vertices.
        """
        self.dim = dim
        self.name = name
        self.p = vertices

    def test_edge_primal(self, i: int, j: int) -> bool:
        """Checks whether the vertices are adjacent using the primal model.

        Args:
            i: First vertex.
            j: Second vertex.

        Returns:
            Whether the vertices are adjacent.
        """
        model = Model()
        model.setParam('LogToConsole', 0)
        model.setParam('DualReductions', 0)
        self.__primal_model(model, i, j)

        model.update()
        model.optimize()
        status = model.status

        return True if status == AdjacencyProblem.STATUS_INFEASIBLE else False

    def test_edge_dual(self, i: int, j: int) -> bool:
        """Checks whether the vertices are adjacent using the dual model.

        Args:
            i: First vertex.
            j: Second vertex.

        Returns:
            Whether the vertices are adjacent.
        """
        model = Model()
        model.setParam('LogToConsole', 0)
        model.setParam('DualReductions', 0)
        self.__dual_model(model, i, j)

        model.update()
        model.optimize()
        status = model.status

        return True if status == AdjacencyProblem.STATUS_UNBOUNDED else False

    def __primal_model(self, m: Model, i: int, j: int):
        """Defines the primal model.

        Args:
            m: The gurobi model.
            i: First vertex.
            j: Second vertex.
        """
        lbd = dict()

        for d in self.p.keys():
            lbd[d] = m.addVar(name=f'lbd_{d}', vtype=GRB.CONTINUOUS, lb=0, ub=1)

        m.setObjective(0, GRB.MINIMIZE)

        for d in range(self.dim):
            m.addConstr(quicksum(lbd[k] * self.p[k][d] for k in self.p.keys() if k != i and k != j) == lbd[i] * self.p[i][d] +
                        lbd[j] * self.p[j][d])

        for d in self.p.keys():
            m.addConstr(lbd[d] >= 0)

        m.addConstr(quicksum(lbd[k] for k in self.p.keys() if k != i and k != j) == 1)
        m.addConstr(lbd[i] + lbd[j] == 1)

    def __dual_model(self, m: Model, i: int, j: int):
        """Defines the dual model.

        Args:
            m: The gurobi model.
            i: First vertex.
            j: Second vertex.
        """
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


class IntersectionProblem:
    """Linear program model to determine the intersections.

    Attributes:
        dim: The space dimension.
        name: The instance name.
        cones: Set of cones.
        hyperplanes: Set of hyperplanes.
    """

    STATUS_OPTIMAL = 2
    STATUS_INFEASIBLE = 3
    STATUS_UNBOUNDED = 5
    EPSILON = 1E-4

    dim: int
    name: str

    cones: Dict[int, 'Cone']
    hyperplanes: Dict[int, 'Hyperplane']
    euclidean_hyperplanes: List['Hyperplane']

    def __init__(self, dim: int, name: str, cones: Dict[int, 'Cone'], hyperplanes: Dict[int, 'Hyperplane'], triangles: List[List[int]]):
        """Initializes the intersection model.

        Args:
            dim: The space dimension.
            name: The instance name.
            cones: Set of cones.
            hyperplanes: Set of hyperplanes.
        """
        self.dim = dim
        self.name = name
        self.cones = cones
        self.hyperplanes = hyperplanes
        self.euclidean_hyperplanes = self.__get_euclidean_hyperplanes(triangles)

    def test_intersection(self, region: 'Region', cone: int, hyperplane: int) -> Tuple[bool, bool]:
        """Checks whether the hyperplane intercepts the given cone.

        Args:
            region: Restriction of the space.
            cone: The cone index.
            hyperplane: The hyperplane index.

        Returns:
            Whether the hyperplane intercepts the cone.
        """
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
            x[d] = m.addVar(name=f'x_{d}', vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)

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


class Bisection:
    """Represents the bisection of the solutions by a given hyperplane.

    Given a hyperplane this object represents which solution regions don't
    intercept the hyperplane, being completely contained in either side of
    the hyperplane.

    Attributes:
        left: List of solution indices to the left of the hyperplane.
        right: List of solution indices to the right of the hyperplane.
    """

    left: List[int]
    right: List[int]

    def __init__(self, left: List[int] = None, right: List[int] = None):
        """Initializes the bisection.

        The bisection can be initialized with empty lists and the solutions
        can be added later.

        Args:
            left: List of solution indices to the left of the hyperplane.
            right: List of solution indices to the right of the hyperplane.
        """
        self.left = sorted(left) if left is not None else []
        self.right = sorted(right) if right is not None else []

    def add_left(self, left: int):
        """Adds a new solution to the left side, keeping the list sorted.

        Args:
            left: The solution index.
        """
        insort(self.left, left)

    def add_right(self, right: int):
        """Adds a new solution to the right side, keeping the list sorted.

        Args:
            right: The solution index.
        """
        insort(self.right, right)

    def __str__(self):
        return str({'left': self.left, 'right': self.right})

    def __repr__(self):
        return str((self.left, self.right))


class Intersections:
    """Computes the intersections of hyperplanes and solution cones.

    The files are stored in order to speed up the process in case of any kind
    of interruptions.


    Attributes:
        type: The instance type.
        name: The instance name.
        polytope: The polytope.
        hyperplanes: The polytope's set of hyperplanes.
        cones: The polytope's solution cones.
        intersection_lp: Instance of the intersection linear program model.
    """

    EPSILON = 1E-4
    LEFT = 0
    RIGHT = 1

    type: str
    name: str
    intersection_file: str

    hyperplanes: Dict[int, 'Hyperplane']
    cones: Dict[int, 'Cone']
    intersection_lp: IntersectionProblem
    positions: Dict[str, Dict[int, Bisection]]

    def __init__(self, polytope):
        """Initializes the intersections.

        Args:
            polytope: The polytope.
        """
        self.type = polytope.instance.type
        self.name = polytope.instance.name
        self.positions = dict()

        self.polytope = polytope
        self.hyperplanes = polytope.hyperplanes
        self.cones = polytope.voronoi.cones
        self.intersection_lp = IntersectionProblem(polytope.dimension, polytope.instance.name, self.cones, self.hyperplanes,
                                                   polytope.instance.get_triangles())

    def get_positions(self, region: 'Region', cones: List[int], hyperplanes: List[int] = None) -> Dict[int, 'Bisection']:
        """Returns the the positions of cones with respect to hyperplanes.

        Computes the positions of cones relative to all possible hyperplanes
        that do not delimit the given region.

        Args:
            region: The region to be considered.
            cones: The cones to be considered.
            hyperplanes: List of hyperplanes to be considered.
        Returns:
            The bisections of the given cones for each hyperplane.
        """
        if hyperplanes is None:
            hyperplanes = [h for h in self.hyperplanes.keys() if h not in region.hyperplanes and -h not in region.hyperplanes]

        if hash(region) in self.positions:
            hyperplanes = [h for h in hyperplanes if h not in self.positions[repr(region)].keys()]

            if len(hyperplanes) > 0:
                self.__compute_positions(region, cones, hyperplanes)
        else:
            self.positions[repr(region)] = dict()
            self.__compute_positions(region, cones, hyperplanes)

        return self.positions[repr(region)]

    def __compute_positions(self, region: 'Region', reference_cones: List[int], reference_hyperplanes: List[int]):
        """Returns the the positions of cones with respect to hyperplanes.

        Args:
            region: The region to be considered.
            reference_cones: The cones to be considered.
            reference_hyperplanes: The hyperplanes whose bisections we want.

        Returns:
            The bisections of the given cones for each hyperplane.
        """
        intersections = self.__compute_intersections(region, reference_cones, reference_hyperplanes)

        for h in reference_hyperplanes:
            self.positions[repr(region)][h] = Bisection()
            cones = [c for (c, value) in intersections[h].items() if value[0] is False or value[1] is False]

            for c in cones:
                if intersections[h][c][self.RIGHT] is True:
                    self.positions[repr(region)][h].add_right(c)
                else:
                    self.positions[repr(region)][h].add_left(c)

    def __compute_intersections(self, region: 'Region', cones: List[int], hyperplanes: List[int]) -> Dict[int, Dict[int, Tuple[bool, bool]]]:
        """Computes the intersections of each hyperplane with each cone.

        Args:
            region: The region to be considered.
            cones: The cones to be considered.
            hyperplanes: The hyperplanes whose bisections we want.

        Returns:
            The intersections of the hyperplanes with cones.
        """
        intersections = dict()

        for h in hyperplanes:
            intersections[h] = dict()

            for c in cones:
                intersections[h][c] = self.intersection_lp.test_intersection(region, c, h)

        return intersections


class Kn:
    """Represents the complete graph with n nodes.

    Attributes:
        n: The number of nodes.
        nodes: List of nodes [1..n].
        edges: List of edges.
    """

    n: int
    nodes: List[int]
    edges: List[str]

    def __init__(self, n: int):
        """Initializes the Kn graph.

        Args:
            n: The number of nodes.
        """
        if n <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        self.n = n
        self.nodes = list(range(1, n + 1))
        self.edges = []

        for i in range(0, self.n):
            for j in range(i + 1, self.n):
                self.edges.append(f'{self.nodes[i]}-{self.nodes[j]}')

    def get_hamilton_cycles(self) -> Dict[int, 'Point']:
        """Returns all Hamiltonian cycles.

        Returns:
            All Hamiltonian cycles as points.
        """
        permutations = get_permutations(self.nodes[1:])
        permutations = [(self.nodes[0], ) + p + (self.nodes[0], ) for p in permutations]
        cycles = set()

        for permutation in permutations:
            cycles.add(self.__get_point_from_permutation(permutation))

        cycles = list(cycles)
        cycles.sort()

        return dict((key, cycles[key]) for key in range(len(cycles)))

    def get_cuts(self) -> Dict[int, 'Point']:
        """Returns all possible cuts.

        Returns:
            All cuts as points that represent that edges to be removed.
        """
        cuts = {Point.origin(len(self.edges))}

        for i in range(1, floor(self.n / 2) + 1):
            combinations = get_combinations(self.nodes, i)

            for combination in combinations:
                combination = list(combination)
                complement = [node for node in self.nodes if node not in combination]
                cuts.add(self.__get_point_from_partition(combination, complement))

        cuts = list(cuts)
        cuts.sort()

        return dict((key, cuts[key]) for key in range(len(cuts)))

    def get_triangles(self) -> List[List[int]]:
        """Returns all triangles.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        triangles = []

        for i in range(self.n):
            for j in range(i + 1, self.n):
                for k in range(j + 1, self.n):
                    triangle = [f'{self.nodes[i]}-{self.nodes[j]}',
                                f'{self.nodes[i]}-{self.nodes[k]}',
                                f'{self.nodes[j]}-{self.nodes[k]}']
                    point = self.__get_point_from_edges(triangle)
                    indices = [i for i, e in enumerate(point.coords) if e == 1]
                    triangles.append(indices)

        return triangles

    def __get_point_from_permutation(self, permutation: tuple) -> 'Point':
        """Returns a point from a permutation of the nodes.

        Args:
            permutation: Permutation of the nodes.
        """
        edges = []

        for i in range(self.n):
            if permutation[i] < permutation[i + 1]:
                edges.append(f'{permutation[i]}-{permutation[i + 1]}')
            else:
                edges.append(f'{permutation[i + 1]}-{permutation[i]}')

        return self.__get_point_from_edges(edges)

    def __get_point_from_partition(self, a: List[int], b: List[int]) -> 'Point':
        """Returns a point from a partition of the nodes.

        Args:
            a: One set of the partition.
            b: Other set of the partition.
        """
        edges = []

        for i in range(len(a)):
            for j in range(len(b)):
                if a[i] < b[j]:
                    edges.append(f'{a[i]}-{b[j]}')
                else:
                    edges.append(f'{b[j]}-{a[i]}')

        return self.__get_point_from_edges(edges)

    def __get_point_from_edges(self, edges: List[str]) -> 'Point':
        """Returns a point from a list of edges.

        Args:
            edges: List of edges.
        """
        coords = [1 if e in edges else 0 for e in self.edges]
        return Point(coords)


class DBSkeleton(DBModel):

    name: str
    type: str
    dimension: int
    size: int
    nodes: List[int]
    hyperplanes: Dict[int, Hyperplane]
    n_skeleton_hyperplanes: int
    n_complement_hyperplanes: int
    skeleton_edges: List[Tuple[int, int, int]]
    complement_edges: List[Tuple[int, int, int]]

    def __init__(self, name: str, type: str, dimension: int, size: int, nodes: List[int] = None,
                 hyperplanes: Dict[int, Hyperplane] = None, n_skeleton_hyperplanes: int = None, n_complement_hyperplanes: int = None,
                 skeleton_edges: List[Tuple[int]] = None, complement_edges: List[Tuple[int]] = None):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.size = size
        self.nodes = list(range(1, size + 1)) if nodes is None else nodes
        self.hyperplanes = dict() if hyperplanes is None else hyperplanes
        self.n_skeleton_hyperplanes = 0 if n_skeleton_hyperplanes is None else n_skeleton_hyperplanes
        self.n_complement_hyperplanes = 0 if n_complement_hyperplanes is None else n_complement_hyperplanes
        self.skeleton_edges = [] if skeleton_edges is None else skeleton_edges
        self.complement_edges = [] if complement_edges is None else complement_edges

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        skeleton = DBSkeleton(doc['name'], doc['type'], doc['dimension'], doc['size'])
        skeleton.load_doc(doc)

        return skeleton

    @classmethod
    def get_collection(cls) -> str:
        return SKELETONS

    def get_file_name(self) -> str:
        return self.name

    def load_doc(self, doc: dict):
        self.n_skeleton_hyperplanes = doc['n_skeleton_hyperplanes']
        self.n_complement_hyperplanes = doc['n_complement_hyperplanes']

        for (key, value) in doc['hyperplanes'].items():
            hyperplane = Hyperplane(Point(value[:-1]), d=value[-1])
            self.hyperplanes[int(key)] = hyperplane

        for s_edge in doc['skeleton_edges']:
            self.skeleton_edges.append((s_edge[0], s_edge[1], s_edge[2]))

        for c_edge in doc['complement_edges']:
            self.complement_edges.append((c_edge[0], c_edge[1], c_edge[2]))

    def get_repr(self) -> dict:
        hyperplanes = dict()
        skeleton_edges = []
        complement_edges = []

        for (key, value) in self.hyperplanes.items():
            h = list(value.normal.coords) + [value.d]
            hyperplanes[f'{key}'] = h

        for s_edge in self.skeleton_edges:
            skeleton_edges.append(list(s_edge))

        for c_edge in self.complement_edges:
            complement_edges.append(list(c_edge))

        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'size': self.size,
                'n_skeleton_hyperplanes': self.n_skeleton_hyperplanes,
                'n_complement_hyperplanes': self.n_complement_hyperplanes,
                'nodes': self.nodes,
                'hyperplanes': hyperplanes,
                'skeleton_edges': skeleton_edges,
                'complement_edges': complement_edges}


class Skeleton:
    """Represents the skeleton of a polytope.

    Attributes:
        graph: The skeleton graph.
    """

    graph: Graph

    def __init__(self):
        """Initializes the skeleton graph.
        """
        self.graph = Graph()

    @property
    def edges(self) -> List[Tuple]:
        """Returns the edges of the skeleton.
        """
        edges = list(self.graph.edges)
        edges.sort()
        return edges

    @property
    def nodes(self) -> List[int]:
        """Returns the nodes of the skeleton.
        """
        return list(self.graph.nodes)

    @property
    def degree(self) -> float:
        """Returns the skeleton average degree.
        """
        degrees = [self.graph.degree(i) for i in self.graph.nodes]
        return round(sum(degrees) / max(len(degrees), 1), 3)

    def add_edge(self, i: int, j: int, h: int = None):
        """Adds a new edge to the skeleton graph.

        Args:
            i: First node.
            j: Second node.
            h: Corresponding hyperplane.
        """
        if h is None:
            self.graph.add_edge(i, j)
        else:
            self.graph.add_edge(i, j, h=h)

    def get_edge(self, i: int, j: int, key: str = 'h') -> int:
        """Returns the edge if it exists.

        Args:
            i: First node.
            j: Second node.
            key: Key to data.
        """
        try:
            return self.graph[i][j][key]
        except KeyError as e:
            raise KeyError(f'Invalid key: {e}')

    def get_edges(self, i: int) -> Dict[int, Dict]:
        """Returns the edges adjacent to the given node.

        Args:
            i: The node.
        """
        return self.graph.adj[i]

    def has_edge(self, i: int, j: int) -> bool:
        """Returns whether the skeleton has the given edge.

        Args:
            i: First node.
            j: Second node.
        """
        return self.graph.has_edge(i, j)


class DBInstance(DBModel):

    name: str
    type: str
    dimension: int
    size: int
    solutions: Dict[int, Point]

    def __init__(self, name: str, type: str, dimension: int, size: int, solutions: Dict[int, Point] = None):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.size = size
        self.solutions = dict() if solutions is None else solutions

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        instance = DBInstance(doc['name'], doc['type'], doc['dimension'], doc['size'])
        instance.load_doc(doc)

        return instance

    @classmethod
    def get_collection(cls) -> str:
        return INSTANCES

    def get_file_name(self) -> str:
        return self.name

    def load_doc(self, doc: dict):
        for (key, value) in doc['solutions'].items():
            point = Point(value)
            self.solutions[int(key)] = point

    def get_repr(self) -> dict:
        solutions = dict()

        for (key, value) in self.solutions.items():
            solutions[f'{key}'] = list(value.coords)

        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'size': self.size,
                'solutions': solutions}


class Instance(ABC):
    """Base class that generates instance for different problems.

    Attributes:
        name: Instance name.
        type: Instance type.
        dimension: Instance dimension.
        size: Number of solutions.
        n: Main instance parameter.
        solutions: List of solution points.
    """

    instance_file: str
    name: str
    type: str
    dimension: int
    size: int
    n: int
    solutions: List[Point]

    def __init__(self, name: str, instance_type: str, dimension: int, size: int, n: int):
        """Initializes the instance.

        Args:
            name: Instance name.
            instance_type: Instance type.
            dimension: Instance dimension.
            size: Number of solutions.
            n: Main instance parameter.
        """
        self.name = name
        self.type = instance_type
        self.dimension = dimension
        self.size = size
        self.n = n

        db_instance = DBInstance(self.name, self.type, self.dimension, self.size)
        doc = db_instance.get_doc()

        if doc is not None:
            self.solutions = list(db_instance.solutions.values())
        else:
            self.solutions = self.generate_solutions()
            db_instance.solutions = self.get_solution_dict()
            db_instance.add_doc()

    def get_solution_list(self) -> List[Point]:
        """Returns the solutions as list of points.
        """
        return self.solutions

    def get_solution_dict(self) -> Dict[int, Point]:
        """Returns the solutions as dictionary.
        """
        return dict((key + 1, self.solutions[key]) for key in range(len(self.solutions)))

    def get_best_solution(self, point: Point) -> int:
        """Returns the solution the minimizes the given objective function.

        Args:
            point: A point representing the objective function.

        Returns:
            Index of the best solution.
        """
        min_value, min_solution = float('inf'), 0
        one = Point([1] * self.dimension)

        for index, solution in enumerate(self.solutions):
            x = (2 * solution) - one
            value = point * x

            if value < min_value:
                min_value, min_solution = value, index + 1

        return min_solution

    @abstractmethod
    def generate_solutions(self) -> List[Point]:  # pragma: no cover
        """Generate the solution list.

        Returns:
            The solution list.
        """
        pass

    @abstractmethod
    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        pass


class CutInstance(Instance):
    """Generates instance for the Cut problem.
    """

    def __init__(self, **kwargs):
        """Initializes the cut instance.

        Args:
            **kwargs: A dictionary containing the parameters.
        """
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        n = int(kwargs["n"])
        dimension = int(n * (n - 1) / 2)
        size = 2 ** (n - 1)

        Instance.__init__(self, f'CUT-n{n}', 'cut', dimension, size, n)

    def generate_solutions(self) -> List['Point']:
        """Generate the solution list.

        Returns:
            The solution list.
        """
        kn = Kn(self.n)
        cuts = kn.get_cuts()
        return list(cuts.values())

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        kn = Kn(self.n)
        return kn.get_triangles()


class TSPInstance(Instance):
    """Generates instance for the Traveling Salesman problem.
    """

    def __init__(self, **kwargs):
        """Initializes the tsp instance.

        Args:
            **kwargs: A dictionary containing the parameters.
        """
        if 'n' not in kwargs:
            raise ValueError('Wrong arguments.')

        if kwargs['n'] <= 2:
            raise ValueError('The dimensions must be greater than 2.')

        n = int(kwargs["n"])
        dimension = int(n * (n - 1) / 2)
        size = int(factorial(n - 1) / 2)

        Instance.__init__(self, f'TSP-n{n}', 'tsp', dimension, size, n)

    def generate_solutions(self) -> List['Point']:
        """Generate the solution list.

        Returns:
            The solution list.
        """
        kn = Kn(self.n)
        cycles = kn.get_hamilton_cycles()
        return list(cycles.values())

    def get_triangles(self) -> List[List[int]]:
        """Returns the triangles to be consider in the triangle inequalities.

        Returns:
            A list containing the triangles with each triangle being represented
            by a list of three vertices.
        """
        kn = Kn(self.n)
        return kn.get_triangles()


class VoronoiDiagram:
    """Represents a Voronoi diagram with the corresponding Delaunay triangulation.

    Attributes:
        type: The instance type.
        name: The instance name.
        skeleton: The skeleton graph.
        hyperplanes: The corresponding hyperplanes for each Delaunay edge.
        cones: The cones for each solution.
    """

    type: str
    name: str
    cone_file: str

    instance: Instance
    skeleton: Skeleton
    hyperplanes: Dict[int, Hyperplane]
    cones: Dict[int, Cone]

    def __init__(self,  instance: Instance, skeleton: Skeleton, hyperplanes: Dict[int, Hyperplane]):
        """Initializes the Voronoi diagram.

        Args:
            skeleton: The skeleton graph.
            hyperplanes: The corresponding hyperplanes for each Delaunay edge.
        """
        self.type = instance.type
        self.name = instance.name

        self.instance = instance
        self.skeleton = skeleton
        self.hyperplanes = hyperplanes

    def build(self, solutions: Dict[int, Point]):
        """Builds the Voronoi diagram based on the given solutions.

        Args:
            solutions: The Voronoi vertices.
        """
        db_cone = DBCone(self.instance.name, self.instance.type, self.instance.dimension, self.instance.size)
        doc = db_cone.get_doc()

        if doc is not None:
            self.cones = dict()

            for (key, value) in db_cone.cones.items():
                self.cones[key] = Cone(key, solutions[key], value)
        else:
            self.cones = self.__generate_cones(solutions)
            cones = dict()

            for (key, value) in self.cones.items():
                cones[key] = value.hyperplanes

            db_cone.cones = cones
            db_cone.add_doc()

    def __generate_cones(self, solutions: Dict[int, Point]) -> Dict[int, Cone]:
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
            edges = self.skeleton.get_edges(s)
            hyperplanes = [self.skeleton.get_edge(s, e) for e in edges]

            for h in hyperplanes:
                hyperplane = self.hyperplanes[h]

                if hyperplane.in_halfspace(solution):
                    cone.add_hyperplane(h)
                else:
                    cone.add_hyperplane(-h)

            cones[s] = cone

        return cones


class DBPolytope(DBModel):

    name: str
    type: str
    dimension: int
    solutions: int
    hyperplanes: int
    edges: int
    degree: float

    def __init__(self, name: str, type: str, dimension: int, size: int, hyperplanes: int, edges: int, degree: float):
        self.name = name
        self.type = type
        self.dimension = dimension
        self.solutions = size
        self.hyperplanes = hyperplanes
        self.edges = edges
        self.degree = degree

    @classmethod
    def from_doc(cls, doc: dict) -> DBModel:
        polytope = DBPolytope(doc['name'], doc['type'], doc['dimension'], doc['solutions'], doc['hyperplanes'], doc['edges'], doc['degree'])
        polytope.load_doc(doc)

        return polytope

    @classmethod
    def get_collection(cls) -> str:
        return POLYTOPES

    def get_file_name(self) -> str:
        return self.name

    def load_doc(self, doc: dict):
        pass

    def get_repr(self) -> dict:
        return {'name': self.name,
                'type': self.type,
                'dimension': self.dimension,
                'solutions': self.solutions,
                'hyperplanes': self.hyperplanes,
                'edges': self.edges,
                'degree': self.degree}


class Polytope(ABC):
    """Base class that build the polytopes for different instances.

    Attributes:
        full_name: The polytope full name.
        name: The instance name.
        dimension: The instance dimension.
        size: The instance size.
        n: The instance main parameter.
        instance: The instance.
        skeleton: The skeleton graph.
        complement: The extended skeleton graph.
        hyperplanes: The set of hyperplanes.
        voronoi: The Voronoi diagram.
        vertices: The polytope vertices.
    """

    full_name: str
    name: str
    dimension: int
    size: int
    n: int
    polytope_file: str

    instance: Instance
    skeleton: Skeleton
    complement: Skeleton
    hyperplanes: Dict[int, Hyperplane]
    n_skeleton_hyperplanes: int
    n_complement_hyperplanes: int
    voronoi: VoronoiDiagram
    vertices: Dict[int, Point]

    def __init__(self, instance: Instance, full_name: str):
        """Initializes the polytope with the given instance and name.

        Args:
            instance: The instance.
            full_name: The polytope full name.
        """
        self.instance = instance
        self.full_name = full_name
        self.name = self.instance.type
        self.dimension = self.instance.dimension
        self.size = self.instance.size
        self.n = self.instance.n

        self.vertices = self.instance.get_solution_dict().copy()
        self.vertices = dict((key, Point([1] * self.dimension) - 2 * point) for (key, point) in self.vertices.items())

        self.build_skeleton()
        self.voronoi = VoronoiDiagram(self.instance, self.skeleton, self.hyperplanes)
        self.voronoi.build(self.vertices)

        db_polytope = DBPolytope(instance.name, instance.type, instance.dimension, instance.size,
                                 self.n_skeleton_hyperplanes, len(self.skeleton.edges), self.skeleton.degree)

        if db_polytope.get_doc() is None:
            db_polytope.add_doc()

    def build_skeleton(self):
        """Build the polytope skeleton.

        If the skeleton has been previously computed it is loaded from the file.
        Otherwise it is generated and saved.
        """
        db_skeleton = DBSkeleton(self.instance.name, self.instance.type, self.instance.dimension, self.instance.size, list(self.vertices.keys()))
        doc = db_skeleton.get_doc()

        if doc is not None:
            self.hyperplanes = db_skeleton.hyperplanes
            self.n_skeleton_hyperplanes = db_skeleton.n_skeleton_hyperplanes
            self.n_complement_hyperplanes = db_skeleton.n_complement_hyperplanes
            self.skeleton = Skeleton()
            self.complement = Skeleton()

            for s_edge in db_skeleton.skeleton_edges:
                self.skeleton.add_edge(s_edge[0], s_edge[1], s_edge[2])

            for c_edge in db_skeleton.complement_edges:
                self.complement.add_edge(c_edge[0], c_edge[1], c_edge[2])
        else:
            self.hyperplanes, self.skeleton, self.complement, self.n_skeleton_hyperplanes, self.n_complement_hyperplanes = self.__generate_skeleton()
            db_skeleton.hyperplanes = self.hyperplanes
            db_skeleton.n_skeleton_hyperplanes = self.n_skeleton_hyperplanes
            db_skeleton.n_complement_hyperplanes = self.n_complement_hyperplanes
            db_skeleton.skeleton_edges = self.skeleton.graph.edges.data('h')
            db_skeleton.complement_edges = self.complement.graph.edges.data('h')
            db_skeleton.add_doc()

    def get_bisector(self, i: int, j: int) -> int:
        """Returns the bisector of two points.

        Args:
            i: First node.
            j: Second node.

        Returns:
            The index of the bisector hyperplane, chosen from the skeleton or
            the extended skeleton.
        """
        if self.skeleton.has_edge(i, j):
            return self.skeleton.get_edge(i, j, 'h')
        else:
            return self.complement.get_edge(i, j, 'h')

    def get_hyperplane(self, h: int) -> Hyperplane:
        return self.hyperplanes[h]

    def __generate_skeleton(self) -> Tuple[Dict[int, Hyperplane], Skeleton, Skeleton, int, int]:
        """Generates the skeleton along with the hyperplanes.

        Returns:
            The skeleton graph.
            The set of hyperplanes.
            The extended skeleton graph.
            The extended set of hyperplanes.
        """
        skeleton = Skeleton()
        extended_skeleton = Skeleton()
        adjacency_lp = AdjacencyProblem(self.dimension, self.instance.name, self.vertices)
        hyperplanes = set()
        extended_hyperplanes = set()
        vertices = self.instance.get_solution_dict()

        for i in range(1, self.size + 1):
            for j in range(i + 1, self.size + 1):
                h = Hyperplane(vertices[j] - vertices[i], d=0)

                if adjacency_lp.test_edge_primal(i, j):
                    hyperplanes.add(h)
                    skeleton.add_edge(i, j, h=hash(h))
                else:
                    extended_hyperplanes.add(h)
                    extended_skeleton.add_edge(i, j, h=hash(h))

        hyperplanes = list(hyperplanes)
        hyperplanes.sort()
        hyperplanes = dict((key + 1, hyperplanes[key]) for key in range(len(hyperplanes)))

        extended_hyperplanes = list(extended_hyperplanes)
        extended_hyperplanes.sort()
        extended_hyperplanes = dict((key + len(hyperplanes) + 1, extended_hyperplanes[key]) for key in range(len(extended_hyperplanes)))

        map_dict = {hash(hyperplanes[i]): i for i in hyperplanes.keys()}
        extended_map_dict = {hash(extended_hyperplanes[i]): i for i in extended_hyperplanes.keys()}

        for edge in skeleton.edges:
            skeleton.add_edge(edge[0], edge[1], h=map_dict[skeleton.get_edge(edge[0], edge[1], 'h')])

        for edge in extended_skeleton.edges:
            extended_skeleton.add_edge(edge[0], edge[1], h=extended_map_dict[extended_skeleton.get_edge(edge[0], edge[1], 'h')])

        return {**hyperplanes, **extended_hyperplanes}, skeleton, extended_skeleton, len(hyperplanes), len(extended_hyperplanes)

    def __repr__(self):  # pragma: no cover
        degrees = [self.skeleton.graph.degree(i) for i in self.skeleton.graph.nodes]

        return f'NAME: {self.instance.name}\n' \
               f'TYPE: {self.instance.type.upper()}\n' \
               f'DIMENSION: {self.dimension}\n' \
               f'SOLUTIONS: {self.size}\n' \
               f'HYPERPLANES: {self.n_skeleton_hyperplanes}\n' \
               f'EDGES: {len(self.skeleton.edges)}\n' \
               f'AVERAGE DEGREE: {self.skeleton.degree}\n'


class CutPolytope(Polytope):
    """Extends the base polytope for cut instances.
    """

    def __init__(self, n: int):
        """Initializes the cut polytope with the Cut instance.

        Args:
            n: The number of nodes in the graph.
        """
        Polytope.__init__(self, CutInstance(n=n), 'cut')


class TSPPolytope(Polytope):
    """Extends the base polytope for traveling salesman instances.
    """

    def __init__(self, n: int):
        """Initializes the tsp polytope with the Traveling Salesman instance.

        Args:
            n: The number of nodes in the graph.
        """
        Polytope.__init__(self, TSPInstance(n=n), 'traveling salesman')


class DBTree(DBModel):

    name: str
    type: str
    graph: DiGraph
    root: str
    height: int
    k: int

    def __init__(self, name: str, type: str, k: int):
        self.name = name
        self.type = type
        self.k = k
        self.graph = DiGraph()
        self.root = ''
        self.height = 0

    def add_node(self, node: str, height: int, solutions: List[int], hyperplane: int):
        self.graph.add_node(node, height=height, solutions=solutions, hyperplane=hyperplane)
        self.height = max(self.height, height)

    def add_edge_left(self, parent: str, child: str):
        self.graph.add_edge(parent, child, direction='left')

    def add_edge_right(self, parent: str, child: str):
        self.graph.add_edge(parent, child, direction='right')

    @classmethod
    def from_doc(cls, doc: dict) -> 'DBModel':
        tree = DBTree(doc['name'], doc['type'], doc['k'])
        tree.load_doc(doc)

        return tree

    @classmethod
    def get_collection(cls) -> str:
        return TREES

    def get_file_name(self) -> str:
        return f'{self.name}-k{self.k}'

    def load_doc(self, doc: dict):
        self.height = doc['height']
        self.root = doc['root']
        self.graph = DiGraph()

        for (node, data) in doc['nodes'].values():
            self.add_node(node, data['height'], data['solutions'], data['hyperplane'])

        for edge in doc['edges']:
            if edge[2] == 'left':
                self.add_edge_left(edge[0], edge[1])
            else:
                self.add_edge_right(edge[0], edge[1])

    def get_repr(self) -> dict:
        nodes = dict()
        edges = []

        for n in self.graph.nodes:
            node = self.graph.nodes[n]
            nodes[n] = {'height': node['height'], 'hyperplane': node['hyperplane'], 'solutions': node['solutions']}

        for edge in self.graph.edges.data():
            edges.append((edge[0], edge[1], edge[2]['direction']))

        return {'name': self.name,
                'type': self.type,
                'k': self.k,
                'height': self.height,
                'root': self.root,
                'nodes': nodes,
                'edges': edges}


class Node:

    hash: str
    region: List[int]
    solutions: List[int]
    hyperplanes: List[int]

    hyperplane: int
    height: int
    left: str
    right: str

    threshold: int
    explored: List[int]

    def __init__(self, region: Region, solutions: List[int], hyperplanes: List[int]):
        self.hash = repr(region)
        self.region = region.hyperplanes
        self.solutions = solutions
        self.hyperplanes = hyperplanes
        self.threshold = 0
        self.explored = []

    def set_leaf(self):
        self.set_node(0, -1)
        self.hyperplanes = []

    def set_node(self, height: int, threshold: int, hyperplane: int = None, left: str = None, right: str = None):
        self.height = height
        self.threshold = threshold
        self.hyperplane = hyperplane
        self.left = left
        self.right = right


class TreeBuilder:

    polytope: Polytope

    def __init__(self, polytope: Polytope):
        self.polytope = polytope

    def build_tree(self, nodes: Dict[str, Node], root: Node, k: int) -> DBTree:
        tree = DBTree(self.polytope.instance.name, self.polytope.instance.type, k)
        tree.root = root.hash
        tree.add_node(root.hash, 0, root.solutions, root.hyperplane)
        queue = [(root, 0)]

        while len(queue) > 0:
            node, height = queue.pop(0)
            left_node = nodes[node.left]
            tree.add_node(left_node.hash, height + 1, left_node.solutions, left_node.hyperplane)
            tree.add_edge_left(node.hash, left_node.hash)

            if len(left_node.solutions) > 1:
                queue.append((left_node, height + 1))

            right_node = nodes[node.right]
            tree.add_node(right_node.hash, height + 1, right_node.solutions, right_node.hyperplane)
            tree.add_edge_left(node.hash, right_node.hash)

            if len(right_node.solutions) > 1:
                queue.append((right_node, height + 1))

        return tree


class IterativeTree:

    polytope: Polytope
    intersections: Intersections

    threshold: int
    lb: int
    ub: int

    table: Dict[int, List[List[int]]]
    nodes: Dict[str, Node]
    tree_builder: TreeBuilder

    def __init__(self, polytope: Polytope):
        self.polytope = polytope
        self.intersections = Intersections(polytope)
        self.threshold = INFINITY
        self.lb = ceil(log2(len(self.polytope.vertices)))
        self.ub = len(self.polytope.vertices) - 1
        self.table = self.get_ordering_table()
        self.nodes = dict()
        self.tree_builder = TreeBuilder(polytope)

    def build_tree(self, threshold: int = INFINITY):
        region = Region()
        solutions = list(self.polytope.vertices.keys())
        hyperplanes = list(self.polytope.hyperplanes.keys())
        positions = self.intersections.get_positions(region, solutions)
        hyperplanes = self.process_hyperplanes(hyperplanes, positions, len(solutions))
        node = Node(region, solutions, hyperplanes)
        self.threshold = min(threshold, len(hyperplanes))
        self.lb = self.get_lower_bound(node)

        start_time = time.time()

        for k in range(1, self.threshold + 1):
            root = self.explore_node(node, k, self.lb)
            self.ub = root.height
            tree = self.tree_builder.build_tree(self.nodes, root, k)
            tree.add_doc()
            e = int(time.time() - start_time)
            print(k, root.height, '{:02d}:{:02d}:{:02d}'.format(e // 3600, (e % 3600 // 60), e % 60))

            if root.threshold == -1:
                print('OPTIMAL SOLUTION FOUND')
                break

    def explore_node(self, node: Node, k: int, lb: int) -> Node:
        if node.hash in self.nodes:
            node = self.nodes[node.hash]

        if node.threshold == -1:                                                # node calculated to optimality
            return node
        else:
            if node.hash not in self.nodes:                                     # first time calculation
                min_height = INFINITY
                node.hyperplane = None
                node.left = None
                node.right = None
                node.height = INFINITY
                valid_tree = False
            else:                                                               # node previous calculated
                min_height = node.height
                valid_tree = True

            optimal_tree = False

            # run computations for k hyperplanes in each level
            # a previous calculated node stores how many hyperplanes as threshold
            for i in range(k):
                h = node.hyperplanes[i]

                if len(node.region) >= self.ub:
                    break

                new_hyperplanes = node.hyperplanes.copy()
                new_hyperplanes.remove(h)

                left_solutions = [item for item in node.solutions if item not in self.intersections.positions[node.hash][h].right]

                if len(left_solutions) == 1:
                    left_subtree = self.case_1(node, left_solutions, new_hyperplanes, -h)
                elif len(left_solutions) == 2:
                    left_subtree = self.case_2(node, left_solutions, new_hyperplanes, -h)
                else:
                    left_node = self.case_default(node, left_solutions, new_hyperplanes, -h)
                    left_subtree = self.explore_node(left_node, k, self.get_lower_bound(left_node))

                if left_subtree.height <= min_height:
                    right_solutions = [item for item in node.solutions if item not in self.intersections.positions[node.hash][h].left]
                    right_region = Region(node.region)
                    right_region.add_hyperplane(h)

                    if len(right_solutions) == 1:
                        right_subtree = self.case_1(node, right_solutions, new_hyperplanes, h)
                    elif len(right_solutions) == 2:
                        right_subtree = self.case_2(node, right_solutions, new_hyperplanes, h)
                    else:
                        right_node = self.case_default(node, right_solutions, new_hyperplanes, h)
                        right_subtree = self.explore_node(right_node, k, self.get_lower_bound(right_node))

                    height = max(left_subtree.height, right_subtree.height)

                    if height < min_height - 1:
                        min_height = height + 1
                        node.hyperplane = h
                        node.height = height + 1
                        node.left = left_subtree.hash
                        node.right = right_subtree.hash
                        valid_tree = True

                if i >= node.threshold:
                    node.threshold = node.threshold + 1

                if node.height == lb:
                    optimal_tree = True
                    break

            if optimal_tree or len(node.hyperplanes) == 0:
                node.threshold = -1
                node.hyperplanes = []

            if node.hash not in self.nodes or valid_tree:
                self.nodes[node.hash] = node

            return node

    def process_hyperplanes(self, hyperplanes: List[int], positions: Dict[int, Bisection], s: int) -> List[int]:
        ordered_hyperplanes = []

        for h in hyperplanes:
            s_l = s - len(positions[h].right)
            s_r = s - len(positions[h].left)
            order = self.table[s][s_l][s_r]

            if s_l + s_r > s or s_l > 0 and s_r > 0:
                ordered_hyperplanes.append((h, order))

        ordered_hyperplanes.sort(key=lambda x: x[1])

        return [h[0] for h in ordered_hyperplanes]

    def get_ordering_table(self) -> Dict[int, List[List[int]]]:
        table = dict()

        for s in range(2, self.polytope.instance.size + 1):
            table[s] = [[0 for _ in range(s + 1)] for _ in range(s + 1)]
            half = ceil(s / 2)
            order = 1

            for i in range(half, s + 1):
                for j in range(s - i, i + 1):
                    table[s][i][j] = table[s][j][i] = order
                    order = order + 1

        return table

    def get_lower_bound(self, node: Node) -> int:
        best_l = len(node.solutions) - len(self.intersections.positions[node.hash][node.hyperplanes[0]].left)
        best_r = len(node.solutions) - len(self.intersections.positions[node.hash][node.hyperplanes[0]].right)
        return ceil(log2(max(best_l, best_r))) + 1

    def case_1(self, node: Node, solutions: List[int], hyperplanes: List[int], hyperplane: int) -> Node:
        region = Region(node.region)
        region.add_hyperplane(hyperplane)
        new_node = Node(region, solutions, hyperplanes)
        new_node.set_leaf()

        self.nodes[new_node.hash] = new_node
        return new_node

    def case_2(self, node: Node, solutions: List[int], hyperplanes: List[int], hyperplane: int) -> Node:
        region = Region(node.region)
        region.add_hyperplane(hyperplane)
        new_node = Node(region, solutions, hyperplanes)
        h = self.polytope.get_bisector(solutions[0], solutions[1])

        left_region = Region(new_node.region)
        left_region.add_hyperplane(-h)
        left_node = Node(left_region, [solutions[1]], hyperplanes)
        left_node.set_leaf()
        self.nodes[left_node.hash] = left_node

        right_region = Region(new_node.region)
        right_region.add_hyperplane(h)
        right_node = Node(right_region, [solutions[0]], hyperplanes)
        right_node.set_leaf()
        self.nodes[right_node.hash] = right_node

        new_node.set_node(1, -1, self.polytope.get_bisector(solutions[0], solutions[1]), left_node.hash, right_node.hash)
        new_node.hyperplanes = []

        self.nodes[new_node.hash] = new_node
        return new_node

    def case_default(self, node: Node, solutions: List[int], hyperplanes: List[int], hyperplane: int) -> Node:
        region = Region(node.region)
        region.add_hyperplane(hyperplane)
        positions = self.intersections.get_positions(region, solutions)
        new_hyperplanes = self.process_hyperplanes(hyperplanes, positions, len(solutions))
        new_node = Node(region, solutions, new_hyperplanes)

        return new_node


if __name__ == '__main__':
    print(MAIN_DIRECTORY)
    polytope = CutPolytope(3)
    # polytope = TSPPolytope(5)

    tree = IterativeTree(polytope)
    tree.build_tree()
