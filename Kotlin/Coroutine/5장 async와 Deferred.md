
## async 사용해 결과값 수신하기
### async 사용해 Deffered 만들기
launch 코루틴 빌더와 async 코루틴 빌더는 매우 비슷함.

```kotlin
// async 명세
public fun <T> CoroutineScope.async(
	context: CoroutineContext = EmptyCoroutineContext,
	start: CoroutineStart = CoroutineStart.DEFAULT,
	block: suspend CoroutineScope.() -> T
): Deffered<T>
```

launch 함수의 명세와 같다.

async와 launch의 다른점은 Job 대신 deffered를 반환한다.

이 두 반환 타입의 특징은:
- Job: 행위 자체에 대한 추상화 객체.
- Deffered: Job에서 추가로 결과값을 Wrapping한 객체.
이다.

Deffered의 사용법은 간단하다.
```kotlin
val networkDeferred: Deferred<String> = async(Dispatchers.IO) {
	delay(1000L)
	return@async "Dummy Response"
}
```

타입 선언시 결과값을 타입을 한번 Deferred로 감싸주고 반환에서 리턴 스코프를 async 함수로 지정해주면 된다.

### 결과값 수신
Deffered는 결과값 수신을 위해 await라는 함수를 제공한다.

```kotlin
fun main() = runBlocking<Unit> {
	val networkDeferred: Deferred<String> = async(Dispatchers.IO) {
		delay(1000L)
		return@async "Dummy Response"
	}

	val result = networkDeferred.await()
	println(result)
}
```

이렇게 하면 된다. 이러면 코루틴에서 리턴받은 값을 이용할 수 있다.

## Deferred는 특수한 형태의 Job이다.
뭔가 Deferred는 Job과는 다르다고 생각할 수 있지만 실상은 아니다. Deferred는 Job의 서브 타입이다. Job이 할 수 있는 모든 건 Deferred도 할 수 있다.

## 복수의 코루틴으로부터 결괏값 수신하기
### await를 이용해 수신하기
```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentMillis()
	val participantDeferred1: Deferred<Array<String>> = async(Dispatchers.IO) {
		delay(1000L)
		return@async arrayOf("James", "Jason")
	}
	val participants1 = participantDeferred1.await()

	val participantDeferred2: Deferred<Array<String>> = async(Dispatchers.IO) {
		delay(1000L)
		return@async arrayOf("Jenny")
	}
	val participants2 = participantDeferred2.await()
}
```

이렇게 일단은 하는거로 생각할 수 있다. 근데 이거 블라킹 코드나 다름이 없다. 실제로 2초정도 걸림.

왜? await를 하면 호출부의 코루틴이 일시 정지된다. 그렇기에 두 코루틴의 병렬진행이 안 되는 것이다.

```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentMillis()
	val participantDeferred1: Deferred<Array<String>> = async(Dispatchers.IO) {
		delay(1000L)
		return@async arrayOf("James", "Jason")
	}

	val participantDeferred2: Deferred<Array<String>> = async(Dispatchers.IO) {
		delay(1000L)
		return@async arrayOf("Jenny")
	}
	val participants1 = participantDeferred1.await()
	val participants2 = participantDeferred2.await()
}
```

이렇게 하면? 코루틴이 병렬 진행된다. 이전의 코드는 코루틴 1의 await 다음에 코루틴2의 정의가 있어 코루틴 1이 끝날때까지 코루틴 2가 돌지 못하는 것이었다. 지금은 이렇게 해놓으니 둘 다 같이 시작한다.

살짝 헷갈릴 수도 있는데 await가 정지 시키는건 **호출부의** 코루틴이다. 호출된 녀석들은 await와 관계없이 끝까지 돈다.

그렇기에 병렬이 되는 것!

### awaitAll로 결과 수신
일일히 await하는게 많아지면 힘들 수 있다. 일괄 처리를 할 수 있도록 해놓자.

```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentMillis()
	val participantDeferred1: Deferred<Array<String>> = async(Dispatchers.IO) {
		delay(1000L)
		arrayOf("James", "Jason")
	}

	val participantDeferred2: Deferred<Array<String>> = async(Dispatchers.IO) {
		delay(1000L)
		arrayOf("Jenny")
	}
	val results: List<Array<String>> = awaitAll(participantDeferred1, participantDeferred2)

	println(...대충 출력)
}
```

이렇게 한번에 처리할 수도 있다는거! 모든 코루틴이 다 완료될때까지 awaitAll 다음이 안 돌아간다.

### 컬렉션에 대해 대해 awaitAll 사용하기
코루틴 라이브러리는 Collection에 대해 awaitAll 함수를 확장함수로 제공하기도 한다.

```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentMillis()
	val participantDeferred1: Deferred<Array<String>> = async(Dispatchers.IO) {
		delay(1000L)
		arrayOf("James", "Jason")
	}

	val participantDeferred2: Deferred<Array<String>> = async(Dispatchers.IO) {
		delay(1000L)
		arrayOf("Jenny")
	}
	val results: List<Array<String>> = listOf(participantDeferred1, participantDeferred2).awaitAll()

	println(...대충 출력)
}
```

그냥 awaitAll 쓰는거랑 완벽하게 똑같이 돌아간다.

