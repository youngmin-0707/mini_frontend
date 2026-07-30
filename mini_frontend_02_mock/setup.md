# 통합 프로젝트 Setup

이 문서는 `frontend`와 `backend` 프로젝트를 로컬 환경에서 함께 설치하고 실행하는 방법을 설명한다.

## 1. 준비 사항

- Python 3.11 이상
- PowerShell
- Gemini API 키

프로젝트 루트 경로:

```text
C:\mini_frontend\mini_frontend_02_mock
```

## 2. 백엔드 설치

PowerShell을 열고 백엔드 폴더로 이동한다.

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 3. 백엔드 환경 변수 설정

`backend` 폴더에 `.env` 파일을 만들고 다음 내용을 입력한다.

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash-lite
```

`your_api_key_here`는 실제 Gemini API 키로 변경한다. `.env` 파일은 Git에 올리지 않는다.

현재 백엔드 코드가 `.env` 파일을 자동으로 읽도록 구성되지 않은 경우, 실행할 PowerShell에서 다음과 같이 환경 변수를 설정한다.

```powershell
$env:GEMINI_API_KEY="your_api_key_here"
$env:GEMINI_MODEL="gemini-2.5-flash-lite"
```

## 4. 백엔드 실행

백엔드 가상환경이 활성화된 PowerShell에서 실행한다.

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

실행 주소:

- API 서버: `http://127.0.0.1:8000`
- API 문서: `http://127.0.0.1:8000/docs`

백엔드 실행 창은 종료하지 않고 그대로 둔다.

## 5. 프론트엔드 설치

새 PowerShell 창을 열고 프론트엔드 폴더로 이동한다.

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\frontend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 6. 프론트엔드 실행

프론트엔드 가상환경이 활성화된 PowerShell에서 실행한다.

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\frontend
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

실행 후 브라우저가 자동으로 열리지 않으면 다음 주소에 접속한다.

```text
http://localhost:8501
```

## 7. 실행 순서

매번 프로젝트를 실행할 때는 PowerShell 창을 두 개 사용한다.

### PowerShell 1: 백엔드

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\backend
.\.venv\Scripts\Activate.ps1
$env:GEMINI_API_KEY="your_api_key_here"
$env:GEMINI_MODEL="gemini-2.5-flash-lite"
python -m uvicorn app.main:app --reload
```

### PowerShell 2: 프론트엔드

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\frontend
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

## 8. 테스트 실행

백엔드 테스트:

```powershell
cd C:\mini_frontend\mini_frontend_02_mock\backend
.\.venv\Scripts\Activate.ps1
python -m pytest
```

## 9. 현재 확인할 사항

- 프론트엔드의 서버 상태 확인 화면은 `GET /health`를 호출하지만 현재 백엔드에는 해당 API가 없어 개발 전에는 `404`가 발생할 수 있다.
- Gemini 채팅은 올바른 `GEMINI_API_KEY`가 설정되어 있어야 동작한다.
- 현재 상품 API는 실제 데이터베이스가 아닌 예시 데이터를 사용한다.
- 현재 로그인과 회원가입은 백엔드 인증 및 데이터 저장과 연결되어 있지 않다.

## 10. 종료 방법

각 PowerShell 실행 창에서 `Ctrl + C`를 눌러 프론트엔드와 백엔드 서버를 종료한다.
