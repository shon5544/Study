
PEP 484에서 소개된 거다. PEP 484에서는 함수의 인자, 리턴 값, 변수에 타입을 정의할 수 있는 문법을 소개했다. 이렇듯 이제 파이썬은 프로젝트 컨벤션에 따라 강타입 언어로도 쓸 수 있게됐다. 우하하.
한번 파이썬의 타입 힌트에 대해서 알아보자.

## 들어가기 전에..
정적 타입 힌트에는 한계가 있다고 한다. 책에서는 자세히 설명하지 않는데 찾아보니 유연성 부족, 추상화의 제약 등의 한계가 있다고 한다. 

왜? 고차 함수나 제네릭 프로그래밍에서 매우 복잡한 타입을 다루는 경우 타입 시스템이 그 복잡성을 모두 처리하지 못할 수 있기 때문이다. 사실 정확하게 공감은 안 간다. 대충 뉘앙스정도는 파악되니 일단 넘어가지만 나중에 더 자세히 알아보자. 

아무튼 이러한 정적 타입 힌트의 한계를 타파하기 위한 PEP 484의 제안은 gradual type system, 점진적 타입 시스템이었다. 이에 대해 먼저 이해하고 넘어가보자.

## 점진적 타입 시스템에 대해서
점진적 타입 시스템이란 정적 타이핑, 동적 타이핑 사이에 있는 무언가다. 내가 타이핑을 할 수도 있고 안 할 수도 있는 시스템을 의미한다. 대표적인걸로 타입스크립트가 있다. 요 점진적 타입 시스템이란 것의 특징을 알아보자. 

### 점진적 타입 시스템 특.
옵셔널함.
- 기본적으로 타입 체커는 타입 힌트가 없는 코드에 대해 경고를 방출하지 않는다.
- 타입 체커는 오브젝트의 타입을 결정할 수 없을 땐 `Any` 타입으로 간주한다.

런타임에 타입 에러를 캐치하지 않음.
- 타입 힌트는 정적 타입 체커나 린터, IDE에서 경고를 발생시키는 데 사용되는데,
- 이것들이 런타임에 함수나 변수에 일관성 없는 값들이 지정되도록(엉망진창 타입 값 할당하는걸) 반드시 막아준다! 는 아님.

성능 향상을 시키는 건 아님.
- 타입 어노테이션들은 이론적으로 생성된 바이트 코드에 대해 최적화가 될 수 있는 데이터를 제공할 수 있다.
- 근데 이러한 최적화는 2021 7월 기준 어떤 파이썬 런타임에도 제공되어있지 않다.
- 그니까 이론적으로는 데이터 타입에 따라 최적화할 수 있을 텐데 이를 파이썬에서는 딱히 지원하지 않는 다는 듯 하다.

### 점진적 타입 시스템 쓰면 뭐가 좋은데.
점진적 타입 시스템의 가장 큰 장점은 이 모든 것들이 옵셔널하다는 것이다. 정적으로 했을 때에 대한 문제와 동적으로 했을 때에 대한 문제를 적절히 절충했다. 이게 좋다는 것이다.

너무 복잡한 데이터 같으면 이를 적절히 Any 정도로 처리할 수 있겠지. 그런 것들이 복잡도를 낮춘다고 보는 것 같다. 별도의 커스텀 타입을 만들어주지 않아도 괜찮으니까.

너무 많이 타입을 할당하는 것은 파이썬의 유연함을 제대로 활용하지 못하게하는 근본적인 이유가 되므로 조심하라고 책에서 얘기하니 참고해보자.

## 점진적 타입 예제
예제로 타입힌트가 어케 돌아가는지 함 보자. mypy를 이용해 심플한 파이썬 함수에 타입힌트를 달아보자.

> 💡 타입 체커가 mypy밖에 없음?
> 그건 아님. pytype, Pyright, Pyre 등등 타입 체커는 굉장히 많다.
> 예제에서 마이파이 쓰는건 이 당시 마이파이가 제일 유명해서 그런 것이라고 얘기하니 참고하자.

