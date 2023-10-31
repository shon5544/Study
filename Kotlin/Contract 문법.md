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
이렇게 활용이 가능하다. 원래 Int?와 Int는 다른 자료형이다. 그러나 위에서 contract에서 value가 null이 아님을 알았으니 Int에 Int?의 대입이 가능한 것이다. 즉, 컴파일러에게 잘못되지 않았음을 알려줬으니 실제로는 잘못된 문법이었더라도 바로 가능한 것이다.

### callsInPlace를 활용해보자.
---
```kotlin
@ExperimentalContracts
fun invokeLambda(lambda: () -> Unit) {
	contract {
		callsInPlace(lambda, InvocationKind.EXACTLY_ONCE)
	}
	lambda()
}
```
위의 코드처럼, implies 대신 callsInPlace를 사용하기도 한다.

callsInPlace는 람다 함수를 사용할 때, 그 함수의 호출 횟수를 명시적으로 컴파일러에게 이해시켜주기 위해 사용하는 문법이다.

### callsInPlace는 왜 쓰나요?
---
```kotlin
// callsInPlace가 없을 때.
val value: String
Contract.invokeLambda {
	value = "TEMP" // Captured values initialization is forbidden due to possible reassignment
}
return value // Variable 'value' must be initialized
```
val로 선언한 값이 초기화 되어있지 않은 상황이다.

- Captured ~ : invokeLambda 함수가 **몇 번 호출되는지 명확히 모르기 때문에, val 변수 특성 상 여러 번 값이 변할 수 있어 오류 발생**

- Variable ~ : 마찬가지로, invokeLambda 함수가 **몇 번 호출되는지 명확히 모르기 때문에, return 값이 다를 수 있어 오류 발생**

만약 위의 코드를 실행 시켰다면 위와 같은 오류가 발생할 것이다.
왜냐하면 인자로 들어갈 람다가 몇 번 호출될 지 모르기 때문이다.

val 변수의 특성 상 인자로 들어가는 람다는 단 한 번만 작동해야 한다. 왜냐하면 val의 초기화는 단 한번만 이뤄지니까.

그런데 invokeLambda 안에서 람다를 몇 번 호출하는지 명시되어 있지 않기 때문에 오류가 발생하는 것이다.

### 이상하네
---
> 😠: '아니,, 한 번만 작동하게 썼잖아,,' 

개발자 입장에선 이상할 수 밖에 없다. 당연히 이 val의 문제를 알고 있으며 어련히 한 번만 호출되게 썼지만, 이게 중복 문제로 오류를 뱉으니 어이가 없는 거다.

그러나 이게 컴파일러 입장에서는 두리뭉술 하기에, 어쩔 수 없이 개발자가 배려해주는 것이다. 이걸 챙김으로써 혹시 모를 위협에서 더 안전해지기도 하니 겸사겸사라고 생각을 하자!