import sys

input = sys.stdin.readline

t = int(input().rstrip())

ans = []

d = [[0 for _ in range(15)]]

for _ in range(t):
    a = int(input().rstrip())
    b = int(input().rstrip())
    
    for i in range(a):
        d.append([0 for _ in range(15)])
    
    for i in range(1, b + 1):
        d[0][i] = i
    
    for i in range(1, a + 1):
        for j in range(1, b + 1):
            s = 0
            for k in range(1, j + 1):
                s += d[i - 1][k]
            d[i][j] = s

    ans.append(s)

for i in ans:
    print(i)