JavaScript의 비동기 처리 패턴은 총 3번에 걸쳐서 진화했다.

Callback -> Promise -> async/await의 순서대로 진화하였다.

사실 셋의 기능은 거의 동일하다. 그럼 어째서 이렇게 변화를 거치게 된 것일까?
한번 세 패턴에 대해 공부하면서 생각해보자.

## Callback
[콜백 함수](https://developer.mozilla.org/ko/docs/Glossary/Callback_function)란, 다른 함수에 전달인자로 들어갈 수 있는 함수를 의미한다. 비동기 패러다임에서 Callback은 주로 비동기 작업의 흐름을 정의하기 위해서 주로 사용됐다.

```js
    function fetchData(callback) {
        setTimeout(() => {
            callback('Data loaded');
        }, 1000);
    }

    fetchData(data => {
        console.log(data); // 'Data loaded'
    });
```
다음과 같은 함수를 보자. fetchData 함수의 인자로 callback 함수를 받는다. 여기서의 callback은 fetchData에 화살표 함수로 정의된 인자다.

주로 이게 비동기 상황에서 어떻게 쓰였냐면:
```js
// 1. 파일 시스템 작업의 비동기 콜백
const fs = require('fs');

console.log('1. 파일 시스템 비동기 작업 시작');

// 파일 읽기 작업
fs.readFile('user.json', 'utf8', (err, userData) => {
    if (err) {
        console.error('파일 읽기 실패:', err);
        return;
    }

    // 파일 내용을 파싱
    const user = JSON.parse(userData);
    
    // 새로운 데이터로 파일 쓰기
    user.lastLogin = new Date();
    
    fs.writeFile('user.json', JSON.stringify(user, null, 2), (err) => {
        if (err) {
            console.error('파일 쓰기 실패:', err);
            return;
        }
        console.log('사용자 로그인 시간이 업데이트되었습니다.');
    });
});

// 2. HTTP 요청의 비동기 콜백
const https = require('https');

function fetchUserData(userId, callback) {
    console.log('\n2. HTTP 요청 시작');
    
    https.get(`https://api.example.com/users/${userId}`, (res) => {
        let data = '';
        
        // 데이터를 청크로 받음
        res.on('data', (chunk) => {
            data += chunk;
        });
        
        // 데이터 수신 완료
        res.on('end', () => {
            try {
                const user = JSON.parse(data);
                callback(null, user);
            } catch (error) {
                callback(error, null);
            }
        });
    }).on('error', (error) => {
        callback(error, null);
    });
}

// 3. 데이터베이스 작업의 비동기 콜백
const mysql = require('mysql');

const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'password',
    database: 'test_db'
});

function getUserOrders(userId, callback) {
    console.log('\n3. 데이터베이스 쿼리 시작');
    
    connection.query(
        'SELECT * FROM orders WHERE user_id = ?',
        [userId],
        (error, orders) => {
            if (error) {
                callback(error, null);
                return;
            }
            
            // 각 주문에 대한 상세 정보 조회
            let completedQueries = 0;
            const orderDetails = [];
            
            orders.forEach(order => {
                connection.query(
                    'SELECT * FROM order_items WHERE order_id = ?',
                    [order.id],
                    (error, items) => {
                        if (error) {
                            callback(error, null);
                            return;
                        }
                        
                        orderDetails.push({
                            ...order,
                            items: items
                        });
                        
                        completedQueries++;
                        if (completedQueries === orders.length) {
                            callback(null, orderDetails);
                        }
                    }
                );
            });
        }
    );
}

// 4. setTimeout을 사용한 비동기 작업
function simulateAsyncOperation(data, callback) {
    console.log('\n4. 비동기 작업 시뮬레이션 시작');
    
    setTimeout(() => {
        try {
            // 어떤 처리 수행
            const result = data.map(item => item * 2);
            callback(null, result);
        } catch (error) {
            callback(error, null);
        }
    }, 2000);
}

// 사용 예제
simulateAsyncOperation([1, 2, 3], (error, result) => {
    if (error) {
        console.error('작업 실패:', error);
        return;
    }
    console.log('처리된 결과:', result);
});

