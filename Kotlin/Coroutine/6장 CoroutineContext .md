
## CoroutineContext?
우리가 지금까지 사용하던 Dispatcher 시리즈는 CoroutineContext 객체의 구성요소이기에 context로서 사용할 수 있었다.

컨텍스트 자체에 대한 정의를 하진 않았던 것 같은데, 우리가 앞으로 다룰 코루틴 컨텍스트란 코루틴 실행 환경을 설정하고 관리하는 인터페이스라고 생각할 수 있다. 이 CoroutineContext는 CoroutineDispatcher, CoroutineName, Job 등의 객체를 조합해 코루틴의 실행 환경을 설정한다. 

즉 CoroutineContext 객체는 코루틴을 실행하고 관리하는 데 핵심적인 역할을 하며 코루틴 실행과 관련한 모든 설정을 하는 역할을 가지고 있다.

이 코루틴 컨텍스트의 구성 요소와 구성 방법, 접근, 제거하는 방법을 알아보자.

## CoroutineContext의 구성요소
CoroutineContext 객체는 CoroutineName, CoroutineDispatcher, Job, CroutineExceptionHandler의 네 가지 주요한 구성 요소를 가진다. 이 외에도 다양한 구성요소가 있지만 코루틴 실행의 중심에 있는 건 이 네가지이기 때문에 이들만 중점적으로 보자.

- CoroutineName: 코루틴의 이름을 설정한다.
- CoroutineDispatcher: 코루틴을 스레드에 할당해 실행한다.
- Job: 코루틴의 추상체로 코루틴을 조작하는데 사용된다.
- CoroutineExceptionHandler: 코루틴에서 발생한 예외를 처리한다.

## CoroutineContext 구성하기
### CoroutineContext가 구성 요소를 관리하는 방법
![[Pasted image 20240726200409.png]]
CoroutineContext(이하 Context) 객체는 키-값 쌍으로 각 구성 요소를 관리한다.

각 구성 요소는 고유한 키를 가진다. 당연히 중복된 값은 허용하지 않는다. Context 객체는 CoroutineName, CoroutineDispatcher, Job, CoroutineExceptionHandler 객체를 하나만 가질 수 있다.

### CoroutineContext 구성
Context 객체는 키-값으로 구성 요소를 관리한다. 그러나 키에 값을 직접 대입하는 방법을 사용하지는 않는다. 

Context 객체 간에 더하기 연산자를 사용해 CoroutineContext 객체를 구성한다.

```kotlin
val coroutineContext: CoroutineContext = newSingleThreadContext("MyThread") + CoroutineName("MyCoroutine")
```

이런 식으로 말이다.

이러면 다음 사진처럼 컨텍스트가 구성될 것이다.

![[Pasted image 20240726200940.png]]

만들어진 CoroutineContext 객체는 코루틴 빌더 함수의 context 인자에 넘겨서 사용할 수 있다.

```kotlin
fun main() = runBlocking<Unit> {
	val coroutineContext: CoroutineContext = newSingleThreadContext("MyThread") + CoroutineName("MyCoroutine")

	launch(context = coroutineContext) {
		println("[${Thread.currentThread().name}] 실행")
	}
}

/*
[MyThread @MyCoroutine#2] 실행
*/
```

이렇게 말이다.

실행 결과를 보면 알 수 있듯 우리가 설정한 스레드 이름과 코루틴 이름으로 된 것을 볼 수 있다.

### CoroutineContext 구성 요소 덮어씌우기
Context 객체에 만약 같은 구성 요소가 둘 이상 더해진다면 나중에 추가된 녀석이 이전 값을 덮어씌운다.

```kotlin
fun main() = runBlocking<Unit> {
	val coroutineContext: CoroutineContext = newSingleThreadContext("MyThread") + CoroutineName("MyCoroutine")

	val newContext: CoroutineContext = coroutineContext + CoroutineName("NewCoroutine")

	launch(context = newContext) {
		println("[${Thread.currentThread().name}] 실행")
	}
}

/*
[MyThread @NewCoroutine#2] 실행
*/
```

실행결과를 통해 알 수있다.

### 여러 구성 요소로 이뤄진 CoroutineContext 합치기
여러 구성 요소로 이뤄진 Context 객체 2개가 합쳐지고 2개의 Context 객체에 동일한 키를 가진 구성 요소가 있다면 나중에 들어온 값이 선택된다.

```kotlin
val coroutineContext1 = CoroutineName("MyCoroutine1") + newSingleThreadContext("MyThread1")

val coroutineContext2 = CoroutineName("MyCoroutine2") + newSingleThreadContext("MyThread2")

val combinedCoroutineContext = coroutineContext1 + coroutineContext2
```

