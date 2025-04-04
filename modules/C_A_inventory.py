# 재고 자동 경고 
# 글로벌 재고 최적화, 공급망 관리


import streamlit as st
from .C_A_inventory_distribution import distribution_ui
from .C_A_inventory_warning import warning_ui
from .C_A_inventory_turnover import turnover_ui


def inventory_ui():
    # 탭 스타일 커스터마이징
    st.markdown("""
        <style>
            div[data-baseweb="tabs"] > div {
                background-color: #fff;
                padding: 0.5rem 1rem;
            }
            div[data-baseweb="tab"] {
                font-weight: 500;
                color: #666;
            }
            div[data-baseweb="tab"][aria-selected="true"] {
                border-bottom: 3px solid #ff4b4b;
                color: black !important;
                font-weight: 700;
            }
        </style>
    """, unsafe_allow_html=True)

    # 탭 구성
    tab_names = [
        "공장 및 차종별 재고 현황",
        "재고 경고 시스템",
        "재고 회전율 분석"

        ""
    ]
    
    selected_tab = st.tabs(tab_names)

    # 각 탭별 UI 호출
    with selected_tab[0]:
        distribution_ui()       # 공장/지역별 재고 분포

    with selected_tab[1]:
        warning_ui()            # 재고 경고 시스템   

    with selected_tab[2]:
        turnover_ui()          # 재고 회전율 분석