
"""
[ 프로그램 상세 로직 및 구조 엄격 유지 ]
1. 자산 축적: 가입 후 20년까지 연 8% 단리, 이후 개시 전까지 연 5% 단리 적용.
2. 장기유지 가산보너스는 유지20년시 7%, 25년시 16%, 30년시 24% 적용.
3. 연금준비금: (원금 + 적립이자) × (1 + 가산율 보너스).
4. 연금 수령액: 최종준비금 × 연령별 지급률 (남성 0.2% 추가 가산).
5. 시각화 출력: 스트림릿(Streamlit) 환경에 맞춘 핵심 요약 지표 및 3대 차트(파이/바/영역) 순정 유지.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from fpdf import FPDF
import io

# PDF 생성 함수
def create_pdf(current_age, final_reserve, monthly_pension):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Pension Simulation Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Current Age: {current_age}", ln=True)
    pdf.cell(200, 10, txt=f"Final Reserve: {final_reserve:,.0f} KRW", ln=True)
    pdf.cell(200, 10, txt=f"Expected Monthly Pension: {monthly_pension:,.0f} KRW", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- [1] 페이지 기본 설정 ---
st.set_page_config(
    page_title="최저보증 변액종신연금 컨설팅 시뮬레이터",
    page_icon="프리미엄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- [2] 핵심 계산 로직 함수 ---
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

# --- [3] 사이드바 (입력부) ---
with st.sidebar:
    st.title("고객 정보 입력")
    gender = st.selectbox("▶ 성별", ["남", "여"], index=1)
    col1, col2 = st.columns(2)
    today = datetime.date.today()
    with col1:
        birth_year = st.number_input("출생 연도", min_value=1940, max_value=today.year, value=1994, step=1)
    with col2:
        birth_month = st.number_input("출생 월", min_value=1, max_value=12, value=4, step=1)
    current_age = today.year - birth_year
    if today.month < birth_month: current_age -= 1
    st.success(f"현재 나이: **만 {current_age}세**")
    monthly_pay = st.number_input("▶ 월 납입 금액 (만원)", min_value=10, max_value=500, value=50, step=10)
    pay_years = st.selectbox("▶ 납입 기간 (년)", [5, 7, 10, 12, 15, 20, 25], index=2)
    min_retire_age = current_age + pay_years + 5
    target_r_age = st.slider("▶ 분석할 연금 개시 나이", min_value=min_retire_age, max_value=90, value=max(65, min_retire_age))
    compare_range = st.slider("▶ 비교할 개시 연령 범위", min_value=min_retire_age, max_value=90, value=(max(60, min_retire_age), min(max(60, min_retire_age) + 10, 90)))

# --- [4] 메인 화면 대시보드 ---
st.title("최저보증 변액종신연금 시뮬레이터")
t_prin, t_int, t_bonus, f_res, ann_pen = calculate_details(current_age, gender, monthly_pay, pay_years, target_r_age)
month_pen = ann_pen / 12

col1, col2, col3 = st.columns(3)
with col1: st.metric(label="총 납입 원금", value=f"{t_prin:,.0f} 만원")
with col2: st.metric(label=f"최종 연금 준비금 ({target_r_age}세)", value=f"{f_res:,.0f} 만원", delta=f"수익 +{(t_int+t_bonus):,.0f} 만원")
with col3: st.metric(label="예상 월 수령액", value=f"{month_pen:,.0f} 만원/월", delta=f"연 {ann_pen:,.0f} 만원")

# --- CSS 최적화 (요청 사항 반영) ---
st.markdown("""
    <style>
    /* 1. 사이드바 폭 축소 (20% 가량 축소) */
    [data-testid="stSidebar"] { min-width: 200px !important; max-width: 240px !important; }
    
    /* 2. 타이틀 텍스트 축소 */
    h1 { font-size: 28px !important; }
    
    /* 기존 스타일 유지 */
    .stApp { font-size: 16px !important; }
    h2, h3 { font-weight: 700 !important; }
    [data-testid="stMetricValue"] { font-size: 24px !important; }
    </style>
    """, unsafe_allow_html=True)

# 차트 구성 (로직 유지)
st.subheader("1. 예상 연금 준비금 구성 비율")
df_pie = pd.DataFrame({"항목": ["순수 납입 원금", "누적 적립 이자", "장기유지 가산보너스"], "금액": [t_prin, t_int, t_bonus]})
fig_pie = px.pie(df_pie, values="금액", names="항목", hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
st.plotly_chart(fig_pie, use_container_width=True)
