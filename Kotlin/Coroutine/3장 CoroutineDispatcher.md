
## 3장 내용 요약
- CoroutineDispatcher 객체의 역할
- 제한된 디스패처와 무제한 디스패처의 차이
- 제한된 디스패처 생성하기
- CoroutineDispatcher 사용해 코루틴 실행하기
- 코루틴 라이브러리에 미리 정의된 디스패처의 종류와 사용처

## CoroutineDispatcher란?
디스패터: 무언가를 보내는 주체.
코루틴 디스패처란 코루틴을 보내는 주체다. 꽤나 간단한 정의.

그렇다면 궁금점. 코루틴 디스패처가 코루틴을 어디로 보낸다는 걸까? 그 목적지는 바로 스레드다. 스레드에 코루틴을 할당하는 것이다. 코루틴은 일시 중단이 가능한 '작업'이기 때문에 스레드가 있어야 실행될 수 있다.

코루틴 디스패처는 코루틴을 스레드에 보내 실행시키는 것까지의 역할을 가진다.
따라서 코루틴 디스패처는 사용가능한 스레드, 스레드풀을 가지며 코루틴을 실행 요청한 스레드에서 실행되도록 만들 수 있는 녀석이다.

### CoroutineDispatcher의 동작 살펴보기
**가정**
- 우리의 CoroutineDispatcher는 2개의 스레드로 구성된 스레드풀을 사용할 수 있다.
- 2개의 스레드 중 하나의 스레드에 이미 Coroutine1이 실행 중이다.

![[Pasted image 20240705175701.png]]
코루틴 디스패처 객체는 작업 대기열을 가진다. 이 작업 대기열의 역할은 실행되어야 하는 작업들을 저장하는 것이다.

코루틴 디스패처가 사용할 수 있는 스레드 풀에는 Thread-1, Thread-2가 있다.

> CoroutineDispatcher의 구현에 따라 구조는 달라질 수 있다고 한다.

![[Pasted image 20240705175823.png]]
디스패처 객체에 Coroutine2 코루틴의 실행이 됐을 때: 
1. 디스패처 객체는 실행 요청받은 코루틴을 위와 같이 작업 대기열에 넣는다.
2. 디스패처가 사용할 수 있는 스레드가 있는지 확인한다.
3. 있다면 해당 스레드에 할당한다. 그림에서는 Thread-2가 남으니 Coroutine2를 그곳에 할당한다.

![[Pasted image 20240705202711.png]]
이런식으로 스레드에 할당하여 코루틴을 실행 시키는 모습을 간단하게 살펴봤다.

Coroutine 3이 추가된다고 해도 예상 가능한 그림 그대로다.
1. Coroutine3이 작업 대기열에 올라감.
2. 스레드 풀 내에 할당 가능한 스레드가 없으므로 대기한다.
3. 대기하다가 자리가 나면 해당 스레드에 Coroutine3을 할당한다.

코루틴 디스패처의 행동을 요약해보자면, 실행 요청된 코루틴을 작업 대기열에 적재 후 사용 가능한 스레드에 할당하는 것이라고 할 수 있겠다.

### CoroutineDispatcher의 역할
역할 자체는 스케줄러와 유사하다. 코루틴용 스케줄러라고 봐도 괜찮지 않을까라는 생각이 들엇다.

## 제한된 디스패처와 무제한 디스패처
코틀린 디스패처에는 두 가지 종류가 있다. 하나는 제한된 디스패처, 나머지 하나는 무제한 디스패처이다.

제한된 디스패처: 사용할 수 있는 스레드/스레드풀이 제한되어있음.
무제한 디스패처: 그 반대. 그러한 제한이 없다.

제한된 디스패처는 아까 앞에서 다룬 것들이다. 아까 코루틴을 할당하지 못하고 큐에 넣어놓았던 상황을 떠올려보자.

무제한 디스패처는 실행할 수 있는 스레드가 제한되지 않았다고 해서 요청된 코루틴이 아무 스레드에서나 돌지는 않는다. 무제한 디스패처는 실행 요청된 코루틴이 이전 코드가 실행되던 스레드에서 계속해서 실행되도록 하는 것이다. 이 때문에 실행되는 스레드가 매번 달라질 수 있고, 특정 스레드로 제한되어 있지 않아 무제한 디스패처라는 이름을 갖게 된 것이다.

