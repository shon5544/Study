import sys

input = sys.stdin.readline

n = int(input().rstrip())

sol = list(map(int, input().split()))
sol.reverse()

d = [1] * n

for i in range(1, n):
    for j in range(i):
        if sol[j] < sol[i]:
            d[i] = max(d[i], d[j] + 1)

print(n - max(d))