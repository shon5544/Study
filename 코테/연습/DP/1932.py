import sys

input = sys.stdin.readline

n = int(input().rstrip())

d = [[0 for _ in range(i)] for i in range(1, n + 1)]

tri = []
for i in range(n):
    tri.append(list(map(int, input().split())))

d[0][0] = tri[0][0]

if n > 1:
    d[1][0] = tri[0][0] + tri[1][0]
    d[1][1] = tri[0][0] + tri[1][1]

for i in range(2, n):
    for j in range(len(d[i])):
        if j == 0:
            d[i][j] = tri[i][j] + d[i - 1][j]
            continue
        if j == len(d[i]) - 1:
            d[i][j] = tri[i][j] + d[i - 1][j - 1]
            continue

        d[i][j] = max(tri[i][j] + d[i - 1][j - 1], tri[i][j] + d[i - 1][j])

print(max(d[n - 1]))