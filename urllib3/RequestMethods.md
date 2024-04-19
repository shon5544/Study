
## RequestMethods?
- 요청을 날리는 구현 클래스를 위한 추상클래스임.
- 제공하는 메서드:
	- `urlopen()` - 추상 메서드
	- `request()`
	- `request_encode_url()`
	- `request_encode_body()`
- 생성자:
	- header를 세팅해줌.
	- header는 typing.Mapping | typing.Dict 타입임.

## Python Type hints: typing.Mapping vs typing.Dict
> https://stackoverflow.com/questions/52487663/python-type-hints-typing-mapping-vs-typing-dict
- Dict는 `Dict[byte, str]`과 같은 형태를 지원하는 **리터럴 dict임을 나타낼 때** 씀.
- Mapping은 매직메서드 `__getitem__`,`__len__`,`__iter__`가 정의된 오브젝트임.
- 실제 사용은 Mapping, 반환형등 이것이 dict임을 나타낼때는 Dict를 쓰는 식으로 구분하는 듯.