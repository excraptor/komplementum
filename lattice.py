def metszet(elem1, elem2):
    res = set()
    for s1 in elem1:
        for s2 in elem2:
            res.add(s1.intersection(s2))
    res.discard(frozenset())
    return res

def egyesites(elem1, elem2):
    res = elem1.union(elem2)

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

