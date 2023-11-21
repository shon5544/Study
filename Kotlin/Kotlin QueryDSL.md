
## 목차

-  [세팅 과정](#%EC%84%B8%ED%8C%85%20%EA%B3%BC%EC%A0%95)
	-  [1. build.gradle.kts](#1.%20build.gradle.kts)
	-  [2. QueryDslConfig](#2.%20QueryDslConfig)
- [사용](#%EC%82%AC%EC%9A%A9)
-  [각 Method들에서 신경쓸 점](#%EA%B0%81%20Method%EB%93%A4%EC%97%90%EC%84%9C%20%EC%8B%A0%EA%B2%BD%EC%93%B8%20%EC%A0%90)


## 세팅 과정
---
### 1. build.gradle.kts
```groovy
plugins {
	...
	kotlin("kapt")  version "1.6.10" // kapt 등록
}

// Kotlin QClass Setting  
kotlin.sourceSets.main {  
    println("kotlin sourceSets builDir:: $buildDir")  
    setBuildDir("$buildDir")  
}  
  
apply(plugin = "kotlin-kapt")

dependencies {
	...
	// querydsl  
	api("com.querydsl:querydsl-jpa:")  
	implementation("com.querydsl:querydsl-jpa:5.0.0")  
	implementation("com.querydsl:querydsl-apt:5.0.0")  
	implementation("javax.annotation:javax.annotation-api:1.3.2")  
	implementation("javax.persistence:javax.persistence-api:2.2")  
	annotationProcessor(group = "com.querydsl", name = "querydsl-apt", classifier = "jpa")  
	kapt("com.querydsl:querydsl-apt:5.0.0:jpa")
}
```

### 2. QueryDslConfig
```kotlin
package com.yourssu.assignmentblog.global.common.config  
  
import com.querydsl.jpa.impl.JPAQueryFactory  
import org.springframework.context.annotation.Bean  
import org.springframework.context.annotation.Configuration  
import javax.persistence.EntityManager  
import javax.persistence.PersistenceContext  
  
@Configuration  
class QueryDslConfig(  
    @PersistenceContext  
    private val entityManager: EntityManager  
) {  
  
    @Bean  
    fun jpaQueryFactory(): JPAQueryFactory {  
        return JPAQueryFactory(this.entityManager)  
    }}
```

사실 이 두 가지면 사용을 위한 세팅은 끝이다.

각 세팅 과정의 코드는 설명 안해도 이해할 수 있을 거라 믿는다.

## 사용
---
```kotlin
import com.yourssu.assignmentblog.domain.user.domain.QUser.user as qUser

@Repository  
class UserRepositoryImpl(  
    private val userJpaRepository: UserJpaRepository,  
    private val jpaQueryFactory: JPAQueryFactory  
): UserRepository {
	...

	private fun selectUsersByArgs(username: String?, email: String?, createdAtStart: LocalDate?, createdAtEnd: LocalDate?): List<User>? {  
	    val startDateTime: LocalDateTime? = createdAtStart?.atStartOfDay()  
	    val endDateTime: LocalDateTime? = createdAtEnd?.atTime(LocalTime.MAX)  
	  
	    return jpaQueryFactory.selectFrom(qUser)  
	        .where(  
	            eqUsername(username),  
	            eqEmail(email),  
	            greaterEqDate(startDateTime),  
	            lessEqDate(endDateTime),  
	            qUser.role.eq(Role.USER)  
	        )        
	        .orderBy(qUser.id.desc())  
	        .fetch()  
	}
}
```

jpaQueryFactory를 주입받아 사용한다. method chaining을 통해 원하는 동적 쿼리를 만드는 식이다.

## 각 Method들에서 신경쓸 점
---
굉장히 직관적인 편이라 그냥 보고 감으로 쓰면 얼추 다 맞는다.
여기서는 다 기재하지 않고 딱 알아야하는 것들만 기재한다.

- `selectFrom()`: QClass 들의 내부 엔티티를 인자로 받는다. 이걸 통해서 어떤 테이블을 참조할지 결정한다.

- `where()`: 평소에 알던 그 `where`와 똑같다. 응용해먹을 수 있는 점을 소개하겠다. 
	- 콤마(`comma`)로 `and` 연산을 표현할 수 있다. 
	- 각 조건부로 들어온 부분이 `null`이면 그냥 그 조건은 검사 안 한다.
		- 위 코드에서 `eqUsername` 함수는 `qUser.username.eq(유저 이름)`으로 진행되는데, 만약 유저 이름이 `null`이면 `null`을 `return` 하도록 되어있다. 그 경우 `where` 메서드는 유저 이름 조건은 쿼리에서 그냥 제외시켜버리고 간다.
		- 동적인 쿼리를 정말 쉽게 짤 수 있는 것이다.

- `fetch~()`: 마지막은 항상 fetch 혹은 fetchOne, fetchFirst 중 하나를 써야한다.
	- fetch(): List<엔티티>로 반환한다.
	- fetchOne(): 엔티티로 반환해준다. 값을 하나만 가져올 때 쓴다.
	- fetchFirst(): 엔티티로 반환해준다. 리스트로 나와야할 결과 값에서 가장 앞의 값을 반환한다.