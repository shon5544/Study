import sys

input = sys.stdin.readline

a1 = [""] + list(input().rstrip())
a2 = [""] + list(input().rstrip())

LCS = [[""] * len(a2) for _ in range(len(a1))]

for i in range(1, len(a1)):
    for j in range(1, len(a2)):
        if a1[i] == a2[j]:
            LCS[i][j] = LCS[i - 1][j - 1] + a1[i]
        elif len(LCS[i - 1][j]) >= len(LCS[i][j - 1]):
            LCS[i][j] = LCS[i - 1][j]
        else:
            LCS[i][j] = LCS[i][j - 1]

ans = LCS[-1][-1]
print(len(ans))
print(ans)