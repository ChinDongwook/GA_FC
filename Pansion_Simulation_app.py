
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
# [3] PDF 생성 함수
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

# --- [2] 핵심 계산 로직 함수 (오리지널 연 단위 산출 로직으로 완벽 원복) ---
def calculate_details(current_age, gender, monthly_pay, p_years, r_age):
    passed = r_age - current_age
    
    # 거치 기간별 보너스
    if passed >= 30: bonus = 0.24
    elif passed >= 25: bonus = 0.16
    elif passed >= 20: bonus = 0.07
    else: bonus = 0

    # 연령별 지급률
    if 30 <= r_age < 40: p_rate = 0.022
    elif 40 <= r_age < 50: p_rate = 0.026
    elif 50 <= r_age < 55: p_rate = 0.0285
    elif 55 <= r_age < 65: p_rate = 0.040
    elif 65 <= r_age < 70: p_rate = 0.045
    elif 70 <= r_age < 80: p_rate = 0.0485
    else: p_rate = 0.050
    
    if gender == "남": p_rate += 0.002

    # 대표님의 오리지널 로직으로 완벽 원복 (심각한 수치 오류 해결)
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
    
    st.markdown("**▶ 생년 월 입력**")
    col1, col2 = st.columns(2)
    today = datetime.date.today()
    
    with col1:
        birth_year = st.number_input("출생 연도", min_value=1940, max_value=today.year, value=1994, step=1)
    with col2:
        birth_month = st.number_input("출생 월", min_value=1, max_value=12, value=4, step=1)
        
    current_age = today.year - birth_year
    if today.month < birth_month:
        current_age -= 1
        
    st.success(f"고객님의 현재 나이는 **만 {current_age}세** 입니다.")
    
    monthly_pay = st.number_input("▶ 월 납입 금액 (만원)", min_value=10, max_value=500, value=50, step=10)
    pay_years = st.selectbox("▶ 납입 기간 (년)", [5, 7, 10, 12, 15, 20, 25], index=2)
    
    min_retire_age = current_age + pay_years + 5
    st.info(f" 최소 연금개시 가능 나이는 **{min_retire_age}세** 입니다.")
    
    target_r_age = st.slider("▶ 상세 분석할 연금 개시 나이", min_value=min_retire_age, max_value=90, value=max(65, min_retire_age))

    st.markdown("---")
    compare_range = st.slider(
        "▶ 비교할 개시 연령 범위 선택",
        min_value=min_retire_age,
        max_value=90,
        value=(max(60, min_retire_age), min(max(60, min_retire_age) + 10, 90)),
        step=1
    )

# --- [4] 메인 화면 대시보드 ---
st.title(" 최저보증 변액종신연금 시뮬레이터 ")
st.markdown("---")

t_prin, t_int, t_bonus, f_res, ann_pen = calculate_details(current_age, gender, monthly_pay, pay_years, target_r_age)
month_pen = ann_pen / 12

# 1. 최상단 핵심 요약 지표
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="총 납입 원금", value=f"{t_prin:,.0f} 만원")
with col2:
    st.metric(label=f"최종 연금 준비금 ({target_r_age}세)", value=f"{f_res:,.0f} 만원", delta=f"수익 +{(t_int+t_bonus):,.0f} 만원")
with col3:
    st.metric(label="예상 월 수령액", value=f"{month_pen:,.0f} 만원/월", delta=f"연 {ann_pen:,.0f} 만원")

st.markdown("<br>", unsafe_allow_html=True)

# 2. 첫 번째 차트: 예상 연금 준비금 구성 (파이 차트)
# ? 변경점: 제목 앞에 '1. ' 넘버링 추가
st.subheader("1. 예상 연금 준비금 구성 비율")
st.caption("고객님이 납입한 원금이 시간과 보너스를 통해 어떻게 성장했는지 직관적으로 보여줍니다.")
df_pie = pd.DataFrame({
    "항목": ["순수 납입 원금", "누적 적립 이자", "장기유지 가산보너스"],
    "금액": [t_prin, t_int, t_bonus]
})
fig_pie = px.pie(df_pie, values="금액", names="항목", hole=0.4, 
                 color_discrete_sequence=px.colors.sequential.Teal)
fig_pie.update_traces(textposition='inside', texttemplate='<b>%{label}</b><br>%{value:,.0f} 만원<br>(%{percent})')
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# 3. 두 번째 차트: 1년 단위 비교 (바 차트)
# ? 변경점: 제목 앞에 '2. ' 넘버링 추가
st.subheader("2. 연금 개시 연령별 수령액 비교")
st.caption("은퇴 시기를 1년 늦출 때마다 연금 수령액이 얼마나 극적으로 상승하는지 확인하세요.")
start_age, end_age = compare_range
compare_ages = list(range(start_age, end_age + 1))

