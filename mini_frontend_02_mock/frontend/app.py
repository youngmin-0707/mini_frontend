"""초보자를 위한 가장 간단한 Streamlit 멀티페이지 앱입니다."""

import streamlit as st
from streamlit_session_browser_storage import SessionStorage

from core.auth import init_state, is_logged_in, logout


st.set_page_config(
    page_title="Layout",
    page_icon="🌱",
    layout="wide",
)

storage = SessionStorage(key="login_session_storage")
stored_loginout = storage.getItem("loginout") or "logout"

if "loginout" not in st.session_state:
    init_state(stored_loginout)

if st.session_state.loginout != stored_loginout:
    storage.setItem(
        "loginout",
        st.session_state.loginout,
        key=f"save_{st.session_state.loginout}",
    )

home_page = st.Page("app_pages/01_home.py", title="홈", icon="🏠", default=True)
login_page = st.Page("app_pages/00_login.py", title="로그인", icon="🔐")
signup_page = st.Page("app_pages/02_signup.py", title="회원가입", icon="📝")
weather_page = st.Page("app_pages/03_weather.py", title="날씨조회", icon="📝")
health_page = st.Page("app_pages/04_health.py", title="서버체크", icon="📝")



if st.session_state.loginout == "login":
    pages = [
        home_page,
        weather_page
    ]
else:
    pages = [home_page, login_page, signup_page, health_page]


navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    st.page_link(home_page)

    if st.session_state.loginout == "login":
        st.button("LOGOUT", on_click=logout, use_container_width=True)
        st.page_link(weather_page)
    else:
        st.page_link(login_page)
        st.page_link(signup_page)
        st.page_link(health_page)

navigation.run()
