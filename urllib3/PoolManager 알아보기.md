

## PoolManager
`PoolManager.py` 에 있는 클래스. [[RequestMethods]]를 상속했다.
[[RequestMethods]]를 상속한 것으로 이것이 요청을 서버로 보내기 위한 모듈임을 알 수 있다.

주석으로 설명된 이 클래스의 정의에 대해서 보면:
> 당신(클라이언트)에게 필요한 커넥션 풀을 투명하게 추적하면서 임의의 요청을 허용합니다.

##### 궁금점.
- 여기서 이야기하는 투명하게란 무엇일까?

##### 좀 자세하게 들어가보면:
PoolManager 클래스는 HTTP 요청을 처리하고 연결을 관리하는 데 사용된다. 이 클래스는 요청을 보낼 때마다 필요한 커넥션 풀을 자동으로 관리하기도 한다.

##### 주요 기능:
1. 요청에 대한 커넥션 풀을 유지 관리.
2. 요청 시마다 새로운 커넥션 풀을 만들어 할당.
3. 커넥션 풀의 수를 제한하고 최근에 사용된 커넥션 풀을 버림.
4. 요청에 대한 헤더를 처리하고 기본적으로 포함.
5. 요청을 보내고 응답을 처리.
6. 리다이렉트를 관리하고 재시도 로직을 구현합니다.

요약하면, PoolManager 클래스는 HTTP 요청의 연결 관리와 관련된 모든 작업을 담당하는 중요한 클래스입니다.

## 필드
- `proxy: Url | None = None`
- `proxy_config: ProxyConfig | None = None`
- `connection_pool_kw: typing.Any`
- `pools: RecentlyUsedContainer[PoolKey, HTTPConnectionPool]`
- `pool_classes_by_scheme: typing.Dict | typing.Mapping`
- `key_fn_by_scheme: `

1. `proxy`: 프록시 서버의 URL을 저장하는 필드. 이 필드를 통해 요청이 프록시를 통해 전달될지 직접 목적지 서버로 전달될지 결정됨.
    
2. `proxy_config`: 프록시 설정을 나타내는 객체를 저장하는 필드. 프록시 서버의 인증 정보 및 연결 제한 등과 같은 프록시 설정이 이 필드에 저장됨.
    
3. `connection_pool_kw`: 커넥션 풀 생성에 필요한 추가 매개변수를 저장하는 딕셔너리. 이 필드를 통해 커넥션 풀이 생성될 때 사용되는 매개변수를 설정할 수 있음.
    
4. `pools`: 커넥션 풀을 저장하는 딕셔너리임. 각 풀은 호스트, 포트, 프로토콜 등의 정보를 키로 사용하여 관리됨.
    
5. `pool_classes_by_scheme`: 프로토콜별 커넥션 풀 클래스를 저장하는 딕셔너리. 프로토콜에 따라 다른 커넥션 풀 클래스가 사용될 수 있음.
    
6. `key_fn_by_scheme`: 프로토콜별 키 생성 함수를 저장하는 딕셔너리임. 프로토콜에 따라 다른 키 생성 함수가 사용될 수 있음.

## 메서드
### `__init__`
```python
def __init__(
	self,
	num_pools: int = 10,
	headers: typing.Mapping[str, str] | None = None,
	**connection_pool_kw: typing.Any,
) -> None:
	super().__init__(headers)
	self.connection_pool_kw = connection_pool_kw
	self.pools: RecentlyUsedContainer[PoolKey, HTTPConnectionPool]
	self.pools = RecentlyUsedContainer(num_pools)
	
	# Locally set the pool classes and keys so other PoolManagers can
	# override them.
	self.pool_classes_by_scheme = pool_classes_by_scheme
	self.key_fn_by_scheme = key_fn_by_scheme.copy()
```

- `num_pools`, `headers`, `connection_pool_kw` 세 개의 매개변수를 받음.
-  `headers`는 모든 요청에 포함될 헤더를 나타냄.
-  `connection_pool_kw`는 추가적인 매개변수로, 새로운 `ConnectionPool` 인스턴스를 생성하는 데 사용.
-  `num_pools`는 캐시할 커넥션 풀의 수를 나타냄.
-  `pools`는 `RecentlyUsedContainer[PoolKey, HTTPConnectionPool]` 타입의 객체로, 커넥션 풀을 저장하는 컨테이너임.
-  `pool_classes_by_scheme` 및 `key_fn_by_scheme` 변수에 풀 클래스와 키 함수를 설정합니다. (다른 `PoolManager`에서 이러한 변수를 재정의할 수 있도록 함)
-  부모 클래스의 생성자를 호출하여 초기화합니다.
-  `__enter__()` 및 `__exit__()` 메서드를 오버라이드하여 컨텍스트 관리를 지원합니다.

## `clear`
```python
def clear(self) -> None:

	"""
	Empty our store of pools and direct them all to close.

	This will not affect in-flight connections, but they will not be
	re-used after completion.
	"""
	self.pools.clear()
```

- `clear()` 메서드는 PoolManager에 저장된 모든 커넥션 풀을 비움.
- 이 메서드를 호출하면 PoolManager가 관리하는 모든 커넥션 풀이 비워지며, 비워진 풀은 더 이상 사용되지 않습니다.
- 더 이상 새로운 요청을 처리하지 않을 때 사용되는 듯(gpt 피셜).

