import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from fpdf import FPDF
import io

# [1] 페이지 기본 설정 (최상단에 단독 배치)
st.set_page_config(
    page_title="최저보증 변액종신연금 컨설팅 시뮬레이터",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일 적용
st.markdown("""
    <style>
    .stApp { font-size: 18px !important; }
    h1, h2, h3 { font-weight: 700 !important; }
    [data-testid="stMetricValue"] { font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

# [2] 핵심 계산 로직 함수
def calculate_details(current_age, gender, monthly_pay, p_years, r_age):
    passed = r_age - current_age
    bonus = 0.24 if passed >= 30 else (0.16 if passed >= 25 else (0.07 if passed >= 20 else 0))

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
    final_reserve = base_reserve * (1 + bonus)
    return total_prin, total_interest, (base_reserve * bonus), final_reserve, final_reserve * p_rate

# [3] 사이드바 입력부
with st.sidebar:
    st.title("고객 정보 입력")
    gender = st.selectbox("성별", ["남", "여"], index=1)
    birth_year = st.number_input("출생 연도", 1940, 2026, 1994)
    monthly_pay = st.number_input("월 납입 금액 (만원)", 10, 500, 50, 10)
    pay_years = st.selectbox("납입 기간 (년)", [5, 7, 10, 12, 15, 20, 25], index=2)
    
    current_age = datetime.date.today().year - birth_year
    min_retire_age = current_age + pay_years + 5
    target_r_age = st.slider("연금 개시 나이", min_retire_age, 90, max(65, min_retire_age))

    st.markdown("---")
    st.subheader("💡 추가 분석 옵션")
    show_expectancy = st.checkbox("4. 기대여명 분석 보기")
    life_adj = st.slider("기대여명 보정 (세)", -10, 10, 0)

# [4] 메인 화면
st.title("최저보증 변액종신연금 시뮬레이터")
t_prin, t_int, t_bonus, f_res, ann_pen = calculate_details(current_age, gender, monthly_pay, pay_years, target_r_age)

# 요약 지표
c1, c2, c3 = st.columns(3)
c1.metric("총 납입 원금", f"{t_prin:,.0f} 만원")
c2.metric("최종 준비금", f"{f_res:,.0f} 만원", f"수익 +{(t_int+t_bonus):,.0f} 만원")
c3.metric("예상 월 수령액", f"{ann_pen/12:,.0f} 만원", f"연 {ann_pen:,.0f} 만원")

# 2. 개시 연령별 수령액 비교
st.subheader("2. 연금 개시 연령별 수령액 비교")
compare_data = [{"개시 연령": f"{a}세", "월 수령액": calculate_details(current_age, gender, monthly_pay, pay_years, a)[4]/12, 
                 "연 수령액": calculate_details(current_age, gender, monthly_pay, pay_years, a)[4]} for a in range(target_r_age-5, target_r_age+6)]
fig_bar = px.bar(pd.DataFrame(compare_data), x="개시 연령", y="월 수령액", text_auto='.0f', hover_data=["연 수령액"])
st.plotly_chart(fig_bar, use_container_width=True)

# [4번 기대여명 섹션] 체크박스 연동
if show_expectancy:
    st.markdown("---")
    st.subheader("4. 기대여명으로 보는 예상 수익")
    mid_life = int((85 + life_adj) + (target_r_age - current_age) * 0.25)
    st.write(f"고객님의 예상 기대수명은 **{mid_life-3}세 ~ {mid_life+7}세**입니다.")
    
    roi_data = pd.DataFrame([
        {"구간": "기대수명 하단", "수익률": ((ann_pen*(mid_life-3-target_r_age+1)-t_prin)/t_prin)*100},
        {"구간": "기대수명 중단", "수익률": ((ann_pen*(mid_life-target_r_age+1)-t_prin)/t_prin)*100},
        {"구간": "기대수명 상단", "수익률": ((ann_pen*(mid_life+7-target_r_age+1)-t_prin)/t_prin)*100}
    ])
    st.plotly_chart(px.bar(roi_data, x="구간", y="수익률", text_auto='.1f'))