### Mypy 시작하는 법
pip install mypy 하면 됨. 끝.

이제 이렇게 하고 `mypy --some-command-line file.py`하면 된다.

### 빡세게 하기
--disallow-untyped-defs 커맨드 라인은 마이파이가 모든 매개변수와 값에 대해서 타입힌트가 없는 함수 정의를 플래그로 지정한다. 얘를 사용하면 타입이 없는 경우 마이파이가 에러문으로 혼내준다.

```python
@mark.parametrize('qty, expected', [
    (1, '1 part'),
    (2, '2 parts'),
])
def test_show_count(qty, expected): 
	got = show_count(qty, 'part') 
	assert got == expected

def test_show_count_zero():  
	got = show_count(0, 'part') 
	assert got == 'no parts'
```

적당히 파이테스트 코드를 써보자. 얘를 `mypy --disallow-untyped-defs ..` 로 실행시키면 에러가 터진다.

```
.../no_hints/ $ mypy --disallow-untyped-defs messages_test.py
    messages.py:14: error: Function is missing a type annotation
    messages_test.py:10: error: Function is missing a type annotation
    messages_test.py:15: error: Function is missing a return type annotation
    messages_test.py:15: note: Use "-> None" if function does not return a value
    Found 3 errors in 2 files (checked 1 source file)
```

이렇게. 신기하죠잉. 파이썬 런타임 언어인데 뭔가 컴파일 에러처럼 작동하니까.

점진적 타이핑의 첫 스텝에선 일단 --disallow-incomplete-defs 를 쓰는 것을 선호한다. 이거 쓰면 처음에는 아무 것도 알려주지 않는다.

```
 .../no_hints/ $ mypy --disallow-incomplete-defs messages_test.py
    Success: no issues found in 1 source file
```

대충 이렇게.. 근데 여기서 타입을 추가한다면?

```python
def test_show_count(qty, expected) -> str: 
	...
```

이러고 마이파이로 실행한다면 다음과 같이 나온다.

```
/no_hints/ $ mypy --disallow-incomplete-defs messages_test.py
    messages.py:14: error: Function is missing a type annotation
    for one or more arguments
    Found 1 error in 1 file (checked 1 source file)
```

인자에 타입 힌팅이 빠졌다고 혼내준다. 타입 힌팅을 쓴 부분에 대해선 다른 부분에 빠지는게 없는지 확인해주는 것이다. 그야말로 점진적 타입힌팅이라 할 수 있다.

```python
def test_show_count(qty: str, expected: str) -> str: 
	...
```

이렇게 하면 에러 안남.

위에서 말했듯이 과도한 타입 강제는 파이썬의 유연함을 제대로 활용 못하게 만드니까 이렇게 하는 걸 추천하는 것이다. 왠만하면 이렇게 하도록 하자.

### 파라미터 디폴트 값
```python
def show_count(count, word): 
	if count == 1:
		return f'1 {word}'  
	count_str = str(count) if count else 'no' 
	
	return f'{count_str} {word}s'
```

이런 함수가 있다고 하자.

```python
def test_irregular() -> None:  
	got = show_count(2, 'child', 'children') 
	assert got == '2 children'
```

이렇게 하고 마이파이로 돌리면 테스트 부터가 안 돌아간다.

```
.../hints_2/ $ mypy messages_test.py  
messages_test.py:22: error: Too many arguments for "show_count" Found 1 error in 1 file (checked 1 source file)
```

이렇게 고쳐보자:

```python
def show_count(count: int, singular: str, plural: str = '') -> str: 
	if count == 1:
		return f'1 {singular}'  
	count_str = str(count) if count else 'no' 
	if not plural:
		plural = singular + 's' 
	return f'{count_str} {plural}'
```

이러면 잘 된다. 이런식으로 타입 변수에 디폴트 값을 줄 수도 있다.