## `connection_from_host`
```python
...
	def connection_from_host(
        self,
        host: str | None,
        port: int | None = None,
        scheme: str | None = "http",
        pool_kwargs: dict[str, typing.Any] | None = None,
    ) -> HTTPConnectionPool:
        """
        Get a :class:`urllib3.connectionpool.ConnectionPool` based on the host, port, and scheme.

        If ``port`` isn't given, it will be derived from the ``scheme`` using
        ``urllib3.connectionpool.port_by_scheme``. If ``pool_kwargs`` is
        provided, it is merged with the instance's ``connection_pool_kw``
        variable and used to create the new connection pool, if one is
        needed.
        """

        if not host:
            raise LocationValueError("No host specified.")

        request_context = self._merge_pool_kwargs(pool_kwargs)
        request_context["scheme"] = scheme or "http"
        if not port:
            port = port_by_scheme.get(request_context["scheme"].lower(), 80)
        request_context["port"] = port
        request_context["host"] = host

        return self.connection_from_context(request_context)
```

- 매개변수로 호스트(`host`), 포트(`port`), 스킴(`scheme`) 및 커넥션 풀에 대한 추가 매개변수(`pool_kwargs`)를 입력으로 받음.
- 만약 호스트가 주어지지 않았다면, `LocationValueError`를 발생시킴.
- 커넥션 풀에 대한 설정을 담은 `pool_kwargs`와 인스턴스의 `connection_pool_kw` 변수를 병합하여 새로운 요청 컨텍스트(`request_context`)를 생성함.
	- 병합을 한다는 건 `connection_pool_kw`가 가변 매개변수
- 요청 컨텍스트에 스킴이 주어지지 않았다면 기본값으로 "http"를 설정.
- 만약 포트가 주어지지 않았다면, 스킴에 따라 기본 포트를 가져와서 설정함.
- 최종적으로 요청 컨텍스트를 사용하여 `connection_from_context` 메서드를 호출하여 커넥션 풀을 가져옴.

## `connection_from_context`
```python
def connection_from_context(
	self, request_context: dict[str, typing.Any]
) -> HTTPConnectionPool:

	"""
	Get a :class:`urllib3.connectionpool.ConnectionPool` based on the request context.

	``request_context`` must at least contain the ``scheme`` key and its
	value must be a key in ``key_fn_by_scheme`` instance variable.
	"""

	if "strict" in request_context:
		warnings.warn(
			"The 'strict' parameter is no longer needed on Python 3+. "
			"This will raise an error in urllib3 v2.1.0.",
			DeprecationWarning,
		)
		request_context.pop("strict")

	scheme = request_context["scheme"].lower()
	pool_key_constructor = self.key_fn_by_scheme.get(scheme)
	if not pool_key_constructor:
		raise URLSchemeUnknown(scheme)	
	pool_key = pool_key_constructor(request_context)

	return self.connection_from_pool_key(pool_key, request_context=request_context)
```
주어진 요청 컨텍스트에 기반하여 `HTTPConnectionPool`을 가져오는 역할을 함.

- 주어진 `request_context`에는 적어도 `scheme` 키가 포함되어 있어야 함. 이 키의 값은 `key_fn_by_scheme` 인스턴스 변수의 키여야 함.
    
- 만약 `request_context`에 "strict" 키가 포함되어 있다면, 이것은 더 이상 필요하지 않으며 Python 3+에서는 필요하지 않다는 경고가 발생한다. 추가로 이 키는 제거됨.
    
- 주어진 `request_context`에서 `scheme` 값을 가져와서 소문자로 변환.
    
- `pool_key_constructor` 변수를 사용하여 `scheme`에 해당하는 키 함수를 가져옴. 이 키 함수는 `pool_key_constructor` 딕셔너리에 등록된 것이어야 한다.
    
- `pool_key_constructor`를 사용하여 `request_context`에서 생성된 풀 키를 가져온다.
    
- `connection_from_pool_key` 메서드를 사용하여 가져온 풀 키를 기반으로 `HTTPConnectionPool`을 가져온다. 이때 `request_context`를 전달하여 필요한 경우 추가적인 정보를 제공할 수 있음.

## `connection_from_pool_key`
```python
def connection_from_pool_key(
	self, 
	pool_key: PoolKey, 
	request_context: dict[str, typing.Any]
) -> HTTPConnectionPool:

	"""
	Get a :class:`urllib3.connectionpool.ConnectionPool` based on the provided pool key.
	
	``pool_key`` should be a namedtuple that only contains immutable objects. At a minimum it must have the ``scheme``, ``host``, and ``port`` fields.

	"""

	with self.pools.lock:

		# If the scheme, host, or port doesn't match existing open
		# connections, open a new ConnectionPool.
		pool = self.pools.get(pool_key)
		if pool:
			return pool
			
		# Make a fresh ConnectionPool of the desired type
		scheme = request_context["scheme"]
		host = request_context["host"]
		port = request_context["port"]
		pool = self._new_pool(scheme, host, port, request_context=request_context)

		self.pools[pool_key] = pool

	return pool
```
제공된 풀 키를 기반으로 적절한 연결 풀(`HTTPConnectionPool`)을 가져오는 역할.

- `self.pools.lock`을 사용하여 커넥션 풀 딕셔너리를 잠금. 이렇게 함으로써 여러 스레드가 동시에 커넥션 풀에 접근하지 못하도록 보호한다.
    
- 주어진 `pool_key`를 사용하여 커넥션 풀 딕셔너리에서 해당하는 커넥션 풀을 찾는다. 만약 이미 해당하는 커넥션 풀이 존재한다면 그것을 리턴한다.
    
- 커넥션 풀이 존재하지 않는 경우, 새로운 커넥션 풀을 생성한다.
    
- 새로운 커넥션 풀을 생성하기 위해 `request_context`에 포함된 정보를 사용한다. 여기서 `scheme`, `host`, `port` 정보가 필요함.
    
- 새로 생성된 커넥션 풀을 커넥션 풀 딕셔너리에 추가.
    
- 커넥션 풀을 반환.

## `connection_from_url`
