---
undefined: 
File: 4장 코루틴 빌더와 Job
---
## 코루틴 빌더와 Job
우리가 지난시간 열심히 배웠던 코루틴 빌더 함수(runBlocking, launch)는 호출될 시 코루틴을 만들고 이것이 추상화된 **Job** 객체를 만든다. Job이란 추상화된 코루틴이라고 생각하면 될 것 같다.

이 Job 객체를 이용하여 코루틴의 상태를 추적 및 제어할 수 있다.

```Kotlin
fun main() = runBlocking<Unit> {
	val job: Job = launch(Dispatchers.IO) {
		println("[${Thread.currentThread().name}] 실행")
	}
}
```

코루틴은 일시 정지가 가능한 녀석이다. 이 녀석이 추상화된 Job 객체는 코루틴을 제어할 수 있는 함수와 상태를 나태내는 값들을 외부에 노출한다. 사실상 코루틴 핸들링은 이 Job을 이용한다고 보면 된다.

이번 스터디에서 이를 잘 알 수 있을테니 열심히 공부해보자

## join을 사용한 코루틴 순차 처리
코루틴 간에 순차 처리가 필요한 경우가 종종 있다.

예를 들어 DB 작업을 순차적으로 처리해야하거나 캐싱된 토큰 값이 업데이트 된 이후에 네트워크 요청을 해야하는 상황 등이다. 

이런 상황에서 Job은 join이라는 함수를 제공해 먼저 처리해야하는 코루틴의 실행이 완료될 떄까지 호출부의 코루틴이 정지되도록 할 수 있다. 어케 사용할 수 있을까?

### join 함수를 사용해 순차 처리하기
join 함수를 쓰는 법은 간단하다.
JobA 코루틴 완료 -> JobB가 해결되어야 한다면.
JobA 코루틴에 join 함수를 호출하면 된다.

코드로 보자. updateTokenJob이 반드시 networkCallJob 전에 완료되어야한다고 하자.
```Kotlin
fun main() = runBlocking<Unit> {
	val updateTokenJob = launch(Dispatchers.IO) {
		println("[${Thread.currentThread().name}] 토큰 업데이트 시작")
		delay(100L)
		println("[${Thread.currentThread().name}] 토큰 업데이트 완료")
	}
	
	updateTokenJob.join() // 일시 정지
	
	val networkCallJob = launch(Dispatchers.IO) {
		println("[${Thread.currentThread().name}] 네트워크 요청")
	}
}
```

`join`을 호출하면 `join`의 대상이 된 코루틴의 작업이 완료될 때까지 `join`을 호출한 코루틴이 일시 중단된다. `runBlocking` 코루틴이 `updateTokenJob.join()`을 호출하면 `runBlocking` 코루틴은 `updateTokenJob` 코루틴이 완료될 때까지 일시 중지한다.

`updateTokenJob`이 끝나면? 당연히 `networkCallJob`을 수행할 것이다.

![[Pasted image 20240718154407.png]]

위의 그림으로 플로우를 정리할 수 있겠다.

**주의사항**
join은 join을 호출한 함수만 정지한다.
join을 한 건 정지하겠지만 그 외의 것들은 계속 돌아간다.

```Kotlin
fun main() = runBlocking<Unit> {
	val updateTokenJob = launch(Dispatchers.IO) {
		println("[${Thread.currentThread().name}] 토큰 업데이트 시작")
		delay(100L)
		println("[${Thread.currentThread().name}] 토큰 업데이트 완료")
	}

	val someJob = launch(Dispatchers.IO) {
		println("[${Thread.currentThread().name}] someJob 시작")
		delay(100L)
		println("[${Thread.currentThread().name}] someJob 완료")
	}
	
	updateTokenJob.join() // 일시 정지
	
	val networkCallJob = launch(Dispatchers.IO) {
		println("[${Thread.currentThread().name}] 네트워크 요청")
	}
}
```

위 코드라면 updateTokenJob은 정지되겠지만 someJob은 정지되지 않는다.

