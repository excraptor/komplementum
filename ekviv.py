# gyartani egy komplementumot

# megszamolni hany osztalya van

# megnezni az osszes tobbi ennyi osztalyu elemet, es kiprobalgatni, hogy melyikek komplementumok

# megnezni van e mas komplementum

# calculate every possible partition of a list recursively

from codecs import getreader
import functools

from matplotlib.pyplot import get
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


def komplementum1(osztalyozas):
    # vegigmegyunk az osszes osztalyon
    # mindegyikbol csinalunk ilyen parokat, hogy hozzaveszunk a kovi osztalybol egy elemet
    ret = []
    for t in range(len(osztalyozas)-1):
        kapcsolo = [osztalyozas[t][-1], osztalyozas[t+1][0]]
        ret.append(kapcsolo) 
    
    # nem jo: lehet olyan is hogy tobb osztaly olvad egybe
    # minden olyan osztalyt ossze kell olvasztani, amiben van ugyanolyan elem
    for i,k in enumerate(ret):
        if(i+1 < len(ret) and k[-1] == ret[i+1][0]):
            ret.append(list({*ret[i], *ret[i+1]}))
            ret.pop(i+1)
            ret.pop(i)
    

    for a in A:
        found = False
        for c in ret:
            if(a in c):
                found = True
        if(not found):
            ret.append([a])
    return ret


def maxEgyMetszet(elem, komplementumCandidate):
    for c in komplementumCandidate:
        for osztaly in elem:
            if(len(set(c).intersection(set(osztaly))) > 1):
                return False
    return True

def isKomplementum(elem1, elem2):
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

def show(partitions, isForTypes=False):
    net = Network('2000px', '2000px')
    net.toggle_physics(False)
    net.add_nodes([toString(x) for x in partitions])

    edges = []
    for p in partitions:
        for q in partitions:
            if(p != q):
                # print(f"p: {toString(p)}\nq: {toString(q)}")
                if(isForTypes):
                    if(lessForTypes(p, q)):
                        edges.append((toString(p), toString(q)))
                else:
                    if(kisebb(p, q, numberOfElements)):
                        edges.append((toString(p), toString(q)))

    for e in edges:
        net.add_edge(e[0], e[1])    

    # print(f"p1: {partitions[2]}\np2: {partitions[4]}")
    # print(kisebb(partitions[2], partitions[4], numberOfElements))

    net.show('ekviv.html')

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
    

def calculateTypes(partitions):
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

# join = egyesites(E, F)
# print(toClasses(join))


def compareEquivs(e, f):
    return len(e) - len(f)

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
types = calculateTypes(getComplements(partitions, E)).keys()
representants = getRepresentants(types, partitions)
print(types)
print(f"type: {getTypeOfPartition(E)}")
show(representants, True)


# for x in partition(A):
#     partitions.append([set(c) for c in x])
# print(partitions)
# print("######")
# elem = [x for x in partitions if len(x) == 2][0]
# k = komplementum(elem)
# print(f"osztalyozas: {elem}")
# print(f"egy komplementum: {k}")
# komplementumCandidates = [x for x in partitions if len(x) == len(k)]
# print(f"lehetseges komplementumok: {komplementumCandidates}")

# candidates = []
# for candidate in komplementumCandidates:
#     if(maxEgyMetszet(elem, candidate)):
#         candidates.append(candidate)

# print(f"ezek kozul amire igaz a feltetel: {candidates}")

