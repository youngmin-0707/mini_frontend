from core.api_client import request

def login_process(id:str, pwd:str):
    """  로그인 진행 ID와 PWD 입력 하면 사용자 정보 리턴"""
    return request("POST", f"/auth/signin", json={"id":id, "pwd":pwd})

def logout_process(id:str):
    return request("GET", f"/auth/signout/{id}")

def register_process(auth:dict):
    return request("POST", f"/auth/create", json=auth)

def get_auth_process(id:str):
    """ ID를 전달하여 회원 정보를 조회 """
    return request(
        "GET",
        "/auth/get",
        params={"id": id},
    )

def update_password_process(id:str, current_pwd:str, new_pwd:str):
    """ 현재 비밀번호를 확인하고 새 비밀번호로 변경 """
    return request(
        "PUT",
        "/auth/password",
        json={
            "id": id,
            "current_pwd": current_pwd,
            "new_pwd": new_pwd,
        },
    )