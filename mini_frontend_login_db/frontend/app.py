"""초보자를 위한 가장 간단한 Streamlit 멀티페이지 앱입니다."""

import streamlit as st
from streamlit_session_browser_storage import SessionStorage

# 로그인 상태를 초기화하고 확인하는 공통 함수를 가져옵니다.
from core.auth import init_state, is_logged_in, logout


# 브라우저 탭 제목, 아이콘, 화면 너비 등 앱 전체 설정입니다.
st.set_page_config(
    page_title="Layout",
    page_icon="🌱",
    layout="wide",
)

# st.markdown
#--------------------------------------------------------------
# 브라우저를 새로고침해도 로그인 상태를 유지할 수 있도록 저장소를 만듭니다.
storage = SessionStorage(key="login_session_storage")

# 브라우저 저장소에 값이 없으면 로그아웃 상태와 빈 문자열을 기본값으로 사용합니다.
stored_loginout = storage.getItem("loginout") or "logout"
stored_login_id = storage.getItem("login_id") or ""
stored_login_name = storage.getItem("login_name") or ""


# Streamlit 세션이 처음 만들어졌을 때만 로그인 상태를 초기화합니다.
if "loginout" not in st.session_state:
    init_state(stored_loginout, stored_login_id, stored_login_name)

# 세션의 로그인 상태가 바뀌면 브라우저 저장소에도 반영합니다.
if st.session_state.loginout != stored_loginout:
    storage.setItem(
        "loginout",
        st.session_state.loginout,
        key=f"save{st.session_state.loginout}",
    )
# 로그아웃 상태라면 브라우저에 남은 로그인 정보를 모두 지웁니다.
if st.session_state.loginout == "logout":
    # 브라우저 Session Storage의 로그인 정보 삭제
    storage.deleteAll(key="login_session_storage")
else:
    storage.setItem(
        "login_id",
        st.session_state.login_id,
        key="save_login_id",
    )
    storage.setItem(
        "login_name",
        st.session_state.login_name,
        key="save_login_name",
    )
#로그인 상태저장
#--------------------------------------------------------------------
home_page = st.Page("app_pages/01_home.py", title="홈", icon="🏠", default=True)
login_page = st.Page("app_pages/00_login.py", title="로그인", icon="🔐")
signup_page = st.Page("app_pages/02_signup.py", title="회원가입", icon="📝")
weather_page = st.Page("app_pages/03_weather.py", title="날씨", icon="📝")
health_page = st.Page("app_pages/04_health.py", title="서버체크", icon="📝")
product_management_page = st.Page(
    "app_pages/05_product_create.py",
    title="product management",
    icon="📦",
)
product_update_delete_page = st.Page(
    "app_pages/07_product_update_delete.py",
    title="물품 수정·삭제",
    icon="🛠️",
)

# 로그인 여부에 따라 접근 가능한 페이지 목록을 구성합니다.
if st.session_state.loginout == "login":
    pages = [
        home_page,
        weather_page,
        product_management_page,
        product_update_delete_page,
    ]
else:
    pages = [
        home_page,
        login_page,
        signup_page,
        health_page,
    ]


# 기본 내비게이션 메뉴는 숨기고 사이드바 메뉴를 직접 구성합니다.
navigation = st.navigation(
    pages,
    position="hidden",
)


# 사이드바 메뉴를 구성합니다.
with st.sidebar:
    st.page_link(home_page)

    if st.session_state.loginout == "login":
        st.page_link(weather_page)
        st.page_link(product_management_page)
        st.page_link(product_update_delete_page)

        # 메뉴 링크 아래에 간격을 추가합니다.
        st.divider()

        # 로그아웃 버튼을 사이드바 요소 중 마지막에 배치합니다.
        st.button(
            "LOGOUT",
            on_click=logout,
            use_container_width=True,
        )

    else:
        st.page_link(login_page)
        st.page_link(signup_page)
        st.page_link(health_page)

# 현재 선택된 페이지의 Python 코드를 실행합니다.
navigation.run()

