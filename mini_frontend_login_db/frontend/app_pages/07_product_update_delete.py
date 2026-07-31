import httpx
import pandas as pd
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8001"


def load_products() -> list[dict]:
    """전체 상품을 조회합니다."""
    response = httpx.get(
        f"{API_BASE_URL}/product/getall",
        timeout=60.0,
    )

    response.raise_for_status()

    return response.json()["data"]


@st.dialog("물품 수정")
def update_dialog(product: dict) -> None:
    """선택한 상품을 수정하는 팝업입니다."""
    st.write(f"상품 ID: `{product['id']}`")

    with st.form("update_dialog_form"):
        updated_name = st.text_input(
            "상품명",
            value=product["name"],
        )

        updated_price = st.number_input(
            "가격",
            min_value=1,
            value=int(product["price"]),
            step=100,
        )

        save_button = st.form_submit_button(
            "저장",
            type="primary",
            use_container_width=True,
        )

    if save_button:
        response = httpx.put(
            f"{API_BASE_URL}/product/{product['id']}",
            json={
                "name": updated_name,
                "price": int(updated_price),
            },
            timeout=60.0,
        )

        if response.status_code == 200:
            st.session_state.product_message = (
                f"{updated_name} 물품을 수정했습니다."
            )
            st.rerun()
        else:
            st.error(
                f"수정하지 못했습니다. "
                f"오류 코드: {response.status_code}"
            )


@st.dialog("물품 삭제")
def delete_dialog(product: dict) -> None:
    """선택한 상품을 삭제하는 팝업입니다."""
    st.warning("삭제한 물품은 복구할 수 없습니다.")

    st.write(f"상품 ID: `{product['id']}`")
    st.write(f"상품명: **{product['name']}**")
    st.write(f"가격: **{product['price']:,.0f}원**")

    if st.button(
        "삭제 확인",
        type="primary",
        use_container_width=True,
    ):
        response = httpx.delete(
            (
                f"{API_BASE_URL}/product/delete/"
                f"{product['id']}"
            ),
            timeout=60.0,
        )

        if response.status_code == 200:
            st.session_state.product_message = (
                f"{product['name']} 물품을 삭제했습니다."
            )
            st.rerun()
        else:
            st.error(
                f"삭제하지 못했습니다. "
                f"오류 코드: {response.status_code}"
            )


def product_update_delete() -> None:
    """전체 목록에서 선택한 상품을 수정하거나 삭제합니다."""
    st.title("🛠️ 물품 수정·삭제")
    st.caption("목록에서 물품을 선택한 후 작업 버튼을 누르세요.")

    # 팝업에서 수정·삭제가 완료된 후 메시지를 표시합니다.
    message = st.session_state.pop(
        "product_message",
        None,
    )

    if message:
        st.success(message)

    try:
        products = load_products()
    except httpx.RequestError:
        st.error("백엔드 서버에 연결할 수 없습니다.")
        return
    except httpx.HTTPStatusError:
        st.error("상품 목록을 조회하지 못했습니다.")
        return

    if not products:
        st.info("등록된 상품이 없습니다.")
        return

    # 상품 목록을 표로 변환합니다.
    table = pd.DataFrame(products)[
        ["id", "name", "price", "created_at"]
    ]

    table.columns = [
        "ID",
        "물품명",
        "가격",
        "등록일시",
    ]

    # 표에서 한 행만 선택할 수 있도록 설정합니다.
    table_event = st.dataframe(
        table,
        use_container_width=True,
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
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

    selected_rows = table_event.selection.rows

    if not selected_rows:
        st.info("수정하거나 삭제할 물품을 선택하세요.")
        return

    # 선택된 표의 행 번호로 원본 상품을 찾습니다.
    selected_index = selected_rows[0]
    selected_product = products[selected_index]

    st.write(
        f"선택한 물품: **{selected_product['name']}**"
    )

    update_col, delete_col = st.columns(2)

    with update_col:
        if st.button(
            "수정",
            type="primary",
            use_container_width=True,
        ):
            update_dialog(selected_product)

    with delete_col:
        if st.button(
            "삭제",
            use_container_width=True,
        ):
            delete_dialog(selected_product)


product_update_delete()