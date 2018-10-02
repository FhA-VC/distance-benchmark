#
# Python script to demonstrate the usage of the CAD distance benchmark.
#
import gzip
import math
import os
import platform
import psutil # may need installation: python.exe -m pip install psutil
import sys
import time

fileA = ""
fileB = ""

if (len(sys.argv) != 2):
    print("A Benchmark for Distance Measurements")
    print("   by U. Krispel, D.W. Fellner, T. Ullrich")
    print("   presented at Cyberworlds 2018, Singapore")
    print("")
    print("USAGE:    python3 benchmark.py XXX")
    print("")
    print("XXX is the number of the test case:")
    print("         0 system test,")
    print("   1 -  13 tools test with varying number of elements,")
    print("  14 -  26 rosetta test with varying number of elements,")
    print("  27 -  39 spirit test with varying number of elements,")
    print("  40 -  52 sphere test with varying number of elements,")
    print("  53 -  65 intersection test with varying number of elements.")
    print("")
    print("Each test can be executed in different test size with increasing")
    print("number of elements (vertices or faces -- depending on the test):")
    print("  XXX+0         100 elements")
    print("  XXX+1         200 elements")
    print("  XXX+2         500 elements")
    print("  XXX+3       1.000 elements")
    print("  XXX+4       2.000 elements")
    print("  XXX+5       5.000 elements")
    print("  XXX+6      10.000 elements")
    print("  XXX+7      20.000 elements")
    print("  XXX+8      50.000 elements")
    print("  XXX+9     100.000 elements")
    print("  XXX+10    200.000 elements")
    print("  XXX+11    500.000 elements")
    print("  XXX+12  1.000.000 elements")
    print("")
    exit()
else:
    benchmarkFile = sys.argv[0]
    benchmarkDataDirectory = benchmarkFile[:-len("benchmark.py")] + "data3d" + os.sep
    benchmarkTestNumber = int(sys.argv[1])
    benchmarkTestFilesA = [ "",
        "tools_100_A.obj.gz",           "tools_200_A.obj.gz",           "tools_500_A.obj.gz", 
        "tools_1000_A.obj.gz",          "tools_2000_A.obj.gz",          "tools_5000_A.obj.gz", 
        "tools_10000_A.obj.gz",         "tools_20000_A.obj.gz",         "tools_50000_A.obj.gz",  
        "tools_100000_A.obj.gz",        "tools_100000_A.obj.gz",        "tools_100000_A.obj.gz",
        "tools_1000000_A.obj.gz",
        "rosetta_XXX_A.obj.gz",         "rosetta_XXX_A.obj.gz",         "rosetta_XXX_A.obj.gz", 
        "rosetta_XXX_A.obj.gz",         "rosetta_XXX_A.obj.gz",         "rosetta_XXX_A.obj.gz", 
        "rosetta_XXX_A.obj.gz",         "rosetta_XXX_A.obj.gz",         "rosetta_XXX_A.obj.gz", 
        "rosetta_XXX_A.obj.gz",         "rosetta_XXX_A.obj.gz",         "rosetta_XXX_A.obj.gz", 
        "rosetta_XXX_A.obj.gz", 
        "spirit_100_A.obj.gz",          "spirit_200_A.obj.gz",          "spirit_500_A.obj.gz", 
        "spirit_1000_A.obj.gz",         "spirit_2000_A.obj.gz",         "spirit_5000_A.obj.gz", 
        "spirit_10000_A.obj.gz",        "spirit_20000_A.obj.gz",        "spirit_50000_A.obj.gz",  
        "spirit_100000_A.obj.gz",       "spirit_100000_A.obj.gz",       "spirit_100000_A.obj.gz",
        "spirit_1000000_A.obj.gz",
        "sphere_100_A.obj.gz",          "sphere_200_A.obj.gz",          "sphere_500_A.obj.gz", 
        "sphere_1000_A.obj.gz",         "sphere_2000_A.obj.gz",         "sphere_5000_A.obj.gz", 
        "sphere_10000_A.obj.gz",        "sphere_20000_A.obj.gz",        "sphere_50000_A.obj.gz",  
        "sphere_100000_A.obj.gz",       "sphere_100000_A.obj.gz",       "sphere_100000_A.obj.gz",
        "sphere_1000000_A.obj.gz",
        "intersection_100_A.obj.gz",    "intersection_200_A.obj.gz",    "intersection_500_A.obj.gz", 
        "intersection_1000_A.obj.gz",   "intersection_2000_A.obj.gz",   "intersection_5000_A.obj.gz", 
        "intersection_10000_A.obj.gz",  "intersection_20000_A.obj.gz",  "intersection_50000_A.obj.gz",  
        "intersection_100000_A.obj.gz", "intersection_100000_A.obj.gz", "intersection_100000_A.obj.gz",
        "intersection_1000000_A.obj.gz"]
    fileA = benchmarkDataDirectory + benchmarkTestFilesA[benchmarkTestNumber]
    benchmarkTestFilesB = [ "",
        "tools_100_B.obj.gz",           "tools_200_B.obj.gz",           "tools_500_B.obj.gz", 
        "tools_1000_B.obj.gz",          "tools_2000_B.obj.gz",          "tools_5000_B.obj.gz", 
        "tools_10000_B.obj.gz",         "tools_20000_B.obj.gz",         "tools_50000_B.obj.gz",  
        "tools_100000_B.obj.gz",        "tools_100000_B.obj.gz",        "tools_100000_B.obj.gz",
        "tools_1000000_B.obj.gz",
        "rosetta_100_B.obj.gz",         "rosetta_200_B.obj.gz",         "rosetta_500_B.obj.gz", 
        "rosetta_1000_B.obj.gz",        "rosetta_2000_B.obj.gz",        "rosetta_5000_B.obj.gz", 
        "rosetta_10000_B.obj.gz",       "rosetta_20000_B.obj.gz",       "rosetta_50000_B.obj.gz", 
        "rosetta_100000_B.obj.gz",      "rosetta_200000_B.obj.gz",      "rosetta_500000_B.obj.gz", 
        "rosetta_1000000_B.obj.gz", 
        "spirit_100_B.obj.gz",          "spirit_200_B.obj.gz",          "spirit_500_B.obj.gz", 
        "spirit_1000_B.obj.gz",         "spirit_2000_B.obj.gz",         "spirit_5000_B.obj.gz", 
        "spirit_10000_B.obj.gz",        "spirit_20000_B.obj.gz",        "spirit_50000_B.obj.gz",  
        "spirit_100000_B.obj.gz",       "spirit_100000_B.obj.gz",       "spirit_100000_B.obj.gz",
        "spirit_1000000_B.obj.gz",
        "sphere_100_B.obj.gz",          "sphere_200_B.obj.gz",          "sphere_500_B.obj.gz", 
        "sphere_1000_B.obj.gz",         "sphere_2000_B.obj.gz",         "sphere_5000_B.obj.gz", 
        "sphere_10000_B.obj.gz",        "sphere_20000_B.obj.gz",        "sphere_50000_B.obj.gz",  
        "sphere_100000_B.obj.gz",       "sphere_100000_B.obj.gz",       "sphere_100000_B.obj.gz",
        "sphere_1000000_B.obj.gz",
        "intersection_100_B.obj.gz",    "intersection_200_B.obj.gz",    "intersection_500_B.obj.gz", 
        "intersection_1000_B.obj.gz",   "intersection_2000_B.obj.gz",   "intersection_5000_B.obj.gz", 
        "intersection_10000_B.obj.gz",  "intersection_20000_B.obj.gz",  "intersection_50000_B.obj.gz",  
        "intersection_100000_B.obj.gz", "intersection_100000_B.obj.gz", "intersection_100000_B.obj.gz",
        "intersection_1000000_B.obj.gz"]
    fileB = benchmarkDataDirectory + benchmarkTestFilesB[benchmarkTestNumber]

