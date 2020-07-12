# Tiny Problems

This project implements the ideas presented in the **Exact algorithms for small-scale combinatorial optimization problems**. 

The architecture was designed in a way to support any optimization problem whose possible solutions are a subset of the vertices of 0-1 polytope (in any dimension). 
The main elements are instances and polytopes.

#### Structure
This project is made of three directories:

* **docs**: contains the code documentation along with more details regarding the specifications and architecture.
* **files**: contains the preprocessed files used to speed up future computations (see the logging section for more details).
* **tinypy**: contains the source code implemented in Python.

## Getting started

The first thing you need to do is make sure you have all necessary python packages. 
You just need to run the following command to install required dependencies:

```
pip install -r requirements.txt
```

### Polytopes

The polytope currently supported are:
* `cub` - Hypercube Polytope
* `cut` - Cut Polytope
* `pyr` - Hyperpyramid Polytope
* `rnd` - Random Polytope
* `tsp` - Symmetric Travelling Salesman Polytope

### Logging

In order to speed up future processes we log the structure of all basic objects we have in the `files` directory. 
Once an object is stored, there are not further computations to reuse that object in the future (besides the file reading).

Currently we store the following objects with their respective structures:
* `benchmarks` - benchmark files to test the generates trees along with their solutions
* `cones` - list of hyperplanes delimiting the cone of each solution
* `instances` - list of solutions
* `polytopes` - summary of attributes (the system doesn't actually read this file to construct a polytope, it read the previous three)
* `skeleton` - list of hyperplanes and edges with correspondent hyperplane

## Extending the code

You can extend this code easily for any applicable problems. In order to do that there are two basic steps.

### Adding a new instance
When adding a new problem the first task is to implement the generator for your instances. 
Just create a `foo_instance.py` file inside the `instances` module and implement it like the other ones.
Note that, you don't need to implement the `generate_solutions` method if you have your solution files in the `.tpif` format stored in the files
 directory.

### Adding a new polytope
You just need to create a `foo_polytope.py` file inside the `polytopes` module and set up the `instance` used with its `full_name`.

## Examples
Here is an example on how you can build a polytope, generate its decision tree and write it to a file.

```
from tinypy.polytopes.tsp_polytope import TSPPolytope
from tinypy.trees.enumeration_tree import EnumerationTree
from tinypy.trees.tree_writer import TreeWriter

tsp5 = TSPPolytope(5)
tree = EnumerationTree(tsp5)
tree.make_tree()

writer = TreeWriter(tree)
wrtier.write_tree()
```


Once you have writen the tree you can evaluate its performance in the following way.

```
from tinypy.polytopes.tsp_polytope import TSPPolytope
from tinypy.benchmark.tsp_benchmark import TSPBenchmark
from tinypy.benchmark.benchmark_runner import BenchmarkRunner
from tinypy.generated.trees.tsp.TSP_n5 import TSPTree

tsp5 = TSPPolytope(5)
benchmark = TSPBenchmark(n=5)
benchmark.generate_benchmark()
runner = BenchmarkRunner(TSPTree(tsp5))
runner.run()
```