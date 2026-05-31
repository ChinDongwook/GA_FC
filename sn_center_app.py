import streamlit as st
import pandas as pd
import plotly.express as px
import datetime

# --- [1] 페이지 기본 설정 ---
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

# --- [2] 계산 로직 함수 ---
def calculate_details(current_age, gender, monthly_pay, p_years, r_age):
    passed = r_age - current_age
    if passed >= 30: bonus = 0.24
    elif passed >= 25: bonus = 0.16
    elif passed >= 20: bonus = 0.07
    else: bonus = 0
    if 30 <= r_age < 40: p_rate = 0.022
    elif 40 <= r_age < 50: p_rate = 0.026
    elif 50 <= r_age < 55: p_rate = 0.0285
    elif 55 <= r_age < 65: p_rate = 0.040
    elif 65 <= r_age < 70: p_rate = 0.045
    elif 70 <= r_age < 80: p_rate = 0.0485
    else: p_rate = 0.050
    if gender == "남": p_rate += 0.002
    total_prin = monthly_pay * 12 * p_years
    total_interest = 0
    for year in range(1, p_years + 1):
        time_to_retire = r_age - (current_age + year) + 1
        y_8 = max(0, min(time_to_retire, 20 - year + 1))
        y_5 = max(0, time_to_retire - y_8)
        total_interest += (monthly_pay * 12) * (0.08 * y_8 + 0.05 * y_5)
    base_reserve = total_prin + total_interest
    bonus_amount = base_reserve * bonus
    final_reserve = base_reserve + bonus_amount
    annual_pension = final_reserve * p_rate
    return total_prin, total_interest, bonus_amount, final_reserve, annual_pension

# --- [3] 메인 레이아웃 (탭 구성) ---
st.title("🏢 더블유에셋 성남센터")
tab1, tab2 = st.tabs(["센터 소개", "연금 시뮬레이터"])

with tab1:
    st.header("성남센터에 오신 것을 환영합니다")
    st.write("더블유에셋 성남센터는 고객의 성공적인 자산 관리와 안정적인 노후를 위해 최선을 다합니다.")
    st.divider()
    st.subheader("우리의 약속")
    st.info("데이터에 기반한 철저한 재무 컨설팅을 제공합니다.")

with tab2:
    st.header("프리미엄 연금 시뮬레이터")
    # 시뮬레이터 로직
    with st.sidebar:
        st.title("⚙️ 입력부")
        gender = st.selectbox("성별", ["남", "여"], index=1)
        birth_year = st.number_input("출생 연도", 1940, 2024, 1994)
        current_age = datetime.date.today().year - birth_year
        monthly_pay = st.number_input("월 납입 금액 (만원)", 10, 500, 50, 10)
        pay_years = st.selectbox("납입 기간 (년)", [5, 10, 15, 20, 25], index=2)
        target_r_age = st.slider("연금 개시 나이", current_age + pay_years + 5, 90, 65)

    t_prin, t_int, t_bonus, f_res, ann_pen = calculate_details(current_age, gender, monthly_pay, pay_years, target_r_age)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("총 납입 원금", f"{t_prin:,.0f} 만원")
    col2.metric("최종 준비금", f"{f_res:,.0f} 만원")
    col3.metric("예상 월 수령액", f"{(ann_pen/12):,.0f} 만원")
    
    st.subheader("1. 예상 연금 준비금 구성 비율")
    df_pie = pd.DataFrame({"항목": ["원금", "이자", "보너스"], "금액": [t_prin, t_int, t_bonus]})
    fig = px.pie(df_pie, values="금액", names="항목", hole=0.4)
    fig.update_traces(texttemplate='<b>%{label}</b><br>%{value:,.0f} 만원')
    st.plotly_chart(fig, use_container_width=True)