### joinAll을 사용한 코루틴 순차 처리
실제 개발 시에는 서로 독립적인 여러 코루틴을 병렬로 실행한 후 실행한 요청들이 모두 끝날때까지 있다가 다음 작업으로 넘어가는게 효율적이다.

SNS 이미지 업로드 기능이라면 사용자가 복수의 이미지를 업로드하는 경우가 있다. 이미지 변환을 해야한다고 했을 때 이것들은 순차적으로 될 필요가 없다. 코루틴으로 업로드 작업을 분리하여 동시에 변환 작업을 진행하고 모든 코루틴이 다 끝났을 때 다음으로 넘어가는게 훨 빠를 것이다.

이런 경우를 위해 코루틴 라이브러리는 복수의 코루틴이 모두 끝날 때 까지 호출부의 코루틴을 일시정지 시키는 `joinAll` 함수를 제공한다.

```kotlin
public suspend fun joinAll(vararg jobs: Job): Unit = jobs.forEach {
	it.join()
}
```

요렇게 생겨먹음 쓴다면 job을 인자에 계속 넣어서 쓰면 된다

```Kotlin
fun main() = runBlocking<Unit> {
	val convertImageJob1: Job = launch(Dispatchers.Default) {
		Thread.sleep(1000L)
		println("[${Thread.currentThread().name}] 이미지 1 변환 완")
	}

	val convertImageJob2: Job = launch(Dispatchers.Default) {
		Thread.sleep(1000L)
		println("[${Thread.currentThread().name}] 이미지 2 변환 완")
	}

	val convertImageJob3: Job = launch(Dispatchers.Default) {
		Thread.sleep(1000L)
		println("[${Thread.currentThread().name}] 이미지 3 변환 완")
	}

	joinAll(convertImageJob1, convertImageJob2, convertImageJob3)

	val uploadImageJob: Job = launch(Dispatchers.IO) {
		...
	}
	...
}
```

쓸 때는 이렇게 쓰면 됨

## CoroutineStart.LAZY
코루틴 라이브러리는 생성된 코루틴을 지연 시작할 수 있도록 하는 기능을 제공한다.

### 지연 시작을 살펴보기 위한 준비
지연 시작에 대해 알아보기 위해선 시간을 측정할 수 있는 도구가 필요하다.

```kotlin
fun getElapsedTime(startTime: Long): String = 
	"지난 시간: ${System.currentTimeMillis() - startTime}ms"
```

위와 같은 함수를 만들어 사용해보자.

앞으로 이 파트에선 요녀석을 사용할 거다.

### CoroutineStart.LAZY 사용해 코루틴 지연 시작하기
지연 시작이 적용된 코루틴은 생성 후 대기 상태에 놓이며 실행을 요청하지 않으면 시작되지 않는다.

이걸 이제 lauch 함수의 start 인자로 CoroutineStart.LAZY를 넘겨서 지연 시작 옵션을 적용한다면 구현할 수 있다.

함 만들어보자

```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentTimeMillis()
	val lazyJob: Job = launch(start = CoroutineStart.LAZY) {
		println("[${getElapsedTime(startTime)}] 지연 실행")
	}
}
```

이거 돌리면 아무것도 안나온다. LAZY로 설정되어있는데 실행시켜주는 로직이 없기 때문이다.

```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentTimeMillis()
	val lazyJob: Job = launch(start = CoroutineStart.LAZY) {
		println("[${getElapsedTime(startTime)}] 지연 실행")
	}
	delay(1000L)

	lazyJob.start()
}

/*
결과:
[main @coroutine#2][지난 시간: 1014ms] 지연 실행
*/
```

start 부분을 추가해주니 이제야 뭐가 찍힌다. 우리가 위에서 얘기한대로 잘 된다.

이렇게 코루틴을 지연 시작하는 방법에 대해 알아봤다. 앞으로 코루틴이 좀 나중에 실행되어야한다거나 하는 일이 있다면 써먹어보도록 하자.

#### 기능적으로 필요할 때는 언제일까?
뭔가 떠오르는게 코드를 좀 깔끔하게 쓰고 싶다거나 말고는 크게 떠오르지가 않더군요.

