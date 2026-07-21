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
    page_icon="최저보증 변액연금",
    layout="wide",
    initial_sidebar_state="expanded"
)

# [핵심] 타이틀 텍스트 크기 축소 CSS
st.markdown("""
    <style>
    /* 수정된 부분: 콘텐츠 컨테이너 너비 제한 */
    .block-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    /* 타이틀(h1) 및 서브헤더(h3) 크기 조정 */
    h1 { font-size: 28px !important; }
    h3 { font-size: 20px !important; }
    .stApp { font-size: 18px !important; }
    [data-testid="stMetricValue"] { font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

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
    cust_name = st.text_input("▶ 고객 이름", value="홍길동")
    gender = st.selectbox("▶ 성별", ["남", "여"], index=1)
    col1, col2 = st.columns(2)
    today = datetime.date.today()
    birth_year = col1.number_input("출생 연도", min_value=1940, max_value=today.year, value=1994, step=1)
    birth_month = col2.number_input("출생 월", min_value=1, max_value=12, value=4, step=1)
    current_age = today.year - birth_year - (1 if today.month < birth_month else 0)
    st.success(f"고객님의 현재 나이는 **만 {current_age}세** 입니다.")
    monthly_pay = st.number_input("▶ 월 납입 금액 (만원)", min_value=10, max_value=500, value=50, step=10)
    pay_years = st.selectbox("▶ 납입 기간 (년)", [5, 7, 10, 12, 15, 20, 25], index=2)
    min_retire_age = current_age + pay_years + 5
    target_r_age = st.slider("▶ 상세 분석할 연금 개시 나이", min_value=min_retire_age, max_value=90, value=max(65, min_retire_age))
    compare_range = st.slider("▶ 비교할 개시 연령 범위 선택", min_value=min_retire_age, max_value=90, value=(max(60, min_retire_age), min(max(60, min_retire_age) + 10, 90)), step=1)

# --- [4] 메인 화면 ---
st.title(" 최저보증 변액종신연금 시뮬레이터 ")
st.markdown("---")

t_prin, t_int, t_bonus, f_res, ann_pen = calculate_details(current_age, gender, monthly_pay, pay_years, target_r_age)
col1, col2, col3 = st.columns(3)
col1.metric("총 납입 원금", f"{t_prin:,.0f} 만원")
col2.metric(f"최종 연금준비금 ({target_r_age}세)", f"{f_res:,.0f} 만원", f"누적이자 +{(t_int+t_bonus):,.0f} 만원")
col3.metric("예상 월 수령액", f"{ann_pen/12:,.0f} 만원/월", f"연 {ann_pen:,.0f} 만원")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("1. 예상 연금 준비금 구성 비율")
color_map = {
    "순수 납입 원금": "#1F4E79",
    "누적 적립 이자": "#548235",
    "장기유지 가산보너스": "#FFC000"
}
fig_pie = px.pie(pd.DataFrame({"항목": ["순수 납입 원금", "누적 적립 이자", "장기유지 가산보너스"], "금액": [t_prin, t_int, t_bonus]}), values="금액", names="항목", hole=0.4, color="항목", color_discrete_map=color_map)
fig_pie.update_traces(textinfo='label+percent', textposition='outside')
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.subheader("2. 연금 개시 연령별 수령액 비교")
compare_data = []
for age in range(compare_range[0], compare_range[1] + 1):
    ann_pension = calculate_details(current_age, gender, monthly_pay, pay_years, age)[4]
    compare_data.append({
        "개시 연령": f"{age}세<br>(연 {ann_pension:,.0f}만)",
        "월 수령액 (만원)": ann_pension / 12
    })
fig_bar = px.bar(pd.DataFrame(compare_data), x="개시 연령", y="월 수령액 (만원)", text_auto='.0f', color="월 수령액 (만원)", color_continuous_scale="Blues")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")
st.subheader(f"3. 개시 연령별 연금준비금 총액 및 납입원금 ({target_r_age}세 개시 기준)")
df_cum = pd.DataFrame([{"생존 나이": s_age, "납입 원금": t_prin, "연금 누적 수익": max(0, (ann_pen * (s_age - target_r_age + 1)) - t_prin)} for s_age in range(80, 131)])
st.plotly_chart(px.area(df_cum, x="생존 나이", y=["납입 원금", "연금 누적 수익"], color_discrete_map={"납입 원금": "#E74C3C", "연금 누적 수익": "#2E86C1"}), use_container_width=True)

# 4. 기대여명 섹션 복구
st.markdown("---")
st.subheader("4. 기대 여명으로 보는 예상 수익")
base_life = 92 if gender == "남" else 98
mid_life = int(base_life + (target_r_age - current_age) * 0.25)
roi_data = [{"구간": "기대수명 하단", "수익률": (max(0, ann_pen * ((mid_life-2) - target_r_age + 1) - t_prin) / t_prin) * 100},
            {"구간": "기대수명 중단", "수익률": (max(0, ann_pen * (mid_life - target_r_age + 1) - t_prin) / t_prin) * 100},
            {"구간": "기대수명 상단", "수익률": (max(0, ann_pen * ((mid_life+10) - target_r_age + 1) - t_prin) / t_prin) * 100}]
st.plotly_chart(px.bar(pd.DataFrame(roi_data), x="구간", y="수익률", text_auto='.1f', color="수익률", color_continuous_scale="Viridis"), use_container_width=True)
st.success(f"고객님의 예상 최대 기대여명은 **{mid_life+10}세**이며, 이때까지 연금을 수령하실 경우 원금 대비 최대 **{roi_data[2]['수익률']:.1f}%**의 수익을 기대할 수 있습니다.")
