# Mini Frontend + FastAPI + Supabase 학습 리캡

> 이 문서는 프로젝트를 진행하면서 실제로 수정한 내용과 만난 오류를 초보자 관점에서 다시 학습할 수 있도록 정리한 기록입니다.

---

## 1. 프로젝트에서 만든 흐름

현재 애플리케이션은 다음 순서로 동작합니다.

```text
사용자
  ↓
Streamlit 프런트엔드
  ↓ HTTP 요청
FastAPI 백엔드
  ↓ Supabase Python Client
Supabase Database
```

각 기술의 역할은 다음과 같습니다.

| 구분 | 사용 기술 | 역할 |
|---|---|---|
| 화면 | Streamlit | 로그인, 회원가입, 상품 관리 화면 |
| HTTP 통신 | httpx | 프런트엔드에서 백엔드 API 호출 |
| API 서버 | FastAPI | 요청 검증, 서비스 함수 호출, HTTP 응답 |
| 데이터 검증 | Pydantic | 요청·응답 데이터 형식 검사 |
| 데이터베이스 | Supabase | 회원과 상품 데이터 저장 |

---

## 2. 현재 주요 디렉터리 구조

```text
mini_frontend_login_db/
├─ backend/
│  └─ app/
│     ├─ core/
│     │  └─ supabase_client.py
│     ├─ routers/
│     │  ├─ auth_router.py
│     │  └─ product_router.py
│     ├─ schemas/
│     │  ├─ auth.py
│     │  └─ product_schema.py
│     └─ services/
│        ├─ auth_service.py
│        └─ product_service.py
│
├─ frontend/
│  ├─ app.py
│  ├─ core/
│  │  └─ api_client.py
│  └─ app_pages/
│     ├─ 00_login.py
│     ├─ 01_home.py
│     ├─ 02_signup.py
│     ├─ 03_weather.py
│     ├─ 04_health.py
│     ├─ 05_product_create.py
│     ├─ 06_product_select.py
│     └─ 07_product_update_delete.py
│
├─ PRODUCT_MANAGEMENT_PLAN.md
└─ LEARNING_RECAP.md
```

---

## 3. 백엔드 코드 구조 이해하기

백엔드 상품 기능은 세 단계로 나뉩니다.

```text
Router
  ↓
Service
  ↓
Supabase
```

### Router

파일:

```text
backend/app/routers/product_router.py
```

Router는 HTTP 주소와 메서드를 결정합니다.

```python
@product_router.post("/product/create")
def create(product: ProductCreate):
    return product_create(product)
```

### Schema

파일:

```text
backend/app/schemas/product_schema.py
```

Schema는 요청 데이터가 올바른지 검사합니다.

```python
class ProductCreate(BaseModel):
    name: str
    price: int
```

따라서 상품 생성 요청에는 `name`, `price`만 전달합니다.

```json
{
  "name": "무선 키보드",
  "price": 35000
}
```

상품 ID와 등록 시간은 백엔드에서 생성합니다.

### Service

파일:

```text
backend/app/services/product_service.py
```

Service는 실제 Supabase CRUD 작업을 담당합니다.

```python
supabase.table("products").insert(...).execute()
supabase.table("products").select("*").execute()
supabase.table("products").update(...).execute()
supabase.table("products").delete().execute()
```

---

## 4. Supabase 연결 구조

연결 파일:

```text
backend/app/core/supabase_client.py
```

서비스 파일에서는 다음 함수를 가져옵니다.

```python
from app.core.supabase_client import get_supabase
```

함수 안에서 연결 객체를 생성합니다.

```python
supabase = get_supabase()
```

환경변수는 다음 파일에서 읽습니다.

```text
backend/.env
```

```env
SUPABASE_URL=프로젝트_URL
SUPABASE_SERVICE_ROLE_KEY=서버용_비밀키
```

> `.env`의 실제 키는 코드, 화면, GitHub, 문서에 노출하지 않습니다.

---

## 5. 구현한 API

### 인증 API

| 기능 | 메서드 | 주소 |
|---|---|---|
| 회원가입 | POST | `/auth/create` |
| 로그인 | POST | `/auth/signin` |
| 로그아웃 | GET | `/auth/signout/{input_id}` |

### 상품 API

| 기능 | 메서드 | 주소 |
|---|---|---|
| 상품 생성 | POST | `/product/create` |
| 상품 한 개 조회 | GET | `/product/get/{product_id}` |
| 상품 전체 조회 | GET | `/product/getall` |
| 상품 수정 | PUT | `/product/{product_id}` |
| 상품 삭제 | DELETE | `/product/delete/{product_id}` |

CRUD와 HTTP 메서드의 관계:

