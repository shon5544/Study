
## Repository 테스트를 하는 기준?
명확한 정답은 없다. 나의 경우 **Repository에 내가 직접 짠 메서드가 있을 경우**에 테스트를 해본다. Spring Data JPA에 사전에 준비된 메서드들, 이런 것들의 동작마저 테스트를 해봐야할까? 

그건 테스트 안 해봐도 된다고 생각한다. 기본 메서드에 대한 동작은 당연히 제대로 된 테스트를 거쳐서 라이브러리의 스펙으로 자리잡은 것이다. 그러나 내가 작성한 메서드 이름, 혹은 JPQL 등으로 만들어지는 쿼리들은 의도한대로 동작하지 않을 수 있다.

그렇기에 Repository에 메서드를 작성했다면 당연히 테스트 해봐야한다. 이번엔 h2를 이용하여 Repository의 실제 동작을 테스트한다면 어떻게 만들면 될까라는 주제로 글을 써보겠다.

## @DataJpaTest
jpa 관련 테스트를 할 때 쓰는 어노테이션이다.

**기본적인 특징**
- `@ExtendWith(SpringExtension.class)`가 내장되어있다. 
	- 스프링 환경에서 돌아갈 수 있도록 해주므로 Bean을 주입받을 수 있다.
- `@Transactional`이 적용되어있다. 
	- JUnit 환경에서 테스트를 한다면 SELECT를 제외한 모든 것이 롤백된다. 실제 커밋되지는 않는 다는 의미.
	- 따라서 `@DataJpaTest(showSql = true)` 프로퍼티를 넣어줘야 실제 쿼리가 보인다.
- `@AutoConfigureTestDatabase(replace=AutoConfigureTestDatabase.Replace`로 설정되어있다.
	- 인메모리 DB를 활용한다.
	- H2, DERBY, HSQL, HSQLDB 중 사용 가능한 in-memory DB에 자동으로 커넥션을 설정한다.
	- 물론 `replace=AutoConfigureTestDatabase.NONE`으로 값을 덮어 씌우면 인메모리 DB를 안 쓸 수도 있다.

## @SpringBootTest
- SpringBoot 관련 테스트를 할 때 쓰는 어노테이션이다.
- 주로 통합 테스트를 할 때 쓰인다.
- Spring Context 완전 구성에 필요한 모든 설정들을 로드해서 운영환경과 가장 유사한 테스트가 가능하다.
- 당연히 Repository 관련 테스트도 가능하다.

## @DataJpaTest vs @SpringBootTest
주요 차이는 다음과 같다.

**컨텍스트 로드**
- `@DataJpaTest`: ApplicationContext에 JPA에 필요한 것들만 불러온다.
- `@SpringBootTest`: 모든 Bean들을 불러온다. full context load라고 보면 된다.
- 때문에 당연히 `@DataJpaTest`가 더 빠르다.

**@Transactional**
- `@DataJpaTest`: 디폴트로 내장되어 있음.
- `@SpringBootTest`: 없다. Transactional 넣고 싶으면 사용자가 직접 추가해줘야함.

때문에 Repository 테스트에선 `@DataJpaTest`를 쓰는 것이 더 바람직하다고 볼 수 있을 것 같다.

### 번외. @DataMongoTest
- @DataJpaTest와 거의 유사하게 동작하나 Mongo 관련 컴포넌트를 위한 어노테이션이 있다.
- 똑같이 인메모리 db를 사용하고 그렇다.
- 이처럼 다른 플랫폼에 대해서도 유사품이 있다는 걸 확인했다. 있는 경우 잘 사용하면 될 것 같다.
- 없는 경우는 어쩔 수 없이 `@TestContainer`를 써야한다.
	- dynamoDB, elasticsearch 등.....

## 간단한 테스트 코드를 짜보자

Repository 관련 config는 resource 하위의 `application.properties` 혹은 `application.yml`을 만들어줘서 설정해주면 된다.

```yaml
# h2 인메모리 db로 테스트하기.
spring:
	datasource:
		url: jdbc:h2:mem:mytest:MODE=MySQL;DB_CLOSE_DELAY=-1 # datasource url 맞는 거로
		driverClassName: org.h2.Driver 
		username: sa # username
		password: # 패스워드
	h2:
		console:
			enabled: true
	jpa:
		hibernate:
			dialect: org.hibernate.dialect.MariaDBDialect # 하고 싶은 dialect로
			ddl-auto: create-drop # 하고 싶은 ddl로
		database-platform: org.hibernate.dialect.H2Dialect # 하고 싶은 dialect로
```

```java
public interface UserRepository extends JpaRepository<UserEntity, Long> {
	Optional<UserEntity> findByEmail(String email);
}
```

```java
@DataJpaTest(showSql = true)
public class UserRepositoryTest {

	@Autowired
	private UserRepository userRepository;

	@Test
	void Repository_연결_테스트() {
		// given
		UserEntity userEntity = new UserEntity();
		userEntity.setProfile(
			"shon",
			"shon5544@gmail.com",
			"Seoul"
		)

		// when
		UserEntity result = userRepository.save(userEntity);
		assertThat(result.getNickname()).isEqualTo("shon");
	}
}
```

원하는 결과를 얻을 수 있다.