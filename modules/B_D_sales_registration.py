import streamlit as st
import pandas as pd
from datetime import datetime

def sales_registration_ui():
    st.subheader("🧾 판매 등록")

    if "직원이름" not in st.session_state or st.session_state["직원이름"] == "":
        st.warning("딜러 정보를 먼저 등록하세요.")
        return

    # Load car list dataset
    car_df = pd.read_csv("data/hyundae_car_list.csv")
    car_df = car_df.loc[car_df["브랜드"] != "기아", :]
    plant_df = pd.read_csv("data/inventory_data.csv")
    plant_df.columns = plant_df.columns.str.strip()
    plant_df = plant_df[plant_df["생산상태"] == "생산중"]

    model_options = sorted(car_df["모델명"].dropna().unique())

    # 판매 등록 입력 폼
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.markdown("##### 🚗 차량 선택")

        selected_model = st.selectbox("차종", model_options)
        available_trims = car_df[car_df["모델명"] == selected_model]["트림명"].dropna().unique()
        selected_trim = st.selectbox("트림명", sorted(available_trims), key=f"trim_{selected_model}")

        filtered_factories = plant_df[
            (plant_df["모델명"] == selected_model) &
            (plant_df["트림명"] == selected_trim)
        ]["공장명"].dropna().unique()
        selected_factory = st.selectbox("공장명", sorted(filtered_factories))

        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("##### 📝 판매 정보")

        stock_qty = plant_df[
            (plant_df["모델명"] == selected_model) &
            (plant_df["트림명"] == selected_trim) &
            (plant_df["공장명"] == selected_factory)
        ]["재고량"].min()

        customer = st.text_input("👤 고객명")
        contact = st.text_input("📞 연락처")
        sale_date = st.date_input("📅 판매일자", value=datetime.today())

        if st.button("✅ 판매 등록"):
            if not customer:
                st.warning("⚠️ 고객명을 입력해주세요.")
            elif stock_qty is None or stock_qty < 1 or selected_factory is None:
                st.error("🚫 해당 차량의 재고가 부족합니다.")
            else:
                if len(customer) >= 2:
                    masked_customer = customer[0] + "*" + customer[2:]
                else:
                    masked_customer = customer

                new_sale = {
                    "차종": selected_model,
                    "트림명": selected_trim,
                    "공장명": selected_factory,
                    "고객명": masked_customer,
                    "수량": 1,
                    "판매일자": sale_date.strftime("%Y-%m-%d"),
                }

                if "sales_log" not in st.session_state:
                    st.session_state.sales_log = []
                st.session_state.sales_log.append(new_sale)

                # 판매 고객 정보 및 차량 스펙 저장용 항목 구성
                car_info = car_df[
                    (car_df["모델명"] == selected_model) &
                    (car_df["트림명"] == selected_trim)
                ].iloc[0]  # assume 1 match

                customer_record = {
                    "이름": masked_customer,
                    "성별": st.session_state.get("성별", "미상"),
                    "현재 나이": st.session_state.get("나이", "미상"),
                    "연령대": st.session_state.get("연령대", "미상"),
                    "거주 지역": st.session_state.get("지역", "미상"),
                    "차량 구매 횟수": st.session_state.get("구매횟수", 1),
                    "고객 평생 가치": st.session_state.get("LTV", 0),
                    "브랜드": car_info["브랜드"],
                    "모델명": car_info["모델명"],
                    "기본가격": car_info["기본가격"],
                    "공장명": selected_factory
                }

                # 파일에 누적 저장
                csv_path = "data/D_domestic_sales_.csv"
                try:
                    existing_df = pd.read_csv(csv_path)
                    updated_df = pd.concat([existing_df, pd.DataFrame([customer_record])], ignore_index=True)
                except FileNotFoundError:
                    updated_df = pd.DataFrame([customer_record])

                # updated_df.to_csv(csv_path, index=False)

                st.success("✅ 판매 등록이 완료되었습니다.")

        st.markdown("</div>", unsafe_allow_html=True)

    # 누적 판매 통계
    if "sales_log" in st.session_state and st.session_state.sales_log:
        st.markdown("#### 📈 누적 판매량 (차종 기준)")
        df = pd.DataFrame(st.session_state.sales_log)
        stat_df = df.groupby(["차종", "트림명"])["수량"].sum().reset_index().sort_values(by="수량", ascending=False)
        st.dataframe(stat_df.rename(columns={"차종": "차종명", "수량": "누적 판매량"}), use_container_width=True, hide_index=True)

        st.markdown("#### 📊 최근 판매 현황")
        df = df.sort_values(by="판매일자", ascending=False)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("아직 등록된 판매 이력이 없습니다.")