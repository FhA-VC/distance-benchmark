# A Benchmark for Distance Measurements

by U. Krispel, D.W. Fellner, T. Ullrich

presented at Cyberworlds 2018, Singapore

## Abstract 

The need to analyze and visualize distances bet-
ween objects arises in many use cases. Although the problem
to calculate the distance between two polygonal objects may
sound simple, real-world scenarios with large models will always
be challenging, but optimization techniques – such as space
partitioning – can reduce the complexity of the average case
significantly.
Our contribution to this problem is a publicly available bench-
mark to compare distance calculation algorithms.

## Contents

This repository contains the test cases described in the paper in the 
"data3d" subdirectory. Each test object is in gzipped Wavefront .OBJ format.
It contains the test cases "Tools", "Rosetta", "Spirit", "Sphere" and
"Intersection" with sizes of 100, 200, 500, 1k, 2k, 5k, 10k, 20k, 50k, 100k, 
200k, 500k and 1M triangles.

## Running

This rpository also provides an exemplaric distance calculation script written
in python that demontrates the benchmark use. 
Please note that this implementation is not intended to be used in production 
environments, as it naively evaluates the distance of all triangle-triangle 
pairs of the test objects. Furthermore, the distanceTriangle2Triangle method
is a simple, inaccurate brute-force variant.

Prerequisites: Python 3, "psutil" package, install with 
```python -m pip install psutil``` if necessary

run the demo application with
```python benchmark.py```

    USAGE:    python3 benchmark.py XXX

    XXX is the number of the test case:
             0 system test,
       1 -  13 tools test with varying number of elements,
      14 -  26 rosetta test with varying number of elements,
      27 -  39 spirit test with varying number of elements,
      40 -  52 sphere test with varying number of elements,
      53 -  65 intersection test with varying number of elements.

    Each test can be executed in different test size with increasing
    number of elements (vertices or faces -- depending on the test):
      XXX+0         100 elements
      XXX+1         200 elements
      XXX+2         500 elements
      XXX+3       1.000 elements
      XXX+4       2.000 elements
      XXX+5       5.000 elements
      XXX+6      10.000 elements
      XXX+7      20.000 elements
      XXX+8      50.000 elements
      XXX+9     100.000 elements
      XXX+10    200.000 elements
      XXX+11    500.000 elements
      XXX+12  1.000.000 elements