### 디폴트 값 None으로 주기(는 안 중요하고 Optional 소개하는 자리)
```python
def show_count(count: int, singular: str, plural: str = '') -> str: 
```

우리가 이렇게 기존에 디폴트 값을 줬었다. 충분히 멋쟁이 방법이지만 맥락에 따라 None을 주는 것이 더 좋은 디폴트 값이 될 때가 있다.

```python
from typing import Optional

def show_count(count: int, singular: str, plural: Optional[str] = None) -> str: 
```

이렇게 만들면 plural에 None도 들어갈 수 있고 str도 들어갈 수 있다. 이게 좋을 땐 언제일까? 값이 주입되면 None이 아니라 str 값일 것이다. plural 값이 None이라는 것은 값을 안넣어줬다라는 의미이다.

이에 대한 적절한 분기가 하고 싶을 때 None이 효과적일 수 있다. 물론 `plural == ''` 도 가능하겠지만 가독성이 좋지는 않다.

다음은 코틀린 코드인데 내가 비슷한 상황에 nullable 변수를 사용한 것이다. nullable 변수는 Optional이라고 생각하면 된다.

```kotlin
// 이러한 함수 시그니처가 있다고 하자.
fun findBySocialId(  
    socialId: String  
): User?

val user = userReader.findBySocialId(profile.id!!)  
    ?: return userWriter.register(  
        socialId = profile.id,  
        socialType = SocialInfoEnum.NAVER,  
        email = profile.email!!,  
        nickname = profile.nickname!!  
    ).toResult()
```

?:로 정의되는 코드 블록은 해당 함수의 값이 null이라면 동작하게 할 함수의 블록이다.
만약 해당 socialId를 가진 유저가 있으면 가져오고, 만약 없다면 유저를 회원가입 시키는 로직이다.
이런 식의 분기처리가 쉬우니 매우 용이하다.

## 타입은 지정되는 연산에 의해 정의된다.
뭔 멍소리냐 싶은데 한번 천천히 보자.

```python
from collections import abc 

def double(x: abc.Sequence):
	return x * 2
```

이 코드를 보자. 반환형에 대한 타입 정의는 안 됐는데 암튼 이건 대충 무시하고, 인자의 타입과 함수의 내용에 좀 집중을 해보자.

x는 abc.Sequence 타입이다. 함수의 내용에서는 `x * 2` 를 쓰고 있다. 이거 마이파이로 돌리면 어케될 것 같나?

터진다. 왜? Sequence는 `__mul__()` 매직 메서드가 없다. 이 연산을 할 수 있는 타입만 x의 타입이 될 수 있는 것이다. 

마이파이는 곱하기 소스를 분석하는 동안 `x * 2` 를 잘못된 것으로 판단한다. 이는 선언된 타입에 대해 지원되지 않는 연산이기 때문이다.

이런 모든 연산에 대해서 잘 돌아가면 타입으로 지정한 것이 통과되므로 연산에 의해 정의된다라는 표현을 쓴 것이다.

그러나 좀 알아둬야할 게 있다.

연산에 의해서 정의되기는 하는데, 반드시 연산을 통해야지만 타입을 체크할 수 있는 건 아니다.

```python
a: int = "hey"
```

이 코드를 돌려봐라. 당연히 터진다. 타입을 체크하는 기준은 연산도 있지만 위처럼 변수의 타입 정보를 수집한 뒤, 검사하는 식으로도 이뤄진다. 코드의 맥락을 파악했을 때 일관적이지 못한 점을 잡아서도 체크를 하니 참고를 하자.

그럼 여기서 더 궁금한점. "hey"라는 녀석이 str인걸 타입 체커는 어떻게 알 수 있을까? 일단 헤이가 str라는 걸 알아봤으니까 퍽 터지는거 아니야.

진짜 초 간단하다. 리터럴의 형태를 보고 파악한다. 대충 쌍따옴표 있으면 str 이렇게 알아본다는 것이다. 타입 체커들은 리터럴의 형태를 다 알고 있다. 신기하죠?

