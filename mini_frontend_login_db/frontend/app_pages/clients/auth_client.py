"""인증 화면이 사용할 백엔드 API 호출 함수를 모아 둔 클라이언트입니다.

화면은 정확한 URL이나 HTTP 세부 설정을 알 필요 없이 이 함수들만 호출합니다.
실제 통신과 공통 오류 처리는 `core.api_client.request()`가 담당합니다.
"""

# 모든 HTTP 요청에 공통으로 사용하는 request 함수를 가져옵니다.
from core.api_client import request

# ID와 비밀번호를 JSON으로 만들어 로그인 API에 전달합니다.
def login_process(id:str, pwd:str):
    """로그인 정보를 JSON 본문으로 보냅니다."""
    return request("POST", f"auth/signin",json={"id":id,"pwd":pwd})

# 사용자 ID를 이용해 로그아웃 API를 호출합니다.
def logout_process(id:str):
    """현재 사용자 ID로 로그아웃 API를 호출합니다."""
    return request("GET",f"auth/get",{input_id})

# 회원가입 폼에서 만든 딕셔너리를 회원가입 API에 전달합니다.
def register_process(auth:dict):
    """회원가입 폼의 딕셔너리를 JSON으로 보냅니다."""
    return request("POST",f"/auth/create",json = auth)
