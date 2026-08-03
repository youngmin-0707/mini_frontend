# My Page(나의 정보 조회) 구현 계획

## 1. 목표

로그인한 사용자가 홈 아래의 **My Page** 메뉴에서 자신의 정보를 조회할 수 있도록 한다.

- 화면 이름: `My Page` (`나의 정보 조회`)
- 백엔드 경로: `GET /auth/get`
- 요청 데이터: 사용자 ID
- 응답 데이터: `id`, `name`
- 사용자 ID 기본값: 브라우저 Session Storage의 `login_id`

## 2. 현재 구조

로그인 성공 시 아래 정보가 저장된다.

- Streamlit 세션: `st.session_state.login_id`, `st.session_state.login_name`
- 브라우저 Session Storage: `login_id`, `login_name`, `loginout`
- 백엔드 주소: `frontend/core/api_client.py`의 `BACKEND_URL`
- 사용자 테이블: Supabase `customers`
- 공개 사용자 스키마: `AuthPublic(id, name)`

My Page에서는 비밀번호를 전달하지 않고 Session Storage에서 복원된 `login_id`를 조회 ID의 기본값으로 사용한다.

## 3. API 계약

### 요청

```http
GET /auth/get?id=id01
```

| 항목 | 위치 | 필수 | 설명 |
|---|---|---:|---|
| `id` | Query parameter | 예 | 조회할 사용자 ID |

### 성공 응답 (`200 OK`)

```json
{
  "id": "id01",
  "name": "홍길동"
}
```

응답에는 `pwd`와 Supabase 내부 정보가 포함되지 않아야 한다.

### 오류 응답

- `404 Not Found`: 해당 ID의 사용자가 존재하지 않음
- `422 Unprocessable Entity`: ID가 누락되었거나 유효하지 않음
- `500 Internal Server Error`: Supabase 조회 등 서버 내부 오류

## 4. 백엔드 구현 계획

### 4.1 라우터 추가

대상: `backend/app/routers/auth_router.py`

- `GET /auth/get` 엔드포인트를 추가한다.
- 쿼리 파라미터 `id`를 받는다.
- 서비스의 사용자 조회 함수를 호출한다.
- 반환 타입은 기존 `AuthPublic`을 사용한다.

예정 인터페이스:

```python
@auth_router.get("/auth/get", response_model=AuthPublic)
def get_auth(id: str) -> AuthPublic:
    return get_auth_process(id)
```

### 4.2 서비스 로직 추가

대상: `backend/app/services/auth_service.py`

- 기존 `_customer_get(customer_id)`를 재사용한다.
- 사용자가 없으면 `HTTPException(status_code=404, ...)`을 발생시킨다.
- 조회 결과를 `AuthPublic`으로 변환해 `id`, `name`만 반환한다.
- DB 결과의 `pwd`는 응답에 포함하지 않는다.

### 4.3 백엔드 테스트 추가

대상: `backend/tests/test_auth_router.py` 신규 생성

- 존재하는 ID 조회 시 `200`인지 확인한다.
- 응답에 `id`, `name`이 있고 `pwd`가 없는지 확인한다.
- 존재하지 않는 ID 조회 시 `404`인지 확인한다.
- ID 파라미터가 없을 때 `422`인지 확인한다.
- 실제 Supabase 대신 monkeypatch를 사용한다.

## 5. 프론트엔드 구현 계획

### 5.1 인증 API 클라이언트 추가

대상: `frontend/clients/auth_client.py`

- `get_my_info(id: str)` 함수를 추가한다.
- 공통 `request()` 함수를 통해 `/auth/get`을 호출한다.
- 입력값을 안전하게 인코딩하기 위해 `frontend/core/api_client.py`의 `request()`가 선택적으로 `params`를 받도록 확장한다.

예정 호출:

```python
request("GET", "/auth/get", params={"id": id})
```

최종 요청 예시:

```text
http://127.0.0.1:8000/auth/get?id=id01
```

### 5.2 My Page 화면 생성

대상: `frontend/app_pages/05_my_page.py` 신규 생성

화면 구성:

