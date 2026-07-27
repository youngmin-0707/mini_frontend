import streamlit as st
import pandas as pd



st.title("LOGIN")

students = [
    {
        "id": "student1",
        "password": "1234",
        "name": "홍길동",
    },
    {
        "id": "student2",
        "password": "5678",
        "name": "김철수",
    },
]

df = pd.DataFrame(students)


with st.form("login_form"):
    login_id = st.text_input("ID 입력")
    login_password = st.text_input("PWD 입력", type="password")
    login_submitted = st.form_submit_button("LOGIN")

if login_submitted:
    login_user = None

    # 입력한 ID와 비밀번호가 일치하는 회원 찾기
    for student in students:
        if (
            student["id"] == login_id
            and student["password"] == login_password
        ):
            login_user = student
            break

    if login_user:
        st.success(f"{login_user['name']}님, 로그인되었습니다.")
    else:
        st.error("ID 또는 비밀번호가 올바르지 않습니다.")