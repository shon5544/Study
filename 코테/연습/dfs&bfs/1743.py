import sys

input = sys.stdin.readline

n, m, k = map(int, input().split())

my_map = [[0 for _ in range(m)] for _ in range(n)]
visited = [[0 for _ in range(m)] for _ in range(n)]
trash_max_size = 0

for _ in range(k):
    r, c = map(int, input().split())
    my_map[r - 1][c - 1] = 1

def dfs(x, y, trash_size):
    global trash_max_size

    if visited[x][y] == 1:
        return

    dx = [-1, 1, 0, 0]
    dy = [0, 0, 1, -1]
    visited[x][y] = 1
    cur_trash_size = trash_size

    if my_map[x][y] == 1:
        cur_trash_size += 1
    else:
        trash_max_size = max(trash_max_size, cur_trash_size)
        cur_trash_size = 0

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        # print(nx, ny)

        if 0 <= nx < n and 0 <= ny < m:
            
            dfs(nx, ny, cur_trash_size)

dfs(0, 0, 0)
print(visited)
print(my_map)
print(trash_max_size)