코드 스코프에서 코루틴 정의부와 실행부를 나눠서 실행 흐름을 좀 더 이쁘게 보여줄 수 있을 것 같긴한데 기능적으로 지연 시작이 필요할 일이 있을까? 라는 생각이 들었어요.

혹시 다른 분들은 어떻게 생각하세요?

## 코루틴 취소하기
코루틴 실행 중 실행할 필요가 없어지면 취소해야한다. 코루틴은 끝날 때까지 스레드를 점유할 테니까.

### cancel 사용해 Job 취소하기
```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentTimeMillis()
	val longJob: Job = launch(Dispatchers.Default) {
		repeat(10) { repeatTime ->
			delay(1000L)
			println("[{${getElapsedTime(startTime)}}] 반복횟수 ${repeatTime}")
		}
	}
}
/*
결과:
[지난시간: 1015ms]반복횟수0 
[지난시간: 2022ms]반복횟수1 
[지난시간: 3028ms]반복횟수2 
•••
[지난시간: 8050ms]반복횟수7 
[지난시간: 9057ms]반복횟수8 
[지난시간: 10062ms]반복횟수9 
*/
```

다 끝날 때까지 대략 10초 걸리는 코드다.

```kotlin
fun main() = runBlocking<Unit> {
	val startTime = System.currentTimeMillis()
	val longJob: Job = launch(Dispatchers.Default) {
		repeat(10) { repeatTime ->
			delay(1000L)
			println("[{${getElapsedTime(startTime)}}] 반복횟수 ${repeatTime}")
		}
	}

	delay(3500L)
	longJob.cancel()
}
/*
결과:
[지난시간: 1015ms]반복횟수0 
[지난시간: 2022ms]반복횟수1 
[지난시간: 3028ms]반복횟수2 
*/
```

3.5초 지난 후에 잡이 캔슬되므로 프린트도 세개밖에 안 찍힌다.

이런식으로 캔슬 가능하니 참고

### cancelAndJoin을 이용한 순차처리
```kotlin
fun main() = runBlocking<Unit> {
	val longJob: Job = launch(Dispatchers.Default) {
		// do something
	}

	longJob.cancel()
	executeAfterJobCancelled() // 코루틴 종료 후 실행되는 동작
}
```

잘 실행될 것 같은가?

잘 돌아갈 것 같이 생겼지만 순차성 관점에서 중요한 문제점이 있다.
cancel이 호출된다고 해서 즉시 취소되는게 아니라 Job 내부의 취소 확인용 플래그를 `취소 요청됨` 상태로 변경함으로써 코루틴이 취소돼야한다는 것만 알린다.

이후 미래 시점에 코루틴 취소가 요청됐는지 체크하고 취소된다.

쉽게 말해 즉시 취소가 아니라 `비동기적으로` 취소를 맡긴다는 것이다. 취소가 비동기 논블라킹스럽게 돈다. 

순차 처리가 필요한데 정확한 순차 처리를 보장할 수 없다. 비결정적인 로직이 된단 말이다!! 그것은 정말 슬픈 일이야.

따라서 순차성 보장이 반드시 되어야하는 로직에게는 `cancelAndJoin` 함수를 호출하는 식으로 하면 된다. 얘는 순차성 보장을 한다. 취소가 완료될 때까지 runBlocking이 멈춘다.

```kotlin
fun main() = runBlocking<Unit> {
	val longJob: Job = launch(Dispatchers.Default) {
		// do something
	}

	longJob.cancelAndJoin()
	executeAfterJobCancelled() // 코루틴 종료 후 실행되는 동작
}
```
이렇게 하면 된다. 실행흐름을 잘보고 맞는 걸 선택하자

## 코루틴 취소 확인
cancel, cancelAndJoin을 쓴다해서 바로 멈추는게 아니라는 걸 배웠다. 취소 플래그를 건드리고, 이 플래그를 감지해서 비동기적으로 바꾸는 것이 큰 틀이다.

그렇다면 코루틴 취소를 확인하는 시점은 언젤까? 일반적으로는 일시 중단 지점이나 코루틴이 실행을 대기하는 시점이다. 이 시점이 없으면 코루틴은 취소되지 않는다.

