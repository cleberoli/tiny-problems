# Project Documentation

This project implements the ideas presented in the **Exact Algorithms for Small-Scale 
Combinatorial Optimization Problems** paper which is still an ongoing project.
This brief documentations describes the specifications, architecture and quality tests.

Note that since the system has no interface the user should directly interact with the code provided.
Therefore, this documentation along with the one found on the `README` file in the root 
directory such suffice as user manual.

## Specification

The goal of this project is to design small decision trees to solve small instances
of well-known classical problems, based on the geometric characteristics of these polytopes.
In order to accomplish this goal our system has six main use cases shown in the figure below.

![Use case diagram](https://github.com/cleberoli/tiny-problems/blob/develop/docs/uml/use-cases.jpg?raw=true)

The user is responsible for performing all use cases as it is specified.

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