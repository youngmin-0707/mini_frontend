import streamlit as st
from app_pages.clients.auth_client import register_process

st.title("📝 회원가입")

# 최초 실행 시 회원가입 완료 여부 초기화
st.session_state.setdefault("signup_complete", False)
st.session_state.setdefault("signup_name", "")

if not st.session_state.signup_complete:
    st.write("회원 정보를 입력해 주세요.")

    with st.form("signup_form", clear_on_submit=True):
        signup_id = st.text_input(
            "ID",
            placeholder="사용할 ID를 입력하세요",
        )
        signup_pwd = st.text_input(
            "PWD",
            type="password",
            placeholder="사용할 비밀번호를 입력하세요",
        )
        signup_name = st.text_input(
            "이름",
            placeholder="이름을 입력하세요",
        )

        signup_submitted = st.form_submit_button(
            "회원가입",
            type="primary",
            use_container_width=True,
        )

    if signup_submitted:
        if not signup_id or not signup_pwd or not signup_name:
            st.warning("ID, PWD, 이름을 모두 입력해 주세요.")
        else:
            payload = {
                "id": signup_id,
                "pwd": signup_pwd,
                "name": signup_name,
            }

            result = register_process(payload)

            if result is not None:
                st.session_state.signup_complete = True
                st.session_state.signup_name = result["name"]
                st.rerun()

else:
    st.success(
        f"{st.session_state.signup_name}님, "
        "회원가입 정보가 입력되었습니다."
    )