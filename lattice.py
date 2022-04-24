def metszet(elem1, elem2):
    res = set()
    for s1 in elem1:
        for s2 in elem2:
            res.add(s1.intersection(s2))
    res.discard(frozenset())
    return res

def egyesites(elem1, elem2, numOfElements = -1):
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

def kisebb(a, b, numOfElements):
    m = metszet(a, b)
    e = egyesites(a, b, numOfElements)
    print(f"metszet: {m}")
    print(f"egyesites: {e}")
    if((len(a) == numOfElements and len(b) == 1) or (len(a) == 1 and len(b) == numOfElements)):
        return False
    if(m == a and e == b):
        return True
    elif (m == b and e == a):
        return True
    return False