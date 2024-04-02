
## SUT
```java
@DisplayName("유저 북마크 테스트")
@Test
void test_user_bookmark() {
	// given
	User sut = User.builder()
			.bookmark(new ArrayList<>())
			.build();

	// when
	sut.toggleBookmark("my-link");

	//then
	boolean result = sut.hasBookmark("my-link");
	assertThat(result).isTrue();
}
```
- 테스트 하려고 하는 대상.
- 여기선 user가 SUT다.

## BDD
- 행동 기반 개발
- 유저 스토리를 강조하는 기법
- given-when-then이 BDD에 속해있다.

## 상태 기반 테스트
```
```
- 내가 평소에 항상하는 테스트.
- 어떤 함수에 데이터를 넣고, 그 함수의 결과값으로 나온 데이터를 비교하여 테스트 여부를 결정하는 테스트.

## 행동 기반 테스트(상호 작용 테스트)
> `verify(sut).markModified();`
- 위와 같은 방식이 행동 기반 테스트이다.
- 어떤 sut의 함수가 호출되었는지 확인하는 테스트이다.
- 이건 별로 좋지 않다. 왜? sut의 내부 구현을 뜯어보는 테스트이기 때문.
- 캡슐화가 깨지는 것이다 이건.
- 그래서 지양해야하는 기법.

## 테스트 픽스처
```java
private User sut;

@BeforeEach
void setup() {
	sut = User.builder()
	...
}

@DisplayName("test")
@Test
void test1() {
	// given
	...
	// when
	...
	// then
	...
}
```
- 테스트에 필요한 사전 자원이라고 생각하면 된다.
- 이 경우 User sut가 테스트 픽스처가 된다.

## 비욘세 규칙
> 네가 나를 좋아했다면, 프로포즈를 했어야지
> 상태를 유지하고 싶었다면, 테스트를 만들었어야지
- 대중적인 규칙은 아님
- 유지하고 싶은 정책이나 규칙이 있으면 알아서 테스트를 만들었어야 한다는 얘기다.
- 뭔 얘기인지는 아래에서 다룬다.

## 테스트는 일종의 정책 / 계약이다.
- 예를 들어보자. "어 이거 수정해도 되겠네, 이 부분 수정해도 되나요?"라는 질문이 들어왔다 해보자.
- 한번쯤은 OK, 편하게 알려줄 수 있지. 근데 다른 팀원이 들어오고, 같은 질문을 물어보고.. 이게 100번 반복된다고 해보자.
- 머리 터진다 진짜.
- 혹은 내가 휴가를 가서 답장을 할 수 없는 상황이라고 해보자.
- 팀원이 내 코드와 사이드 이펙트가 생기는 코드를 PR 냈고 문맥을 파악하지 못한 다른 팀원이 이를 머지했다고 하자.
- 큰일 나는거다. 그냥..
- 테스트 코드가 잘 있다면 작업 완료하고 테스트 코드 실행시켜보면 되는 거다. 되는지 안 되는지 테스트 코드는 정답을 알고있다.
- 팀원들은 내가 쓴 테스트 코드를 기반으로 어떻게 할지 질문없이 갈 수 있다.
- 따라서 테스트 코드는 내 코드에 대한 나와 팀원들간의 일종의 정책 혹은 계약이다.

## Testabllity
- 소프트웨어가 테스트 가능한 구조인지에 대한 것이다.
- 나중에 따로 문서를 파서 기록할 예정

## 테스트 더블
- 인증 메일을 날리는 코드를 테스트한다고 하자.
- 테스트 한번 할 때마다 유저한테 진짜 메일을 날려야할까?
- MailSender를 진짜배기가 아니라 짝퉁을 넣어서 테스트를 보는 것. 이것이 바로 테스트 더블이다.
- 가짜 대역을 넣어주는 것이다.
- 이건 가짜 대역이 어느정도의 역할이 있느냐에 따라 다양한 분류로 나뉘어진다.

```java
public class Subway {
	private Chef chef = new Beomsu();

	private Bread bread = new FlatBread();
	private Cheese cheese = new Mozzarella;
	private Vegetable vegatable = new Olive();
	private Sauce sauce = new Ranch();
}
```


```java
public class Subway {
	private Chef chef;

	private Bread bread;
	private Cheese cheese;
	private Vegetable vegatable;
	private Sauce sauce;

	public Subway(
		Chef chef,
		Bread bread,
		Cheese cheese,
		Vegetable vegatable,
		Sauce sauce
	) {
		this.chef = chef;
		this.bread = bread;
		this.cheese = cheese;
		this.vegetable = vegetable;
		this.sauce = sauce;
	}
}
```

```java
@Component
@RequiredArgsConstructor
public class Subway {
	private final Chef chef;

	private final Bread bread;
	private final Cheese cheese;
	private final Vegetable vegatable;
	private final Sauce sauce;
}
```

```java
@Component
public class UserLoginManager {
	...

	public User login(
		String id, 
		String password,
		LocalDateTime dateTime
	) {
		...생략
		user.lastLoginStamp = dateTime;
		...생략

		return user;
	}
}
```

