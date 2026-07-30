"""Customer 데이터를 입력하는 Streamlit 화면입니다."""

import streamlit as st

from clients.customer_client import customer_insert
from core.api_client import BackendAPIError


st.subheader("Customer 입력")
st.caption("ID는 id01, 비밀번호는 pwd01 형식으로 입력해 주세요.")

with st.form("customer_form", clear_on_submit=True):
    customer_id = st.text_input("ID", placeholder="id01")
    customer_pwd = st.text_input("PWD", type="password", placeholder="pwd01")
    customer_name = st.text_input("NAME", placeholder="이름 입력")
    customer_age = st.number_input("AGE", min_value=0, max_value=150, step=1)
    submitted = st.form_submit_button("등록")

if submitted:
    # 화면에서도 빈 입력을 먼저 확인하고, 최종 형식 검사는 백엔드가 담당합니다.
    if not customer_id.strip() or not customer_pwd.strip() or not customer_name.strip():
        st.warning("모든 항목을 입력해 주세요.")
    else:
        payload = {
            "id": customer_id.strip(),
            "pwd": customer_pwd.strip(),
            "name": customer_name.strip(),
            "age": int(customer_age),
        }

        try:
            with st.spinner("Customer를 등록하고 있습니다."):
                result = customer_insert(payload)

            customer = result["customer"]
            st.success(result["message"])
            st.write(
                f"ID: {customer['id']} / 이름: {customer['name']} / "
                f"나이: {customer['age']} / 등록시각: {customer['timestamp']}"
            )
        except BackendAPIError as error:
            st.error(str(error))