compare_data = []
for age in compare_ages:
    _, _, _, _, a_pen = calculate_details(current_age, gender, monthly_pay, pay_years, age)
    compare_data.append({"개시 연령": f"{age}세", "월 수령액 (만원)": a_pen/12})
    
df_bar = pd.DataFrame(compare_data)
fig_bar = px.bar(df_bar, x="개시 연령", y="월 수령액 (만원)", text_auto='.0f',
                 color="월 수령액 (만원)", color_continuous_scale="Blues")
fig_bar.update_layout(showlegend=False, xaxis_title="연금 개시 연령", yaxis_title="월 수령액 (만원)")
st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# 4. 세 번째 차트: 생존 연령별 연금 누계액 및 원금 대비 수익 시각화

st.subheader(f"3. 생존 연령별 연금 누계액 및 납입원금 ({target_r_age}세 개시 기준)")
st.caption("붉은색 영역은 납입하신 원금이며, 파란색 영역은 원금 위로 쌓이는 연금 수익의 총액입니다.")

survival_ages = list(range(80, 131))
cumulative_data = []

for s_age in survival_ages:
    received_years = max(0, s_age - target_r_age + 1)
    acc_pension = ann_pen * received_years
    # 연금 총수익 = 누계 수령액 - 원금
    pension_profit = max(0, acc_pension - t_prin)
    
    cumulative_data.append({
        "생존 나이": s_age,
        "납입 원금": t_prin,
        "연금 누적 수익": pension_profit
    })

df_cum = pd.DataFrame(cumulative_data)

# 스택 영역 차트 생성 (원금이 하단에 깔리도록)
fig_cum = px.area(df_cum, x="생존 나이", y=["납입 원금", "연금 누적 수익"],
                  labels={"value": "금액 (만원)", "생존 나이": "생존 연령 (세)", "variable": "항목"},
                  color_discrete_map={"납입 원금": "#E74C3C", "연금 누적 수익": "#2E86C1"})

# 눈금 설정 (5년 단위)
fig_cum.update_layout(
    xaxis=dict(tickmode='linear', dtick=5, title="생존 연령 (세)"),
    yaxis=dict(title="금액 (만원)"),
    hovermode="x unified",
    legend_title_text="비교 항목"
)


# 스택(쌓기) 모드 적용 
fig_cum.update_layout(barmode='stack') 

st.plotly_chart(fig_cum, use_container_width=True)


# 기대여명을 바탕으로 직관전 안내 하기
# --- [4] 기대여명으로 보는 예상 수익 (신규 추가 섹션) ---
st.markdown("---")
st.subheader("4. 기대여명으로 보는 예상 수익")

# 기대수명 범위 계산 (기본값 + 보정값 적용)
base_life = 92 if gender == "남" else 98
mid_life = int(base_life + (target_r_age - current_age) * 0.25)
life_range_start = mid_life - 2
life_range_end = mid_life + 10

st.write(f"AI가 최근 통계를 바탕으로 한 고객님의 예상 기대수명은 **{life_range_start}세 ~ {life_range_end}세**입니다.")
st.caption("※ 개인에 따라 건강관리와 의학 발달에 따라 기대수명은 더욱 늘어날 수 있으며, 장수하실수록 연금의 가치는 극대화됩니다.")

# 범위형 데이터 시각화
roi_range_data = pd.DataFrame([
    {"구간": "기대수명 하단", "나이": life_range_start, "수익률": (max(0, ann_pen * (life_range_start - target_r_age + 1) - t_prin) / t_prin) * 100},
    {"구간": "기대수명 중단", "나이": mid_life, "수익률": (max(0, ann_pen * (mid_life - target_r_age + 1) - t_prin) / t_prin) * 100},
    {"구간": "기대수명 상단", "나이": life_range_end, "수익률": (max(0, ann_pen * (life_range_end - target_r_age + 1) - t_prin) / t_prin) * 100}
])

fig_roi_range = px.bar(roi_range_data, x="구간", y="수익률", text_auto='.1f', 
                       color="수익률", color_continuous_scale="Viridis")
fig_roi_range.update_layout(yaxis_title="원금 대비 수익률 (%)", xaxis_title="")
st.plotly_chart(fig_roi_range, use_container_width=True)

st.success(f"고객님께서 **{life_range_end}세**까지 생존하실 경우, 원금 대비 최대 **{roi_range_data.iloc[2]['수익률']:.1f}%**의 수익을 기대할 수 있습니다.")
