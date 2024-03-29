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

def numOfComplements(A):
    # A = [1,2,3,4,5,6,7,8]
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    types = eq.getTypes(partitions)
    representants = eq.getRepresentants(types, partitions)
    numOfComplements = dict()
    # print(f"representants: {representants}")
    for r in representants:
        # print(f"r: {r}")
        complements = eq.getComplements(partitions=partitions, c=r)
        numOfComplements[eq.toString(r)] = len(complements)
    
    sortedRes = dict(sorted(numOfComplements.items(), key=lambda item: item[1]))
    return sortedRes
    # return eq.prettyDict(sortedRes)

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

def getComplementsOf(c):
    size = functools.reduce(lambda x,y: x+y, [len(x) for x in c])
    A = [i for i in range(1,size+1)]
    partitionsUnsorted = generatePartitions(fromList = A)
    partitions = sortPartitions(partitionsUnsorted)
    return eq.getComplements(partitions, c)
    # print([eq.toString(x) for x in complements])
    # return [eq.toString(x) for x in complements]

def classToFrozenset(c):
    return frozenset(map(lambda x: frozenset(map(lambda i: int(i), x.split(","))), c.split("|")))

def test1():
    """this proof is not working sadly"""
    c1 = getComplementsOf(classToFrozenset("1|2,3,4,5,6,7"))
    c2 = getComplementsOf(classToFrozenset("1|2|3,4,5,6,7"))
    c3 = getComplementsOf(classToFrozenset("1,2|3,4,5,6,7"))
    c4 = getComplementsOf(classToFrozenset("1,2|3|4,5,6,7"))
    c5 = getComplementsOf(classToFrozenset("1,2|3|4|5,6,7"))
    c6 = getComplementsOf(classToFrozenset("1,2|3,4|5,6,7"))
    c7 = getComplementsOf(classToFrozenset("1,2|3|4|5|6,7"))

    print(len(set(c1) & set(c2)) == len(c1))
    print(len(set(c2) & set(c3)) == len(c2))
    print(len(set(c3) & set(c4)) == len(c3))
    print(len(set(c4) & set(c5)) == len(c4))
    print(len(set(c5) & set(c6)) == len(c5))
    print(len(set(c6) & set(c7)) == len(c6))

    with open("feldarabolos_osszevonos.txt", "w") as f:
        c = getComplementsOf(classToFrozenset("1|2,3,4,5,6,7"))
        f.write(f"elem: 1|2,3,4,5,6,7 komplementumai:")
        for cc in c:
            f.write(f"{cc}\n")
        c = getComplementsOf(classToFrozenset("1|2|3,4,5,6,7"))
        f.write(f"elem: 1|2|3,4,5,6,7 komplementumai:")
        for cc in c:
            f.write(f"{cc}\n")
        c = getComplementsOf(classToFrozenset("1,2|3,4,5,6,7"))
        f.write(f"elem: 1,2|3,4,5,6,7 komplementumai:")
        for cc in c:
            f.write(f"{cc}\n")
        c = getComplementsOf(classToFrozenset("1,2|3|4,5,6,7"))
        f.write(f"elem: 1,2|3|4,5,6,7 komplementumai:")
        for cc in c:
            f.write(f"{cc}\n")
        c = getComplementsOf(classToFrozenset("1,2|3|4|5,6,7"))
        f.write(f"elem: 1,2|3|4|5,6,7 komplementumai:")
        for cc in c:
            f.write(f"{cc}\n")
        c = getComplementsOf(classToFrozenset("1,2|3,4|5,6,7"))
        f.write(f"elem: 1,2|3,4|5,6,7 komplementumai:")
        for cc in c:
            f.write(f"{cc}\n")
        c = getComplementsOf(classToFrozenset("1,2|3,4|5|6,7"))
        f.write(f"elem: 1,2|3,4|5|6,7 komplementumai:")
        for cc in c:
            f.write(f"{cc}\n")

def testMatrices():
    a = eq.adjacencyMatrixFromClasses(classToFrozenset("1,2|3,4|5"))
    for r in a:
        print(r)

def writeMatrix(f, m):
    for r in m:
        for c in r:
            f.write(f"{c} ")
        f.write("\n")
    f.write("\n")

def test2():
    c1 = getComplementsOf(classToFrozenset("1|2,3,4,5,6,7"))
    c2 = getComplementsOf(classToFrozenset("1|2|3,4,5,6,7"))
    c7 = getComplementsOf(classToFrozenset("1,2|3,4|5,6|7"))

    with open("feldarabolos_matrixokkal.txt", "w") as f:
        c1_A = eq.adjacencyMatrixFromClasses(classToFrozenset("1|2,3,4,5,6,7"))
        writeMatrix(f, c1_A)
        
        for cc in c1:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)
        
        f.write("#########################################")
        c2_A = eq.adjacencyMatrixFromClasses(classToFrozenset("1|2|3,4,5,6,7"))
        writeMatrix(f, c2_A)

        for cc in c2:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)
        
        f.write("#########################################")
        c7_A = eq.adjacencyMatrixFromClasses(classToFrozenset("1,2|3,4|5,6|7"))
        writeMatrix(f, c7_A)

        for cc in c7:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)

