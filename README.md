# 🤖 Smart CS — LangGraph 기반 모바일 CS 웹 서비스

<div align="center">

**삼성 갤럭시 사용자를 위한 AI 고객센터 웹 서비스**

</div>

팀명 : **알려조**

---

## 👥 팀원 소개

| 이름 | 역할 |
| --- | --- |
| 김나연 |  |
| 김지현 |  |
| 박범수 |  |
| 이하윤 |  |
| 여해준 |  |

---

🏆 [SKN Family AI캠프] 4차 단위 프로젝트  
📅 개발 기간: 2026.04.25 ~ 2026.04.29

---

## 📑 목차
1. [프로젝트 개요](#-프로젝트-개요)
2. [문제 정의 및 목표](#-문제-정의-및-목표)
3. [주요 기능](#-주요-기능)
4. [기술 스택](#-기술-스택)
5. [시스템 아키텍처](#-시스템-아키텍처)
6. [프로젝트 디렉토리 구조](#-프로젝트-디렉토리-구조)
7. [핵심 구현 내용](#-핵심-구현-내용)
8. [차별화 포인트](#-차별화-포인트)
9. [API 명세](#-api-명세)
10. [환경 구축 및 실행 방법](#-환경-구축-및-실행-방법)
11. [한 줄 회고](#-한-줄-회고)

---

## 🎯 프로젝트 개요

### 프로젝트 정보
- **프로젝트명**: Smart CS (스마트 고객센터)
- **개발 기간**: 3차(LangGraph RAG 챗봇) + 4차(Django 웹 서비스) 연속 프로젝트
- **팀 구성**: 5명
- **개발 환경**: Python 3.12, Django, FastAPI, LangGraph

### 프로젝트 배경

기존 삼성전자 고객센터는 FAQ가 정해진 키워드에만 반응하여 사용자의 다양한 구어체 표현이나 복잡한 맥락을 이해하기 어렵습니다. 또한 자가수리 정보와 서비스센터 안내가 분리되어 있어, 문제 해결을 위해 사용자가 여러 채널을 직접 찾아야 하는 번거로움이 있습니다. 한국어만 지원하여 외국어 사용자가 이용하기 어렵고, 실제 서비스 환경에서 접근 가능한 웹 인터페이스도 부재했습니다.

---

## 💡 문제 정의 및 목표

### 단계별 문제 해결

#### 3차 프로젝트: LangGraph 기반 RAG 챗봇 개발

**문제 의식**
- 키워드 기반 검색의 맥락 부재 — 구어체 표현을 FAQ 검색에 연결하지 못함
- 소프트웨어/하드웨어 문제를 한 번에 처리하는 통합 CS 시스템 부재
- 자가수리 가이드와 서비스센터 안내가 분리된 불편함

**해결 방안**
- FAQ 1,850개 + 삼성 공식 자가수리 매뉴얼 PDF 기반 RAG 시스템 구축
- LangGraph 조건부 라우팅으로 SW/HW 문제 자동 분기
- ChromaDB + BM25 하이브리드 검색으로 검색 정확도 향상

**3차 성과**

| 지표 | 점수 |
| --- | --- |
| DeepEval Answer Relevancy | 0.864 |
| DeepEval Faithfulness | 0.883 |
| RAGAS Context Precision | 0.865 |
| RAGAS Context Recall | 0.857 |
| RAGAS Faithfulness | 0.740 |

**3차 챗봇을 사용하며 발견된 한계**
- ❌ Streamlit 기반 로컬 실행 환경으로 실제 서비스 배포 불가
- ❌ 한국어만 지원하여 외국어 사용자 접근 불가
- ❌ 웹 표준 UI/UX 부재로 실사용자 경험 부족
- ❌ 음성 입력 미지원으로 접근성 제한

#### 4차 프로젝트: Django 풀스택 웹 서비스 구축

**목표**
> "3차에서 구축한 RAG 챗봇을 실제 서비스 수준의 웹 애플리케이션으로 전환하고, 다국어 지원·음성인식을 추가하여 누구나 접근 가능한 AI 고객센터를 만든다."

**핵심 가치**
- ✅ Django 풀스택으로 실서비스 수준의 웹 UI/UX 제공
- ✅ 한국어/영어 자동 전환으로 외국어 사용자 지원
- ✅ 음성인식으로 접근성 향상
- ✅ Nginx + Docker 기반 클라우드 배포로 실제 서비스 환경 구축

---

## 🎨 주요 기능

### 1. 🌐 다국어 지원 (한국어 / 영어)

사용자가 상단 언어 토글에서 언어를 선택하면 전체 서비스가 해당 언어로 전환됩니다.

**채팅 번역 파이프라인**
- 영어로 질문 입력 → 백엔드에서 한국어로 번역 후 기존 RAG 처리 → 최종 답변을 다시 영어로 번역하여 반환

**정적 번역**
- 홈 화면 추천 칩(Battery, Charging, Wi-Fi), 기기 시리즈/모델 표시
- `app.js`의 `T` 객체와 `applyTranslations()`가 담당
- LLM 번역 없이 정적 치환 방식으로 처리하여 성능과 안정성 확보

**동적 번역**
- FAQ 제목, 본문, 관련 질문, 카테고리, 검색 결과 등 서버에서 내려오는 데이터도 번역
- `views.py`에서 `translate_to_language()`를 사용해 `display_title`, `display_content` 등 표시용 필드를 생성하여 템플릿에 전달

**언어 세션 동기화**
- Django 세션에 `selected_language`를 저장하여 홈/FAQ/검색 어디서든 언어 변경 시 서버도 현재 언어를 인식
- `/language/` 엔드포인트 추가 및 CSRF 처리 보강

### 2. 🎙️ 음성인식

브라우저 내장 Web Speech API(`window.SpeechRecognition`)를 활용하여 별도 설치 없이 마이크 음성 입력을 지원합니다.  
현재 선택된 언어(한국어/영어)에 따라 인식 언어(`ko-KR` / `en-US`)를 자동으로 전환합니다.  
인식된 텍스트는 채팅 입력창에 자동으로 채워지며, 마이크 권한 거부/네트워크 오류 등 에러 상황별 안내 메시지도 한국어/영어로 분기 처리됩니다.

**처리 흐름**
```
마이크 버튼 클릭
      ↓
Web Speech API (SpeechRecognition) 시작
lang = getCurrentLang() === "en" ? "en-US" : "ko-KR"
      ↓
음성 인식 결과 (transcript)
      ↓
채팅 입력창(#chat-question)에 자동 입력
```

### 3. 🔀 지능형 의도 파악 (Intent Routing)

사용자의 메시지를 GPT-4 Turbo가 실시간으로 분석하여 **인사/잡담**, **기기 증상 문의**, **서비스센터 찾기** 3가지 의도로 자동 분류합니다.  
멀티턴 대화 맥락을 고려하여 이전 대화 흐름에 맞는 응답을 제공합니다.

### 4. ⚡ Agentic RAG 파이프라인

LangGraph 기반의 조건부 라우팅으로 **소프트웨어 문제 → FAQ 답변**, **하드웨어 문제 → 자가수리 가이드**, **검색 실패 → Fallback 안내**로 이어지는 동적 워크플로우를 수행합니다.

### 5. 🔍 하이브리드 검색

ChromaDB 벡터 검색(의미 기반)과 BM25(키워드 기반)를 결합한 하이브리드 검색을 적용합니다.  
LLM 쿼리 변환으로 일상적인 표현을 FAQ 검색에 최적화된 키워드로 변환하여 검색 정확도를 높입니다.

### 6. 🛠️ 자가수리 가이드

사용자가 수리 의향을 밝히면 선택한 기기 모델을 자동 감지하여 삼성 공식 수리 매뉴얼 기반의 단계별 분해·교체 절차를 안내합니다.  
자가수리 지원 모델 여부를 자동으로 판별합니다.

### 7. 📍 위치 기반 서비스센터 안내

카카오맵 API와 연동하여 사용자 현재 위치 기반 반경 5km 이내 가까운 삼성전자 서비스센터 3곳의 이름, 주소, 거리를 실시간으로 안내합니다.

---

## 🛠 기술 스택

### Backend & AI

| 구분 | 기술 | 설명 |
| --- | --- | --- |
| LLM | GPT-4 Turbo | 답변 생성, 의도 분류, 쿼리 변환, 번역 |
| RAG Framework | LangChain / LangGraph | 하이브리드 검색 + 조건부 라우팅 RAG 파이프라인 |
| 임베딩 | text-embedding-3-small | 텍스트 벡터 임베딩 |
| AI Backend | FastAPI + Uvicorn | LangGraph 서빙 및 언어 파라미터 수신 |
| 데이터 검증 | Pydantic | 구조화된 출력 및 데이터 검증 |
| 비동기 작업 | Celery + Redis | 스케줄러 및 비동기 로그 플러시 |
| 음성인식 | Web Speech API (브라우저 내장) | 마이크 음성 입력 → 채팅 텍스트 자동 전환 |

### Frontend & Web

| 구분 | 기술 | 설명 |
| --- | --- | --- |
| Web Framework | Django 풀스택 | 템플릿 렌더링, 세션 관리, 번역 처리 |
| Frontend | HTML5 / CSS3 / JavaScript | 언어 토글, 채팅 UI, 음성인식 인터페이스 |

### Data & Storage

| 구분 | 기술 | 설명 |
| --- | --- | --- |
| 벡터 DB | ChromaDB | FAQ 및 자가수리 임베딩 저장·검색 |
| 키워드 검색 | BM25 (rank-bm25) | 키워드 기반 하이브리드 검색 |
| 로그 DB | MongoDB | 대화 로그 및 사용 기록 저장 |
| 캐시 | Redis | Celery 브로커 및 Stream 로그 |
| DB | SQLite3 | Django 기본 데이터베이스 |

### DevOps

| 구분 | 기술 | 설명 |
| --- | --- | --- |
| Container | Docker | 애플리케이션 컨테이너화 |
| Web Server | Nginx | 리버스 프록시 |
| External API | OpenAI API / 카카오맵 API | LLM 및 서비스센터 위치 검색 |

---

## 🏗 시스템 아키텍처

### 전체 구조

```
사용자 브라우저
      ↓
Nginx (리버스 프록시)
      ↓
Django (Port 8010)
  — HTML/CSS/JS 프론트엔드
  — 언어 세션 관리 (selected_language)
  — 정적/동적 번역 처리 (translate_to_language)
  — FastAPI 연동 서비스
      ↓
FastAPI (Port 8000)
  — LangGraph AI 서빙
  — 언어 파라미터 수신 → 번역 파이프라인 실행
      ↓
┌──────────────────────────────────────────────────┐
│  MongoDB   │  ChromaDB + BM25  │  Redis + Celery │
│         OpenAI API  │  카카오맵 API               │
└──────────────────────────────────────────────────┘
```

### LangGraph 워크플로우

```
사용자 질문 수신
      ↓
translate_input_node  ← 영어 선택 시 한국어로 번역
      ↓
route_question  →  인사/잡담     →  chat_node
              →  기기 증상 문의  →  retrieve_node
              →  센터 방문      →  nearest_center_node
      ↓ (기기 증상 문의 경로)
retrieve_node  →  LLM 쿼리 변환 + ChromaDB + BM25 하이브리드 검색
      ↓
route_issue_type  →  SW 이슈  →  generate_node
                →  HW 이슈  →  self_repair_classifier_node
                →  Fallback →  fallback_node
      ↓ (HW 경로)
self_repair_classifier_node
      ↓
route_after_self_repair_check  →  자가수리 가능  →  self_repair_guide_node
                              →  수리 불가/방문 →  nearest_center_node
      ↓
translate_output_node  ← 영어 선택 시 영어로 재번역
      ↓
최종 답변 반환
```

### 노드 구성

| 노드명 | 역할 |
| --- | --- |
| `translate_input_node` | 영어 질문을 한국어로 번역 |
| `translate_output_node` | 한국어 답변을 영어로 번역 |
| `chat_node` | 인사/잡담 응대 및 대화 요약 처리 |
| `retrieve_node` | LLM 쿼리 변환 + ChromaDB + BM25 하이브리드 검색 |
| `generate_node` | 검색된 FAQ 문서 기반 단계별 답변 생성 |
| `self_repair_classifier_node` | 기기 모델명, 하드웨어 여부, 자가수리 의향 동시 판별 |
| `self_repair_guide_node` | 자가수리 매뉴얼 RAG 검색 및 가이드 제공 |
| `nearest_center_node` | 카카오맵 API 기반 주변 서비스센터 안내 |
| `fallback_node` | FAQ 검색 실패 시 선택지 제공 |

---

## 📁 프로젝트 디렉토리 구조

```
SKN25-4th-1Team/
├── .env                               # 로컬 환경 변수 파일 (Git 추적 제외)
├── .env.example                       # 환경 변수 템플릿 파일
├── .gitignore
├── Dockerfile                         # 애플리케이션 컨테이너화 설정
├── requirements.txt
├── django_frontend/                   # Django 풀스택 웹 애플리케이션
│   ├── config/                        # Django 프로젝트 설정
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── manage.py
│   ├── db.sqlite3
│   └── smartcs/                       # Smart CS 앱
│       ├── static/smartcs/
│       │   ├── css/app.css            # 전체 스타일시트
│       │   ├── js/app.js              # 언어 토글·채팅·음성인식 프론트엔드 로직
│       │   └── images/
│       ├── templates/smartcs/
│       │   ├── base.html              # 공통 레이아웃 (언어 토글 포함)
│       │   ├── home.html              # 메인 채팅 화면
│       │   ├── faq.html               # FAQ 화면
│       │   ├── search.html            # 검색 화면
│       │   ├── service_centers.html   # 서비스센터 안내 화면
│       │   ├── login.html             # 로그인 화면
│       │   └── signup.html            # 회원가입 화면
│       ├── views.py                   # 뷰 로직 (동적 번역 처리 포함)
│       ├── services.py                # FastAPI 연동 서비스 모듈
│       ├── data.py                    # FAQ 토픽 등 정적 데이터
│       └── urls.py                    # URL 라우팅 (/language/ 엔드포인트 포함)
├── entrypoint/                        # FastAPI AI 서빙 진입점
│   ├── main.py                        # FastAPI 메인 실행 파일
│   ├── ingest.py                      # 데이터 파싱 및 DB 적재
│   ├── check_db.py                    # DB 적재 상태 확인
│   └── query.py                       # RAG 파이프라인 질의 테스트
├── src/                               # LangGraph 핵심 로직
│   ├── pipelines/
│   │   ├── generation_pipeline.py     # 전체 RAG 파이프라인 통합 실행
│   │   ├── embedding_pipeline.py      # 임베딩 및 벡터 저장소 관리
│   │   ├── ingestion_pipeline.py      # 데이터 전처리 및 적재
│   │   └── self_repair_rag_pipeline.py# 자가수리 전용 RAG 파이프라인
│   ├── utils/
│   │   ├── translator.py              # 다국어 번역 모듈 (4차 신규)
│   │   ├── logger.py                  # Redis Stream 기반 로그 저장
│   │   └── tasks.py                   # Celery 비동기 작업 및 로그 플러시
│   ├── graph.py                       # LangGraph 워크플로우 구성 및 컴파일
│   ├── nodes.py                       # LangGraph 노드 및 라우팅 정의
│   └── state.py                       # GraphState 및 상태 관리 구조
└── eval/                              # 성능 평가 모듈
    ├── deepeval_runner.py
    ├── ragas_runner.py
    └── dataset/
```

---

## 🔑 핵심 구현 내용

### 다국어 파이프라인 — translator.py

**역할**  
사용자의 언어 선택을 기반으로 입력/출력 번역을 처리하는 다국어 지원 모듈입니다.

**처리 흐름**
```
영어 질문 입력
    ↓
translate_input_node — 영어 → 한국어 번역
    ↓
기존 RAG 파이프라인 (ChromaDB + BM25 + LangGraph)
    ↓
translate_output_node — 한국어 답변 → 영어 번역
    ↓
영어 답변 반환
```

**번역 방식 구분**

| 구분 | 방식 | 적용 범위 |
| --- | --- | --- |
| 채팅 번역 | LLM 번역 (translator.py) | 질문 입력, 챗봇 답변 |
| 동적 번역 | LLM 번역 (views.py) | FAQ 제목, 본문, 관련 질문, 검색 결과 |
| 정적 번역 | 정적 치환 (app.js T 객체) | 홈 추천 칩, 기기 모델명, UI 고정 문구 |

### 프론트엔드 구현 — app.js

**다국어 정적 번역 시스템**

`T` 객체에 한국어/영어 번역 키-값을 정의하고, `data-i18n` 속성이 붙은 DOM 요소에 `applyTranslations()`로 일괄 적용합니다.  
선택된 언어는 `localStorage`에 저장되어 페이지 이동 후에도 유지됩니다.

```
언어 토글 버튼 클릭
      ↓
setLanguage(lang) → localStorage 저장
      ↓
applyTranslations(lang) → data-i18n 속성 요소 일괄 번역
      ↓
/language/ 엔드포인트 → Django 세션 동기화
```

**커버리지 범위**

| 구분 | 항목 |
| --- | --- |
| 네비게이션 | FAQ, Service Centers, Login, Sign Up |
| 홈 화면 | 히어로 타이틀, 기기 시리즈/모델 라벨, 검색 플레이스홀더 |
| FAQ | 제목, 검색창, 인기 주제, 관련 질문, 목록으로 버튼 |
| 검색 | 정렬 옵션, 카테고리 필터, 빈 결과 안내 |
| 서비스센터 | 안내 문구, 좌표 입력 플레이스홀더, 조회 버튼 |
| 로그인/회원가입 | 폼 라벨, 플레이스홀더, 제출 버튼 |

**채팅 SPA 구조**

페이지 이동 없이 채팅이 동작하도록 SPA 방식으로 구현했습니다.  
사용자 메시지와 어시스턴트 답변을 동적으로 렌더링하고, 대화 기록 유무에 따라 홈 화면 레이아웃을 자동 전환합니다.

**기기 시리즈/모델 연동**

시리즈 선택 시 해당 시리즈의 모델 목록을 동적으로 렌더링하고, 선택된 모델을 `/device/` 엔드포인트로 서버에 즉시 동기화합니다.

---

### Django 뷰 구현 — views.py

**채팅 세션 관리**

Django 세션을 활용하여 대화 히스토리, thread_id, 선택된 기기 모델을 서버 측에서 유지합니다.  
새 세션 진입 시 초기 어시스턴트 메시지와 고유 thread_id를 자동 생성합니다.

| 엔드포인트 | 역할 |
| --- | --- |
| `GET /` | 홈 화면 렌더링 (대화 히스토리, 기기 목록, 인기 질문 포함) |
| `POST /chat/` | 질문 수신 → FastAPI 전달 → 답변 반환, 세션에 대화 기록 저장 |
| `POST /chat/reset/` | 대화 초기화, 새 thread_id 발급 |
| `POST /device/` | 선택된 기기 모델 세션 저장 |
| `GET /faq/` | FAQ 브라우저 렌더링 (인기 주제, 질문 상세 포함) |
| `GET /search/` | 키워드/카테고리/정렬 기반 FAQ 검색 |
| `GET /service-centers/` | 위도·경도 기반 카카오맵 API 서비스센터 조회 |

**채팅 답변 우선순위**

```
사용자 질문 수신
      ↓
answer_override 있으면 그대로 사용 (인기 질문 클릭 시)
      ↓
find_direct_answer() — 로컬 데이터에서 즉시 답변 가능하면 반환
      ↓
chat_with_fastapi() — LangGraph RAG 파이프라인 호출
      ↓
세션에 대화 기록 저장 후 반환
```

**FAQ 검색 필터링**

pandas DataFrame 기반으로 카테고리 필터, 키워드 검색(제목+본문), 정렬(최신순/조회순/제목순)을 조합하여 처리합니다.

---

### 하이브리드 검색 — retrieve_node

**설계 의도**

| 방식 | 특징 |
| --- | --- |
| ChromaDB (벡터 검색) | 의미 기반으로 유사한 맥락의 문서 검색 |
| BM25 (키워드 검색) | 정확한 단어 매칭으로 누락 없는 검색 |
| **하이브리드 (채택)** | 두 방식의 결과를 결합하여 검색 정확도 향상 |

### 자가수리 PDR 파이프라인 — self_repair_rag_pipeline.py

**Parent Document Retrieval 설계 의도**

| 방식 | 문제점 |
| --- | --- |
| 청크 크게 | 여러 내용이 섞여 벡터 희석 → 검색 부정확 |
| 청크 작게 | LLM에 전달되는 컨텍스트 부족 → 답변 품질 저하 |
| **PDR (채택)** | 작은 청크(300자)로 정밀 검색 + 전체 섹션으로 풍부한 컨텍스트 전달 |

---

## 🏆 3차 → 4차 개선 포인트

| 구분 | 3차 Smart CS | 4차 Smart CS |
| --- | --- | --- |
| **프론트엔드** | Streamlit | Django + HTML/CSS/JS |
| **배포 환경** | 로컬 실행 | Nginx + Docker 클라우드 배포 |
| **언어 지원** | 한국어만 | ✅ 한국어/영어 전환 + 동적 번역 |
| **음성 입력** | ❌ 없음 | ✅ 브라우저 마이크 음성인식 |
| **포트 구성** | FastAPI 8000 + Streamlit 8501 | Django 8010 + FastAPI 8000 |
| **번역 처리** | ❌ 없음 | ✅ 채팅/동적/정적 3단계 번역 파이프라인 |

---

## 📡 API 명세

### Django 엔드포인트

| Method | Path | 설명 |
| --- | --- | --- |
| GET | `/` | 홈 채팅 화면 |
| GET | `/faq/` | FAQ 상세 및 인기 주제 화면 |
| GET | `/search/` | FAQ 검색 및 필터 화면 |
| GET | `/service-centers/` | 서비스센터 조회 화면 |
| GET | `/login/` | 로그인 화면 |
| GET | `/signup/` | 회원가입 화면 |
| POST | `/chat/` | 채팅 AJAX API |
| POST | `/chat/reset/` | 대화 초기화 |
| POST | `/device/` | 선택 기기 세션 저장 |
| POST | `/language/` | 선택 언어 세션 저장 |

### FastAPI 엔드포인트

| Method | Path | 설명 |
| --- | --- | --- |
| POST | `/api/chat` | 상담 요청 처리 |

**Request Body**
```json
{
  "question": "사용자 질문",
  "selected_device": "SM-S921N",
  "thread_id": "uuid",
  "selected_language": "korean 또는 english"
}
```

**Response Body**
```json
{
  "answer": "생성된 답변"
}
```

오류 발생 시 HTTP 500과 detail 반환

---

## 🌐 환경 구축 및 실행 방법

### 환경 구축

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 데이터 적재

```bash
python -m entrypoint.ingest
```

### Django 실행

```bash
cd django_frontend
python manage.py migrate
python manage.py runserver 8010
```

### FastAPI AI 서버 실행

```bash
python -m uvicorn entrypoint.main:app --reload --port 8000
```

### Docker 실행

```bash
docker build -t smart-cs .
docker run -p 8010:8010 -p 8000:8000 smart-cs
```

### 환경 변수 설정 (.env)

```
OPENAI_API_KEY=your_openai_api_key
KAKAO_API_KEY=your_kakao_api_key
MONGO_URI=your_mongodb_uri
CHROMA_PERSIST_DIR=./data/vector_store
REDIS_URL=redis://localhost:6379
```

---

## 🚀 향후 개발 계획

### 아쉬운 점
**1. RAGAS Faithfulness 개선 여지**
- 3차 기준 0.740으로 다른 지표 대비 낮은 수치
- generate_node 프롬프트 엔지니어링 추가 고도화 필요

**2. 다국어 확장**
- 현재 한국어/영어 2개 언어만 지원
- 일본어, 중국어 등 추가 언어 지원 검토


### 향후 개선 계획
- 📊 **대시보드 고도화**: MongoDB 로그 데이터 기반 실시간 통계 시각화
- 🌍 **다국어 확장**: 영어 외 추가 언어 지원
- 📱 **모바일 최적화**: 반응형 디자인 고도화

---

## 💬 한 줄 회고

> #### 김나연
>

---

> #### 김지현
>

---

> #### 박범수
>

---

> #### 이하윤
>

---

> #### 여해준
>

