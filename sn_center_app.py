import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- [1] 페이지 설정 ---
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

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

# --- [3] 메인 포털 레이아웃 (3개 탭) ---
st.title("🏢 더블유에셋 성남센터")
tab1, tab2, tab3 = st.tabs(["1. 센터 소개", "2. 금융 정보 칼럼", "3. 연금 시뮬레이터"])

with tab1:
    st.header("전문가 그룹, 성남센터입니다")
    st.markdown("고객의 자산을 내 자산처럼 소중히 여기는 더블유에셋 성남센터입니다.")
    st.divider()
    st.subheader("센터 안내")
    st.write("📍 위치: 경기도 성남시 (상세 주소 입력)")
    st.write("📞 문의: 센터 연락처 입력")

with tab2:
    st.header("금융 정보 칼럼")
    st.markdown("---")
    st.subheader("💡 박곰희 노후준비 머니 매니지먼트")
    st.write("현금으로 썩히지 마세요! 퇴직연금(DC형) 운용 팁을 확인하세요.")
    if st.button("박곰희 투자 전략 더 보기"):
        st.write("1. 계좌 시스템화: 무관심 투자가 장기 수익률을 높입니다.")
        st.write("2. 깔대기 전략: 월급통장 → CMA → ISA 계좌로 흐르게 하세요.")
    
    st.markdown("---")
    st.subheader("💰 ISA 계좌 활용법")
    st.write("전 금융기관 통틀어 딱 1개만 개설 가능한 ISA, 절세의 핵심입니다.")

with tab3:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("현재 나이와 납입 계획을 입력하여 노후 수령액을 계산해 보세요.")
    
    # 시뮬레이터 입력창
    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("성별", ["남", "여"], index=1)
        birth_year = st.number_input("출생 연도", 1940, 2024, 1994)
    with col2:
        monthly_pay = st.number_input("월 납입 (만원)", 10, 500, 50)
        pay_years = st.selectbox("납입 기간 (년)", [5, 10, 15, 20, 25], index=1)
    
    current_age = datetime.date.today().year - birth_year
    target_r_age = st.slider("연금 개시 나이", current_age + pay_years + 5, 90, 65)
    
    t_prin, t_int, bonus, f_res, ann_pen = calculate_details(current_age, gender, monthly_pay, pay_years, target_r_age)
    
    st.divider()
    m_col1, m_col2 = st.columns(2)
    m_col1.metric("최종 연금 준비금", f"{f_res:,.0f} 만원")
    m_col2.metric("예상 월 수령액", f"{(ann_pen/12):,.0f} 만원")
