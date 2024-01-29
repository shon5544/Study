import sys
input_sys = sys.stdin.readline

# 11660번
n, m = map(int, input_sys().split())
arr = [list(map(int, input_sys().split())) for _ in range(n)]
sum = [[0] * (n+1) for _ in range(n+1)]

# 2차원 배열의 부분합 계산
for i in range(1, n+1):
    for j in range(1, n+1):
        sum[i][j] = arr[i-1][j-1] + sum[i-1][j] + sum[i][j-1] - sum[i-1][j-1]

# 구간 합 계산
for _ in range(m):
    x1, y1, x2, y2 = map(int, input_sys().split())
    result = sum[x2][y2] - sum[x2][y1-1] - sum[x1-1][y2] + sum[x1-1][y1-1]
    print(result)