```kotlin
fun main() = runBlocking<Unit> {
	val whileJob: Job = launch(Dispatchers.Default) {
		while(true) {
			println("작업 중")
		}
	}
	delay(100L)
	whileJob.cancel()
}
```

위 같은 상황에서 취소되지 않는다. 캔슬 담에 취소를 확인할만한 요소가 없기 때문이다.

취소 시키는 세가지 방법이 있다.

1. delay를 사용한 취소 확인
2. yield를 사용한 취소 확인
3. CoroutineScope.isActive를 사용한 취소 확인

### delay를 사용한 취소 확인
얘는 suspend fun으로 선언돼 특정 시간만큼 **호출부의 코루틴**을 일시 중단하게 만든다.

위에서 언급했듯 코루틴은 일시 중단 시점에도 취소를 확인한다.

```kotlin
fun main() = runBlocking<Unit> {
	val whileJob: Job = launch(Dispatchers.Default) {
		while(true) {
			println("작업 중")
			delay(1L) // 추가됨!
		}
	}
	delay(100L)
	whileJob.cancel()
}

/*
결과:
...
작업 중 
작업 중 
작업 중
Process finished with exit code 0 
*/
```

whileJob이 계속 멈추면서 자신이 캔슬됐는지 체크하게 된다.

의도한대로는 돌아가긴하는데.. 효율적이지 않다. 계속 작업이 지연되잖아. 성능저하로 이어진다.

### yield를 사용한 취소 확인
yield()가 호출되면 자신이 사용하던 스레드를 양보한다. 스레드를 양보한다는건 스레드 사용을 중단한다는 내용이므로 일시 중단된다. 그때 취소확인을 하게된다.

```kotlin
fun main() = runBlocking<Unit> {
	val whileJob: Job = launch(Dispatchers.Default) {
		while(true) {
			println("작업 중")
			yield() // 추가됨!
		}
	}
	delay(100L)
	whileJob.cancel()
}

/*
결과:
...
작업 중 
작업 중 
작업 중
Process finished with exit code 0 
*/
```

이 상황에서 스레드 점유하는 코루틴이 whileJob 밖에 없어 잠깐 중지됐다 바로 재개된다.

근데 얘도 결국 스레드를 계속 양보하면서 일시 중단된다는 문제가 있다. 일시 중단이 매우 빈번하게 일어난다는 것은 성능저하의 원인이 될 수도 있다는 것이다.

얘도 탈락 !

### CoroutineScope.isActive를 사용한 취소 확인
```kotlin
fun main() = runBlocking<Unit> {
	val whileJob: Job = launch(Dispatchers.Default) {
		// 수정됨!
		while(this.isActive) {
			println("작업 중")
		}
	}
	delay(100L)
	whileJob.cancel()
}

/*
결과:
...
작업 중 
작업 중 
작업 중
Process finished with exit code 0 
*/
```

cancel시에 코루틴의 isActive 값이 false가 된다. 위처럼 해놓으면 while의 조건에서 바로 현 코루틴의 컨디션을 체크하니 더 효율적이다. 굳이 일시 정지라는 프로세스를 거치지 않기 때문이다.

만약 코루틴이 일시 중단 지점 없이 계속 되어야하는 상황이라면 명시적으로 코루틴의 컨디션을 체크하는 코드를 넣어줌으로서 효율적으로 취소를 할 수 있도록 만들어주자.

## 코루틴의 상태와 Job의 상태 변수
![[Pasted image 20240719192017.png]]

코루틴은 위처럼 6가지의 상태를 가진다.
- 생성
- 실행 중
- 실행 완료 중
- 실행 완료
- 취소 중
- 취소 완료

어떤 경우에 각 상태로 전이 되는지 확인해보자.
실행 완료 중은 다음에 더 깊게 다뤄본다고 한다. 그러니 설명에도 빠져있다. 참고.

- 생성: New
	- 코루틴 빌더를 통해 코루틴을 생성하면 생성 상태에 기본적으로 들어간다. 
	- 자동으로 생성 상태에서 변하지 않게 하고 싶으면 지연 시작을 쓰도록하자.