def test4():
    e1 = "1|2,3,4"
    e2 = "1|2|3,4"
    e3 = "1,2|3,4"
    c1 = getComplementsOf(classToFrozenset(e1))
    c2 = getComplementsOf(classToFrozenset(e2))
    c3 = getComplementsOf(classToFrozenset(e3))

    with open("feldarabolos_matrixokkal.txt", "w") as f:
        c1_A = eq.adjacencyMatrixFromClasses(classToFrozenset(e1))
        writeMatrix(f, c1_A)
        
        for cc in c1:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)
        
        f.write("#########################################")
        c2_A = eq.adjacencyMatrixFromClasses(classToFrozenset(e2))
        writeMatrix(f, c2_A)

        for cc in c2:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)
        
        f.write("#########################################")
        c7_A = eq.adjacencyMatrixFromClasses(classToFrozenset(e3))
        writeMatrix(f, c7_A)

        for cc in c3:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)

def test5():
    e1 = "1|2,3,4,5"
    e2 = "1|2|3,4,5"
    e3 = "1,2|3,4,5"
    e4 = "1|2,3|4,5"
    c1 = getComplementsOf(classToFrozenset(e1))
    c2 = getComplementsOf(classToFrozenset(e2))
    c3 = getComplementsOf(classToFrozenset(e3))
    c4 = getComplementsOf(classToFrozenset(e4))

    with open("feldarabolos_matrixokkal.txt", "w") as f:
        c1_A = eq.adjacencyMatrixFromClasses(classToFrozenset(e1))
        writeMatrix(f, c1_A)
        
        for cc in c1:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)
        
        f.write("#########################################\n")
        c2_A = eq.adjacencyMatrixFromClasses(classToFrozenset(e2))
        writeMatrix(f, c2_A)

        for cc in c2:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)
        
        f.write("#########################################\n")
        c7_A = eq.adjacencyMatrixFromClasses(classToFrozenset(e3))
        writeMatrix(f, c7_A)

        for cc in c3:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)

        f.write("#########################################\n")
        c7_A = eq.adjacencyMatrixFromClasses(classToFrozenset(e4))
        writeMatrix(f, c7_A)

        for cc in c4:
            a = eq.adjacencyMatrixFromClasses(cc)
            f.write(f"{cc}\n")
            writeMatrix(f, a)

def test5WithClasses():
    
    e1 = "1|2|3,4,5"
    e2 = "1|2|3|4,5"

    c1 = getComplementsOf(classToFrozenset(e1))
    c2 = getComplementsOf(classToFrozenset(e2))

    with open("feldarabolos_levagos_5.txt", "w") as f:
        f.write(f"{eq.toString(classToFrozenset(e1))}\n\n")
        
        for cc in c1:
            f.write(f"{eq.toString(cc)}\n")
        
        f.write("\n#########################################\n")

        f.write(f"{eq.toString(classToFrozenset(e2))}\n\n")

        for cc in c2:
            f.write(f"{eq.toString(cc)}\n")
        
def pretty(c):
    s = c.replace("}{", " | ").replace("{{", "").replace("}}", "")
    return s

def latexNumOfComplements():
    A = [1,2]
    s = "\\begin{center}\n"
    for i in range(3, 7):
        s += "\\begin{tabular}{ |c|c| }\n"
        A.append(i)
        num = numOfComplements(A)
        for k, v in num.items():
            if v != 1:
                s += "\\hline\n"
                s += f"{pretty(k)} & {v} \\\\\n"
        s += "\\hline\n\\end{tabular}\n"
    s += "\\end{center}\n"
    return s

def onesWithBig(e):
    c2 = getComplementsOf(classToFrozenset(e))
    for c in c2:
        print(f"{pretty(eq.toString(c))} \\\\")

def numOfComplementsPaperTest(pi, n):
    m = len(pi)
    print(f"m: {m}")
    prod = 1
    for c in pi:
        prod *= len(c) 
    return prod * (n-m+1)**(m-2)

def main():
    e = "1|2,3|4,5"
    # asd = numOfComplementsPaperTest(classToFrozenset(e), 6)
    asd = getComplementsOf(classToFrozenset(e))
    with open('complements.txt', 'a') as f:
        for c in asd:
            f.write(f"{pretty(eq.toString(c))}\n")
    # onesWithBig(e)
    # # A = [1,2,3,4,5]
    # # partitionsUnsorted = generatePartitions(fromList = A)
    # # partitions = sortPartitions(partitionsUnsorted)
    # # types = eq.getTypes(partitions)
    # # representants = eq.getRepresentants(types, partitions)
    # # for asd in [pretty(eq.toString(x)) for x in representants]:
    # #     print(asd)
    # with open("numOfComplementsLatex.txt", "w") as f:
    #     s = latexNumOfComplements()
    #     f.write(s)
    # test5WithClasses()
    # getComplementsOf(classToFrozenset("1|2,3,4"))
    # r = [frozenset({1, 2, 3}), frozenset({4, 5, 6}), frozenset({7, 8})]
    # rr = [frozenset({1, 2}), frozenset({3}), frozenset({4, 5}), frozenset({6}), frozenset({7, 8})]
    # res = feldarabolosKicsi(r, rr, n = 8)
    # print(res)
    # num = numOfComplements([1,2,3,4])
    # print(num)
    # testMax([frozenset({3, 4}), frozenset({5, 6}), frozenset({1, 2})], [1,2,3,4,5,6])
    # print("####")
    # odd = whyIsItOdd()
    # print(odd)
    # print(len(odd))
    # testCubicSpline([3,4,5,6,7,8,9], [2,6,16,68,232,1240,5136])

if __name__ == "__main__":
    main()