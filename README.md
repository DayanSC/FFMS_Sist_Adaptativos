# FFMSP

This repository contains the implementation of the Far From Most String Problem (FFMSP) using various algorithms. The project includes both C++ and Python implementations.

## Repository Structure

```plain
datasets/
    100-300-001.txt
    100-300-002.txt
    ...
src-cpp/
    ffms-mh.cpp
    ...
src-python/
    FFMS-greedy.py
    FFMSP-mh.py
    ...
testing/
    test-instances.py
```

## Directories

- datasets: Contains the dataset files used for testing the algorithms. Each file represents a different problem instance.
- src-cpp: Contains the C++ source code for the FFMSP problem.
- src-python: Contains the Python source code for the FFMSP problem.
- testing: Contains scripts for testing the implementations.

## Files

- FFMSP_mh.cpp: C++ implementation of the FFMSP problem using a metaheuristic approach.
- FFMSP-greedy.py: Python implementation of the greedy algorithm for the FFMSP problem.
- FFMSP-mh.py: Python implementation of the metaheuristic approach for the FFMSP problem.
- FFMSP-ag.py: Python implementation of the genetic algorithm for the FFMSP problem.
- FFMSP-aco.py: Python implementation of the ant colony optimization algorithm for the FFMSP problem.
- test-instances.py: Script to test different instances of the problem using the provided datasets.

## Getting Started

### Prerequisites

- C++ compiler (e.g., g++)
- Python 3
- NumPy

### Building the C++ Project

To build the C++ project, run the following command:

```bash
g++ -o ffms-mh src-cpp/ffms-mh.cpp
```

### Running the Executable

```bash
./ffms-mh -i <dataset_file> -t <time> -th <threshold> -dr <determinism-rate>
```

### Running the Python Scripts

To run the Python scripts, use the following command:

```bash
python src-python/<*.py>
```
**Note:** The Python scripts require datasets to be in the same directory.