```java
public class UserLoginTest {

	...

	@Test
	void loginTest() {
		// given
		UserLoginManager sut = new UserLoginManager();
		LocalDateTime dateTime = LocalDateTime.now();

		User user = User.builder()
				...
				.build();
				
		User expectedResult = User.builder()
				...
				.lastLoginStamp(dateTime);
				

		// when
		User result = sut.login(아이디 비번 정보, dateTime);

		// then
		assertThat(result, expectedResult);
	}
}
```

```java
public class UserLoginTest {

	...

	@Test
	void loginTest() {
		// given
		UserService sut = new UserService();
		LocalDateTime dateTime = LocalDateTime.now();

		User user = User.builder()
				...
				.build();
				
		User expectedResult = User.builder()
				...
				.lastLoginStamp(dateTime);
				

		// when
		User result = sut.login(user, dateTime);

		// then
		assertThat(result, expectedResult);
	}
}
```


```java
public interface DateTimeHolder {
	LocalDateTime now();
}
```

```java
public class DateTimeImpl implements DateTimeHolder {
	@Override
	public LocalDateTime now() {
		return LocalDateTime.now();
	}
}
```

```java
public class TestDateTime implements DateTimeHolder {
	@Override
	public LocalDateTime now() {
		return LocalDateTime.of(
			특정 날짜 설정
		)
	}
}
```

```java
@Component
public class UserLoginManager {
	
	public User login(
		String id, 
		String password, 
		DateTimeHolder dateTime
	) {
		...생략
		user.lastLoginStamp = dateTime.now();
		...생략

		return user;
	}
}
```

```java
@Service
@RequiredArgsConstructor
public class UserService {
	...
	private final UserLoginManager loginManager;
	private final DateTimeHolder dateTime;

	public User login(유저 정보 리퀘스트) {
		...
		return loginManager.login(
			id,
			password,
			dateTime
		);
	}
}
```

```java
public class UserServiceTest {

	@Test
	void loginTest() {
		// given
		UserLoginManager loginManager = new UserLoginManager();
		DateTimeHolder dateTime = new TestDateTime();
		유저 정보 리퀘스트 request = new 유저 정보 리퀘스트(아디, 비번);
		
		UserService sut = new UserService(
			loginManager,
			dateTime
		);

		User expectedResult = User.builder()
			...
			.build();
		
		// when
		User result = sut.login(request);
		
		// then
		assertThat(result, expectedResult);
	}

}
```

```java
public class UserLoginTest {

	...

	@Test
	void loginTest() {
		// given
		UserLoginManager sut = new UserLoginManager();
		DateTimeHolder dateTime = new TestDateTime();

		User user = User.builder()
				...
				.build();
				
		User expectedResult = User.builder()
				...
				.lastLoginStamp(dateTime);
				

		// when
		User result = sut.login(user, dateTime);

		// then
		assertThat(result, expectedResult);
	}
}
```

```java
public class FastFood {
	...
	Subway subway = new Subway(
		new Beomsu(
			new Head(),
			new Body(),
			new Hand(),
			new Leg()
		),
		new Mozzarella(),
		new Olive(),
		new Ranch(),
	);
}
```

```java
@Component
public class Subway {
	private Chef chef;

	private Bread bread;
	private Cheese cheese;
	private Vegetable vegatable;
	private Sauce sauce;

	public Subway(
		Chef chef,
		Bread bread,
		Cheese cheese,
		Vegetable vegatable,
		Sauce sauce
	) {
		this.chef = chef;
		this.bread = bread;
		this.cheese = cheese;
		this.vegetable = vegetable;
		this.sauce = sauce;
	}
}
```

```java
@Component
public class Beomsu {
	...
}
```

```java
@Component
@RequiredArgsConstructor
public class FastFood {
	...
	// 이러면 Subway를 받는 생성자가 있는거랑 다름 없어짐.
	// = 바로 주입 받을 수 있다!
	private final Subway subway;
}
```

```java
@Configuration
public class FastFoodConfiguration {

	@Bean
	public Subway subwayBeomsuBean() {
		Beomsu beomsu = new Beomsu(...);
		Bread bread = new FlatBread();
		...

		return new Subway(
			beomsu,
			bread,
			...
		)
	}

}
```

```Java
@Bean  
public PasswordEncoder passwordEncoder() {  
    return new BCryptPasswordEncoder();  
}
```

```Java
@Service
public class UserService {
	...
	public void signup() {
		...
	}

	public void login() {
		...
	}

	public void withdraw() {
		...
	}
}
```

```Java
@Component 
@Aspect 
public class MyAspect { 

	@Around(value = "execution(*io.security.corespringsecurity.aopsecurity.ExampleService.*(..))") 
	public Object logPerf(ProceedingJoinPoint pjp) throws Throwable { 
		StopWatch stopWatch = new StopWatch(); 
		
		stopWatch.start(); 
		Object retVal = pjp.proceed(); 
		stopWatch.stop(); 
		
		System.out.println(stopWatch.prettyPrint()); 
		
		return retVal; 
	} 
}
```


