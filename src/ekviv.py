# gyartani egy komplementumot

# megszamolni hany osztalya van

# megnezni az osszes tobbi ennyi osztalyu elemet, es kiprobalgatni, hogy melyikek komplementumok

# megnezni van e mas komplementum

# calculate every possible partition of a list recursively

from codecs import getreader
import functools

from lattice import lessForTypes, metszet, egyesites, kisebb, toClasses, toRelations
from pyvis.network import Network


def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller


def maxEgyMetszet(elem, komplementumCandidate):
    for c in komplementumCandidate:
        for osztaly in elem:
            if(len(set(c).intersection(set(osztaly))) > 1):
                return False
    return True

def isKomplementum(elem1, elem2):
    # print(f"elem1: {elem1}")
    # print(f"elem1.1: {elem1[0]}")
    numberOfElements = functools.reduce(lambda x,y: x+y, list(map(lambda x: len(x), elem1)))
    return len(metszet(elem1, elem2)) == numberOfElements and len(egyesites(elem1, elem2)) == 1

def toString(fs: frozenset):
    s = "{"
    for fs2 in fs:
        s+="{"
        for idx, e in enumerate(fs2):
            if(idx != len(fs2)-1):
                s+=str(e)+", "
            else:
                s+=str(e)
        s+="}"
    s+="}"
    return s

def adjacencyMatrixFromClasses(c):
    n = functools.reduce(lambda x,y: x+y, list(map(lambda x: len(x), c)))
    a = [[0 for _ in range(n)] for _ in range(n)]
    for cc in c:
        for i in cc:
            for j in cc:
                a[i-1][j-1] = 1 # because matrix rows are from 0 to n-1
    return a

        

# def show(partitions, isForTypes=False):
#     net = Network('2000px', '2000px')
#     net.toggle_physics(False)
#     net.add_nodes([toString(x) for x in partitions])

#     edges = []
#     for p in partitions:
#         for q in partitions:
#             if(p != q):
#                 # print(f"p: {toString(p)}\nq: {toString(q)}")
#                 if(isForTypes):
#                     if(lessForTypes(p, q)):
#                         edges.append((toString(p), toString(q)))
#                 else:
#                     if(kisebb(p, q, numberOfElements)):
#                         edges.append((toString(p), toString(q)))

#     for e in edges:
#         net.add_edge(e[0], e[1])    

#     # print(f"p1: {partitions[2]}\np2: {partitions[4]}")
#     # print(kisebb(partitions[2], partitions[4], numberOfElements))

#     net.show('ekviv.html')

def isSameType(a, b):
    """
    assuming its sorted
    """
    return getTypeOfPartition(a) == getTypeOfPartition(b)
    

def getTypeOfPartition(partition):
    """
    assuming its sorted
    """
    res = ""
    for c in partition:
        res += str(len(c)) + "+"
    return res[:-1]
    

def getTypes(partitions):
    res = dict()
    for eq in partitions:
        eqType = getTypeOfPartition(eq)
        if(eqType in res.keys()):
            res[eqType] += 1
        else:
            res[eqType] = 1
    return res

def getComplements(partitions, c):
    """
    assuming partitions are sorted
    """
    res = []
    for p in partitions:
        if(p != c):
            if(isKomplementum(c, p)):
                res.append(p)
    return res

def getRepresentants(types, partitions):
    res = []
    for t in types:
        for p in partitions:
            if(getTypeOfPartition(p) == t):
                res.append(p)
                break
    return res

def compareEquivs(e, f):
        return len(e) - len(f)

def prettyDict(dict: dict):
    res = "{\n\t"
    for (key, value) in dict.items():
        res += str(key) + ": " + str(value) + "\n\t"
    return res + "\n}"

def contains(eq1, eq2):
    if(equals(metszet(eq1, eq2), eq2)):
        return True
    return False

def equals(eq1, eq2):
    for c in eq1:
        if c not in eq2:
            return False
    return True

def _stuff():
    A = [1,2,3,4,5,6,7,8]
    numberOfElements = len(A)
    partitionsList = list(partition(A))
    partitions = []
    for e in partitionsList:
        s = set()
        for fs in e:
            s.add(frozenset(fs))
        partitions.append(s)
    # E = partitions[53]
    # F = partitions[4]
    E = partitions[80]
    print(E)

    counter = 0
    with open("results.txt", "w") as f:
        f.write(f"{E}\n")
        partitionsSorted = sorted(partitions, key=functools.cmp_to_key(compareEquivs))
        for i in [sorted(c, key=functools.cmp_to_key(compareEquivs)) for c in partitionsSorted]:
            if(i != E):
                asd = isKomplementum(E, i)
                if(asd):
                    #f.write(f"{toString(i)}: {asd}\n")
                    f.write(f"{[sorted(c) for c in i]}\n")
                if(asd):
                    counter += 1
        f.write(f"complements: {counter}\n")

    print([sorted(c) for c in E])
    partitionsSorted = sorted(partitions, key=functools.cmp_to_key(compareEquivs))
    partitions = [sorted(c, key=functools.cmp_to_key(compareEquivs)) for c in partitionsSorted]
    types = getTypes(getComplements(partitions, E)).keys()
    representants = getRepresentants(types, partitions)
    print(types)
    print(f"type: {getTypeOfPartition(E)}")
    # show(representants, True)

