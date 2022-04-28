def metszet(elem1, elem2):
    res = set()
    for s1 in elem1:
        for s2 in elem2:
            res.add(s1.intersection(s2))
    res.discard(frozenset())
    return frozenset(res)

def egyesites1(elem1, elem2, numOfElements = -1):
    res = elem1.union(elem2)
    print(f"res: {res}")
    if(numOfElements == len(elem1)):
        return elem2
    elif(numOfElements == len(elem2)):
        return elem1
    while True:
        current = set()
        for s1 in res:
            for s2 in res:
                if(s1 != s2):
                    current.add(s1.union(s2))
                    # print(f"union: {s1.union(s2)}")
        if(current == res):
            break
        if(current == set()):
            break
        #print(f"current: {current}")
        res = current

    res.discard(frozenset())
    return res

# ezt biztos lehet gyorsabban
def toRelations(e):
    res = set()
    for c in e:
        for pivot in c:
            for elem in c:
                res.add((pivot, elem))
    return res

def isEquiv(a, b, equiv):
    return (a, b) in equiv or (b, a) in equiv

def listToFrozensets(list):
    res = set()
    for l in list:
        res.add(frozenset(l))
    return frozenset(res)

def toClasses(relations):
    res = []
    for x,y in relations:
        found = False
        for c in res:
            if(isEquiv(x, c[0], relations)):
                c.append(x)
                found = True
                break
        if(not found):
            res.append([x])
    res = listToFrozensets(res)
    return res

def egyesites(a, b):
    closure = toRelations(a.union(b))
    while True:
        new_relations = set((x,w) for x,y in closure for q,w in closure if q == y)

        closure_until_now = closure | new_relations

        if closure_until_now == closure:
            break

        closure = closure_until_now
    
    return toClasses(closure)

def kisebb(a, b, numOfElements):
    m = metszet(a, b)
    e = egyesites(a, b)
    # print(f"metszet: {m}")
    # print(f"egyesites: {e}")
    # print(f"egyenloek: {m == a}, {e == b}")
    # if((len(a) == numOfElements and len(b) == 1) or (len(a) == 1 and len(b) == numOfElements)):
    #     return False
    # if(m == a and e == b):
    #     return True
    # elif (m == b and e == a):
    #     return True
    # return False
    if((len(a) == numOfElements and len(b) != numOfElements -1) or (len(b) == numOfElements and len(a) != numOfElements -1) or (len(a) == 1 and len(b) != 2) or (len(b) == 1 and len(a) != 2)):
        return False
    return (m == a and e == b) or (m == b and e == a)