// 5. 여러 비동기 작업의 순차적 실행
function processUserData(userId) {
    console.log('\n5. 연쇄적 비동기 작업 시작');
    
    fetchUserData(userId, (error, user) => {
        if (error) {
            console.error('사용자 정보 조회 실패:', error);
            return;
        }
        
        getUserOrders(user.id, (error, orders) => {
            if (error) {
                console.error('주문 정보 조회 실패:', error);
                return;
            }
            
            fs.writeFile(
                `user_${userId}_report.json`,
                JSON.stringify({ user, orders }, null, 2),
                (error) => {
                    if (error) {
                        console.error('보고서 저장 실패:', error);
                        return;
                    }
                    console.log('사용자 데이터 처리 완료');
                }
            );
        });
    });
}
```

이 정도의 코드가 적절한 예시가 될 수 있다. 그러나 이 코드, 읽기 편한가?
지금이야 비동기 함수가 많지 않아서 그렇다치지만, 추가적으로 기능이 만들어지고 붙여지고 하는 상황을 고려해보자.

점점 코드의 depth가 늘어날 것이다. 이는 가독성 측면에서 매우 좋지 못하다. 
좀 더 직관적인 예시로 이해해보자.

```Js
// 콜백지옥체험  
class UserStorage {  
	loginUser(id, password, onSuccess, onError) {  
		setTimeout(() => {  
			if (  
				(id === "jay" && password === "1234") ||  
				(id === "coder" && password === "5678")  
			) {  
				onSuccess(id);  
			} else {  
				onError(new Error("not found"));  
			}  
		}, 2000);  
	}  
  
	// 사용자의 역할을 따로 네트워크 요청을 통해 받아와야하는 상황 가정  
	getRoles(user, onSuccess, onError) {  
		setTimeout(() => {  
			if (user === "jay") {  
				onSuccess({ name: jay, role: "admin" });  
			} else {  
				onError(new Error("no access"));  
			}  
		}, 1000);  
	}  
}  
  
const userStorage = new UserStorage();  
const id = prompt("enter your id");  
const password = prompt("enter your password");  
  
userStorage.loginUser(  
	id,  
	password,  
	(user) => {  
		userStorage.getRoles(  
			user,  
			(userWithRole) => {  
				alert(`Hello ${userWithRole.name}, you have a ${userWithRole.role} role`)  
			},  
			(error) => {  
				console.log(error;)  
			}  
		);  
	},  
	(error) => {  
		console.log(error);  
	}  
);
```

읽기 편한가? 계속 depth가 들어가니 어지럽지 않나? 개인적으로는 이 코드는 호흡이 너무 길다라고 느껴진다. 이렇게 `콜백 -> 콜백 -> ... -> 콜백` 의 형태로 가독성을 해치는 상황을 **콜백 지옥**이라고 부른다.

이런 불편함을 호소하는 사람들은 우리들 뿐만이 아니다. 굉장히 많은 사람들이 콜백 지옥으로 떨어졌으며 고통을 겪었다.

따라서 JS 진영은 2015년 ES6에서 Promise라는 새 스펙을 공개하게 된다.

## Promise?
Promise는 이러한 비동기 상황을 컨텍스트, 문맥적인 흐름으로만 관리하는 게 아니라 일급 객체, 즉 값으로서 비동기 상황을 컨트롤하기 위해 새로 생긴 스펙이다.

**비동기 동작**을 Promise 객체로 감싸, 메서드 체이닝으로 흐름 제어를 하도록 만든다.

이해하기 어렵다면 예제로 보자.

```js
// 콜백지옥을 promise로 바꾸기  
class UserStorage {  
	loginUser(id, password) {  
		return new Promise((resolve, reject) => {  
			setTimeout(() => {  
				if (  
					(id === "jay" && password === "1234") ||  
					(id === "coder" && password === "5678")  
				) {  
					resolve(id);  
				} else {  
					reject(new Error("not found"));  
				}  
			}, 2000);  
		});
	}  
  
	// 사용자의 역할을 따로 네트워크 요청을 통해 받아와야하는 상황 가정  
	getRoles(user) {  
		return new Promise((resolve, reject) => {  
			setTimeout(() => {  
				if (user === "jay") {  
					onSuccess({ name: jay, role: "admin" });  
				} else {  
					onError(new Error("no access"));  
				}  
			}, 1000);  
		});  
	}  
}  
  
const userStorage = new UserStorage();  
const id = prompt("enter your id");  
const password = prompt("enter your password");  
  
