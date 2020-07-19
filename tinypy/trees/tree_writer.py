from tinypy.trees.base_tree import Tree
from tinypy.utils.file import create_directory, file_exists, get_full_path

TAB = '    '


class TreeWriter:
    """Takes a tree and writes the program to perform the comparisons.

    Attributes:
        tree: The tree.
        tree_file: The path where the generated tree should be stored.
    """

    tree: Tree
    tree_file: str

    def __init__(self, tree):
        """Initializes the writer.

        Args:
            tree: The tree.
        """
        self.tree = tree
        self.tree_file = get_full_path('tinypy', 'generated', 'trees',
                                       tree.polytope.instance.type, f'{tree.polytope.instance.name.replace("-", "_")}.py')
        create_directory(get_full_path('tinypy', 'generated', 'trees', tree.polytope.instance.type))
        with open(get_full_path('tinypy', 'generated', 'trees', tree.polytope.instance.type, '__init__.py'), 'w') as file:
            file.write('')

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
        file.write(f'class {self.tree.polytope.instance.type.upper()}Tree(GeneratedTree):\n\n')
        file.write(f'{TAB}def __init__(self, polytope):\n')
        file.write(f'{TAB}{TAB}GeneratedTree.__init__(self, polytope)\n\n')

    def __write_test(self, file):
        """Writes the test method.

        Args:
            file: The file.
        """
        file.write(f'{TAB}def test(self, point: Point):\n')
        self.__write_if(file, self.tree.root)

    def __write_if(self, file, index: int):
        """Writes the if condition.

        Args:
            file: The file.
            index: The node index.
        """
        node = self.tree.graph.nodes[index]
        solutions, height = node['solutions'], node['height']

        if len(solutions) == 1:
            file.write(f'{TAB}{TAB}{TAB * height}return {solutions[0]}, {index}, {height}\n')
        else:
            hyperplane = node['hyperplane']
            successors = self.tree.graph.succ[index]
            left_node, right_node = 0, 0

            for (key, value) in successors.items():
                if value['direction'] == 'left':
                    left_node = key
                if value['direction'] == 'right':
                    right_node = key

            file.write(f'{TAB}{TAB}{TAB * height}if self.hyperplanes[{hyperplane}].in_halfspace(point):\n')
            self.__write_if(file, right_node)
            file.write(f'{TAB}{TAB}{TAB * height}else:\n')
            self.__write_if(file, left_node)
