from audioop import maxpp
import enum
import functools
import ekviv as eq
import fordfulkerson as ff

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
    A = [1,2,3,4,5,6,7,8]
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    types = eq.getTypes(partitions)
    representants = eq.getRepresentants(types, partitions)
    numOfComplements = dict()
    # print(f"representants: {representants}")
    for r in representants:
        print(f"r: {r}")
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

def testMax(repr, A):
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    complements = eq.getComplements(partitions, repr)
    print(complements)

def feldarabolos():
    A = [1,2,3,4,5,6,7,8]
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    # types = eq.getTypes(partitions)
    # representants = eq.getRepresentants(types, partitions)
    r = [frozenset({1, 2, 3}), frozenset({4, 5, 6}), frozenset({7, 8})]
    s = eq.getComplements(partitions, r)
    rr = [frozenset({1, 2}), frozenset({3}), frozenset({4, 5}), frozenset({6}), frozenset({7, 8})]
    ss = eq.getComplements(partitions, rr)

    # ssDict = dict.fromkeys(ss, False)
    with open("feldarabolos.txt", "w") as f:
        for c in s:
            f.write(f"{c}-et tartalmazo s'-k:\n")
            for cc in ss:
                if eq.contains(cc, c):
                    f.write(f"{cc}\n")
                    ss.remove(cc)
            f.write("\n")
            
        f.write(f"maradek: {len(ss)}\n")
        for k in ss:
            f.write(f"{k}\n")

    return len(s) - len(ss)

def feldarabolosKicsi(r, rr, n):
    A = [i for i in range(1, n+1)]
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    # types = eq.getTypes(partitions)
    # representants = eq.getRepresentants(types, partitions)
    s = eq.getComplements(partitions, r)
    ss = eq.getComplements(partitions, rr)

    d = dict()
    for c in s:
        for cc in ss:
            if eq.contains(cc, c):
                if(eq.toString(c) in d.keys()):
                    d[eq.toString(c)].append(eq.toString(cc))
                else:
                    d[eq.toString(c)] = []
    
    maxPairing([eq.toString(c) for c in s], [eq.toString(c) for c in ss], d)

    # ssDict = dict.fromkeys(ss, False)
    with open("feldarabolos.txt", "w") as f:
        for c in s:
            f.write(f"{c}-et tartalmazo s'-k:\n")
            for cc in ss:
                if eq.contains(cc, c):
                    f.write(f"{cc}\n")
                    ss.remove(cc)
            f.write("\n")
            
        f.write(f"maradek: {len(ss)}\n")
        for k in ss:
            f.write(f"{k}\n")

    return len(s) - len(ss)

# kellenek az eredeti komplementumai, a feldarabolté, plusz az "élek", ami egy dict most
def maxPairing(rowData, colData, d):
    graph = [[0 for _ in range(len(colData))] for _ in range(len(rowData))]
    
    # vegigmegyunk az osszes eredeti komplementumon
    for i, c in enumerate(rowData):
        # megnezzuk az ehhez tartozokat
        for cc in d[c]:
            # kivalasztjuk, hogy hanyadik ez, oda kell egy egyes
            j = colData.index(cc)
            graph[i][j] = 1
    
    g = ff.GFG(graph)
    result, matchings = g.maxBPM()
    print ("Maximum number of applicants that can get job is %d " % result)
    with open("feldarabolos_pairing.txt", "w") as f:
        kimaradt = []
        kiiratott = dict.fromkeys(rowData, False)
        for ccIDX, cIDX in enumerate(matchings):
            if(cIDX != -1):
                f.write(f"{rowData[cIDX]} parja:\n{colData[ccIDX]}\n\n")
                kiiratott[rowData[cIDX]] = True
            else:
                kimaradt.append(colData[ccIDX])
        f.write("kimaradt:\n")
        for k in kimaradt:
            f.write(f"{k}\n")
        f.write("nem lett parja:\n")
        for (k, v) in kiiratott.items():
            if(not v):
                f.write(f"{k}\n")



def main():
    r = [frozenset({1, 2, 3}), frozenset({4, 5, 6}), frozenset({7, 8})]
    rr = [frozenset({1, 2}), frozenset({3}), frozenset({4, 5}), frozenset({6}), frozenset({7, 8})]
    res = feldarabolosKicsi(r, rr, n = 8)
    print(res)
    # numOfComplements = interpolationDataPoints()
    # print(numOfComplements)
    # testMax([frozenset({3, 4}), frozenset({5, 6}), frozenset({1, 2})], [1,2,3,4,5,6])
    # print("####")
    # odd = whyIsItOdd()
    # print(odd)
    # print(len(odd))
    # testCubicSpline([3,4,5,6,7,8,9], [2,6,16,68,232,1240,5136])

if __name__ == "__main__":
    main()