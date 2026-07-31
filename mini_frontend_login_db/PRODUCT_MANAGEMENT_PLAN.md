# Product Management 페이지 통합 계획서

## 1. 작업 목표

- 기존 `물품 생성` 페이지와 `물품 조회` 페이지를 한 페이지로 통합한다.
- 통합 페이지는 위쪽에 물품 생성 폼, 아래쪽에 전체 물품 조회·검색·정렬 기능을 배치한다.
- 사이드바 메뉴 이름은 정확히 `product management`로 표시한다.
- 물품 수정·삭제 기능은 별도의 페이지로 만든다.
- 기존 함수명, 화면 구성, 주석, 오류 처리 방식을 가능한 한 재사용한다.
- 상품 데이터 형식과 API 주소는 `backend`의 스키마와 라우터를 기준으로 맞춘다.

## 2. 백엔드 기준 데이터 형식

참조 파일:

- `backend/app/schemas/product_schema.py`
- `backend/app/routers/product_router.py`
- `backend/app/services/product_service.py`
- `backend/app/core/api_response.py`

### 상품 생성 요청

`ProductCreate`에는 다음 두 필드만 있다.

```json
{
  "name": "무선 키보드",
  "price": 35000
}
```

- `id`는 프런트에서 입력하지 않는다.
- `products.id`의 기존 `text` 형식과 기존 데이터는 그대로 유지한다.
- 백엔드 `product_create()`가 현재 시각을 이용해 문자열 ID를 자동 생성한다.
- `created_at`도 백엔드에서 자동 생성한다.

### 상품 수정 요청

`ProductUpdate`에는 다음 두 필드가 필요하다.

```json
{
  "name": "기계식 키보드",
  "price": 45000
}
```

수정할 상품 ID는 요청 본문이 아닌 URL 경로로 전달한다.

```text
PUT /product/{product_id}
```

### 상품 응답

`ProductPublic`의 형식은 다음과 같다.

```json
{
  "id": "20260721170435315246",
  "name": "무선 키보드",
  "price": 35000,
  "created_at": "2026-07-21T17:04:35+09:00"
}
```

백엔드 라우터는 이 상품 객체를 바로 반환하지 않고 `ApiResponse`로 감싸서 반환한다.

```json
{
  "success": true,
  "message": "상품이 등록되었습니다.",
  "data": {
    "id": "20260721170435315246",
    "name": "무선 키보드",
    "price": 35000,
    "created_at": "2026-07-21T17:04:35+09:00"
  }
}
```

따라서 프런트에서는 `response.json()["data"]`를 사용해야 한다.

## 3. 현재 코드에서 먼저 바로잡을 부분

### 생성 화면의 ID 입력 제거

현재 `frontend/app_pages/05_product_create.py`는 사용자가 `product_id`를 입력하게 되어 있지만, 백엔드 `ProductCreate`에는 `id`가 없다.

통합 페이지의 생성 폼은 다음 두 항목만 유지한다.

- 물품명 `name`
- 가격 `price`

생성된 ID는 등록 성공 응답에서 읽어 사용자에게 표시한다.

### API 응답의 `data` 사용

현재 생성 페이지는 다음처럼 응답 전체를 상품으로 사용한다.

```python
created_product = response.json()
```

다음 구조로 변경해야 한다.

```python
created_product = response.json()["data"]
```

현재 조회 페이지도 `response.json()` 전체를 상품 목록으로 사용하고 있으므로 다음처럼 변경해야 한다.

```python
return response.json()["data"]
```

### 백엔드 주소 통일

현재 생성·조회 페이지는 Render 주소를 직접 사용한다.

```python
API_BASE_URL = "https://zero2-mini-project-2.onrender.com"
```

로컬 개발에서는 실행 중인 FastAPI 주소를 사용한다.

```python
API_BASE_URL = "http://127.0.0.1:8001"
```

배포 주소 전환은 이후 환경변수로 분리할 수 있지만, 이번 작업에서는 기존 코드 스타일을 유지하면서 두 상품 페이지에 같은 주소를 사용한다.

