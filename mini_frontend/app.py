"""초보자를 위한 가장 간단한 Streamlit 멀티페이지 앱입니다."""

import streamlit as st
from streamlit_session_browser_storage import SessionStorage


st.set_page_config(
    page_title="Layout",
    page_icon="🌱",
    layout="wide",
)

home_page = st.Page("app_pages/01_home.py", default=True)
login_page = st.Page("app_pages/00_login.py")
signup_page = st.Page("app_pages/02_signup.py")
log_page = st.Page("app_pages/03_log_view.py")
database_page = st.Page("app_pages/05_database_view.py")
df_page = st.Page("app_pages/df.py")
chart_page = st.Page("app_pages/chart.py")
student_page = st.Page("app_pages/student.py")


pages = [home_page, student_page, login_page, signup_page, log_page, database_page, df_page, chart_page]



navigation = st.navigation(pages, position="hidden")

with st.sidebar:
    st.info("화면왼쪽")
    st.divider()
    st.page_link(home_page, label="🌱 HOME")
    st.page_link(login_page, label="🌱 Sign In")
    st.page_link(signup_page, label="🌱 Sign Up")
    st.page_link(log_page, label="🌱 LOG")
    st.page_link(database_page, label="🌱 DATABASE")
    st.divider()
    st.page_link(df_page, label="🌱 DataFrame")
    st.page_link(chart_page, label="🌱 Chart")
    st.page_link(student_page, label="🌱 Student")

navigation.run()