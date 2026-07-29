import httpx
import pandas as pd
import streamlit as st


# 생성 화면과 같은 서버를 사용해야 등록한 물품을 바로 조회할 수 있습니다.
API_BASE_URL = "https://zero2-mini-project-2.onrender.com"


def load_products() -> list[dict]:
    """서버에서 전체 물품 목록을 받아옵니다."""
    response = httpx.get(
        f"{API_BASE_URL}/product/getall",
        timeout=15.0,
    )
    response.raise_for_status()
    return response.json()


def product_select() -> None:
    """물품 목록을 검색하고 정렬해서 보여주는 화면입니다."""
    st.title("🔎 물품 조회")
    st.caption("등록된 물품을 이름 또는 ID로 빠르게 찾아보세요.")

    try:
        with st.spinner("물품 목록을 불러오고 있습니다..."):
            products = load_products()
    except (httpx.RequestError, httpx.HTTPStatusError, ValueError):
        # 서버 연결 실패와 잘못된 응답을 한 곳에서 간단히 안내합니다.
        st.error("물품 목록을 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.")
        if st.button("다시 불러오기", type="primary"):
            st.rerun()
        return

    if not products:
        st.info("등록된 물품이 없습니다. 먼저 물품을 등록해 주세요.")
        st.page_link(
            "app_pages/05_product_create.py",
            label="첫 물품 등록하기",
            icon="📦",
        )
        return

    # 목록 위쪽에서 전체 현황을 한눈에 확인할 수 있습니다.
    total_price = sum(float(product["price"]) for product in products)
    metric_count, metric_average, metric_total = st.columns(3)
    metric_count.metric("전체 물품", f"{len(products)}개")
    metric_average.metric("평균 가격", f"{total_price / len(products):,.0f}원")
    metric_total.metric("가격 합계", f"{total_price:,.0f}원")

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
    filtered_products = [
        product
        for product in products
        if clean_keyword in str(product["id"]).lower()
        or clean_keyword in str(product["name"]).lower()
    ]

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


product_select()
