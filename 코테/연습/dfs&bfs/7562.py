import sys
from collections import deque

input = sys.stdin.readline

n = int(input().rstrip())

graph = []
visited = []

dx = [-2, -1, 1, 2, 2, 1, -1, -2]
dy = [1, 2, 2, 1, -1, -2, -2, -1]

def bfs(x, y, to_x, to_y, I):
    q = deque()
    q.append((x, y))

    graph[x][y] = 1
    while q:
        x, y = q.popleft()
        if x == to_x and y == to_y:
            return graph[to_x][to_y] - 1
        for i in range(8):
            nx = x + dx[i]
            ny = y + dy[i]

            if 0 <= nx < I and 0 <= ny < I and graph[nx][ny] == 0:
                q.append((nx, ny))
                graph[nx][ny] = graph[x][y] + 1

ans = []

for i in range(n):
    I = int(input().rstrip())
    graph = [[0 for _ in range(I)] for _ in range(I)]
    visited = [[0 for _ in range(I)] for _ in range(I)]

    cur_x, cur_y = map(int, input().split())
    to_x, to_y = map(int, input().split())

    result = bfs(cur_x, cur_y, to_x, to_y, I)
    ans.append(result)

for i in ans:
    print(i)