# Customer 기능 작업계획서

## 1. 개요

FastAPI 백엔드에 JSON 파일 기반 Customer CRUD를 추가하고, Streamlit `frontend`에 Customer 등록·조회 화면을 추가한다.

- 데이터 필드: `id`, `pwd`, `name`, `age`, `timestamp`
- `id` 형식: `id01`
- `pwd` 형식: `pwd01`
- `timestamp`: 등록 시 서버에서 한국 시간 기준으로 자동 생성
- 저장소: `backend/data/customers.json`
- 프론트엔드 범위: 등록, 한 개 조회, 전체 조회
- 비밀번호는 JSON 파일에 원문으로 저장하지만 API 응답과 조회 화면에서는 제외

## 2. 기존 디렉토리 활용 계획

프로젝트 구조를 새로 만들지 않고, Product 기능이 배치된 기존 폴더와 같은 위치에 Customer 파일을 추가한다.

### 추가할 파일

```text
backend/
├─ app/
│  ├─ routers/
│  │  └─ customer_router.py       # product_router.py와 같은 위치
│  ├─ schemes/
│  │  └─ customer_scheme.py       # product_scheme.py와 같은 위치
│  └─ services/
│     └─ customer_service.py      # product_service.py와 같은 위치
├─ data/                           # JSON 저장을 위해 추가
│  └─ customers.json
└─ tests/
   └─ test_customer_router.py     # 기존 라우터 테스트와 같은 위치

frontend/
├─ app_pages/
│  ├─ 07_customer_create.py       # 기존 Product 페이지와 같은 위치
│  └─ 08_customer_select.py
└─ clients/
   └─ customer_client.py          # product_client.py와 같은 위치
```

### 수정할 기존 파일

| 파일 | 수정 내용 |
|---|---|
| `backend/app/main.py` | Customer 라우터와 API 문서 태그 연결 |
| `frontend/app.py` | Customer 등록·조회 페이지와 사이드바 메뉴 연결 |
| `frontend/core/api_client.py` | HTTP 오류 메시지 처리 보완 |

`routers`, `schemes`, `services`, `tests`, `app_pages`, `clients` 폴더는 이미 존재하므로 새로 만들지 않는다. `data` 폴더만 Customer JSON 저장을 위해 백엔드에 추가한다.

## 3. API 명세

| 기능 | Method | 경로 | 성공 응답 |
|---|---|---|---|
| 등록 | POST | `/customer/create` | `201`, `message`, `customer` |
| 한 개 조회 | GET | `/customer/get/{customer_id}` | `200`, `customer` |
| 전체 조회 | GET | `/customer/getall` | `200`, `count`, `customers` |
| 수정 | PUT | `/customer/update/{customer_id}` | `200`, `message`, `updated_customer` |
| 삭제 | DELETE | `/customer/delete/{customer_id}` | `200`, `message`, `deleted_id` |

등록 요청 예시:

```json
{
  "id": "id01",
  "pwd": "pwd01",
  "name": "홍길동",
  "age": 25
}
```

주요 오류 응답:

| 상태 | 상황 | 메시지 |
|---|---|---|
| `422` | 입력 형식 오류 | `잘못 기입하셨습니다.` |
| `409` | ID 중복 | `중복된 ID입니다. 다시 입력하세요.` |
| `404` | ID가 존재하지 않음 | `해당 Customer가 없습니다.` |
| `500` | JSON 읽기·저장 실패 | 서버 오류 안내 |

## 4. 구현 및 검증 계획

1. Customer 요청·응답 모델과 입력 검증 작성
2. JSON 파일 읽기·쓰기 및 CRUD 서비스 작성
3. 라우터 작성 후 `main.py`에 연결
4. 등록·한 개 조회·전체 조회 프론트엔드 작성
5. 중복 ID, 잘못된 입력, 조회·수정·삭제 테스트
6. 기존 Product와 Chat 기능 및 테스트의 정상 동작 확인

## 5. Setup 가이드

### 백엔드

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

- API 서버: `http://127.0.0.1:8000`
- API 문서: `http://127.0.0.1:8000/docs`

### 프론트엔드

새 PowerShell 창에서 실행한다.

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

- 접속 주소: `http://localhost:8501`

### 테스트

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\backend
.\.venv\Scripts\Activate.ps1
python -m pytest
```

## 6. 완료 기준

- Customer 데이터가 JSON 파일에 저장되고 서버 재시작 후에도 유지된다.
- CRUD API별 응답 구조와 오류 메시지가 명세와 일치한다.
- 프론트엔드에서 등록, 한 개 조회, 전체 조회가 정상 동작한다.
- API와 화면에서 `pwd`가 노출되지 않는다.
- 기존 기능과 자동 테스트가 정상 동작한다.
