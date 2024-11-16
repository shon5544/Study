import heapq
import sys

input = sys.stdin.readline

tn = int(input().rstrip())

ans = []

for i in range(tn):
    n, m = map(int, input().split())

    docs = list(map(int, input().split()))

    heap = []

    for i, priority in enumerate(docs):
        heapq.heappush(heap, (priority, i))
    
    for i, doc in enumerate(heap):
        if doc[1] == m:
            ans.append(i)

for i in ans:
    print(ans)