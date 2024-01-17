import sys

input = sys.stdin.readline

n, m = map(int, input().split())

edges = []
parent = list(range(n + 1))

for i in range(m):
    a, b, c = map(int, input().split())
    edges.append((c, a, b))

edges.sort(key=lambda x: x[0])

def find_parent(x):
    if parent[x] != x:
        parent[x] = find_parent(parent[x])
    return parent[x]

def union_parent(a, b):
    a = find_parent(a)
    b = find_parent(b)
    if a < b:
        parent[b] = a
    else:
        parent[a] = b

ans = 0
last_edge = 0
for c, a, b in edges:
    if find_parent(a) != find_parent(b):
        union_parent(a, b)
        ans += c
        last_edge = c
print(ans - last_edge)