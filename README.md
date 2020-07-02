# Tiny Problems

This project implements the ideas presented in the **Exact algorithms for small-scale combinatorial optimization problems**. 

The architecture was designed in a way to support any optimization problem whose possible solutions are a subset of the vertices of 0-1 polytope (in any dimension). 
The main elements are instances and polytopes.

## Getting started

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
* `instances` - list of solutions
* `skeleton` - list of hyperplanes and edges with correspondent hyperplane
* `cones` - list of hyperplanes delimiting the cone of each solution
* `polytopes` - summary of attributes (the system doesn't actually read this file to construct a polytope, it read the previous three)

## Extending the code

You can extend this code easily for any applicable problems. In order to do that there are two basic steps.

### Adding a new instance
When adding a new problem the first task is to implement the generator for your instances. 
Just create a `foo_instance.py` file inside the `instances` module and implement it like the other ones.
Note that, you don't need to implement the `generate_solutions` method if you have your solution files in the `.tpif` format stored in the files
 directory.

### Adding a new polytope
You ust neet to create a `foo_polytope.py` file inside the `polytopes` module and set up the `instance` used and its `full_name`.