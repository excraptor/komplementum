
N = 2
M = 3

def numberOfMatchings():
    global N, M
    #leftSet, rightSet = initSets()
    # ADJACENCY MATRIX?
    sum = 0
    n = 1
    while N > 0 and M > 0:
        print(f"sum: {sum}, N: {N}, M: {M}, n: {n}")
        
        N -= 1
        M -= 1
        n += 1
        
        
    return sum


def chooseNEdges(n):
    global N, M
    prod = 1
    for i in range(n):
        prod *= (N-i)*(M-i)
        print(prod)
    return prod/n


def initSets():
    s1 = [i for i in range(N)]
    s2 = [i for i in range(N, N + M)]
    return s1, s2

def fact(n):
    if(n == 1):
        return 1
    return n*fact(n-1)

M = numberOfMatchings()
print(f"matchings: {M}")

print("#################")

print(chooseNEdges(2))