| CRUD | 의미 | HTTP 메서드 |
|---|---|---|
| Create | 생성 | POST |
| Read | 조회 | GET |
| Update | 수정 | PUT |
| Delete | 삭제 | DELETE |

---

## 6. 회원가입 기능에서 배운 내용

### 처음 상태

처음 회원가입 서비스는 입력값을 반환할 뿐 Supabase에 저장하지 않았습니다.

```python
return AuthPublic(
    id=auth.id,
    name=auth.name,
)
```

### 변경 후

`customers` 테이블에 INSERT하도록 변경했습니다.

```python
result = (
    supabase.table("customers")
    .insert(
        {
            "id": auth.id,
            "pwd": auth.pwd,
            "name": auth.name,
        }
    )
    .execute()
)
```

중복 ID가 있으면 `409 Conflict`를 반환하도록 구성했습니다.

```python
if db_customer is not None:
    raise HTTPException(
        status_code=409,
        detail="이미 사용 중인 아이디입니다.",
    )
```

---

## 7. HTTP 상태 코드에서 배운 내용

| 상태 코드 | 의미 | 현재 프로젝트의 사례 |
|---|---|---|
| 200 | 요청 성공 | 상품 생성·조회·수정·삭제 성공 |
| 401 | 인증 실패 | ID는 있지만 비밀번호가 틀림 |
| 404 | 데이터 없음 | 사용자 또는 상품을 찾을 수 없음 |
| 409 | 데이터 충돌 | 이미 존재하는 ID로 회원가입 |
| 422 | 요청 검증 실패 | 필수 필드 누락 또는 자료형 오류 |
| 500 | 서버 내부 오류 | Python 예외 또는 DB 처리 실패 |
| 503 | 외부 서버 사용 불가 | 정지된 Render 서버 호출 |

프런트엔드는 오류 응답과 성공 응답을 구분해야 합니다.

성공 응답 예시:

```json
{
  "id": "user01",
  "name": "홍길동"
}
```

오류 응답 예시:

```json
{
  "detail": "이미 사용 중인 아이디입니다."
}
```

오류 응답에는 `name`이 없기 때문에 무조건 `result["name"]`을 실행하면 `KeyError`가 발생합니다.

---

## 8. 실제로 해결한 Python 오류

### NameError

정의하지 않은 변수를 사용했을 때 발생했습니다.

```python
# 잘못된 코드
if auth_id == "id01":
```

함수 매개변수 이름과 통일했습니다.

```python
if input_id == "id01":
```

### AttributeError

Python 내장 함수인 `input`을 객체처럼 사용해서 발생했습니다.

```python
# 잘못된 코드
input.id
input.pwd
```

문자열 매개변수를 직접 사용하도록 수정했습니다.

```python
input_id
```

### ImportError

`supabase_client.py`에는 `supabase` 변수가 없고 `get_supabase()` 함수만 있었습니다.

```python
# 잘못된 import
from app.core.supabase_client import supabase
```

```python
# 올바른 import
from app.core.supabase_client import get_supabase
```

### KeyError

백엔드 오류 응답에 `name`이 없는데 다음 코드를 실행해서 발생했습니다.

```python
result["name"]
```

HTTP 상태 코드를 먼저 확인하고 오류를 `BackendAPIError`로 처리하도록 수정했습니다.

### SyntaxError

변수 대입문을 `st.info()` 괄호 안에 잘못 넣어서 발생했습니다.

```python
# 잘못된 구조
st.info(
    created_product = response.json()["data"]
)
```

```python
# 올바른 구조
created_product = response.json()["data"]

st.info(
    f"{created_product['name']}"
)
```

### IndentationError

`with st.form()`만 함수 밖으로 빠져서 발생했습니다.

```python
# 잘못된 구조
def product_update_delete():
    st.subheader("상품 수정")

with st.form("update_form"):
    ...
```

```python
# 올바른 구조
def product_update_delete():
    st.subheader("상품 수정")

    with st.form("update_form"):
        ...
```

파이썬에서는 같은 블록의 들여쓰기를 동일하게 유지해야 합니다.

---

## 9. 상품 페이지에서 변경한 내용

### Product Management

파일:

```text
frontend/app_pages/05_product_create.py
```

한 페이지 안에 다음 두 기능을 배치했습니다.

```text
Product Management
├─ 상품 생성 폼
└─ 상품 전체 조회
   ├─ 개수·평균·합계
   ├─ 검색
   ├─ 정렬
   └─ 표
```

상품 생성 요청에서는 백엔드 스키마에 없는 `id` 입력을 제거했습니다.

```python
payload = {
    "name": clean_name,
    "price": int(product_price),
}
```

백엔드의 공통 응답 구조에서 실제 데이터는 `data` 안에 있습니다.

```python
created_product = response.json()["data"]
products = response.json()["data"]
```

