"""공통 로그인 상태와 인증 동작을 관리합니다."""

import streamlit as st


def init_state(stored_loginout: str = "logout") -> None:
    st.session_state.setdefault("loginout", stored_loginout)
    st.session_state.setdefault("login_id", "")
    st.session_state.setdefault("login_pwd", "")


def login() -> None:
    if (
        st.session_state.login_id == "id01"
        and st.session_state.login_pwd == "pwd01"
    ):
        st.session_state.loginout = "login"


def logout() -> None:
    st.session_state.loginout = "logout"
    st.session_state.login_id = ""
    st.session_state.login_pwd = ""


def is_logged_in() -> bool:
    return st.session_state.loginout == "login"
