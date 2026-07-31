from core.api_client import request

def login_process(id:str, pwd:str):
    return request("POST", f"auth/signin",json={"id":id,"pwd":pwd})

def logout_process(id:str):
    return request("GET",f"auth/get",{input_id})

def register_process(auth:dict):
    return request("POST",f"auth/create",json = auth)