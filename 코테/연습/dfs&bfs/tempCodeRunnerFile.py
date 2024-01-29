import sys
sys.setrecursionlimit(10**6)

input = sys.stdin.readline

n = int(input().rstrip())

graph = []
visited = []

cnt = sys.maxsize
dx = [-2, -1, -2, -1, 2, -1, 2, 1]
dy = [-1, -2, 1, 2, -1, -2, 1, 2]

def dfs(cur_x, cur_y, to_x, to_y, cur_cnt, I):
    global cnt
    global visited
    global graph
    global dx, dy
    # print(f"cur_cnt: {cur_cnt}")

    if visited[cur_x][cur_y] == 1:
        return
    
    if cur_x == to_x and cur_y == to_y:
        cnt = min(cnt, cur_cnt)
        # print(f"cnt: {cnt}")
        return
    
    visited[cur_x][cur_y] = 1

    for i in range(8):
        nx = cur_x + dx[i]
        ny = cur_y + dy[i]

        if 0 <= nx < I and 0 <= ny < I:
            dfs(nx, ny, to_x, to_y, cur_cnt + 1, I)

ans = []

for i in range(n):
    I = int(input().rstrip())
    graph = [[0 for _ in range(I)] for _ in range(I)]
    visited = [[0 for _ in range(I)] for _ in range(I)]

    cur_x, cur_y = map(int, input().split())
    to_x, to_y = map(int, input().split())

    dfs(cur_x, cur_y, to_x, to_y, 0, I)

    ans.append(cnt)
    cnt = sys.maxsize

for i in ans:
    print(i)