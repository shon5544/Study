import sys

input = sys.stdin.readline

n = int(input().rstrip())

a = list(map(int, input().split()))

dp = [1] * n

for i in range(n):
    for j in range(i):
        if a[i] > a[j]:
            dp[i] = max(dp[i], dp[j] + 1)

print(max(dp))

ans = []
dpV = max(dp)
for i in range(n - 1, -1, -1):
    if dpV == dp[i]:
        ans.append(a[i])
        dpV -= 1

ans.reverse()
print(*ans)