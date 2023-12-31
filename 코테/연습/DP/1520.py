import sys

input = sys.stdin.readline

a, b = map(int, input().split())

dp = [[-1] * b for _ in range(a)]
i_map = []
dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]

for i in range(a):
    i_map.append(list(map(int, input().split())))

def dfs(x, y):
    if x == a - 1 and y == b - 1:
        return 1
    
    if dp[x][y] != -1:
        return dp[x][y]
    
    way = 0
    for i in range(4):
        nx, ny = x + dx[i], y + dy[i]

        # 마지막 조건은 왜? 내리막길로만 가기로 했으니까!
        if 0 <= nx < a and 0 <= ny < b and i_map[x][y] > i_map[nx][ny]:
            way += dfs(nx, ny)
    
    dp[x][y] = way
    return dp[x][y]

print(dfs(0, 0))