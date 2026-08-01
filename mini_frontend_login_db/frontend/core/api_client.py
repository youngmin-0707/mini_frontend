"""모든 메뉴 API에서 공통으로 사용하는 HTTP 요청 기능입니다.

각 화면에서 httpx 코드를 반복하지 않도록 URL 조합, 타임아웃,
연결 오류, HTTP 상태 코드, JSON 변환을 이 파일 한 곳에서 처리합니다.
"""

import os
from typing import Any

import httpx

# 모든 인증 요청이 공통으로 사용할 백엔드 기본 주소입니다.
BACKEND_URL = "http://127.0.0.1:8001"
# BACKEND_URL = "https://mini-frontend.com"
# 서버 응답을 기다릴 최대 시간(초)입니다.
REQUEST_TIMEOUT = 15.0

# 화면에서 백엔드 오류를 구분해 처리하기 위한 사용자 정의 예외입니다.
class BackendAPIError(Exception):
    """백엔드 연결 또는 API 응답 처리 중 발생한 오류입니다."""


def request(method: str, path: str, json: dict[str, Any] | None = None):
    """HTTP 요청을 보내고 JSON을 반환하며, 실패는 BackendAPIError로 통일합니다."""
    # 네트워크 요청 자체가 실패하는 경우를 먼저 분리해 처리합니다.
    try:
        response = httpx.request(
            method,
            f"{BACKEND_URL}{path}",
            json=json,
            timeout=REQUEST_TIMEOUT,
        )
    except httpx.TimeoutException as error:
        raise BackendAPIError("백엔드 응답 시간이 초과되었습니다.") from error
    except httpx.RequestError as error:
        raise BackendAPIError(
            "백엔드 서버에 연결할 수 없습니다. 서버 실행 상태를 확인해 주세요."
        ) from error

    if response.status_code  == 401:
        raise BackendAPIError(
            "로그인 아이디 또는 패스워드 문제"
        )
    if response.status_code  == 404:
        raise BackendAPIError(
            "존재하지 않습니다."
        )
    if response.status_code  == 409:
        raise BackendAPIError(
            "ID가 사용 중 입니다."
        )
   
    try:
        payload = response.json()
    except ValueError as error:
        raise BackendAPIError("백엔드가 올바른 JSON을 반환하지 않았습니다.") from error
   
    return payload
