"""Customer 한 명 또는 전체 목록을 조회하는 Streamlit 화면입니다."""

import streamlit as st

from clients.customer_client import customer_select, customer_select_all
from core.api_client import BackendAPIError


def show_customer(customer: dict) -> None:
    """비밀번호를 제외한 고객 정보를 화면에 표시합니다."""
    with st.container(border=True):
        st.write(f"ID: {customer['id']}")
        st.write(f"이름: {customer['name']}")
        st.write(f"나이: {customer['age']}")
        st.write(f"등록시각: {customer['timestamp']}")


st.subheader("Customer 조회")
st.caption("ID 한 개를 검색하거나 등록된 Customer 전체를 조회할 수 있습니다.")

customer_id = st.text_input("조회할 ID", placeholder="id01")
one_column, all_column = st.columns(2)

with one_column:
    select_one = st.button("한 개 조회", use_container_width=True)

with all_column:
    select_all = st.button("전체 조회", use_container_width=True)

if select_one:
    if not customer_id.strip():
        st.warning("조회할 ID를 입력해 주세요.")
    else:
        try:
            with st.spinner("Customer를 조회하고 있습니다."):
                result = customer_select(customer_id.strip())
            show_customer(result["customer"])
        except BackendAPIError as error:
            st.error(str(error))

if select_all:
    try:
        with st.spinner("Customer 목록을 조회하고 있습니다."):
            result = customer_select_all()

        st.info(f"전체 Customer 수: {result['count']}")
        if not result["customers"]:
            st.info("등록된 Customer가 없습니다.")
        else:
            for customer in result["customers"]:
                show_customer(customer)
    except BackendAPIError as error:
        st.error(str(error))
