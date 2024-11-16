from collections import deque


test_cases = int(input())  # 테스트 케이스의 수 입력받기

for _ in range(test_cases):
    n, m = map(int, input().split())  # 문서의 개수와 타겟 문서의 인덱스 입력받기
    priorities = list(map(int, input().split()))  # 문서들의 중요도 입력받기
    
    # 문서의 인덱스와 중요도를 저장하는 큐
    queue = deque((i, priority) for i, priority in enumerate(priorities))
    print_order = 0
    
    while queue:
        current = queue.popleft()
        
        # 현재 문서보다 더 중요한 문서가 있으면 뒤로 보낸다
        if any(current[1] < other[1] for other in queue):
            queue.append(current)
        else:
            print_order += 1
            if current[0] == m:
                print(print_order)
                break