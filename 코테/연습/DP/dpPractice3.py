n, m = map(int, input().split())

arr = [0] * n
d = [0] * m
for i in range(n):
    arr[i] = int(input())

for i in range(m):
    d[i] = max(arr[i], arr[i + 1])