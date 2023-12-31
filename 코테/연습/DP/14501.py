import sys

input = sys.stdin.readline

n = int(input().rstrip())
consulting = []
d = [0] * (n + 1)

for i in range(n):
    consulting.append(list(map(int, input().split())))

for i in range(n):
    for j in range(i + consulting[i][0], n + 1):
        if d[j] < d[i] + consulting[i][1]:
            d[j] = d[i] + consulting[i][1]

print(d[-1])