1. 제목 `My Page`
2. 설명 `나의 정보 조회`
3. ID 입력창
4. `조회` 버튼
5. 조회된 ID와 이름 표시 영역
6. 오류 메시지 영역

동작 흐름:

1. 로그인 여부를 확인한다.
2. `st.session_state.login_id`를 ID 입력창 기본값으로 사용한다.
3. 조회 버튼을 누르면 ID의 앞뒤 공백을 제거한다.
4. 빈 ID이면 API를 호출하지 않고 입력 안내를 표시한다.
5. API에 ID를 전달한다.
6. 응답의 `id`, `name`을 출력한다.

### 5.3 메뉴 등록

대상: `frontend/app.py`

- `my_page = st.Page(...)`를 등록한다.
- 로그인 상태의 페이지 목록에서 홈 바로 다음에 배치한다.
- 사이드바에서도 홈 바로 아래에 링크를 표시한다.
- 로그아웃 상태에서는 My Page를 표시하지 않는다.

예정 메뉴 순서:

```text
홈
My Page
날씨조회
LOGOUT
```

## 6. 데이터 흐름

```text
브라우저 Session Storage(login_id)
        ↓ 앱 시작 시 복원
st.session_state.login_id
        ↓ 입력창 기본값
My Page의 ID 입력 및 조회 버튼
        ↓ GET /auth/get?id={id}
FastAPI auth_router
        ↓
auth_service의 사용자 조회
        ↓
Supabase customers 테이블
        ↓
AuthPublic { id, name }
        ↓
My Page 화면 출력
```

## 7. 검증 절차

### 백엔드 자동 테스트

```powershell
cd backend
pytest tests/test_auth_router.py
```

### API 수동 테스트

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/auth/get?id=id01"
```

확인 사항:

- 등록된 ID이면 `id`, `name`이 출력된다.
- 존재하지 않는 ID이면 `404`가 반환된다.
- 응답에 비밀번호가 포함되지 않는다.

### 프론트엔드 수동 테스트

1. 로그인한다.
2. 사이드바 홈 아래에 My Page가 표시되는지 확인한다.
3. My Page에서 로그인 ID가 입력창 기본값인지 확인한다.
4. 조회 버튼을 누르면 ID와 이름이 표시되는지 확인한다.
5. 존재하지 않는 ID와 빈 ID에 알맞은 메시지가 표시되는지 확인한다.
6. 로그아웃 후 My Page 메뉴가 사라지는지 확인한다.
7. 새로고침 후 Session Storage에서 로그인 ID가 복원되는지 확인한다.

## 8. 구현 순서

1. 백엔드 사용자 조회 서비스 추가
2. `GET /auth/get` 라우터 추가
3. 백엔드 테스트 작성 및 실행
4. 공통 API 클라이언트에 `params` 지원 추가
5. 인증 클라이언트에 사용자 조회 함수 추가
6. My Page 화면 생성
7. 로그인 사용자 메뉴에 My Page 등록
8. 백엔드·프론트엔드 통합 확인

## 9. 보안상 제한과 후속 개선

현재 프로젝트는 로그인 ID를 Session Storage에 저장하지만 서버가 검증하는 인증 토큰은 사용하지 않는다. 따라서 사용자가 입력 ID를 바꾸면 다른 사용자의 `id`, `name`을 조회할 수 있다.

이번 기능은 현재 구조에 맞춰 구현하되, 실제 서비스에서는 아래 개선이 필요하다.

- 로그인 성공 시 서버가 세션 또는 JWT를 발급한다.
- My Page API는 요청받은 ID가 아니라 인증 토큰의 사용자 ID를 사용한다.
- 장기적으로는 `GET /auth/me` 형태로 변경한다.
- Service Role key는 백엔드 `.env`에서만 관리한다.

## 10. 완료 기준

- 로그인 사용자에게만 My Page가 보인다.
- Session Storage에서 복원된 ID로 조회할 수 있다.
- `/auth/get`이 `id`, `name`만 반환한다.
- 사용자 미존재 및 빈 입력 오류가 처리된다.
- 기존 로그인·회원가입·로그아웃 기능이 정상 동작한다.
- 백엔드 테스트와 수동 통합 검증을 통과한다.
