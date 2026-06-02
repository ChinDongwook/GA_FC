import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
from fpdf import FPDF

# --- [1] 페이지 설정 및 스타일 ---
st.set_page_config(page_title="성남센터 연금 컨설턴트 Pro", layout="wide")
st.markdown("""
    <style>
    .stApp { font-size: 18px !important; }
    h1, h2, h3 { font-weight: 700 !important; }
    [data-testid="stMetricValue"] { font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 계산 로직 ---
def calculate_details(current_age, gender, monthly_pay, p_years, r_age):
    passed = r_age - current_age
    bonus = 0.24 if passed >= 30 else (0.16 if passed >= 25 else (0.07 if passed >= 20 else 0))
    p_rate = 0.050
    if 30 <= r_age < 40: p_rate = 0.022
    elif 40 <= r_age < 50: p_rate = 0.026
    elif 50 <= r_age < 55: p_rate = 0.0285
    elif 55 <= r_age < 65: p_rate = 0.040
    elif 65 <= r_age < 70: p_rate = 0.045
    elif 70 <= r_age < 80: p_rate = 0.0485
    if gender == "남": p_rate += 0.002
    
    total_prin = monthly_pay * 12 * p_years
    total_interest = 0
    for year in range(1, p_years + 1):
        time_to_retire = r_age - (current_age + year) + 1
        y_8 = max(0, min(time_to_retire, 20 - year + 1))
        y_5 = max(0, time_to_retire - y_8)
        total_interest += (monthly_pay * 12) * (0.08 * y_8 + 0.05 * y_5)
    
    base_reserve = total_prin + total_interest
    final_reserve = base_reserve * (1 + bonus)
    return total_prin, total_interest, (base_reserve * bonus), final_reserve, final_reserve * p_rate

# --- [3] 사이드바 입력 및 컨트롤 ---
with st.sidebar:
    st.title("고객 정보 입력")
    gender = st.selectbox("성별", ["남", "여"], index=1)
    birth_year = st.number_input("출생 연도", 1940, 2026, 1994)
    monthly_pay = st.number_input("월 납입 금액 (만원)", 10, 500, 50, 10)
    pay_years = st.selectbox("납입 기간 (년)", [5, 7, 10, 12, 15, 20, 25], index=2)
    current_age = datetime.date.today().year - birth_year
    target_r_age = st.slider("연금 개시 나이", current_age + pay_years + 5, 90, 65)
    
    st.markdown("---")
    st.subheader("📊 부가 분석 설정")
    show_expectancy = st.checkbox("기대여명 분석 보기")
    life_adj = st.slider("기대여명 보정(세)", -5, 10, 0)

# --- [4] 메인 대시보드 ---
t_prin, t_int, t_bonus, f_res, ann_pen = calculate_details(current_age, gender, monthly_pay, pay_years, target_r_age)

col1, col2, col3 = st.columns(3)
col1.metric("총 납입 원금", f"{t_prin:,.0f} 만원")
col2.metric("최종 연금 준비금", f"{f_res:,.0f} 만원")
col3.metric("예상 월 수령액", f"{ann_pen/12:,.0f} 만원")

# 2. 개시 연령별 비교 (차트 내 월/연 수령액 동시 표시)
st.subheader("2. 연금 개시 연령별 수령액 비교")
compare_data = []
for age in range(target_r_age - 5, target_r_age + 6):
    _, _, _, _, a_pen = calculate_details(current_age, gender, monthly_pay, pay_years, age)
    compare_data.append({"개시 연령": f"{age}세", "월 수령액": a_pen/12, "연 수령액": a_pen})

df_bar = pd.DataFrame(compare_data)
fig_bar = px.bar(df_bar, x="개시 연령", y="월 수령액", text_auto='.0f', hover_data=["연 수령액"])
st.plotly_chart(fig_bar, use_container_width=True)

# 4. 기대여명 분석 (사이드바 체크박스 연동)
if show_expectancy:
    st.markdown("---")
    st.subheader("4. 기대여명으로 보는 예상 수익")
    base_life = 85 + life_adj
    st.write(f"고객님의 예상 기대수명은 **{base_life-2}세 ~ {base_life+8}세**입니다.")
    # (이하 수익률 차트 로직...)
