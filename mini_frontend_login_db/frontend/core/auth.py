"""공통 로그인 상태와 인증 동작을 관리합니다."""

import streamlit as st
from core.api_client import BackendAPIError
# 백엔드의 로그인·로그아웃 API를 호출하는 함수를 가져옵니다.
from app_pages.clients.auth_client import login_process, logout_process

# 로그인 관련 세션 값이 없을 때만 전달받은 기본값으로 초기화합니다.
def init_state(
    stored_loginout: str = "logout",
    stored_login_id: str = "",
    stored_login_name: str = "",
) -> None:
    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", stored_login_id)
    st.session_state.setdefault("login_name", stored_login_name)

# Login with Fronend
# 현재는 학습용 고정 ID와 비밀번호를 비교해 로그인 상태를 변경합니다.
def login(login_id:str, login_pwd:str) -> None:
    if login_id == "id01" and login_pwd == "pwd01":
        st.session_state.loginout = "login"
        st.session_state.login_id = login_id
        st.session_state.login_name = "이말숙"
        # 상태 변경 결과가 즉시 화면에 반영되도록 앱을 처음부터 다시 실행합니다.
        st.rerun()
    else:
        st.error("로그인 아이디 또는 패스워드 틀림")

# 세션에 저장된 로그인 정보를 빈 값으로 되돌립니다.
def logout() -> None:
    st.session_state.loginout = "logout"
    st.session_state.login_id = ""
    st.session_state.login_pwd = ""
    st.session_state.login_name = ""

# Login with Backend
# 아래 주석 블록은 백엔드 API로 로그인할 때 사용할 수 있는 예시 코드입니다.
# def login(login_id:str, login_pwd:str) -> None:
#     try:
#         result = login_process(login_id, login_pwd)
#         if result is not None:
#             st.session_state.loginout = "login"
#             st.session_state.login_id = login_id
#             st.session_state.login_name = result["name"]
#             st.rerun()
#     except BackendAPIError as error:
#         st.error(str(error))

# def logout() -> None:
#     result = logout_process(st.session_state.login_id)
#     if result is not None:
#         st.session_state.loginout = "logout"
#         st.session_state.login_id = ""
#         st.session_state.login_pwd = ""
#         st.session_state.login_name = ""


# 다른 페이지에서 현재 로그인 여부를 간단히 확인하도록 True/False를 반환합니다.
def is_logged_in() -> bool:
    return st.session_state.loginout == "login" 
        
