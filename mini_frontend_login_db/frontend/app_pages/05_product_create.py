import httpx
import pandas as pd
import streamlit as st


# 로컬 FastAPI 상품 API 주소
API_BASE_URL = "https://mini-frontend-login-db-7afb.onrender.com"


def show_api_error(response: httpx.Response) -> None:
    """백엔드가 반환한 오류를 화면에 표시합니다."""
    try:
        payload = response.json()
        detail = payload.get("detail")
    except (ValueError, AttributeError):
        detail = None

    if response.status_code == 404:
        st.error(detail or "상품을 찾을 수 없습니다.")
    elif response.status_code == 422:
        st.error(detail or "입력값의 형식이 올바르지 않습니다.")
    else:
        st.error(
            detail
            or (
                "요청을 처리하지 못했습니다. "
                f"(오류 코드: {response.status_code})"
            )
        )


def load_products() -> list[dict]:
    """백엔드에서 전체 물품 목록을 받아옵니다."""
    response = httpx.get(
        f"{API_BASE_URL}/product/getall",
        timeout=60.0,
    )

    response.raise_for_status()

    payload = response.json()

    return payload["data"]


def product_create() -> None:
    """입력한 물품 정보를 서버에 등록합니다."""
    st.title("📦 Product Management")
    st.subheader("물품 생성")
    st.caption("새 물품의 이름과 가격을 입력해 주세요.")

    with st.container(border=True):
        with st.form(
            "product_create_form",
            clear_on_submit=True,
        ):
            product_name = st.text_input(
                "물품명",
                placeholder="예: 무선 키보드",
                max_chars=50,
            )

            product_price = st.number_input(
                "가격",
                min_value=0,
                step=100,
                help="원 단위로 입력하세요.",
            )

            st.caption(
                f"등록 예정: "
                f"{product_name.strip() or '물품명 미입력'} · "
                f"{product_price:,.0f}원"
            )

            submitted = st.form_submit_button(
                "물품 등록",
                type="primary",
                use_container_width=True,
            )

    if not submitted:
        return

    clean_name = product_name.strip()

    if not clean_name:
        st.warning("물품명을 입력해 주세요.")
        return

    if product_price <= 0:
        st.warning("가격은 0원보다 크게 입력해 주세요.")
        return

    payload = {
        "name": clean_name,
        "price": int(product_price),
    }

    try:
        with st.spinner("물품을 등록하고 있습니다..."):
            response = httpx.post(
                f"{API_BASE_URL}/product/create",
                json=payload,
                timeout=60.0,
            )
    except httpx.RequestError:
        st.error("백엔드 서버에 연결할 수 없습니다.")
        return

    if response.status_code != 200:
        show_api_error(response)
        return

    try:
        created_product = response.json()["data"]
    except (ValueError, KeyError, TypeError):
        st.error("백엔드 응답 형식이 올바르지 않습니다.")
        return

    st.success("물품이 등록되었습니다.")

    st.info(
        f"ID {created_product['id']} · "
        f"{created_product['name']} · "
        f"{created_product['price']:,.0f}원"
    )


def product_select() -> None:
    """물품 목록을 검색하고 정렬해서 보여줍니다."""
    st.subheader("🔎 물품 조회")
    st.caption("등록된 물품을 이름 또는 ID로 찾아보세요.")

    try:
        with st.spinner("물품 목록을 불러오고 있습니다..."):
            products = load_products()
    except (
        httpx.RequestError,
        httpx.HTTPStatusError,
        ValueError,
        KeyError,
        TypeError,
    ):
        st.error("물품 목록을 불러오지 못했습니다.")

        if st.button("다시 불러오기", type="primary"):
            st.rerun()

        return

    if not products:
        st.info("등록된 물품이 없습니다.")
        return

    total_price = sum(
        float(product["price"])
        for product in products
    )

    metric_count, metric_average, metric_total = st.columns(3)

    metric_count.metric(
        "전체 물품",
        f"{len(products)}개",
    )

    metric_average.metric(
        "평균 가격",
        f"{total_price / len(products):,.0f}원",
    )

    metric_total.metric(
        "가격 합계",
        f"{total_price:,.0f}원",
    )

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
            [
                "ID 순",
                "낮은 가격순",
                "높은 가격순",
                "이름순",
            ],
            label_visibility="collapsed",
        )

    with refresh_col:
        if st.button(
            "새로고침",
            use_container_width=True,
        ):
            st.rerun()

    clean_keyword = keyword.strip().lower()

    filtered_products = [
        product
        for product in products
        if (
            clean_keyword in str(product["id"]).lower()
            or clean_keyword in str(product["name"]).lower()
        )
    ]

    sort_rules = {
        "ID 순": lambda product: str(product["id"]),
        "낮은 가격순": lambda product: float(product["price"]),
        "높은 가격순": lambda product: -float(product["price"]),
        "이름순": lambda product: str(product["name"]),
    }

    filtered_products.sort(
        key=sort_rules[sort_option],
    )

    st.caption(f"검색 결과 {len(filtered_products)}개")

    if not filtered_products:
        st.warning("검색 조건에 맞는 물품이 없습니다.")
        return

    table = pd.DataFrame(filtered_products)[
        ["id", "name", "price", "created_at"]
    ]

    table.columns = [
        "ID",
        "물품명",
        "가격",
        "등록일시",
    ]

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.TextColumn("ID"),
            "물품명": st.column_config.TextColumn("물품명"),
            "가격": st.column_config.NumberColumn(
                "가격",
                format="%d원",
            ),
            "등록일시": st.column_config.DatetimeColumn(
                "등록일시",
                format="YYYY-MM-DD HH:mm:ss",
            ),
        },
    )


# 위쪽에 생성 기능을 표시합니다.
product_create()

# 생성 기능과 조회 기능 사이에 구분선을 표시합니다.
st.divider()

# 아래쪽에 조회 기능을 표시합니다.
product_select()