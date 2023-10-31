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
fun isNotNull(value: Int?): Boolean {
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

그렇기 때문에, implies () 의 조건이 어떻든 간에 contract { } 는 그대로 벗어나고, 다음 코드를 이어서 진행한다.

그래서 위 코드는 value의 값이 null이든, null이 아니든 무조건 false를 리턴해주게 됨.

### 아니,, 그럼 뭔 소용이야?
---
```kotlin
@ExperimentalContracts
fun isNotNull(value: Int?): Int {
    contract {
        returns(true) implies (value != null)
    }

	val result: Int = value
	return result
}
```
이렇게 활용이 가능하다. 원래 Int?와 Int는 다른 자료형이다. 그러나 위에서 contract에서 value가 null이 아님을 알았으니 Int에 Int?의 대입이 가능한 것이다. 즉, 컴파일러에게 잘못되지 않았음을 알려줬으니 실제로는 잘못된 문법이었