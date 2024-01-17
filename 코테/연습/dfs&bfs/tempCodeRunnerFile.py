import sys

input = sys.stdin.readline

r, c = map(int, input().split())

graph = [[] for _ in range(r)]

for i in range(r):
    text = input().rstrip()
    
    for j in text:
        graph[i].append(j)

dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]
alpha = set()
maxNum = -sys.maxsize

def dfs(graph, alpha, x, y, cnt):
    global maxNum
    maxNum = max(maxNum, cnt)
    
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]

        if not graph[nx][ny] in alpha:
            if 0 <= nx < r and 0 <= ny < c:
                alpha.add(graph[nx][ny])
                dfs(graph, alpha, nx, ny, cnt + 1)
                alpha.remove(graph[nx][ny])

alpha.add(graph[0][0])
dfs(graph, alpha, 0, 0, 1)
print(maxNum)