## 4. 파일별 작업 계획

### 4.0 디렉터리 구조 원칙

새 폴더를 추가하지 않고 기존 구조를 최대한 재사용한다.

```text
mini_frontend_login_db/
├─ backend/
│  └─ app/
│     ├─ routers/
│     │  └─ product_router.py          # 기존 API 재사용
│     ├─ schemas/
│     │  └─ product_schema.py          # 기존 데이터 형식 재사용
│     └─ services/
│        └─ product_service.py         # 기존 생성·조회·수정·삭제 로직 재사용
└─ frontend/
   ├─ app.py                           # 사이드바 이름과 페이지 연결 변경
   └─ app_pages/
      ├─ 05_product_create.py          # 기존 생성 + 기존 조회 코드 통합
      ├─ 06_product_select.py          # 통합 완료 전까지 원본 보관
      └─ 07_product_update_delete.py   # 새 수정·삭제 페이지
```

기존 데이터, API 주소, 함수 이름을 재사용하므로 파일 이동이나 대규모 이름 변경은 하지 않는다.

### 4.1 `frontend/app_pages/05_product_create.py`

이 파일을 물품 생성·조회 통합 페이지의 기반 파일로 재사용한다.

유지할 기존 요소:

- `show_api_error()`
- `product_create()`
- 생성 폼의 컨테이너, spinner, 입력 검증
- 생성 성공 메시지
- 네트워크 오류 처리

`06_product_select.py`에서 가져올 요소:

- `load_products()`
- `product_select()`
- 전체 개수·평균 가격·가격 합계 지표
- 검색 기능
- 정렬 기능
- 새로고침 버튼
- pandas DataFrame 표

최종 화면 호출 순서:

```python
product_create()
st.divider()
product_select()
```

생성 성공 직후에는 `st.rerun()`을 호출해 아래 상품 목록에 새 데이터가 즉시 나타나도록 한다.

페이지 제목은 중복 출력을 막기 위해 최상위에서 한 번만 표시한다.

```python
st.title("📦 Product Management")
```

각 기능은 하위 제목으로 구분한다.

```python
st.subheader("물품 생성")
st.subheader("물품 조회")
```

### 4.2 `frontend/app_pages/06_product_select.py`

기존 물품 조회 기능을 그대로 유지한다.

`05_product_create.py`의 통합 조회 기능과 별개로, 기존 조회 전용 페이지의 코드와 파일을 삭제하지 않는다.

### 4.3 `frontend/app_pages/07_product_update_delete.py`

수정·삭제 전용 페이지를 새로 만든다.

재사용할 스타일:

- 기존 상품 페이지의 `API_BASE_URL`
- `httpx` 요청 방식
- `st.container(border=True)`
- `st.form()`
- spinner 및 오류 메시지
- `load_products()`와 동일한 전체 목록 조회 흐름

페이지 구성:

1. 전체 상품 목록을 불러온다.
2. `selectbox`에서 수정·삭제할 상품을 선택한다.
3. 선택한 상품의 ID, 이름, 가격을 표시한다.
4. 수정 폼에는 기존 이름과 가격을 기본값으로 넣는다.
5. 수정 버튼은 `PUT /product/{product_id}`를 호출한다.
6. 삭제 버튼은 `DELETE /product/delete/{product_id}`를 호출한다.
7. 성공 후 `st.rerun()`으로 최신 목록을 다시 불러온다.

수정 요청 예시:

```python
response = httpx.put(
    f"{API_BASE_URL}/product/{product_id}",
    json={
        "name": updated_name,
        "price": int(updated_price),
    },
    timeout=60.0,
)
```

삭제 요청 예시:

```python
response = httpx.delete(
    f"{API_BASE_URL}/product/delete/{product_id}",
    timeout=60.0,
)
```

실수로 삭제하는 것을 막기 위해 확인 체크박스를 둔다.

```python
confirm_delete = st.checkbox("선택한 물품을 삭제하는 것에 동의합니다.")
```

확인하지 않으면 삭제 버튼을 비활성화한다.