userStorage
.loginUser(id, password)  
.then(userStorage.getRoles)  
.then(user => userStorage.getRoles)  
.then(user => alert(`Hello ${user.name}, you have a ${user.role} role`));  
.catch(console.log);
```

흐름이 훨씬 명확하지 않나?? then이라는 메서드를 체이닝하여 해당 함수의 흐름에 대해서 명확하게 만들 수 있었다.

> 💡 then? catch?
> then: Promise의 작업이 성공했을 때 실행될 콜백
> catch: Promise의 작업이 실패했을 때 실행될 콜백

Promise는 일급 객체임을 상기하자. 물론 JS의 함수도 일급 객체인건 동일하지만, 값으로서 일급 객체를 사용한다라는 맥락적인 의미에서 좀 더 명확하게 떠올리자는 의미이다.

아무튼 간에 핵심은 콜백보다 훨씬 가독성이 좋아졌다는 것이다.

## Promise의 아쉬운 점
그러면 그냥 Promise를 잘 쓰면 되지 않을까? 도대체 뭐가 아쉬워서 async / await라는 키워드가 나오게 됐을까?

다음의 예시를 보자.

```js
// Promise 체이닝의 복잡성
getUserInfo()
    .then(user => {
        return getPermissions(user.id)
            .then(permissions => {
                return {
                    user,
                    permissions,
                    timestamp: Date.now()
                };
            });
    })
    .then(data => {
        // 중첩된 데이터 처리...
    });
```

Promise도 완전히 callback만 쓰는 거보다는 낫기야하지만 결국 callback을 사용하는 것이기 떄문에 체이닝 과정에서 복잡성이 생길 수 있게 된다. 비즈니스가 복잡한 상황이라면 결국 callback과 같은 문제가 발생할 수 있다는 말이다.

그러면 또 가독성도 안좋아지고 예외처리하기가 어려워진다.

도대체 어떻게 해야할까?

여러 자바스크립트 아저씨들이 머리를 열심히 굴린 결과, C#에서 영감을 받아 async/await라는 키워드를 창조하여 2017년에 발표하게 된다.

```js
// 동기 코드와 유사한 직관적인 구문
async function getUserData() {
    try {
        const user = await getUserInfo();
        const permissions = await getPermissions(user.id);
        return {
            user,
            permissions,
            timestamp: Date.now()
        };
    } catch (error) {
        console.error('Error fetching user data:', error);
        throw error;
    }
}
```

위의 코드를 그대로 async/await 구문을 이용하여 리팩토링 해봤다. 아주 좋지 아니한가

동기 코드와 매우 유사한 직관적인 구문을 만들 수 있게된다.
비동기 코드에서 동기적으로 동작해야하는 부분들은 `await` 키워드를 이용하여 순서를 보장할 수 있다. `await`가 붙은 비동기 함수가 모두 끝날 때 까지는 다음 코드로 움직이지 않는 것이다.
이렇게 해서 **정지**할 수 있는 함수는 `async` 키워드를 붙여줘야한다.

딱 봐도 감이 오지 않는가. 코루틴이다. `getUserData` 내부에서 `await`문을 만났을 때는(함수가 정지했을 때) 해당 `await` 함수가 다 끝나서 다시 `getUserData`가 돌 때까지 다른 함수가 동작할 수 있다.

```js
async function main() {
	try {
		const userData = getUserData()

		userMediaReader.read() // 비동기 함수. getUserData가 정지되면 동작할 것임.

		...

	} catch (error) {
		console.error('Error fetching user data:', error);
        throw error;
	}
}
```

getUserData의 내부에서 await를 만나면 io 작업이 마무리 될때까지 스레드는 놀게된다.(스레드 블로킹) 이 때 `userMediaReader.read()` 함수가 스레드의 점유가 없을 때 차지해서 작업을 수행할 수 있다는 말이다.

그 말은 스레드를 더 알차게 사용할 수 있다는 의미이다. 이런 루틴간의 컨텍스트 스위칭은 당연히 스레드간의 컨텍스트 스위칭보다 코스트가 더 싸다. 그렇기에 동시성 작업은 싱글 스레드 논블로킹이 오히려 더 효율적일 수 있다. 물론 IO 작업 위주일때만 그럴 것이지만!

아무튼 우리가 우아하게 동시성 프로그래밍을 하며 동기 흐름은 동기적으로 작성할 수 있게끔 해주는 멋진 문법을 배웠다.

이러한 변천사를 잘 알고 사용하는 것은 해당 문법을 더욱 더 날카롭게 쓸 수 있게해주는 무기가 되어줄 것이다. 오늘도 재밌게 공부했다.