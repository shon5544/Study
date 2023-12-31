import sys

input = sys.stdin.readline

n = int(input().rstrip())

start = 0
end = n

while start < end:
    mid = (end + start) // 2
    if mid ** 2 < n:
        start = mid + 1
    else:
        end = mid - 1
    
print(start)