## withContext
### withContext로 async-await 대체하기
```kotlin
public suspend fun <T> withContext(
	context: CoroutineContext,
	block: suspend CoroutineScope.() -> T
): T
```

이런 함수가 있다. 호출되면 context 인자를 통해 block 람다식을 실행하고, 완료되면 그 결과를 반환한다. block 람다식을 모두 실행하면 다시 기존의 CoroutineContext 객체를 사용해 코루틴이 재개된다. async-await 쌍을 연속적으로 실행했을때와 매우 유사하다.

코드로 보자.

```kotlin
fun main() = runBlocking<Unit> {
	val networkDeferred: Deferred<String> = async(Dispatchers.IO) {
		delay(1000L)
		return@async "Dummy Response"
	}

	val result = networkDeferred.await()
	println(result)
}
```

이런 async-await 함수가 있다고 했을때, withContext로 다음과 같이 구현이 가능하다.

```kotlin
fun main() = runBlocking<Unit> {
	val result: Deferred<String> = withContext(Dispatchers.IO) {
		delay(1000L)
		return@async "Dummy Response"
	}

	println(result)
}
```

이렇게 코루틴 선언과 반환 값 수신을 한번에 할 수 있다.

### withContext의 동작 방식
withContext는 겉보기에 async-await를 바로 호출하는 것과 비슷하게 동작하지만 실상은 좀 다르다. 내부 동작이 좀 다름. async-await 쌍은 새로운 코루틴을 생성해 작업을 처리하지만 withContext는 실행 중이던 코루틴을 그대로 유지한채로 실행 컨텍스트만 바꿔서 작업을 처리한다.

```kotlin
fun main() = runBlocking<Unit> {
	println("[${Thread.currentThread().name}] runBlocking 실행")
	withContext(Dispatchers.IO) {
		println("[${Thread.currentThread().name}] withContext 실행")
	}
}

/*
[main @coroutine#1] runBlocking 블록 실행
[DefaultDispatcher-worker-1 @coroutine#1] withContext 블록 실행
*/
```

코드의 실행 결과를 보면 두 출력의 코루틴이름이 `coroutine#1`로 똑같은 것을 알 수 있다.

여기선 CoroutineContext가 Dispatchers.IO로 바뀌었기 때문에 백그라운드 스레드(DefaultDispatcher-worker-1)에서 실행됐다.

withContext 함수의 동작 방식을 좀 더 자세히 알아보자. withContext 함수가 호출되면 실행 중인 코루틴의 실행 환경이 withContext 함수의 context 인자 값으로 변경돼 `실행되며 이를 컨텍스트 스위칭(Context Switching)`이라고 부른다.

만약 context 인자로 CoroutineDispatcher 객체가 넘어온다면 코루틴은 해당 CoroutineDispatcher 객체를 활용해 다시 실행된다. 따라서 앞의 코드에서 withContext가 호출되면 해당 코루틴은 다시 작업 대기열로 이동한 후 Dispatchers.IO가 사용할 수 있는 스레드 중 하나로 보내져 실행된다.

![[Pasted image 20240724172903.png]]

 말이다. withContext 함수는 함수의 block 람다식이 실행되는 동안 코루틴의 실행 환경을 변경시킨다. withContext가 끝나면 coroutine#1은 다시 원래의 스레드로 다시 이동할 것이다.

async는 앞서 얘기했듯 코루틴을 새로 만드는 식으로 간다.

```kotlin
fun main() = runBlocking<Unit> {
	println("[${Thread.currentThread().name}] runBlocking 실행")
	async(Dispatchers.IO) {
		println("[${Thread.currentThread().name}] withContext 실행")
	}.await()
}

/*
[main @coroutine#1] runBlocking 블록 실행
[DefaultDispatcher-worker-1 @coroutine#2] withContext 블록 실행
*/
```

![[Pasted image 20240724173109.png]]

이런 느낌으로.

### withContext 주의점
withContext는 앞서 언급했듯 새 스레드를 만드는 방식이 아니다. 따라서 하나의 코루틴에서 withContext 함수가 여러 번 호출되면 순차적으로 실행된다. 복수의 독립적인 작업이 병렬로 실행돼야하는 상황에 withContext를 사용하면 성능에 문제가 생긴다는 것이다.

병렬 처리가 안 된다!

```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentTimeMillis()
	val helloString = withContext(Dispatchers.IO) {
		delay(1000L)
		return@withContext "Hello"
	}

	val worldString = withContext(Dispatchers.IO) {
		delay(1000L)
		return@withContext "World"
	}

	println(대충 결과값 프린트)
}
```

병렬 실행되지 않는다. 순차 처리된다. withContext는 언급했듯 스레드 실행위치만 달라지는 거지 동작하는 코루틴을 새로만드는게 아니다. 그러니까 블라킹 코드처럼 동작하지.

병렬로 돌리고 싶으면 async-await 써라.

## 뭐야 쓸모없잖아.
그럼 withContext는 걍 블라킹 코드가 되는거 아님? 이라고 생각할 수 있을 것 같다. 쓸모없잖아 이거. 근데 잘 생각해보면 쓸 구석이 있을 것 같다. 백그라운드 스레드로 옮겨져서 실행된다는 것에 좀 주의를 둬보자.

