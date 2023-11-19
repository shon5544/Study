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
@Repository  
class UserRepositoryImpl(  
    private val userJpaRepository: UserJpaRepository,  
    private val jpaQueryFactory: JPAQueryFactory  
): UserRepository {
	...
	override fun findUsers(userDto: GetUsersRequestDto): List<User>? {  
	    val username = userDto.username  
	    val email = userDto.email  
	    val createdAtStart = userDto.createdAtStart  
	    val createdAtEnd = userDto.createdAtEnd  
	  
	    return selectUsersByArgs(username, email, createdAtStart, createdAtEnd)  
	}
}
```