- 실행 중: Active
	- 지연 코루틴이 아닌 코루틴을 만들면 생성 완료되자마자 여기로 들어온다.
- 실행 완료: Completed
	- 코루틴의 모든 코드가 실행 완료되면 이 상태가 된다.
- 취소 중: Cancelling
	- Job.cancel() 등을 통해 취소 요청 시 이 상태가 된다.
- 취소 완료: Cancelled
	- 코루틴의 취소 확인 시점에 취소가 확인된 경우 이 상태가 된다.

위와 같은 상태를 가질 수 있는데, Job 객체는 이런 상태를 나타내는 상태 변수들을 외부에 공개한다.
물론 Job은 코루틴을 추상화한 녀석이니 상태 변수들은 코루틴의 상태를 간접적으로만 나타낸다.

Job의 상태변수는 세가지다. 모두 Boolean이다.
- isActive: 활성화 돼 있는지에 대한 여부. 활성화란 취소 요청이나 실행 완료되지 않은 상태를 의미한다.
- isCancelled: 취소 요청됐는지에 대한 여부. 요청만 해도 true가 나오니 진짜 취소된 것은 아닐 수도 있다는 점 기억하자.
- isCompleted: 실행 완료에 대한 여부. 실행 완료되거나 취소 완료되면 true가 나온다.


### Job의 상태를 출력하는 함수 만들기
```kotlin
fun printJobState(job: Job) {
	println(
		"Job State\n" +
			"isActive >> ${job.isActive}\n" +
			"isCancelled >> ${job.isCancelled}\n" +
			"isCompleted >> ${job.isCompleted}"
	)
}
```

앞으로 스터디 중 계속 써먹을 함수다.

### 생성 상태의 코루틴
```kotlin
fun main() = runBlocking<Unit> {
	val job: Job = launch(start = CoroutineStart.LAZY) {
		delay(1000L)
	}
	printJobState(job)
}
/*
결과:
Job State
isActive >> false 
isCancelled >> false 
isCompleted >> false 
*/
```

생성된 상태에 머물러 있으니 당연히 모든 상태 변수가 false다.

### 실행 중 상태의 코루틴
```kotlin
fun main() = runBlocking<Unit> {
	val job: Job = launch {
		delay(1000L)
	}
	printJobState(job)
}
/*
결과:
Job State
isActive >> true 
isCancelled >> false 
isCompleted >> false 
*/
```

바로 코루틴 디스패처에 의해 스레드로 보내져 실행될테니 isActive는 true다.

### 실행 완료 상태의 코루틴
```kotlin
fun main() = runBlocking<Unit> {
	val job: Job = launch {
		delay(1000L)
	}
	delay(2000L)
	printJobState(job)
}
/*
결과:
Job State
isActive >> false 
isCancelled >> false 
isCompleted >> true 
*/
```

2초면 job이 끝나고도 남는 시간이니 isCompleted가 true다.

### 취소 중인 코루틴
단순한 취소 요청은 바로 취소 완료 상태가 될 수 있으니 전에 배운걸 써먹어보자. 취소 확인 지점을 안만들면 확인할 수 있을 것이다.

```kotlin
fun main() = runBlocking<Unit> {
	val whileJob: Job = launch(Dispatchers.Default) {
		while(true) {
			// 작업 중
		}
	}
	whileJob.cancel()
	printJobState(whileJob)
}

/*
결과:
Job State
isActive >> false 
isCancelled >> true 
isCompleted >> false 
*/
```

이렇게 하니 취소됐는지 보인다. 굿.

### 취소 완료된 코루틴
```kotlin
fun main() = runBlocking<Unit> {
	val job: Job = launch {
		delay(5000L)
	}
	job.cancelAndJoin()
	printJobState(job)
}
/*
결과:
Job State
isActive >> false 
isCancelled >> true 
isCompleted >> true 
*/
```

취소 완료된 녀석은 isCancelled, isCompleted 둘 다 true다.

### 상태 정리
![[Pasted image 20240719193837.png]]
코루틴의 내부에서 어떤 상태 전이가 발생하는지 제대로 아는 것이 중요하다. 내부 상태가 어떨지 잘 생각하면서 코딩하자.