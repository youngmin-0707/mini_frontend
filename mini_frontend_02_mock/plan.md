# 통합 프로젝트 개발 계획서

## 1. 목표

Streamlit 프론트엔드와 FastAPI 백엔드를 연동하여 다음 기능을 제공한다.

- 회원가입, 로그인, 로그아웃
- 상품 등록, 조회, 수정, 삭제
- Gemini AI 채팅
- 도시별 날씨 조회
- 백엔드 서버 상태 확인

## 2. 필수 수정 사항

| 기능 | 현재 상태 | 개발 내용 |
|---|---|---|
| 인증 | 고정 계정 사용, 회원 저장 없음 | 회원 API, 비밀번호 해시, 인증 토큰 구현 |
| 상품 | 고정 데이터 반환 | 저장소 기반 CRUD와 관리 화면 구현 |
| AI 채팅 | 백엔드 API만 존재 | 프론트 채팅 화면과 오류 처리 추가 |
| 날씨 | 프론트에서 외부 API 호출 | 기존 기능 유지 및 오류 처리 정리 |
| 서버 확인 | 백엔드에 `/health` 없음 | 상태 확인 API 추가 |
| 설정 | 일부 주소와 설정이 코드에 고정 | 환경 변수와 공통 API 모듈 사용 |

## 3. 필수 개발 범위

### 프론트엔드

- 백엔드 주소를 환경 변수로 관리
- 공통 API 호출 및 오류 처리 모듈 작성
- 회원가입·로그인 API 연동과 인증 상태 관리
- 상품 목록·등록·수정·삭제 화면 구현
- AI 채팅 화면 구현
- 서버 상태 및 날씨 화면 정리

### 백엔드

- 상태 확인 및 인증 API 구현
- 비밀번호 해시 저장과 인증 토큰 검증
- 상품 서비스를 실제 저장소와 연결
- Gemini 키 누락, 시간 초과, 외부 오류 처리
- API별 입력 검증과 일관된 오류 응답 적용
- 핵심 API 자동 테스트 작성

### 공통

- 데이터 저장소 선택 및 연결
- `.env.example`과 `.gitignore` 정비
- 설치·실행 문서 최신화

## 4. API 명세

- 개발 기본 주소: `http://127.0.0.1:8000`
- 실제 주소는 `API_BASE_URL` 환경 변수로 관리한다.
- 인증 API는 `Authorization: Bearer <access_token>` 헤더를 사용한다.

### 4.1 엔드포인트

| Method | 경로 | 인증 | 요청 | 성공 응답 | 주요 오류 |
|---|---|---:|---|---|---|
| GET | `/health` | 불필요 | 없음 | `200 HealthResponse` | `500` |
| POST | `/auth/signup` | 불필요 | `SignupRequest` | `201 UserResponse` | `409`, `422` |
| POST | `/auth/login` | 불필요 | `LoginRequest` | `200 TokenResponse` | `401`, `422` |
| GET | `/auth/me` | 필요 | 없음 | `200 UserResponse` | `401` |
| POST | `/products` | 필요 | `ProductRequest` | `201 ProductResponse` | `401`, `422` |
| GET | `/products` | 필요 | 없음 | `200 ProductResponse[]` | `401` |
| GET | `/products/{product_id}` | 필요 | 없음 | `200 ProductResponse` | `401`, `404`, `422` |
| PUT | `/products/{product_id}` | 필요 | `ProductRequest` | `200 ProductResponse` | `401`, `404`, `422` |
| DELETE | `/products/{product_id}` | 필요 | 없음 | `204` | `401`, `404` |
| POST | `/chat/gemini` | 필요 | `ChatRequest` | `200 ChatResponse` | `401`, `422`, `502`, `504` |

### 4.2 요청·응답 모델

| 모델 | 필드 |
|---|---|
| `HealthResponse` | `status: string`, `service: string` |
| `SignupRequest` | `login_id: string`, `password: string`, `name: string` |
| `LoginRequest` | `login_id: string`, `password: string` |
| `UserResponse` | `id: int`, `login_id: string`, `name: string` |
| `TokenResponse` | `access_token: string`, `token_type: "bearer"` |
| `ProductRequest` | `name: string`, `price: int` |
| `ProductResponse` | `id: int`, `name: string`, `price: int` |
| `ChatRequest` | `prompt: string` |
| `ChatResponse` | `answer: string` |
| `ErrorResponse` | `detail: string` |

요청 예시:

```json
{
  "login_id": "id01",
  "password": "pwd01",
  "name": "홍길동"
}
```

상품 요청 예시:

```json
{
  "name": "티셔츠",
  "price": 15000
}
```

채팅 요청·응답 예시:

```json
{
  "prompt": "오늘 할 일을 추천해 줘."
}
```

```json
{
  "answer": "오늘 할 일에 대한 추천 답변입니다."
}
```

공통 오류 응답:

```json
{
  "detail": "오류 내용을 설명하는 메시지"
}
```

### 4.3 상태 코드 기준

| 코드 | 의미 |
|---:|---|
| `200` | 조회·수정·로그인 성공 |
| `201` | 회원 또는 상품 생성 성공 |
| `204` | 삭제 성공 |
| `401` | 인증 실패 |
| `404` | 데이터 없음 |
| `409` | 아이디 중복 |
| `422` | 입력값 오류 |
| `502` | Gemini 외부 API 오류 |
| `504` | Gemini 응답 시간 초과 |

## 5. 개발 순서

1. 환경 변수와 공통 설정 정리
2. `/health` 구현 및 연결 확인
3. 저장소, 사용자 모델, 인증 구현
4. 상품 CRUD API와 관리 화면 구현
5. Gemini 채팅 화면 연동
6. 날씨 및 기존 화면 정리
7. 자동 테스트와 전체 흐름 검증
8. README 및 실행 문서 갱신

## 6. 테스트 항목

- 서버 상태 확인 성공 및 연결 실패
- 회원가입 성공, 필수값 누락, 아이디 중복
- 로그인 성공, 잘못된 계정, 인증 만료
- 비인증 사용자의 보호 API 접근 차단
- 상품 등록·조회·수정·삭제와 잘못된 입력
- Gemini 정상 응답, 키 누락, 외부 오류, 시간 초과
- 회원가입 → 로그인 → 상품 관리 → 채팅 → 로그아웃 전체 흐름

## 7. 개발 전 결정 사항

- 사용할 데이터 저장소
- 인증 토큰 유효 시간
- 상품을 전체 공유 또는 사용자별로 관리할지 여부
- 채팅 기록 저장 여부
- 기존 상품 API 경로를 새 경로로 변경할지 여부

## 8. 완료 기준

- 환경 변수 기반으로 두 프로젝트가 연결된다.
- 회원가입, 로그인, 로그아웃이 정상 동작한다.
- 인증 사용자가 상품 CRUD와 AI 채팅을 사용할 수 있다.
- 날씨 및 서버 상태 확인이 정상 동작한다.
- 핵심 자동 테스트와 전체 사용자 흐름이 통과한다.
- 비밀 정보가 저장소에 포함되지 않는다.
- 설치 및 실행 문서가 실제 동작과 일치한다.