책에서는 이 무제한 디스패처를 진정으로 이해하기 위해선 코루틴에 대한 깊은 지식이 필요하므로 먼 미래에 별도로 다룬다고 한다.

## 제한된 디스패처 생성하기
제한된 디스패처는 코루틴을 실행시킬 때 보낼 수 있는 스레드가 제한된 CoroutineDispatcher 객체를 뜻한다. 코루틴 라이브러리는 사용자에게 직접 제한된 디스패처를 만들 수 있도록 몇 가지 함수를 제공하는데 이것들을 한번 알아보자.

### 단일 스레드 디스패처 만들기
단일 스레드 디스패처란, 사용 가능 스레드가 하나인 CoroutineDispatcher 객체를 의미한다.
이는 코루틴 라이브러리가 제공하는 newSingleThreadContext 함수를 사용해 만들 수 있다.

```kotlin
val dispatcher: CoroutineDispatcher = newSingleThreadContext(name = "SingleThread")
```

이 함수의 name 인자는 디스패처에서 관리하는 스레드의 이름이 된다.

![[Pasted image 20240705205443.png]]
이 과정을 통해 만들어진 CoroutineDispatcher 객체는 위와 같은 모습이다. 똑같은 모습인데 스레드 풀에 SingleThread라는 스레드 하나 있는 것을 볼 수 있다.

### 멀티 스레드 디스패처 만들기
```kotlin
val multiThreadDispatcher = CoroutineDispatcher = newFixedThreadPoolContext(
	nThreads = 2,
	name = "MultiThread"
)
```

2개 이상의 스레드를 사용할 수 있는 멀티 스레드 디스패처를 만들기 위해선 위와 같이 `newFixedThreadPoolContext`함수를 사용하면 된다. 이 함수는 스레드의 개수(`nThreads`), 스레드의 이름(`name`)을 매개변수로 받는다. 스레드들은 name 값 뒤에 `-1`부터 1씩 증가해서 이름이 붙여진다.

![[Pasted image 20240705210051.png]]
이렇게. 우리가 위에서 봤던 그 구조다. 이렇게 디스패처를 만들었으면 한번 코루틴을 만들어서 디스패처에 한번 요청해보자.

**번외. `newFixedThreadPoolContext`의 구현**
![[Pasted image 20240705210244.png]]
이처럼 구현이 되어있는데, 흥미로운 점은 내부적으로 ExecutorService를 생성하는 newScheduledThreadPool을 이용한다는 것과 이렇게 만들어진 것들이 데몬 스레드로 생성된다는 것이다. 대체 왜? 에 대해서 좀 더 생각을 해봐야겠다.

## CoroutineDispatcher 사용해서 코루틴 실행하기
### launch의 파라미터로 CoroutineDispatcher 사용하기
#### 단일 스레드 디스패처 사용해서 코루틴 실행하기
```kotlin
fun main() = runBlocking<Unit> {
	val dispatcher = newSingleThreadContext(name = "SingleThread")
	launch(context = dispatcher) {
		println("${Thread.currentThread().name} 실행")
	}
}
```
이 launch 함수에 Trailing Lambda 형식으로 들어간 것이 코루틴으로 돈다. 어떻게 동작할지는 위에서 손이 닳도록 설명한 것 같으니 생략하겠다.

#### 멀티 스레드 디스패처 사용해서 코루틴 실행하기
```kotlin
fun main() = runBlocking<Unit> {
	val multiThreadDispatcher = newFiexedThreadContext(
		nThreads = 2,
		name = "MultiThread"
	)

	launch(context = multiThreadDispatcher) {
		println("${Thread.currentThread().name} 실행")
	}

	launch(context = multiThreadDispatcher) {
		println("${Thread.currentThread().name} 실행")
	}
}
```

멀티 스레드 디스패처의 동작도 위에서 손이 닳도록 설명했으니 넘어가겠다. 이쪽에서 중요한 포인트는 구현을 어떤 코드로 할 것이냐이다.

## 부모 코루틴의 CoroutineDispatcher 사용해 자식 코루틴 실행하기
코루틴은 구조화를 통해 코루틴 내에서 새로운 코루틴을 실행시킬 수 있다.

이때 바깥 코루틴이 부모, 내부 코루틴이 자식이 된다.

