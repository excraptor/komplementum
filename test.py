import functools
import ekviv as eq
from scipy.interpolate import lagrange
import matplotlib.pyplot as plt
import numpy as np

def generatePartitions(fromList):
    partitionsList = list(eq.partition(fromList))
    partitions = []
    for e in partitionsList:
        s = set()
        for fs in e:
            s.add(frozenset(fs))
        partitions.append(s)
    return partitions

def sortPartitions(partitionsToSort):
    partitionsSorted = sorted(partitionsToSort, key=functools.cmp_to_key(eq.compareEquivs))
    partitions = [sorted(c, key=functools.cmp_to_key(eq.compareEquivs)) for c in partitionsSorted]
    return partitions

def interpolationDataPoints():
    A = [1,2,3,4,5,6,7,8,9,10,11,12]
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    types = eq.getTypes(partitions)
    representants = eq.getRepresentants(types, partitions)
    numOfComplements = dict()
    # print(f"representants: {representants}")
    for r in representants:
        #print(f"r: {r}")
        complements = eq.getComplements(partitions=partitions, c=r)
        numOfComplements[eq.toString(r)] = len(complements)
    
    sortedRes = dict(sorted(numOfComplements.items(), key=lambda item: item[1]))
    return eq.prettyDict(sortedRes)

def whyIsItOdd():
    A = [1,2,3,4,5,6]
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    types = eq.getTypes(partitions)
    representants = eq.getRepresentants(types, partitions)
    return eq.getComplements(partitions=partitions, c=representants[3])

def testCubicSpline(x,y):
    cs = lagrange(x,y)
    print(cs)
    print(f"8: {cs(8)}, 9: {cs(9)}, 10: {cs(10)}")

def testMax(repr, A):
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    complements = eq.getComplements(partitions, repr)
    print(complements)

def main():
    numOfComplements = interpolationDataPoints()
    print(numOfComplements)
    # testMax([frozenset({3, 4}), frozenset({5, 6}), frozenset({1, 2})], [1,2,3,4,5,6])
    # print("####")
    # odd = whyIsItOdd()
    # print(odd)
    # print(len(odd))
    # testCubicSpline([3,4,5,6,7,8,9], [2,6,16,68,232,1240,5136])

if __name__ == "__main__":
    main()