![[Pasted image 20240726201735.png]]

결과는 이렇게 된다. 연산자 뒤에 있는 녀석의 값으로 덮어씌여진다고 볼 수 있겠다.

### CoroutineContext에 Job 생성해 추가하기
코루틴 빌더 함수 말고 Job() 과 같은 코드로도 J1ob은 만들어진다. 이걸 컨텍스트 객체에 꽂아줄 수 있다.

```kotlin
val myJob = Job()
val coroutineContext: CoroutineContext = Dispatchers.IO + myJob
```

그러나 Job을 직접 생성해 추가하면 코루틴의 구조화가 깨지기 때문에 주의가 필요하다. 이후에 나올 구조화와 동시성 섹션에서 자세히 보자.

## CoroutineContext 구성 요소에 접근하기
### CoroutineContext 구성 요소의 키
Context 구성 요소의 키는 CoroutineContext.Key 인터페이스를 구현해 만들 수 있는데 일반적으로 Context 구성요소는 자신의 내부에 키를 싱글톤 객체로 구현한다.

```kotlin
public data class CoroutineName(
	val name: String
): AbstractCoroutineContextElement(CoroutineName) {
	public companion object Key : CoroutineContext.Key<CoroutineName>
	...
}
```

이 Key를 사용하면 Context 객체에서 CoroutineName에 접근할 수 있다.

Job 인터페이스 내부도 동일한 코드가 있다.

모든 구성요소는 .Key를 통해 키에 접근할 수 있으니 참고하자.

### 키를 사용해 구성요소 접근하기
#### 싱글톤 키를 통해 접근하기
```kotlin
fun main() = runBlocking<Unit> {
	val coroutineContext = CoroutineName("MyCoroutine") + Dispatchers.IO
	val nameFromContext = coroutineContext[CoroutineName.Key]
	println(nameFromContext)
}

/*
// 결과:
CoroutineName(MyCoroutine)
*/
```

이런식으로 접근이 가능하다. 결과 값은 저렇게 나오니 참고.

#### 구성 요소 자체를 키로 사용해 접근하기
CoroutineName, Job, CoroutineDispatcher, CoroutineExceptionHandler 객체는 동반 객체로 CoroutineContext.Key 를 구현하는 키를 갖고 있어서 Key를 명시적으로 사용하지 않아도 구성 요소 자체를 키로 사용할 수있다.

```kotlin
fun main() = runBlocking<Unit> {
	val coroutineContext = CoroutineName("MyCoroutine") + Dispatchers.IO
	val nameFromContext = coroutineContext[CoroutineName]
	println(nameFromContext)
}

/*
// 결과:
CoroutineName(MyCoroutine)
*/
```

결과는 똑같다.

#### 구성 요소의 key 프로퍼티를 사용해 구성 요소에 접근하기
```kotlin
fun main() = runBlocking<Unit> {
	val coroutineName = CoroutineName("MyCoroutine")
	val dispatcher = Dispatchers.IO
	val coroutineContext = coroutineName + dispatcher
	
	println(coroutineContext[coroutineName.key])
	println(coroutineContext[dispatcher.key])
}

/*
// 결과:
CoroutineName(MyCoroutine)
Dispatchers.IO
*/
```

이렇게도 가져올 수 있음.

구성요소의 key 프로퍼티는 동반 객체로 선언된 Key와 동일한 값을 가지기 때문에 가능하다.

```kotlin
fun main() = runBlocking‹Unit> {
	val coroutineName: CoroutineName = CoroutineName ("MyCoroutine") 
	if (coroutineName.key === CoroutineName.Key) {
		printin("coroutineName.key 와 CoroutineName.Key 동일합니다") }
	}
}
/*
// 결과:
coroutineName.key와 CoroutineName.Key 동일합니다 
*/
```

## CoroutineContext 구성 요소 삭제하기
### minusKey 사용해 구성 요소 제거하기
```kotlin
val coroutineName = CoroutineName("MyCoroutine")
val dispatcher = Dispatchers.IO
val myJob = Job()
val coroutineContext = coroutineName + dispatcher + myJob
```

대충 이렇게 컨텍스트를 만들었다.

```kotlin
val deletedCoroutineContext = coroutineContext.minusKey(CoroutineName)
```

이런 식으로 구성요소를 삭제할 수 있다. 기존에 있던 키의 값은 null이 된다.

### minusKey 주의점
중요한건 기존 컨텍스트를 변경하는게 아니라 minusKey가 적용된 컨텍스트를 새로 반환한다는 점이다.
그러니 착각하지 말자.