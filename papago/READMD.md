# Alfred Workflow: Papago
평소 알프레드 앱에서 기본으로 제공하는 [Google Translation](https://translate.google.com/)를 자주 사용하고 있었다.  
그러다가 우연히 야민정음?에 대한 번역도 [Papago](https://papago.naver.com/)에서 지원한다는 글을 보고 흥미로웠다.  
구글 번역이 아니라 파파고도 쉽게 접하면 번역을 더 재밌게 할 수 있을까? 싶었다.

> We've always defined ourselves by the ability to overcome the impossible.

구글링을 짧게 해봤더니 인터스텔라에서 나온 말처럼 역시 누군가가 이미 아름답고 멋지게 만들어서 공유해준 [워크플로우](http://seungtaek.com/archives/498)를 찾을 수 있었다.

위의 워크플로우도 충분하지만, 다른 언어로 번역하고 싶은 사람이 있을 듯 했다. 그렇게 해서 코드를 수정해보기로 했다.   
기본적으로 Papago API가 제공하는 번역은 제한되어 있다. 이를 최대한 이용해보자.

## Feature
지원하는 언어는 다음과 같다: 한국어, 영어, 스페인어, 중국어 간체, 중국어 번체, 프랑스어, 러시아어.
*일본어는 파파고 사이트를 이용하자.*

* `ppg [문장]`: 영어 -> 한국어, 한국어 -> 영어 번역을 기본적으로 지원한다.
* `ppg [언어 코드] [한국어]`: 한국어 -> 해당 언어 번역을 지원한다.
* `ppg ko [외국어]`: 외국어 -> 한국어 번역을 지원한다.
* `ppg [언어 코드] [외국어]`: 외국어 -> 해당 언어 번역을 지원한다(단, Papago API가 지원할 경우).
* 번역 후의 `return`을 누르면 클립보드에 복사가 된다.
* 번역 후의 `cmd`+`return`을 누르면 [Papago](https://papago.naver.com/)로 연결된다.

## Usage
1. 워크플로우를 다운로드하여 알프레드에 import한다.
2. 네이버 개발자 센터에서 API를 사용할 수 있도록 `client_id`와 `client_secret`을 발급받는다.
3. 워크플로우 변수에 다음과 같이 입력한다:
   [*screenshot*]
4. 알프레드에서 번역을 한다. 반드시 번역할 문장 뒤에 스페이스 바를 눌러 공백문자를 추가한다.

## Reference
- [알프레드(Alfred)에서 파파고(Papago) 번역 자동 완성 워크플로우 - seungtaek.com](http://seungtaek.com/archives/498): 선구자의 워크플로우
- [Workflow API](https://www.deanishe.net/alfred-workflow/index.html)