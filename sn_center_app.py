import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- [1] 페이지 설정 및 스타일 ---
st.set_page_config(page_title="더블유에셋 성남센터", page_icon="🏢", layout="wide")

# CSS를 활용한 세련된 탭 스타일링
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { font-size: 18px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- [2] 계산 로직 ---
def calculate_details(current_age, gender, monthly_pay, p_years, r_age):
    passed = r_age - current_age
    bonus = 0.24 if passed >= 30 else (0.16 if passed >= 25 else (0.07 if passed >= 20 else 0))
    p_rate = 0.040 if 55 <= r_age < 65 else 0.045
    if gender == "남": p_rate += 0.002
    
    total_prin = monthly_pay * 12 * p_years
    total_interest = 0
    for year in range(1, p_years + 1):
        time_to_retire = r_age - (current_age + year) + 1
        y_8 = max(0, min(time_to_retire, 20 - year + 1))
        y_5 = max(0, time_to_retire - y_8)
        total_interest += (monthly_pay * 12) * (0.08 * y_8 + 0.05 * y_5)
    
    final_reserve = (total_prin + total_interest) * (1 + bonus)
    return total_prin, total_interest, bonus, final_reserve, final_reserve * p_rate

# --- [3] 메인 화면 구성 ---
st.title("🏢 더블유에셋 성남센터")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["센터 소개", "금융 전문 칼럼", "연금 시뮬레이터"])

with tab1:
    st.subheader("데이터에 기반한 프리미엄 재무 설계")
    st.write("더블유에셋 성남센터는 고객님의 라이프사이클에 맞춘 체계적인 솔루션을 제공합니다.")
    st.info("전문적인 상담을 통해 안정적인 미래를 준비하세요.")

with tab2:
    st.subheader("전문가 인사이트")
    st.markdown("---")
    with st.expander("💡 박곰희 노후준비: 계좌의 시스템화"):
        st.write("퇴직연금과 ISA 계좌를 활용해 자동 투자 시스템을 구축하는 것이 장기 수익률의 핵심입니다.")
    with st.expander("💰 ISA 계좌, 왜 필수인가?"):
        st.write("1인 1계좌의 절세 혜택. 효율적인 자산 배분을 통해 세금을 최적화하세요.")

with tab3:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("고객님의 노후 자산을 지금 바로 설계해보세요.")
    
    # URL 주소 설정 (공유해주신 링크)
    sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    
    # 현재 창에서 이동하는 세련된 버튼 스타일
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <a href="{sim_url}" target="_self" 
               style="background-color: #003366; color: white; padding: 20px 40px; text-decoration: none; border-radius: 10px; font-size: 22px; font-weight: bold;">
               🚀 시뮬레이터 바로가기
            </a>
        </div>
    """, unsafe_allow_html=True)
