import streamlit as st

from core.auth import is_logged_in, login, logout


if not is_logged_in():
    st.title("LOGIN")

    with st.form("login_form"):
        st.text_input("ID 입력", key="login_id")
        st.text_input("PWD 입력", type="password", key="login_pwd")
        st.form_submit_button("LOGIN", on_click=login)

else:
    st.success("로그인되었습니다.")
    st.button("LOGOUT", on_click=logout)