## 타입들 총 집합~
- typing.Any
- 심플 타입, 클래스
- typing.Optional, typing.Union
- 튜플, 매핑을 포함한 제네릭 콜렉션
더 있지만 제가 이번 스터디에서 소개할 타입들은 여기까지입니다. 

### Any
점진적 타입 시스템에서의 핵심은 요 Any 타입이다. 흔히 다이나믹 타입, 즉 동적 타입으로 많이 알려져있다.

타입 힌트 없이 작업할 때랑 똑같은 취급이다. 다이나믹하게 쓸 수 있슴.

얘는 내부적으로도 좀 특별한 놈인데, 모든 타입의 상위 타입인 object로 예를 들어보자.

```python
def some_func(val: object) -> object:
	return val * 2
```

object는 이게 안 된다. 왜냐면 얘는 `__mul__()` 매직 메서드가 구현되어있지 않기 때문이다. 최상단 타입이니까 그럴 수 있겠지.

근데 Any로 했다면 이게 된다. 왜 되냐, Any는 가장 최상단과 가장 최하단의 모든 계층에 있는 마법의 타입이기 때문이다. 양자역학의 타입인 것이다.

> 💀 뭔 개소리일까. 그딴게 세상에 어딨어. 
> 
> 그래서 좀 더 알아봤습니다.
> Any는 모든 타입을 대표할 수 있는 일종의 "슈퍼 타입"처럼 취급됩니다.
> 
> 얘는 타입 체커들에게 있어서 추상적으로 취급되는 거에요. 
> 
> 위에서 연산을 만나면 이 타입이 이 연산을 구현할 수 있는지로 타입을 체크한다고 얘기했습니다.
> 
> 타입체커는 Any를 만났을 경우 매직 메서드 구현 여부에 대해서 전혀 따지지 않도록 별도의 예외처리를 합니다.
> 
> 검사 결과를 무조건 가능. True로 만들어버리는 예외처리가 되어있다는 것. 사실상 검사 자체를 무력화하는 것이라고 보시면 될 것 같습니다.

 당연히 남발하면 개발 용이성을 떨어뜨리게 될테니 적절히 필요한 곳에 쓰도록 하자.

### 심플 타입과 클래스
심플 타입은 int, float, str, bytes 등 타입 힌트에 직접 쓸 수 있는 녀석들(클래스 같이 따로 정의해줄 필요 없이)을 말한다.

클래스에 대한 설명은 그냥 그 개념을 잘 아는 사람이라면 다 아는 내용들로만 있다. 추상 클래스는 유용한 타입 힌팅이 될 수 있다느니,.. 하위 클래스는 모든 상위 클래스와의 일관성을 가진다니(다형성) ... 등등 더 설명은 않겠다.

## Optional, Union Type
Optional은 아까 봤다. None과 Optional로 감싼 타입의 형태로 받을 수 있도록하는 녀석이다.

Union은 Optional 이랑 비슷한데 좀 더 넓게 줄 수 있는 놈이다. 예를 들면 `Union[int, float]` 같이 말이다. `Union[int, None]` `Optional[int]`는 같은 의미이다.

그외에 딱히 특별한건 없음

## Generic Collections
파이썬 컬렉션의 징그러운 특징을 아십니까. 컬렉션에 여러 유형의 값들을 담을 수 있다는 점을 말하는 것이다. 이게 실제로는 그다지 유용하지 않다. 컬렉션에 객체를 넣으면 나중에 해당 객체를 조작하고 싶을 가능성이 높으며, 일반적으로 이는 최소한 하나의 공통 메서드를 공유해야 함을 의미한다.

말이 안 되잖아 솔직히.

```python
a = ["1", 112, 19212390870]
for i in a:
	i.replace("1", "4")
```

