---
undefined: ""
File: "`@Transactional(readOnly=true)`의 성능 최적화"
---
흔히 트랜잭션을 사용할 때 읽기 전용 메서드의 경우 readOnly 속성을 true로 만들어주는 경우가 많다.
관성적으로 '아 그렇구나'정도로 사용해왔었는데 이걸 사용했을 때 구체적으로 어떻게 성능이 최적화가 되는지 항상 궁금했었다.