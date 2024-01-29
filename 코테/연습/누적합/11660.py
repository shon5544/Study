import sys

input = sys.stdin.readline

n, m = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(n)]
sum_num = [[0] * (n+1) for _ in range(n+1)]

for i in range(1, n+1):
    for j in range(1, n+1):
        sum_num[i][j] = arr[i-1][j-1] + sum_num[i-1][j] + sum_num[i][j-1] - sum_num[i-1][j-1]

for _ in range(m):
    x1, y1, x2, y2 = map(int, input().split())
    result = sum_num[x2][y2] - sum_num[x2][y1-1] - sum_num[x1-1][y2] + sum_num[x1-1][y1-1]
    print(result)