이런식으로 짜면 어떻게 되는데. 당연 박살나겠지. 징그러운 문화다 이건. 책 쓴 아저씨도 이건 별로 안좋다고 했어. 컬렉션으로 데이터를 묶는 건 그 이유가 있어서 그렇다.(공통 처리) 이게 유용할 땐 알고리즘 풀 때나 아주 가끔 유용할 것 같다.(아닐 수도)

그래서 타입힌팅으로 컬렉션 내부 객체들의 타입을 강제할 수 있다.

```python
a: list[int] = [...]
```

이런 느낌으로 말이다.

## 보강 내용
점진적 타입 시스템에서는 서로 다른 두 가지 관점이 상호작용한다.

**덕 타이핑**: 스몰톡, 파이썬, js, 루비 등등이 이 관점을 채택했다.
- 객체에 대해서는 타입이 있지만, 변수에는 타입이 없다.
- 객체의 선언된 유형은 딱히 중요하지 않다고 생각하는 것들이라 보면 됨.
- 실제 지원하는 연산, 파이썬 같은 경우 매직 메서드 등의 메서드가 중요하다고 볼 수 있다.
- birdie.quak()이 가능하면 얜 duck 타입인 거임. 메서드가 중요하다는 맥락.
- 정의에 따르면 duck 타이핑은 객체에 대한 연산이 런타임에 시도될 때 적용된다.

**Nominal Typing**: C++, Java, C#에서 채택한 관점으로 타입힌팅 걸어놓은 Python에서 채택했다.
- 객체와 변수에 유형이 존재하는 것.
- 그러나 객체는 런타임에만 존재하고 타입 체커는 변수에 타입 힌트가 달린 코드에만 관심이 있음.
- 꼭 birdie: Bird로 선언된 변수에만 Duck 인스턴스를 할당할 수 있는 것.
- 그 아래는 그냥 거의 정적 타이핑의 소개와 동일하다.
- 좀 더 특이 사항을 말해보자면 타입을 결정하는 기준이 이름인 것이 명목적 타이핑이다. 같은 구조를 가지고 있더라도 이름이 다르면 다른 타입으로 구분되는 것이다.
- 이와 반대되는 개념으로 구조적 타이핑이라는 녀석도 있다. 얘는 컴파일러가 구조를 기반으로 타입을 분석하는 것이다. 명목적과 반대.
- 명목적 타이핑이 그러면 정적 타이핑이냐? 싶을 수 있는데 이는 완전히 다른 관점에서 봐야한다.
- 각각 타입 호환성과 타입 검사 시점이라는 서로 다른 영역에 초점을 맞추고 있다. 그러기에 비교 선상에 두기 어렵다.
- 정적 타이핑이면서 명목적 타이핑일 수도 있는 것. 위에서 나온 Java, C++들이 그러하다.

아래는 명목적 타이핑, 정적 타입 체킹, 런타임 동작을 대조하는 바보 같은 예시다.(책에서 그랫음)

```python
# birds.py
class Bird: pass

class Duck(Bird):
	def quack(self):
		print('Quack!') 
	
def alert(birdie):
	birdie.quack()  

def alert_duck(birdie: Duck) -> None:
	birdie.quack()
		
def alert_bird(birdie: Bird) -> None: 
	birdie.quack()
```

```python
# daffy.py
from birds import *

daffy = Duck()
alert(daffy)
alert_duck(daffy)
alert_bird(daffy)
```

이런 함수들이 있다고 해보자. 마이파이로 birds.py를 돌리면 뻑난다. 버드는 꽉 메서드가 없으니까.
daffy.py를 돌려도 당연히 같은 이유로 뻑난다.

근데 파이마이는 함수 자체의 동작에는 문제가 없다고 볼 것이다. 일단 돌아는 가잖아. 실제로 그냥 python3로 실행시켜보면 잘 된다.

```python
.../birds/ $ python3 daffy.py
    Quack!
    Quack!
    Quack!
```

우하하.

런타임에서는 파이썬이 진짜 1도 타입을 신경 안쓰는 걸 알 수 있다.