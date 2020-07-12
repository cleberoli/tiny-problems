# Project Documentation

This project implements the ideas presented in the **Exact Algorithms for Small-Scale 
Combinatorial Optimization Problems** paper which is still an ongoing project.
This brief documentations describes the specifications, architecture and quality tests.

Note that since the system has no interface the user should directly interact with the code provided.
Therefore, this documentation along with the one found on the `README` file in the root 
directory such suffice as user manual.

#### Documentation Structure

This documentation is made of this file along with the three other directories:
* **coverage**: contains the coverage report generated, based on the unit tests written.
* **html**: contains the html version of the code documentation, generated based on the
`docstrings` in the files.
* **uml**: contains the image files of the diagrams presented here.

## Specification

The goal of this project is to design small decision trees to solve small instances
of well-known classical problems, based on the geometric characteristics of these polytopes.
In order to accomplish this goal our system has five main use cases shown in the figure below,
where the user is responsible for performing all use cases as it is specified.

![Use case diagram](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/use-cases.jpg?raw=true)

### 1. Generate Instance

#### Goal
Given a defined polytope the user should be able to generate the instances
for that polytope (i.e. the list of its vertices).

#### Flow
1. The user creates the corresponding instance object passing the desired parameters.
2. The system verifies whether an instance matching the parameters exists:

    a) In case such instance already exists the system loads the solutions from file.  
    b) Otherwise it computes the solution according with the definition and saves
    them to a file.
3. The user can now access the instance's solution by calling the methods `get_solution_list` or
`get_solution_dict`.

### 2. Build Polytope

#### Goal
Given a defined polytope the user should able to build it, with its skeleton and voronoi diagram.

#### Flow
1. The user creates the corresponding polytope object passing the desired parameters.
2. The system loads the corresponding instance files.
3. The system verifies whether an skeleton file matching the parameters exists:

    a) In case such skeleton already exists the system loads it from the file.  
    b) Otherwise it computes the skeleton according with the definition and saves
    it to a file.
4. The system creates the voronoi diagram with the computed skeleton.
5. The system computes the solution cones based on the instance solutions.

### 3. Generate Benchmark

#### Goal
Given a defined instance the user should be able to generate benchmark files with
objective functions that correspond to that instance.

#### Flow
1. The user creates the corresponding benchmark object passing the desired parameters.
2. The system loads the corresponding instance files.
3. The system generates the required number of points for each solution and saves them
to a file along with their corresponding solution.

### 4. Generate Decision Tree

#### Goal
Given a defined polytope the user should be able to generate the decision tree that accurately
classifies any given point to its corresponding solution.

#### Flow
1. The user creates the tree object passing the desired polytope as parameter.
2. The system generates the tree with the chosen algorithm.
3. The user calls the `TreeWriter` passing the tree as parameter.
4. The systems writes the source code that will execute the computed tree for any point.

### 5. Evaluate Tree

#### Goal
Given a generated decision tree along with its corresponding benchmark the user should
be able to evaluate the decision tree for its accuracy.

#### Flow
1. The user creates the decision tree file passing the corresponding polytope as parameter.
2. The user creates a `BenchmarkRunner` object passing the generated tree as parameter.
3. The user calls the `run` method from the `BenchmarkRunner`.
4. The system runs the decision tree for each point in the benchmark file and generates
a solution file containing the following for each benchmark point:

    * Whether the solutions are the same
    * Whether the solutions are equivalent (both solutions have the same optimal value)
    * The benchmark solution
    * The solution found by the decision tree
    * The corresponding tree node
    * The node's height
5. The system also computes the average height of the tree as the average of the heights for each
point in the benchmark.

## Architecture

The project's architecture is divided into eight modules, shown as an overview in the class diagram below.

![Overview of classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/overview.jpg?raw=true)

Keeping in mind the general structure presented we shall look into module specifically.

### 1. Benchmark
Contains the benchmark classes with the method for generating them.

The main functions are implemented in the base benchmark and all other possible benchmarks should
extend the base one and implement only the specified function. Along with these classes there is the BenchmarkRunner class which takes a generated tree and runs it
for all benchmarks points.

![Benchmark classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/benchmark.jpg?raw=true)

### 2. Geometry
Offers implementations of basic geometric concepts and objects.

The geometry classes represent geometric entities like points, hyperplanes, and even complex
structures like Voronoi diagrams. The classes here are independent in the sense they can be
initialized freely as long as you respect the parameters.

![Geometry classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/geometry.jpg?raw=true)

### 3. Graph
Offers implementations of graph related objects and graphs themselves.

The geometry classes represent either basic graphs like the complete graph Kn, or graph structures
associated to the problem like the skeleton. All graph implementations are based on the [NetworkX](https://networkx.github.io/) package.

![Graph classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/graph.jpg?raw=true)

### 4. Instances
Contains the instance classes with the methods for generating them.

The main functions are implemented in the base instance and all other possible instances should
extend the base one and implement only the specified function.

![Instance classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/instances.jpg?raw=true)

### 5. Lp
Contains implementation for the linear programming models used.

![Lp classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/lp.jpg?raw=true)

### 6. Polytopes
Contains the polytope classes with the methods for building them.

The main functions are implemented in the base polytope and all other possible polytopes should
extend the base one and only specific the correct instance to be used.

![Polytope classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/polytopes.jpg?raw=true)

### 7. Trees
Contains the different decision tree along their writer.

The main function for building the tree are implemented in the base tree. All possible variations
should extend the base one and define the method for choosing the hyperplane.

![Tree classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/trees.jpg?raw=true)

### 8. Utils
Contains utility functions to deal with combinatorial problems and accessing files.

![Util classes](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/utils.jpg?raw=true)

### Dependencies
The following diagram shows the dependencies among the previous modules, with the exception
of the `utils` module, since every other module depends on it.

![Dependencies](https://github.com/cleberoli/tiny-problems/blob/master/docs/uml/dependencies.jpg?raw=true)

## Quality Assessment
In order to evaluate the system quality two approaches were used.

### 1. Unit Tests
Unit tests were during the developing to evaluate individual functions. 
Inside each module there is a `tests` submodule containing the test files used. 
The assertions made mostly regarded the expected values and sometimes also their types.

The `coverage` directory contains the report generated showing the score of 100% coverage
and the `test.log` file contains the output of tests showing that all of them are passing.

### 2. Validation Tests
These tests were designed to evaluate the system performance as a whole. The goal was to process
the benchmark for the `CUB-n3` and `TSP-n5` instances achieving a 100% accuracy. These results can be
found in the `files/benchmarks` directory with their respective solution files.
