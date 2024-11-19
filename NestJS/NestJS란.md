---
aliases:
  - NestJS란?
  - NestJS란?
---
## NestJS?
NestJS는 JS 기반의 서버 사이드 앱 제작 프레임워크다.
TypeScript로 빌드되고 점진적 JS를 사용하는 것이 특징이다. 순수 JS 스타일로도 개발할 수 있다고 한다.

내부적으로는 Express를 사용하고 있는데 Fastify로도 갈아낄 수 있다는 모양이다. 어떤 상황에서 갈아끼는게 좋을 지는 좀 고민해봐야할 듯.

뭐 이런식으로 Node 프레임워크들을 추상화하여 갈아낄 수 있는 자유를 주기도 하지만, 같은 플랫폼 하에서 돌아가는 무수한 서드파티 모듈들을 낄 수 있는 자유를 주기도 한다.

소개에서 굉장히 자유를 언급하는데 얼마나 자유로운지는 직접 써보면서 체감해보자.


## 역사 & 철학.
역사와 철학 매우 중요하지. 어떤 언어, 프레임워크건 간에 해결하고 싶은 핵심 문제는 곧 역사와 철학에서 나온다고 본다. 잘 알면 더욱 더 날카롭게 쓸 수 있도록 해준다. 그런 면에서 공식 문서에서 소개하는 Nest의 간단한 역사와 철학을 알아보자.

Node js가 나오면서 js란 프론트, 백엔드 개발자들이 모두 같이 쓸 수 있는 영어 같은 존재가 됐다. 공식문서의 표현을 빌리자면, lingua franca. 

아무튼 그래서, js 사용량이 많아지면서 프론트 진영에서는 리액트, 뷰, 앵귤러 같은 여러 멋진 프로젝트들이 더욱 더 승승 장구 할 수 있었다. 이 친구들은 제작을 빠르게 만들어주고, 테스트 용이성이 훌륭하면서, 확장성이 좋았는데, 막상 node를 위한 라이브러리들을 보니까 영 야무진게 없었던 거다. 특히 **아키텍처**에 관련된 문제를 풀어줄만한 녀석 말이다!

그래서 Nest라는 프레임워크라는 게 나오게 됐다. Nest는 개발자들이 더 잘 개발하기 위해 다음에 집중한다.

**높은 테스트 용이성**, **확장 가능성**, **느슨한 결합**, **쉬운 유지보수** 모두 챙기는 것.

어찌보면 4개의 키워드 모두 합쳐서 쉬운 유지보수를 위한 프레임워크라고 할 수 있겠다.

이를 잘 챙기기 위한 Nest의 아키텍처는 Angular에 매우 영감을 받아 만들어졌다.

## 직접 한번 봐보자

```bash
$ npm i -g @nestjs/cli
$ nest new project-name
```

node는 잘 깔려있다고 가정한다. node 버전은 16 이상이면 된다.

위 코드를 입력하면 프로젝트가 생성된다.

src, test 외의 여러 파일, 디렉토리가 생성되는데 천천히 보자.

우선 src의 구성이다.

```
src
	- app.controller.spec.ts
	- app.controller.ts
	- app.module.ts
	- app.service.ts
	- main.ts
```

- `app.controller.ts`: 하나의 루트를 가지는 기본적인 controller 컴포넌트다.
- `app.controller.spec.ts`: 위 controller에 대한 단위 테스트다.
- `app.module.ts`: 앱의 루트 모듈이다.
- `app.service.ts`: 하나의 메서드를 가진 기본적인 service 컴포넌트다.
- `main.ts`: nest 앱 인스턴스를 만들기 위한 NestFactory 코어 함수를 실행하는 파일이다. spring을 사용자를 위한 비유를 해보자면 SpringApplication같은 거다.

이런 구성이 기본으로 되어있다. 기본적으로 mvc 패턴을 따르려고 하는 모습이다.

main 파일을 보면 다음과 같이 되어있다.

```js
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(process.env.PORT ?? 3000);
}
bootstrap();

```

이 함수를 통해서 nest 애플리케이션이 실행된다고 볼 수 있다. 보면 알다시피 PORT 환경변수에 값이 없으면 3000 포트를 디폴트로 쓰는 걸 알 수 있다.