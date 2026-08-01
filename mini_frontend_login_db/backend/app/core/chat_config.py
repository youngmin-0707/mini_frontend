"""Gemini 챗에 필요한 `.env` 환경 변수를 먼저 로드합니다.

`main.py`가 이 모듈을 import하면 아래 코드가 즉시 실행됩니다.
그 다음 `chat_service.py`가 `GEMINI_API_KEY`를 읽을 수 있습니다.
"""

from pathlib import Path

from dotenv import load_dotenv

# 현재 파일의 위치에서 두 단계 위인 backend 폴더를 찾습니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# backend/.env의 값을 운영체제 환경 변수처럼 사용할 수 있게 로드합니다.
load_dotenv(PROJECT_ROOT / ".env")
