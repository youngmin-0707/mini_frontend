# 모든 HTTP 요청에 공통으로 사용하는 request 함수를 가져옵니다.
from core.api_client import request

# ID와 비밀번호를 JSON으로 만들어 로그인 API에 전달합니다.
def login_process(id:str, pwd:str):
    return request("POST", f"auth/signin",json={"id":id,"pwd":pwd})

# 사용자 ID를 이용해 로그아웃 API를 호출합니다.
def logout_process(id:str):
    return request("GET",f"auth/get",{input_id})

# 회원가입 폼에서 만든 딕셔너리를 회원가입 API에 전달합니다.
def register_process(auth:dict):
    return request("POST",f"/auth/create",json = auth)
