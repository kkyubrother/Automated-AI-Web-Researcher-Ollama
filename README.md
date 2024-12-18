# Automated-AI-Web-Researcher-Ollama

## 설명
Automated-AI-Web-Researcher는 Ollama를 통해 로컬에서 실행되는 대규모 언어 모델을 활용하여 주어진 주제나 질문에 대해 철저하고 자동화된 온라인 조사를 수행하는 혁신적인 연구 도우미입니다. 기존의 LLM 상호 작용과 달리 이 도구는 실제로 쿼리를 집중 연구 영역으로 분류하고 웹 검색 및 관련 웹사이트 스크래핑을 통해 각 영역을 체계적으로 조사하고 그 결과를 정리함으로써 구조화된 연구를 수행합니다. 조사 결과는 발견된 모든 콘텐츠와 출처 링크가 포함된 텍스트 문서로 자동 저장됩니다. 조사를 중단하고 싶을 때 언제든지 명령을 입력하면 조사가 종료됩니다. 그러면 LLM이 찾은 모든 콘텐츠를 검토하여 원래 주제나 질문에 대한 종합적인 최종 요약을 제공합니다. 그 후 LLM에 연구 결과에 대해 질문할 수 있습니다.


## Project Demonstration
[![My Project Demo](https://img.youtube.com/vi/hS7Q1B8N1mQ/0.jpg)](https://youtu.be/hS7Q1B8N1mQ "My Project Demo")

Click the image above to watch the demonstration of my project.

## 작동 방식은 다음과 같습니다:
1. 리서치 쿼리를 입력합니다(예: “연구에 따르면 전 세계 인구가 증가하지 않고 감소하기 시작하는 해는 언제일까요?”).
2. LLM이 쿼리를 분석하여 주제 또는 질문과의 관련성에 따라 각각 우선순위가 할당된 5개의 특정 연구 중점 분야를 생성합니다.
3. 우선순위가 가장 높은 영역인 LLM부터 시작합니다:
    - 타깃 검색 쿼리 공식화
    - 웹 검색을 수행합니다.
    - 검색 결과를 분석하여 가장 관련성이 높은 웹 페이지를 선택합니다.
    - 선택한 웹 페이지에서 관련 정보를 스크랩하고 추출합니다.
    - 연구 세션 중에 발견된 모든 콘텐츠를 검색된 웹사이트 링크를 포함하여 연구 텍스트 파일로 문서화합니다.
4. 모든 초점 영역을 조사한 후 LLM은 발견된 정보를 바탕으로 새로운 초점 영역을 생성하고 연구 주기를 반복하며, 종종 이전 결과를 바탕으로 새로운 관련 초점 영역을 발견하여 경우에 따라 흥미롭고 새로운 연구 주제를 도출합니다.
5. 언제든지 종료 명령을 입력할 수 있는 기능을 통해 원하는 만큼 오래 조사할 수 있습니다. 그러면 연구가 중지되고 LLM이 지금까지 수집된 모든 콘텐츠를 전체적으로 검토하여 원래의 쿼리 또는 주제에 대한 종합적인 요약을 생성합니다.
6. 그런 다음 LLM이 대화 모드로 전환되어 원하는 경우 연구 결과에 대해 구체적인 질문을 할 수 있습니다.


중요한 차이점은 단순한 챗봇이 아니라 사용자가 선택한 단일 질문 또는 주제에서 체계적으로 주제를 조사하고 문서화된 연구 흔적을 유지하는 자동화된 연구 도우미라는 점입니다. 시스템과 모델에 따라 비교적 짧은 시간 내에 100개 이상의 검색과 콘텐츠 검색을 수행할 수 있습니다. 실행 상태로 두었다가 관련 웹사이트의 100개 이상의 콘텐츠가 포함된 전체 텍스트 문서로 돌아온 다음, 검색 결과를 요약하도록 한 다음 검색한 내용에 대해 질문할 수 있습니다.


## Features
- 우선순위가 지정된 중점 분야를 통한 자동화된 리서치 계획
- 체계적인 웹 검색 및 콘텐츠 분석
- 모든 리서치 콘텐츠와 소스 URL을 상세 텍스트 문서로 저장
- 연구 요약 생성
- 연구 결과에 대한 연구 후 Q&A 기능
- 자체 개선 검색 메커니즘
- 상태 표시기가 포함된 풍부한 콘솔 출력
- 웹 소스 정보를 사용한 종합적인 답변 합성
- 연구 결과 탐색을 위한 연구 대화 모드

## 설치
**참고:** Windows에서 사용하려면 [/feature/windows-support](https://github.com/TheBlewish/Automated-AI-Web-Researcher-Ollama/tree/feature/windows-support) 브랜치의 안내를 따르세요. Linux 및 MacOS의 경우, 이 메인 브랜치를 사용하고 아래 단계를 따르세요:

1. **리포지토리 복제하기:**

    ```sh
    git clone https://github.com/TheBlewish/Automated-AI-Web-Researcher-Ollama
    cd Automated-AI-Web-Researcher-Ollama
    ```

2. **가상 환경 생성 및 활성화:**

    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

3. **종속성 설치:**

    ```sh
    pip install -r requirements.txt
    ```

4. **올라마 설치 및 구성하기:**

    [https://ollama.ai](https://ollama.ai)의 지침에 따라 Ollama를 설치합니다.

    선택한 모델 파일을 사용하여 필요한 컨텍스트 길이를 가진 사용자 정의 모델 변형을 생성합니다(`phi3:3.8b-mini-128k-instruct` 또는 `phi3:14b-medium-128k-instruct` 권장).

    다음과 같은 내용으로 `modelfile`이라는 파일을 만듭니다:

    ```
    FROM your-model-name

    PARAMETER num_ctx 38000
    ```

    “your-model-name"을 선택한 모델로 바꿉니다(예: `phi3:3.8b-mini-128k-instruct`).

    그런 다음 모델을 생성합니다:

    ```sh
    ollama create research-phi3 -f modelfile
    ```

    **참고:** 이 특정 구성은 최근 Ollama 버전에서는 `phi3:3.8b-mini-128k-instruct`와 같은 모델의 컨텍스트 창이 축소되었지만 이름에는 높은 컨텍스트가 포함되어 있으므로 연구 과정에서 사용되는 정보의 양이 많기 때문에 `modelfile` 단계가 필요하기 때문에 필요합니다.

## 사용법
1. **올라마 시작:**

    ```sh
    ollama serve
    ```

2. **연구자 실행:**

    ```sh
    python Web-LLM.py
    ```

3. **연구 세션 시작하기:**
    - 연구 쿼리 뒤에 `@`를 입력합니다.
    - 제출하려면 `CTRL+D`를 누릅니다.
    - 예: `@전 세계 인구가 감소하기 시작할 것으로 예상되는 해는 언제입니까?`

4. **연구 중에 다음 명령을 사용할 수 있습니다. 관련 문자를 입력한 후 `CTRL+D`로 제출하기:**
    - 상태를 표시하려면 `s`를 사용합니다.
    - 현재 초점을 표시하려면 `f`를 사용합니다.
    - `p`를 사용하여 연구 진행 상황을 일시 중지하고 평가하면 지금까지 수집된 콘텐츠로 쿼리에 대한 답변을 제공할 수 있는지 여부를 판단하기 위해 전체 연구 콘텐츠를 검토한 후 LLM에서 평가 결과를 제공합니다. 그런 다음 연구를 계속하려면 `c`, 종료하려면 `q` 명령 중 하나를 입력할 때까지 기다렸다가 일시 정지 기능을 사용하지 않고 종료한 것과 같은 요약 결과를 표시합니다.
    - 연구를 종료하려면 `q`를 사용합니다.

5. **리서치 완료 후: **
    - 요약이 생성될 때까지 기다렸다가 LLM의 조사 결과를 검토합니다.
    - 대화 모드로 들어가 조사 결과에 대해 구체적인 질문을 합니다.
    - 프로그램 디렉토리에 있는 연구 세션 텍스트 파일에서 찾은 자세한 연구 내용에 액세스합니다. 여기에는 다음이 포함됩니다:
        - 검색된 모든 콘텐츠
        - 모든 정보의 소스 URL
        - 조사된 중점 분야
        - 생성된 요약

## 구성
LLM 설정은 `llm_config.py`에서 수정할 수 있습니다. 연구자가 작동하려면 구성에서 모델 이름을 지정해야 합니다. 기본 구성은 지정된 Phi-3 모델을 사용하는 연구 작업에 최적화되어 있습니다.


## 현재 상태
기능적인 자동화 연구 기능을 보여주는 프로토타입입니다. 아직 개발 중이지만 구조화된 연구 작업을 성공적으로 수행합니다. 테스트를 거쳤으며, 앞서 조언한 대로 컨텍스트를 설정하면 `phi3:3.8b-mini-128k-instruct` 모델과 잘 작동합니다.

## 종속성
- Ollama
- `requirements.txt`에 나열된 파이썬 패키지
- 권장 모델: `phi3:3.8b-mini-128k-instruct` 또는 `phi3:14b-medium-128k-instruct`(사용자 지정 컨텍스트 길이 지정)

## 기여하기
기여를 환영합니다! 이것은 개선 및 새로운 기능을 위한 여지가 있는 프로토타입입니다.

## 라이선스
이 프로젝트는 MIT 라이선스에 따라 라이센스가 부여됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 감사
- 로컬 LLM 런타임을 제공한 Ollama 팀
- 검색 API를 제공한 DuckDuckGo


## 개인 메모
이 도구는 단순한 LLM 상호 작용과 진정한 연구 기능 사이의 간극을 메우기 위한 시도입니다. 연구 프로세스를 구조화하고 문서를 유지 관리함으로써 기존의 LLM 대화보다 더 철저하고 검증 가능한 결과를 제공하는 것을 목표로 합니다. 또한 단순히 웹사이트를 검색하고 스크랩하여 질문에 답할 수 있는 기능만 제공했던 이전 프로젝트인 'Web-LLM-Assistant-Llamacpp-Ollama'를 개선하려는 시도이기도 합니다. 이전 프로그램과 달리 이 프로그램은 그 기능을 새롭고 매우 유용한 방식으로 사용한다고 생각합니다. 신입 프로그래머로서 두 번째로 만든 프로그램인 만큼 그 결과에 대해 매우 기분이 좋습니다. 이 프로그램이 성공했으면 좋겠어요!

실제 도구라기보다는 참신한 느낌이었던 이전 프로그램과 달리 제가 직접 사용해 본 결과, 이 프로그램은 실제로 매우 유용하고 독특하지만 제 편견이 좀 심합니다!

부디 즐겨보세요! 그리고 이 자동화된 인공지능 리서처를 더욱 발전시킬 수 있도록 개선할 점이 있으면 언제든지 제안해 주세요.

## 면책 조항
이 프로젝트는 교육 목적으로만 사용됩니다. 사용된 모든 API와 서비스의 서비스 약관을 준수해야 합니다.

