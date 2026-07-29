import httpx
import streamlit as st


# 물품 관련 API는 현재 정상 응답하는 서버 주소 하나만 사용합니다.
API_BASE_URL = "http://127.0.0.1:8000"


def show_api_error(response: httpx.Response) -> None:
    """서버가 보내 준 오류를 사용자가 이해하기 쉬운 문장으로 보여줍니다."""
    if response.status_code == 422:
        st.error("입력값의 형식이 올바르지 않습니다. ID와 가격을 다시 확인해 주세요.")
    else:
        st.error(f"물품을 등록하지 못했습니다. (오류 코드: {response.status_code})")


def product_create() -> None:
    """입력한 물품 정보를 서버에 등록하는 화면입니다."""
    st.title("📦 물품 생성")
    st.caption("새 물품의 ID, 이름, 가격을 입력해 주세요.")

    with st.container(border=True):
        st.markdown("#### 물품 정보")

        # form 안의 값은 '물품 등록' 버튼을 눌렀을 때 한 번에 처리됩니다.
        with st.form("product_create_form", clear_on_submit=True):
            product_id = st.number_input(
                "물품 ID",
                min_value=1,
                step=1,
                help="다른 물품과 겹치지 않는 숫자를 입력하세요.",
            )
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
                f"등록 예정: ID {product_id} · "
                f"{product_name.strip() or '물품명 미입력'} · {product_price:,.0f}원"
            )
            submitted = st.form_submit_button(
                "물품 등록",
                type="primary",
                use_container_width=True,
            )

    if not submitted:
        return

    clean_name = product_name.strip()

    # 빈 이름과 0원 가격은 실수로 입력했을 가능성이 높아 서버 요청 전에 막습니다.
    if not clean_name:
        st.warning("물품명을 입력해 주세요.")
        return
    if product_price <= 0:
        st.warning("가격은 0원보다 크게 입력해 주세요.")
        return

    payload = {
        "id": int(product_id),
        "name": clean_name,
        "price": int(product_price),
    }

    try:
        with st.spinner("물품을 등록하고 있습니다..."):
            response = httpx.post(
                f"{API_BASE_URL}/product/create",
                json=payload,
                timeout=15.0,
            )
    except httpx.RequestError:
        # 인터넷 연결 또는 서버 문제도 화면이 멈추지 않도록 처리합니다.
        st.error("서버에 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.")
        return

    if response.status_code != 200:
        show_api_error(response)
        return

    created_product = response.json()
    st.success("물품이 등록되었습니다.")
    st.info(
        f"ID {created_product['id']} · {created_product['name']} · "
        f"{created_product['price']:,.0f}원"
    )
    st.page_link(
        "app_pages/06_product_select.py",
        label="등록된 물품 확인하기",
        icon="🔎",
    )


product_create()