if (benchmarkTestNumber <= 0):
    print("TEST ")
    print("TEST cpus             :", psutil.cpu_count(logical=True), psutil.cpu_count(logical=False))
    print("TEST memory       [MB]:", psutil.virtual_memory().total // 1024 // 1024)
    print("TEST platform         :", platform.platform())
    print("TEST system           :", platform.system())
    print("TEST node             :", platform.node())
    print("TEST release          :", platform.release())
    print("TEST machine          :", platform.machine())
    print("TEST python compiler  :", platform.python_compiler())
    print("TEST python build     :", platform.python_build())
    print("TEST ")
    exit()
#
# load obj files
#
def loadOBJ(filename):
    coordinates   = []
    faceIndices  = []
    #
    for line in gzip.open(filename, 'r'):
        if line.startswith(b'v '):
            # a vertex
            tokens = line.split()
            coordinates.append(float(tokens[1]))
            coordinates.append(float(tokens[2]))
            coordinates.append(float(tokens[3]))
        elif line.startswith(b'f '):
            # a face
            tokens = line.split()
            for i in range(4, len(tokens)+1):
                positionA = int(tokens[1])
                positionB = int(tokens[i-2])
                positionC = int(tokens[i-1])
                # insert positions
                if (positionA < 0):
                    faceIndices.append(int(len(coordinates)) // 3 + positionA)
                else:
                    faceIndices.append(positionA - 1)
                #
                if (positionB < 0):
                    faceIndices.append(int(len(coordinates)) // 3 + positionB)
                else:
                    faceIndices.append(positionB - 1)
                #
                if (positionC < 0):
                    faceIndices.append(int(len(coordinates)) // 3 + positionC)
                else:
                    faceIndices.append(positionC - 1)
        else:
            # skip
            pass
    return (coordinates, faceIndices)
#
print("")
print("loading test set {0}".format(fileA))
(coordsA, indicesA) = loadOBJ(fileA)
print("   with {0} vertices, {1} triangles".format(len(coordsA) // 3, len(indicesA) // 3))

print("")
print("loading test set {0}".format(fileB))
(coordsB, indicesB) = loadOBJ(fileB)
print("   with {0} vertices, {1} triangles".format(len(coordsB) // 3, len(indicesB) // 3))
#
# Simple distance calculation between two triangles defined
# by three points each, and three coordinates per point:
#
def distanceTriangle2Triangle(
    p0x, p0y, p0z, p1x, p1y, p1z, p2x, p2y, p2z, 
    q0x, q0y, q0z, q1x, q1y, q1z, q2x, q2y, q2z):
    #
    # WARNING! WARNING! WARNING! WARNING! WARNING! WARNING! WARNING! WARNING!
    #
    # Do not use this routine in real, production environments!
    # 
    # This is not a real implementation of a triangle-to-triangle distance
    # test; this is a simple, inaccurate brute-force variant reducing the
    # triangle-to-triangle test to many (!) point-to-point tests.
    #
    # WARNING! WARNING! WARNING! WARNING! WARNING! WARNING! WARNING! WARNING!
    #
    ps = [ ]
    qs = [ ]
    sampling = 10;
    for i in range(0, sampling+1):
        for j in range (0, sampling+1-i):
            u = i / sampling
            v = j / sampling
            w = (sampling - i - j) / sampling
            ps.append([
                u * p0x + v * p1x + w * p2x,
                u * p0y + v * p1y + w * p2y,
                u * p0z + v * p1z + w * p2z])
            qs.append([
                u * q0x + v * q1x + w * q2x,
                u * q0y + v * q1y + w * q2y,
                u * q0z + v * q1z + w * q2z])
    #
    minimum = float("inf")
    for p in ps:
        for q in qs:
            dx = p[0] - q[0]
            dy = p[1] - q[1]
            dz = p[2] - q[2]
            d = math.sqrt(dx*dx + dy*dy + dz*dz)
    # 
    if (d < minimum):
        minimum = d
    #
    return d

#
# Naive distance measurement
#
timingBeforeDistanceTest = time.perf_counter()
currentDistance = float("inf")
currentDistancePairs = [ ]
#
for i in range(0, len(indicesA) // 3):
    # indices of a triangle in test model A
    indexA0 = indicesA[3*i+0]
    indexA1 = indicesA[3*i+1]
    indexA2 = indicesA[3*i+2]
    # corresponding coordinates
    p0x = coordsA[3*indexA0+0]
    p0y = coordsA[3*indexA0+1]
    p0z = coordsA[3*indexA0+2]
    p1x = coordsA[3*indexA1+0]
    p1y = coordsA[3*indexA1+1]
    p1z = coordsA[3*indexA1+2]
    p2x = coordsA[3*indexA2+0]
    p2y = coordsA[3*indexA2+1]
    p2z = coordsA[3*indexA2+2]
    #
    for j in range(0, len(indicesB) // 3):
        # indices of a triangle in test model B
        indexB0 = indicesB[3*j+0]
        indexB1 = indicesB[3*j+1]
        indexB2 = indicesB[3*j+2]
        # corresponding coordinates
        q0x = coordsB[3*indexB0+0]
        q0y = coordsB[3*indexB0+1]
        q0z = coordsB[3*indexB0+2]
        q1x = coordsB[3*indexB1+0]
        q1y = coordsB[3*indexB1+1]
        q1z = coordsB[3*indexB1+2]
        q2x = coordsB[3*indexB2+0]
        q2y = coordsB[3*indexB2+1]
        q2z = coordsB[3*indexB2+2]
        # the i-j-distance test
        # print("test {0},{1},{2} - {3},{4},{5}".format(
        #    indexA0, indexA1, indexA2, 
        #    indexB0, indexB1, indexB2))
        distance = distanceTriangle2Triangle(
            p0x, p0y, p0z, p1x, p1y, p1z, p2x, p2y, p2z, 
            q0x, q0y, q0z, q1x, q1y, q1z, q2x, q2y, q2z)
        # update distance
        if (distance < currentDistance):
            currentDistance = distance
            currentDistancePairs = [ ]
        # store pair of indices
        if (distance == currentDistance):
            currentDistancePairs.append( (i, j) )
    # print progress
    print("{0} of {1}".format(i+1,  len(indicesA) // 3))        

timingAfterDistanceTest = time.perf_counter()

#
# list all pairs?
#
print(currentDistancePairs)

#
# print test results
#
print("TEST #{0} ; time={1}s ; distance={2} ; pairs={3}".format(
    benchmarkTestNumber,                                                                 
    timingAfterDistanceTest - timingBeforeDistanceTest,
    currentDistance,
    len(currentDistancePairs)))
exit()