## Network-layer function
- Forwarding: 라우터의 인풋에서 라우터의 아웃풋으로 패킷을 이동시키는 기능
	- Data Plane 영역이라 지칭함
- Routing: 소스에서 목적지로 가는 패킷의 경로 정의하는 기능
	- 이 Routing 프로토콜을 통해 Forwarding Table을 만든다. 따라서 Forwarding과 유기적임
	- Control Plane

## Per-router control plane
- 라우터마다 각각 라우팅 알고리즘이 존재하고 이 알고리즘은 연결되어있는 라우터 모두 동일한 알고리즘을 공유한다.
- 각 라우터마다 Control Plane이 있다.
- 각 라우터마다 포워딩 테이블을 각자 만든다.
- 서로 정보를 공유하면서 포워딩 테이블을 만드는 과정이 Control Plane.
- 포워딩 테이블을 기준으로 데이터를 어디로 보낼지 정하고 보내는게 Data Plane.

## Logically centralized control plane
- 라우터에 있는 Control 에이전트에 정보를 다 내려줘서 라우팅을 할 수 있는 경로들을 내려줌
- 결국에는 Remote Controller라는 중앙서버가 전체의 네트워크 상황을 다 본 다음에 전체 룰에 따라 포워딩 테이블을 내려주는 것이 Logically centralized control plane이다.

## Routing protocol goal:
- 결국에는 가장 좋은 경로를 결정하는 것.
- 가장 좋은/효과적인 라우팅을 만들어내는 것이 top-10 네트워킹 챌린지라고 할 수 있다.

## Graph abstraction of the network
- Graph: G = (N, E)
- N = set of routers
- E = set of links

## Routing algorithm classification
### Q: Global or Decentralized information?
- Global:
	- 모든 라우터들은 완벽한 토폴로지에 대한 데이터를 가지고 있고 그에 해당하는 link cost도 알고 있다고 가정한다.
	- lint state 알고리즘이 있다.
	- 현실적으로 쉽지 않음. 동기화도 힘들고..
	- 그래서 Global, Decentralized 두 가지를 혼용해서 쓰기도 한다.
- Decentralized:
	- 라우터는 물리적으로 연결된 이웃들과 이웃들과의 link costs만 알고 있다.
	- "distance vector" 알고리즘이 있다.

### Q: static or dynamic?
- static:
	- 라우팅 알고리즘에 대한 경로가 조금씩 변해서 거의 변하지 않는, 정적인 상황을 이야기.
- dynamic:
	- 라우팅 알고리즘에 대한 결과가 주기적으로 바뀌어서 자주 업데이트하는 효과가 있는 것을 dynamic이라고 함

## Subnet Mask
