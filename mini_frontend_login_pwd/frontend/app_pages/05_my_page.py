import streamlit as st

from clients.auth_client import get_auth_process, update_password_process
from core.api_client import BackendAPIError
from core.auth import is_logged_in


st.title("👤 My Page")
st.write("나의 정보를 조회합니다.")


if not is_logged_in():
    st.warning("로그인 후 이용할 수 있습니다.")
    st.stop()


with st.form("my_page_form"):
    input_id = st.text_input(
        "ID 입력",
        value=st.session_state.login_id,
    )

    submitted = st.form_submit_button("조회")


if submitted:
    input_id = input_id.strip()

    if not input_id:
        st.warning("조회할 ID를 입력해 주세요.")
    else:
        try:
            with st.spinner("회원 정보를 조회하고 있습니다."):
                result = get_auth_process(input_id)

            st.success("회원 정보를 조회했습니다.")

            st.write("ID:", result["id"])
            st.write("이름:", result["name"])

        except BackendAPIError as error:
            st.error(str(error))


st.divider()
st.subheader("🔑 비밀번호 변경")

with st.form("password_form"):
    current_pwd = st.text_input("현재 비밀번호", type="password")
    new_pwd = st.text_input("새 비밀번호", type="password")
    change = st.form_submit_button("비밀번호 변경")

if change:
    if not current_pwd or len(new_pwd) < 4:
        st.warning("현재 비밀번호와 4자 이상의 새 비밀번호를 입력하세요.")
    else:
        try:
            update_password_process(
                st.session_state.login_id,
                current_pwd,
                new_pwd,
            )
            st.success("비밀번호가 변경되었습니다.")
        except BackendAPIError as error:
            st.error(str(error))
            