import sys

input = sys.stdin.readline

t = int(input().rstrip())
ans = []

for _ in range(t):
    n = int(input())
    coins = list(map(int, input().split()))
    m = int(input())

    d = [0] * (m + 1)
    d[0] = 1

    for coin in coins:
        for i in range(m + 1):
            if i >= coin:
                d[i] += d[i - coin]

    ans.append(d[m])

for i in ans:
    print(i)