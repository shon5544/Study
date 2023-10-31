---
tags:
  - 문법
---

### Contract 란?
---
- 불필요한 타입 체크 혹은 불필요한 컴파일 에러등을 방지하고 좀 더 용이하게 사용하기 위한 문법.

### How to use?
---
```kotlin
@ExperimentalContracts
fun isNotNull(value: Any?): Boolean {
    contract {
        returns(true) implies (value != null)
    }
    return false
}

@ExperimentalContracts
fun main(args: Array<String>) {
    val nullableInt: Int? = 5

    if (isNotNull(nullableInt)) {
        val nonNullInt: Int = nullableInt //에러가 발생하지 않습니다.    
    }

}
```

Contracts 함수를 사용하는 함수에 ExperimentalContracts라는 어노테이션을 명시하고 반드시 함수의 시작에 contract 블록을 선언해줘야 한다.

그런데, contract안의 return이 있다고 해서 거기서 함수가 끝나는게 아니다. 
contract { } 의 리턴 값이 **true면 "컴파일러야. 이 조건은 참이야. 기억해!"** 이고,
**false면 "컴파일러야. 이 조건은 거짓이야. 신경쓰지말고 할일 계속 해!"** 이다.