### 기존 물품 조회 페이지

파일:

```text
frontend/app_pages/06_product_select.py
```

기존 조회 전용 페이지는 삭제하지 않고 그대로 유지했습니다.

현재 사이드바에는 등록하지 않았지만 파일과 기존 기능은 보존되어 있습니다.

### 팝업형 수정·삭제 페이지

파일:

```text
frontend/app_pages/07_product_update_delete.py
```

전체 목록에서 행을 선택합니다.

```python
table_event = st.dataframe(
    table,
    on_select="rerun",
    selection_mode="single-row",
)
```

수정 버튼은 수정 팝업을 엽니다.

```python
@st.dialog("물품 수정")
def update_dialog(product: dict):
    ...
```

삭제 버튼은 삭제 확인 팝업을 엽니다.

```python
@st.dialog("물품 삭제")
def delete_dialog(product: dict):
    ...
```

---

## 10. 사이드바에서 배운 내용

`with st.sidebar:` 안에 있는 요소만 사이드바에 표시됩니다.

```python
with st.sidebar:
    st.page_link(home_page)
    st.page_link(weather_page)
    st.page_link(product_management_page)
    st.page_link(product_update_delete_page)

    st.divider()

    st.button(
        "LOGOUT",
        on_click=logout,
        use_container_width=True,
    )
```

로그아웃 버튼을 마지막에 작성해 메뉴 아래쪽에 배치했습니다.

현재 로그인 사용자의 메뉴:

```text
홈
날씨
product management
물품 수정·삭제
────────────────
LOGOUT
```

---

## 11. 로컬 서버 실행 방법

### 백엔드

```powershell
cd C:\mini_frontend\mini_frontend_login_db\backend
uvicorn app.main:app --reload --port 8001 --access-log
```

Swagger:

```text
http://127.0.0.1:8001/docs
```

### 프런트엔드

```powershell
cd C:\mini_frontend\mini_frontend_login_db\frontend
streamlit run app.py
```

---

## 12. 최종 테스트 순서

### 회원 기능

- [ ] 새로운 ID로 회원가입한다.
- [ ] Supabase `customers` 테이블에 저장되는지 확인한다.
- [ ] 같은 ID로 다시 가입해 409 처리를 확인한다.
- [ ] 올바른 비밀번호로 로그인한다.
- [ ] 틀린 비밀번호로 401 처리를 확인한다.
- [ ] 로그아웃한다.

### 상품 기능

- [ ] 상품을 생성한다.
- [ ] Supabase `products` 테이블에 저장되는지 확인한다.
- [ ] 생성된 상품이 조회 표에 표시되는지 확인한다.
- [ ] 상품명과 ID 검색을 확인한다.
- [ ] 가격·이름·ID 정렬을 확인한다.
- [ ] 목록에서 상품을 선택한다.
- [ ] 수정 팝업에서 이름과 가격을 변경한다.
- [ ] 삭제 팝업에서 상품을 삭제한다.
- [ ] Supabase 데이터가 함께 변경되는지 확인한다.

### 백엔드 로그

정상 동작 시 다음과 비슷한 로그가 출력됩니다.

```text
POST /product/create HTTP/1.1" 200 OK
GET /product/getall HTTP/1.1" 200 OK
PUT /product/{product_id} HTTP/1.1" 200 OK
DELETE /product/delete/{product_id} HTTP/1.1" 200 OK
```

---

## 13. 이번 프로젝트의 핵심 학습 포인트

1. 프런트엔드와 백엔드는 HTTP API로 통신한다.
2. FastAPI Router는 URL과 HTTP 메서드를 담당한다.
3. Pydantic Schema는 데이터 형식을 검사한다.
4. Service는 실제 비즈니스 로직과 DB 작업을 담당한다.
5. Supabase 응답 데이터는 `.data`에 들어 있다.
6. 프런트엔드에서는 성공 응답과 오류 응답을 구분해야 한다.
7. Python 변수명은 함수 매개변수와 일관되게 사용해야 한다.
8. Python 들여쓰기는 코드의 실행 범위를 결정한다.
9. Streamlit의 `st.form()`은 입력값을 한 번에 제출한다.
10. `st.dialog()`으로 수정·삭제 팝업을 만들 수 있다.
11. `st.session_state`로 페이지가 다시 실행되어도 상태를 관리할 수 있다.
12. 비밀키는 반드시 백엔드 환경변수에서 관리한다.

---

## 14. 한 문장으로 복습

> Streamlit에서 입력한 데이터를 HTTP 요청으로 FastAPI에 보내고, FastAPI가 Pydantic으로 검증한 뒤 Supabase에 CRUD 작업을 수행하며, 결과와 오류 상태 코드를 다시 화면에 표시하는 프로젝트를 완성했다.