### 4.4 `frontend/app.py`

기존 두 페이지 선언:

- `product_create_page`
- `product_select_page`

이를 다음 두 페이지 선언으로 정리한다.

- `product_management_page`
- `product_update_delete_page`

통합 페이지 선언:

```python
product_management_page = st.Page(
    "app_pages/05_product_create.py",
    title="product management",
    icon="📦",
)
```

수정·삭제 페이지 선언:

```python
product_update_delete_page = st.Page(
    "app_pages/07_product_update_delete.py",
    title="물품 수정·삭제",
    icon="🛠️",
)
```

로그인 상태의 `pages` 목록과 사이드바에는 다음 두 페이지만 상품 메뉴로 등록한다.

```python
product_management_page
product_update_delete_page
```

기존 `product_select_page`는 내비게이션과 사이드바에서 제거한다.

## 5. 백엔드 변경 여부

이번 화면 통합에 필요한 백엔드 API는 이미 구현되어 있다.

- `POST /product/create`
- `GET /product/getall`
- `PUT /product/{product_id}`
- `DELETE /product/delete/{product_id}`

따라서 우선 백엔드 코드는 변경하지 않는다.

프런트엔드는 다음 응답 규칙을 정확히 따라야 한다.

- 성공 데이터: `response.json()["data"]`
- 백엔드 검증 실패: `422`
- 존재하지 않는 상품: `404`
- 서버 또는 DB 처리 실패: `500`

## 6. 구현 순서

1. `05_product_create.py`의 생성 요청을 백엔드 `ProductCreate` 형식에 맞춘다.
2. `06_product_select.py`의 조회 함수와 화면 코드를 `05_product_create.py`에 통합한다.
3. 생성 성공 후 조회 목록이 즉시 갱신되는지 확인한다.
4. 준비된 `07_product_update_delete.py` 뼈대에 수정 기능을 작성한다.
5. 같은 파일에 삭제 기능을 작성한다.
6. `app.py`의 페이지 선언, 로그인 페이지 목록, 사이드바 링크를 변경한다.
7. 기존 `06_product_select.py`가 변경되지 않았는지 확인한다.
8. 로컬 FastAPI와 Streamlit을 실행해 전체 흐름을 검증한다.

## 7. 검증 항목

### 통합 페이지

- 사이드바에 `product management`가 표시된다.
- 물품 생성 폼 아래에 조회 기능이 표시된다.
- 생성 폼에는 이름과 가격만 입력한다.
- 생성하면 Supabase `products` 테이블에 데이터가 추가된다.
- 생성 직후 아래 목록에 새 상품이 나타난다.
- 검색과 네 가지 정렬 옵션이 정상 작동한다.
- 빈 목록과 검색 결과 없음 메시지가 정상 표시된다.

### 수정·삭제 페이지

- 기존 상품을 선택할 수 있다.
- 선택한 상품의 현재 이름과 가격이 수정 폼 기본값으로 표시된다.
- 수정하면 Supabase 데이터와 화면이 함께 변경된다.
- 삭제 확인 전에는 삭제할 수 없다.
- 삭제하면 Supabase와 화면 목록에서 사라진다.
- 존재하지 않는 상품에 대한 `404`를 사용자 메시지로 표시한다.

### 회귀 확인

- 로그인한 사용자에게만 두 상품 페이지가 표시된다.
- 홈, 날씨, 로그인, 회원가입 페이지 동작에 영향이 없다.
- 기존 백엔드 상품 테스트가 계속 통과한다.

## 8. 예상 최종 파일 구성

```text
frontend/
  app.py
  app_pages/
    05_product_create.py          # 생성 + 조회 통합
    06_product_select.py          # 기존 조회 전용 기능 그대로 유지
    07_product_update_delete.py   # 수정 + 삭제
```

기존 파일과 함수명을 최대한 유지하기 위해 통합 페이지의 실제 파일명은 우선 `05_product_create.py`를 그대로 사용한다. 사용자에게 보이는 사이드바 이름만 `product management`로 변경한다.
