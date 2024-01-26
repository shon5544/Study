import sys

input = sys.stdin.readline

n = int(input().rstrip())

dpList = {}

def fibo(n):
    global dpList
    
    if n in dpList:
        return dpList[n]
    
    if n == 0:
        return 0

    if n == 1:
        return 1
    
    result = fibo(n - 1) + fibo(n - 2)
    dpList[n] = result
    
    return result

print(fibo(n))