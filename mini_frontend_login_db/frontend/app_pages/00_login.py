"""로그인 상태에 따라 로그인 폼 또는 로그아웃 버튼을 보여 주는 페이지입니다.

Streamlit은 위젯을 조작할 때마다 파일을 다시 실행하므로
로그인 정보는 `st.session_state`에 보관해 재실행 후에도 유지합니다.
"""

import streamlit as st

# 로그인 상태 확인, 로그인 처리, 로그아웃 처리 함수를 가져옵니다.
from core.auth import is_logged_in, login, logout


# 로그인하지 않은 사용자에게만 로그인 폼을 보여 줍니다.
if not is_logged_in():
    st.title("LOGIN")

    # form 안의 입력값은 LOGIN 버튼을 눌렀을 때 한 번에 제출됩니다.
    with st.form("login_form", clear_on_submit= True):
        login_id = st.text_input("ID 입력", value="id01")
        login_pwd = st.text_input("PWD 입력", type="password", value="pwd01")
        submiitted = st.form_submit_button("LOGIN")
    # 버튼이 눌렸을 때 입력한 ID와 비밀번호로 로그인을 시도합니다.
    if submiitted:
        login(login_id,login_pwd)
else:
    # 이미 로그인한 사용자에게는 성공 메시지와 로그아웃 버튼을 보여 줍니다.
    st.success("로그인되었습니다.")
    st.button("LOGOUT", on_click=logout)
