import sys

input = sys.stdin.readline

n, m = map(int, input().split())

cnt = 0

preFirst = ""
for i in range(n):
    line = input().rstrip()
    if preFirst != line[0]:
        if line[0] == 'W':
            line = f"B{line[1:]}"
        else:
            line = f"W{line[1:]}"
        cnt += 1

    pre = ""

    for j in line:
        if pre == j:
            cnt += 1
        if j == 'W':
            j = 'B'
        else:
            j = 'W'
        pre = j
    preFirst = line[0]

print(cnt)