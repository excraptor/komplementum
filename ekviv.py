# gyartani egy komplementumot

# megszamolni hany osztalya van

# megnezni az osszes tobbi ennyi osztalyu elemet, es kiprobalgatni, hogy melyikek komplementumok

# megnezni van e mas komplementum

# calculate every possible partition of a list recursively
import imp
from os import remove
from lattice import metszet, egyesites

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
    return len(metszet(elem1, elem2)) == 4 and len(egyesites(elem1, elem2)) == 1

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

A = [1,2,3,4]
partitionsList = list(partition(A))
partitions = []
for e in partitionsList:
    s = set()
    for fs in e:
        s.add(frozenset(fs))
    partitions.append(s)
print(partitions[3])
counter = 0
for i in partitions:
    if(i != partitions[3]):
        asd = isKomplementum(partitions[3], i)
        print(f"{toString(i)}: {asd}")
        if(asd):
            counter += 1
print(f"complements: {counter}")




















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