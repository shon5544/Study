> 기본적으로 제 사견이 많이 들어가 있음을 이해해 주세요.
> 지적, 오탈자 지적 환영합니다

## 기본적으로 아키텍처는 살아 숨쉰다
초창기부터 자본을 최대한 투자하면서 하이엔드 스펙의 서버 장비를 맞추는 경우는 잘 없다. 특히 비즈니스가 얽혀있으면 굉장히 신중해진다.
추후 실사용자가 유치되면서 트래픽이 기본적으로 많이 증가해서 서버가 버겁거나, 다양한 이벤트와 같은 마켓팅 등으로 트래픽이 많이 쏠릴 것으로 보일 때 확장/개선을 하는 것이 일반적인 접근이다.
때문에 아키텍처란 쉽게 변하는 것이다. 이런 변화 속에서 기존 서비스 코드를 최대한 유지하면서 변경이 가능하도록 하는 것이 클린 아키텍처, DDD다.

> 물론 운영계획이 확실한 프로젝트의 경우 해당되는 것입니다. 
> 그냥 단순 1회성 프로젝트에 불과하다면 편한대로 만드는게 맞는 것 같습니다.

## 클린 아키텍처?
![](https://velog.velcdn.com/images/shon5544/post/7a99e8e4-28d6-40a0-907c-4930227da47b/image.png)

다 얘기하려면 너무 많이 시간을 써야한다. 클린 아키텍처의 구체적이고 실전적인 형태인 헥사고날 아키텍처로 자세한 예를 들면서 설명하겠다.

> 헥사고날 아키텍처를 설명하기 위한 자리가 아니므로 port와 adapter 등등 이런 것들은 설명하지 않을 것입니다. 
> 그저 아래 코드의 구조가 시사하는 것에 집중하는 것을 권장합니다. 
> 그래도 헥사고날이 궁금하다면 자료가 많으니 한번 읽고 오셔도 좋아요.

결론적인 정의를 이야기 하자면 이렇다. 외부 연결과 관련된 모든 모듈에 대하여 추상화하고, 내부 비즈니스(도메인)는 순수하게 유지하는 것이다. 

이렇게 되면 외부 연결이 아무리 바뀌어도 비즈니스 로직 만큼은 지킬 수 있다. 즉 **아키텍처를 변화 시키는 비용**이 압도적으로 줄어든다. 왜? 외부 연결에 대해서 수정하는게 너무 쉬워지니까. 이게 클린 아키텍처가 궁극적으로 해결하고 싶은 목표 중 하나라고 봐도 무방할 것이다.

단 주의해야할 것은 비즈니스 로직의 순수성은 그냥 챙겨지는 것이 아니라 정말 외부 연결과 연관이 없는 객체들의 협력으로 비즈니스를 풀어내야 챙겨지는 것이다. 개인적으로 DDD에서 이야기하는 도메인 모델 순수성이 없으면 클린 아키텍처의 목적성이 크게 퇴색된다고 본다.

순수한 도메인이 뭔말이냐, 그 어떤 외부 라이브러리/프레임워크와 연관된 것 없이 순수하게 유지되는 POJO 엔티티이다.

한번 보자.

```kotlin
@Document
class UserMongoEntity(
	...
)

@Service
class UserService(
	private val userRepository: UserMongoRepository
) {
	fun signUp(command: UserCreateCommand) {
		... 작업
		user: UserMongoEntity = command.toEntity()
		userRespository.save(user)
	}
}
```

이런 코드로 개발을 했다고 가정한다.
만약에 우리가 첨엔 스키마도 유연하고 나름 괜찮은 가격의 몽고 db로 db 스펙을 결정하고 개발을 한다고 하자. 

근데 얘가 확장되고 디벨롭 되면서 유연한 NoSQL 스키마를 택하는 것보다 복잡한 관계를 관리하기 쉽도록 RDB로 바꾸는 게 나아진 상황이 온 것이다. 그래서 JPA로 바꾸려는 데 바꿔야하는게..

UserEntity, UserService, UserCreateCommand, Repository.. 다 바꿔야한다. User만 해도 이런데 다른 도메인은 어떨까? 진짜 쉽지 않아진다.

반대로
```kotlin
// 엔티티
// 한 파일 안에 도메인 모델까지 정의되어 있으면 안 됨.
// 표현의 편의를 위해 하나의 마크다운 서식으로 표현했음을 이해해주세요.
@Document
class UserMongoEntity(
	...
)

@Entity
class UserJpaEntity(

)

class User(
	...
)
```

```kotlin
// 레포지토리
// 한 파일 안에 순수 interface까지 정의되어 있으면 안 됨.
// 표현의 편의를 위해 하나의 마크다운 서식으로 표현했음을 이해해주세요.
interface UserRepository {
	...
	fun save(user: User)
}

// JPA
@Repository
class UserRepositoryImpl(
	private val userJpaRepository: UserJpaRepository
): UserRepository {

	override fun save(user: User) {
		val toSave = UserJpaEntity(
			user.email
			...
		)
		userJpaRepository.save(toSave)
	}
}

interface UserJpaRepository: JpaRepository<UserEntity, Long>
```

```kotlin
@Service
class UserService(
	private val userRepository: UserRepository
): UserUseCase {

	override fun create(command: UserCreateCommand) {
		... 작업
		user: User = command.toEntity()
		userRespository.save(user)
	}
}
```

위의 서비스 코드를 보면 repository 관련해서 저게 무너질 것 같은가?? 안 무너진다. create라는 도메인 규칙은 그대로 살아남아 그 어떤 변경 없이도 멀쩡하다.

db 바꾸면 그냥 Impl 클래스 삭제하고 다시 만들면 그만이다. UserRepository 인터페이스를 구현하면 구현이 필요한 메서드도 정리된다.

db는 어떻게 보면 프로젝트에 있어서 정말 큰 구성 요소이다. 이것의 변경으로 인한 엄청난 사이드 이펙트를 Repository Impl 객체 하나 새로 바꿔주는 거로 끝냈다.

이 말은 뭐냐? 프로젝트 `스택에 대한 큰 결심 -> 개발`이 아니라 그냥 개발하면서 `db 뭐쓰지?`를 생각할 수 있는 거다.

개발하면서 상황을 보고 스택을 정할 수(+ 변경할 수) 있다는게 큰 의미를 시사한다.

나 같은 경우엔 서버 운영에 동아리 돈을 쓰고, 또 실제 마케팅까지 해서 사용자를 모을 프로덕트 개발을 하는 상황이 자주 있다보니 `도대체 무슨 스택으로 개발해야지/어떤 구조로 가야지 현 상황에서 제일 이득이지?` 라는 고민을 자주했다. 때문에 실제 개발은 오랫동안 못 나갈 때가 종종 있는데 이렇게 구조를 잡으면 유연한 대처가 가능하기에 개발을 바로 나갈 수 있다.

리캡해보자. 

**이게 가능한건** 
- 비즈니스 로직에서 순수한 도메인 엔티티를 썼기 때문
- 외부 연결(DB 등등)에 대해서 추상화 되었기 때문

크게 두 가지 이유라고 할 수 있다. 더 신경을 쓴다면 **패키지 구조** 같은 것도 **상황에 맞도록** **많이 생각을 해봐야하지만** 아무튼 **클래스간 의존 관계가 느슨한 것에 의미가 있다.**

## DDD?
도메인 주도 디자인(Domain Driven Design)이다. 뭐냐? 너무 어렵게 생각할 거 없다. 도메인에 집중하여 이러한 도메인이 주도적으로 비즈니스의 흐름을 만들어내는 것이라고 생각하면 된다.

흔히 우리가 사용하는 서비스는 Application Service이다. 여기에 비즈니스 로직을 다 때려박는 식으로 개발을 종종한다. 

근데 이건 전혀 객체지향적이지 않다. 그냥 모든 비즈니스 로직이 하나의 메서드에서 돌아가고 있다면 그건 그냥 절차지향적인 메서드에 불과하다. 

절차지향? 이게 나쁠 게 뭐 있나? 싶을 수 있지만 나는 운영 계획이 있는 프로젝트 + 객체지향 언어를 위한 프레임워크를 사용할 땐 나쁘다고 생각한다. 결국 객체지향 베이스에서 객체지향이란 유지보수성과 연결되는 이야기이기 때문이다.

![](https://velog.velcdn.com/images/shon5544/post/02fb98fd-89c0-4e32-b420-6d46358b9a9e/image.png)


스프링이랑 jpa 처음 배우고 짰었던 코드다. 비즈니스 흐름이 잘 읽히나? 잘 읽힌다면 주석을 지우고 읽어도 잘 보일 것 같은가? 가독성이 좋지 못하다.

또한 다양한 세부 관심사가 한 메서드 안에 흩어져 응집력이 없다. 이 말은 뭐냐, recipe 객체 세팅을 하려면 위의 `editRecipe` 메서드를 수정해야하고, ingredient 재등록 로직을 수정해야한다면 `editRecipe` 메서드를 수정하고? step 재등록을 수정하려면 `editRecipe`를 수정하고...?

객체지향 SOLID 5원칙 중에는 SRP(단일 책임 원칙)이라는 것이 있다. 이건 하나의 클래스엔 하나의 책임이 있어야한다는 말이지만 조금 실전적으로 풀어서 이야기하자면 

**클래스의 내용이 바뀌는 이유는 단 하나여야한다**로 해석할 수 있다. 이렇게 해야하는 이유는 유지 보수성이다. 클래스가 지고 있는 책임이 적어야 변경하기 쉽고, 변경으로 인한 사이드 이펙트가 적기 때문이다.

DDD에서는 이런 객체지향적인 특징을 살릴 수 있도록 다양한 방법을 제안한다. 위에서 간단히 언급했던 도메인 엔티티에 비즈니스 로직을 위임하고 이러한 도메인 모델들의 **협력**으로 비즈니스를 풀어내도록 유도한다.

> 도메인 모델은 꼭 데이터 집합만을 나타내지 않습니다. 
> 데이터의 집합과 비즈니스 규칙을 함께 묶은 것까지 해서 도메인 모델이라고 부르곤 합니다.
> 도메인 모델이란 행위와 데이터를 둘 다 아우르는 도메인의 개념 모델입니다.(출처: 위키피디아)

또한 여기서 도메인 모델에 위임하기 힘든 로직 같은 경우 도메인 서비스라는 새 객체를 만들어서 거기서 로직을 수행한다. 뭔 말인지 이해하기 힘들겠지만 아래에서 구체적으로 정리합니다.

```java
// 이전 코드

// recipe 객체 세팅
recipe.setTitle(recipeFromDTO.getTitle());
recipe.setThumbnail(recipeFromDTO.getThumbnail());

// IngredientList, StepList가 지연로딩으로 잡혀있기 때문에 get하는 시점에서 쿼리 발생.
// 컬렉션 페치 조인은 하지 않는다. 성능과부화와 차후 페이징기능을 고려하고 있기 때문.
recipe.getIngredientList().clear(); // 재료 삭제. ingredient에 orphanRemoval 적용되어있음.
recipe.getStepList().clear(); // 단계 삭제. step에 orphanRemoval 적용되어있음.

// ingredient 재등록
List<Ingredient> ingredientList = recipeFromDTO.getIngredients().stream()
	.map(ingredientGeneralReqDTO -> ingredientGeneralReqDTO.toEntity(recipe))
    .collect(Collectors.toList());
ingredientRepository.saveAll(ingredientList);

log.info("ingredientList 저장 끝남");

// step 재등록
List<Step> stepList = recipeFromDTO.getStepList().stream()
	.map(stepGeneralReqDTO -> stepGeneralReqDTO.toEntity(recipe))
    .collect(Collectors.toList());
stepRepository.saveAll(stepList);

log.info("stepList 저장 끝남");

return recipe;

```

```java
// 바꾼 코드
String title = recipeFromDTO.getTitle();
String thumbnail = recipeFromDTO.getThumbnail();

recipe.setUp(title, thumbnail);

recipe.subDomainClear();

ingredientRegister.register(recipeFromDTO.getIngredients())

stepRegister.register(recipeFromDTO.getStepList())

return recipe;
```

바꾸고 싶은 것이 더 있지만 기존코드와의 차이를 알 수 있도록 핵심 제외 다 그대로 두었다.

- recipe: 도메인 모델
	- 실제 영속 엔티티를 도메인 모델로 두는 것은 논란이 많지만 일단은 도메인 모델입니다.
- ingredientRegister: 도메인 서비스

정도의 느낌으로 보면 된다.

**이렇게 바꾼 것이 주는 효과**
- 응집력 올라감: 비슷한 관심사의 로직들끼리 모이게 된다. 전처럼 다른 관심사의 구현이 혼재되지 않게 됩니다.
	- 수정하기 쉬워짐: 위에서 얘기한 하나의 클래스는 하나의 이유로 인해 수정되어야한다가 잘 지켜진다. 사이드 이펙트는 최소화된다.
	- 비즈니스 흐름의 가독성이 좋아진다: 우리가 기존에 알던 application service는 일종의 Facade로 동작한다. 그럼으로 인해 비즈니스 흐름이 잘 읽히게 된다.

이런 식으로 굉장히 객체지향적으로 코드를 짤 수 있게 된다. DDD에서는 이렇게 도메인 모델에 응집력 있게 모인 것을 Rich Domain model(풍부한 도메인 모델)이라고 부른다.

아무튼, 이렇게 함으로써 전체적인 유지보수 성이 올라간다 DDD에서는 이것 뿐만이 아니라 다양한 방법을(애그리거트, 순수한 도메인 모델 등등.....) 통해 유지보수성을 챙긴다.

궁극적으로 나는 이 DDD를 잘 챙김으로서 객체지향성을 매우 올릴 수 있다고 생각한다.

때문에 클린 아키텍처와 DDD를 함께 쓰면 유지보수하기 아주 훌륭한 서비스를 만들 수 있는 것이다.

## 부가적인 이점(클린 아키텍처와 DDD)
- Testability가 올라간다.
- 당연히 유연한 구조는 테스트 환경에도 쉽게 적응한다.
- 따라서 커버리지를 유의미하게 챙길 수 있다.

## 주의점
- 두 개 모두 초기 개발 비용이 높은 편이다. 손익분기점이 존재할 것이다.
	- 위에서 언급했듯 1회성 혹은 단기 프로젝트에는 오히려 좋지 않다.
- 너무 과하게 컨셉을 도입해 오버엔지니어링이 되지 않도록 조심해야한다.
	- 클린 아키텍처, DDD 모두 사람이 생각해낸 논리적인 방법론이다. 
	- 상황에 맞도록 컨셉을 차용하는 것은 개발자의 센스다.
	- 적절하게 이용해보자.
- 상당히 생소할 수는 있기 때문에 어느정도 익숙한 개발자들끼리 있을 때 이러한 방법론을 쓰는게 좋다.

## 그럼에도 불구하고.
- 각 방법론이 해결하고 싶은 문제를 공감하여 어느정도 찬양론자가 된 것 같긴하다.
- 내가 생각하는 만큼 다른 사람들에게도 좋게 느껴질진 잘 모르곘다.
- 그럼에도 불구하고 나는 이 두 가지 방법을 굉장히 추천하고 싶다.
- 장기 운영할 프로젝트 유지보수성은 상당히 중요해진다. 
	- 6년정도의 레거시가 쌓인 코드 베이스에서 feature를 개발해본적이 있었는데,(별로 큰 feature는 아니었지만) 이 때 유지보수하는 게 괴로웠다.
	- 물론 내가 괴로웠던 건 문서화가 제대로 되어있지 않은 것도 컸다.
	- 그러나 진짜는 사이드 이펙트가 많은 코드를 고치는 것이었다.
	- 그런 코드는 개발하긴 쉽지만 수정하긴 어렵다.
- 위에서 이야기 했듯이 아키텍처란 살아 숨쉬는 것이므로 언젠가는 무조건 바뀐다.
- 그렇기에 다들 이러한 제안에 대해서 한번씩 고민해보면 좋을 것 같다.