```kotlin
fun main() = runBlocking<Unit> {
	val multiThreadDispatcher = newFiexedThreadContext(
		nThreads = 2,
		name = "MultiThread"
	)

	launch(context = multiThreadDispatcher) {
		println("${Thread.currentThread().name} 실행")

		launch {
			println("${Thread.currentThread().name} 실행")
		}

		launch {
			println("${Thread.currentThread().name} 실행")
		}
	}
}
```
자식 코루틴에 디스패처 설정을 안했으면 부모 코루틴의 디스패처를 따라간다.

![[Pasted image 20240705213449.png]]

이처럼 모든 자식 코루틴이 MultiThread를 쓰는 것을 봤을 때 같은 디스패처를 사용하고 있음을 알 수 있다.

## 미리 정의된 CoroutineDispatcher
앞서 다룬 newFixedThreadPoolContext를 통해서 코루틴 디스패처를 직접 생성하면 경고가 출력된다.
![[Pasted image 20240705213634.png]]

이런 경고를 하는 이유는 사용자가 newFixedThreadPoolContext 함수를 사용해 디스패처를 만드는 것이 비효율적일 수 있기 때문이다. 심지어 그럴 확률 높음 !

이렇게 직접 디스패처를 만들면 이 디스패처에서만 사용되는 스레드 풀이 생성되며, 스레드풀에 속한 스레드의 수가 너무 적거나 많이 생성돼 비효율을 발생시킬 가능성이 있기 떄문이다.

또한 이미 프로젝트 내에 디스패처가 있음에도 협업하는 개발자가 그걸 몰라 디스패처를 또 만들면 메모리 낭비가 된다. 스레드의 생성 비용은 비싸다는 점 숙지하기.

![[Pasted image 20240705213949.png]]
때문에 코루틴 라이브러리는 미리 생성된 디스패처를 제공한다.

### Dispatchers.IO
코루틴 라이브러리에서 제공하는 입출력 관련 디스패처이다.
이 녀석이 사용가능한 스레드의 수는 JVM에서 사용 가능한 프로세서 수와 64 중 큰 값으로 설정된다. 
따라서 이녀석을 사용하면 여러 입출력 작업을 동시에 수행할 수 있다.

```kotlin
fun main() = runBlocking<Unit> {
	launch(Dispatchers.IO) {
		println("${Thread.currentThread().name} 실행")
	}
}
```
이 친구는 싱글톤 인스턴스이므로 그냥 바로 사용할 수 있다.
이 녀석을 사용할 때의 스레드 이름은 DefaultDispatcher-worker-n이다. n은 스레드 넘버다. 

### Dispatchers.Default
CPU bound 작업에서 사용할 때 좋은 디스패처다. 얘도 싱글톤이라 사용법은 똑같다.

```kotlin
fun main() = runBlocking<Unit> {
	launch(Dispatchers.Default) {
		println("${Thread.currentThread().name} 실행")
	}
}
```

#### limitedParallelism 사용해서 스레드 사용 제한하기
Dispatchers.Default를 사용해서 오래 걸리는 연산을 처리하면 특정 연산을 위해 모든 스레드가 사용될 수 있다. 그런 상황을 막기위해 limetedParallelism이라는 함수를 제공한다.

![[Pasted image 20240705214910.png]]
위처럼 사용할 수 있다.

### 공유 스레드 풀을 사용하는 Dispatchers.IO와 Default
둘이 사용하는 스레드 이름이 같은 것을 보아 둘은 같은 스레드 풀을 사용한다는 사실을 알 수 있다. 왜 그러냐면 둘이 공유 스레드 풀을 사용해서 그렇다.

두 디스패처 모두 같은 API를 통해 개발되었기에 공유 스레드 풀을 쓰는 것이다.

![[Pasted image 20240705215109.png]]
공유 스레드 풀을 시각화한 모습이다.

newFixedThreadPoolContext는 자신만 사용가능한 스레드 풀을 만들고 Dispatchers 씨리즈는 공유 스레드 풀을 만든다는 차이를 기억하자.

### Dispatchers.Main
이 녀석은 UI가 있는 애플리케이션에서 메인 스레드의 사용을 위해 사용되는 특별한 디스패처이다.
kotlinx-coroutine-android와 같은 의존성이 추가 되어야 사용할 수 있다.