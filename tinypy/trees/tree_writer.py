from tinypy.trees.enumeration_tree import EnumerationTree
from tinypy.utils.file import create_folder, file_exists, get_full_path

TAB = '    '


class TreeWriter:

    tree: EnumerationTree
    tree_file: str

    def __init__(self, tree):
        self.tree = tree
        self.tree_file = get_full_path('tinypy', 'generated', 'trees',
                                       tree.polytope.instance.type, f'{tree.polytope.instance.name.replace("-", "_")}.py')
        create_folder(get_full_path('tinypy', 'generated', 'trees', tree.polytope.instance.type))
        with open(get_full_path('tinypy', 'generated', 'trees', tree.polytope.instance.type, '__init__.py'), 'w') as file:
            file.write('')

    def write_tree(self):
        # if not file_exists(self.tree_file):
        with open(self.tree_file, 'w+') as file:
            self.write_imports(file)
            self.write_class(file)
            self.write_test(file)

    def write_imports(self, file):
        file.write('from tinypy.generated.trees.generated_tree import GeneratedTree\n\n')
        file.write('from tinypy.geometry.point import Point\n\n\n')

    def write_class(self, file):
        file.write(f'class {self.tree.polytope.instance.type.upper()}Tree(GeneratedTree):\n\n')
        file.write(f'{TAB}def __init__(self, polytope):\n')
        file.write(f'{TAB}{TAB}self.polytope = polytope\n')
        file.write(f'{TAB}{TAB}self.hyperplanes = polytope.H\n\n')

    def write_test(self, file):
        file.write(f'{TAB}def test(self, point: Point):\n')
        self.write_if(file, self.tree.root)

    def write_if(self, file, index: int):
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
            self.write_if(file, right_node)
            file.write(f'{TAB}{TAB}{TAB * height}else:\n')
            self.write_if(file, left_node)
