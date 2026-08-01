"""백엔드의 상품 목록을 검색·정렬해 표로 보여 주는 조회 페이지입니다.

`load_products()`는 HTTP 통신을, `product_select()`는 화면 표시를 담당합니다.
역할을 나누면 코드를 읽고 테스트하기 쉬워집니다.
"""

import httpx
import pandas as pd
import streamlit as st


# 생성 화면과 같은 실제 백엔드 서버를 사용합니다.
# 상품 API 요청에 공통으로 사용할 백엔드 주소입니다.
# API_BASE_URL = "https://zero2-mini-project-2.onrender.com"


def load_products() -> list[dict]:
    """서버에서 전체 물품 목록을 받아옵니다."""
    # 전체 상품 조회 API에 GET 요청을 보냅니다.
    response = httpx.get(
        f"{API_BASE_URL}/product/getall",
        # 무료 서버가 잠든 경우 깨어나는 시간을 고려합니다.
        timeout=60.0,
    )
    # 실패 상태 코드라면 예외를 발생시켜 호출한 쪽에서 처리하게 합니다.
    response.raise_for_status()
    return response.json()


def product_select() -> None:
    """물품 목록을 검색하고 정렬해서 보여주는 화면입니다."""
    st.title("🔎 물품 조회")
    st.caption("등록된 물품을 이름 또는 ID로 빠르게 찾아보세요.")

    # 상품 목록을 불러오는 과정의 네트워크·응답 오류를 한곳에서 처리합니다.
    try:
        with st.spinner("물품 목록을 불러오고 있습니다..."):
            products = load_products()
    except (httpx.RequestError, httpx.HTTPStatusError, ValueError):
        # 서버 연결 실패와 잘못된 응답을 한 곳에서 간단히 안내합니다.
        st.error("물품 목록을 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.")
        if st.button("다시 불러오기", type="primary"):
            st.rerun()
        return

    # 빈 리스트라면 표 대신 상품 등록 페이지로 이동할 링크를 보여 줍니다.
    if not products:
        st.info("등록된 물품이 없습니다. 먼저 물품을 등록해 주세요.")
        st.page_link(
            "app_pages/05_product_create.py",
            label="첫 물품 등록하기",
            icon="📦",
        )
        return

    # 목록 위쪽에서 전체 현황을 한눈에 확인할 수 있습니다.
    # 모든 상품 가격의 합계를 구해 개수·평균·합계 지표를 계산합니다.
    total_price = sum(float(product["price"]) for product in products)
    metric_count, metric_average, metric_total = st.columns(3)
    metric_count.metric("전체 물품", f"{len(products)}개")
    metric_average.metric("평균 가격", f"{total_price / len(products):,.0f}원")
    metric_total.metric("가격 합계", f"{total_price:,.0f}원")

    # 검색창, 정렬 선택, 새로고침 버튼을 한 줄에 배치합니다.
    search_col, sort_col, refresh_col = st.columns([2, 1, 1])
    with search_col:
        keyword = st.text_input(
            "검색",
            placeholder="물품명 또는 ID 입력",
            label_visibility="collapsed",
        )
    with sort_col:
        sort_option = st.selectbox(
            "정렬",
            ["ID 순", "낮은 가격순", "높은 가격순", "이름순"],
            label_visibility="collapsed",
        )
    with refresh_col:
        if st.button("새로고침", use_container_width=True):
            st.rerun()

    # 검색어는 대소문자를 구분하지 않으며 ID 검색도 함께 지원합니다.
    clean_keyword = keyword.strip().lower()
    # ID 또는 상품명에 검색어가 포함된 상품만 새 리스트에 담습니다.
    filtered_products = [
        product
        for product in products
        if clean_keyword in str(product["id"]).lower()
        or clean_keyword in str(product["name"]).lower()
    ]

    # 화면의 정렬 옵션과 실제 정렬 기준 함수를 연결합니다.
    sort_rules = {
        "ID 순": lambda product: product["id"],
        "낮은 가격순": lambda product: float(product["price"]),
        "높은 가격순": lambda product: -float(product["price"]),
        "이름순": lambda product: str(product["name"]),
    }
    filtered_products.sort(key=sort_rules[sort_option])

    st.caption(f"검색 결과 {len(filtered_products)}개")

    if not filtered_products:
        st.warning("검색 조건에 맞는 물품이 없습니다.")
        return

    # 표에 표시할 열 이름과 가격 형식을 사용자가 읽기 쉽게 바꿉니다.
    # 딕셔너리 목록을 화면 표시에 편리한 DataFrame으로 변환합니다.
    table = pd.DataFrame(filtered_products)[["id", "name", "price"]]
    table.columns = ["ID", "물품명", "가격"]

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", format="%d"),
            "물품명": st.column_config.TextColumn("물품명"),
            "가격": st.column_config.NumberColumn("가격", format="%d원"),
        },
    )


# Streamlit이 이 파일을 실행할 때 상품 조회 화면 함수도 실행합니다.
product_select()
