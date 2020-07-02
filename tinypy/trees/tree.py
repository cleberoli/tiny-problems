from typing import Dict

from tinypy.geometry import Cone, Hyperplane, Region
from tinypy.graph import Node


class Tree:

    def __init__(self, cones: Dict[int, 'Cone'], hyperplanes: Dict[int, 'Hyperplane'], dim: int, name: str):
        self.__cones = cones
        self.__hyperplanes = hyperplanes
        self.__dim = dim
        self.__name = name
        self.__queue = []
        self.__root = None
        self.__height = 0
        print(len(hyperplanes))

    def make_tree(self):
        self.__root = Node(0, self.__cones, self.__hyperplanes, self.__dim, Region(self.__dim), f'{self.__name}_T')
        self.__queue.append(self.__root)
        self.bfs()
        print(self.__height)

    def bfs(self):
        while len(self.__queue) > 0:
            node = self.__queue.pop(0)
            self.__height = node.height if node.height > self.__height else self.__height

            if len(node.left_cones) > 1 and len(node.right_cones) > 1:
                left = node.add_left_node()
                right = node.add_right_node()

                if left is not None:
                    self.__queue.append(left)
                if right is not None:
                    self.__queue.append(right)
