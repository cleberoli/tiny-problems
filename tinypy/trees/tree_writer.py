from typing import List

from tinypy.models.tree import Tree
from tinypy.polytopes.base_polytope import Polytope
from tinypy.utils.file import create_directory, get_full_path

TAB = '    '


class TreeWriter:
    """Takes a tree and writes the program to perform the comparisons.

    Attributes:
        tree: The tree.
        tree_file: The path where the generated tree should be stored.
    """

    tree_file: str
    tree: Tree

    def __init__(self, polytope: Polytope):
        """Initializes the writer.

        """
        self.polytope = polytope
        self.tree = Tree(polytope.instance.name, polytope.instance.type, 1)
        self.tree.get_doc()
        self.tree_file = get_full_path('tinypy', 'generated', 'trees',
                                       polytope.instance.type, f'{polytope.instance.name.replace("-", "_")}.py')
        create_directory(get_full_path('tinypy', 'generated', 'trees', polytope.instance.type))

        with open(get_full_path('tinypy', 'generated', 'trees', polytope.instance.type, '__init__.py'), 'w') as file:
            file.write(f'"""Contains the generated tree classes for the {polytope.full_name.title()} polytope.\n')
            file.write('"""')

    def write_tree(self):
        """Writes the generate tree file.
        """
        # if not file_exists(self.tree_file):
        with open(self.tree_file, 'w+') as file:
            self.__write_imports(file)
            self.__write_class(file)
            self.__write_test(file)

    def __write_imports(self, file):
        """Writes the import section.

        Args:
            file: The file.
        """
        file.write('from tinypy.generated.trees.generated_tree import GeneratedTree\n\n')
        file.write('from tinypy.geometry.point import Point\n\n\n')

    def __write_class(self, file):
        """Writes the class definition.

        Args:
            file: The file.
        """
        file.write(f'class {self.polytope.instance.type.upper()}Tree(GeneratedTree):\n\n')
        file.write(f'{TAB}def __init__(self, polytope):\n')
        file.write(f'{TAB}{TAB}GeneratedTree.__init__(self, polytope)\n\n')

    def __write_test(self, file):
        """Writes the test method.

        Args:
            file: The file.
        """
        file.write(f'{TAB}def test(self, point: Point):\n')
        self.__write_if(file, self.tree.root, [])

    def __write_if(self, file, parent: str, hyperplanes: List[int]):
        """Writes the if condition.

        Args:
            file: The file.
        """
        node = self.tree.graph.nodes[parent]
        solutions, hyperplane = node['solutions'], node['hyperplane']
        height = len(hyperplanes)

        if len(solutions) == 1:
            file.write(f'{TAB}{TAB}{TAB * height}return {solutions[0]}, {height}\n')
        else:
            left = None
            right = None

            for child, direction in self.tree.graph[parent].items():
                if direction['direction'] == 'left':
                    left = child
                else:
                    right = child

            h_right = hyperplanes.copy()
            h_left = hyperplanes.copy()
            h_right.append(hyperplane)
            h_left.append(-hyperplane)

            file.write(f'{TAB}{TAB}{TAB * height}if self.hyperplanes[{hyperplane}].in_halfspace(point):\n')
            self.__write_if(file, right, h_right)
            file.write(f'{TAB}{TAB}{TAB * height}else:\n')
            self.__write_if(file, left, h_left)
