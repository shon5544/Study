import sys

input = sys.stdin.readline

n = int(input().rstrip())

house = list(map(int, input().split()))
house.sort()

print(house[(n - 1) // 2])
