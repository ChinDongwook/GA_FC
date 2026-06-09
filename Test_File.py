import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
from fpdf import FPDF
import io

# 1. 페이지 설정 (최상단 단 1회 선언)
st.set_page_config(
    page_title="더블유에셋 성남센터", 
    layout="wide", 
    page_icon="🏢",
    initial_sidebar_state="expanded"
)

# 2. 로그인 상태 초기화
if 'logged_in' not in st.session_state: 
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = "게스트"

# 3. 통합 CSS 스타일링 (사이드바 축소, 타이틀 폰트 축소, 컨테이너 너비 제한)
def inject_custom_css(): 
    st.markdown("""
    <style>
    /* 콘텐츠 컨테이너 너비 제한 */ 
    .block-container { max-width: 1200px !important; margin: 0 auto !important; } 
    /* 사이드바 폭 축소 (모바일 및 데스크탑 대응) */ 
    [data-testid="stSidebar"] { min-width: 200px !important; max-width: 250px !important; }
    /* 텍스트 크기 일괄 확대 및 타이틀(h1) 조절 */ 
    .stApp { font-size: 18px !important; } 
    h1 { font-size: 28px !important; font-weight: 700 !important; } 
    h2, h3 { font-weight: 700 !important; font-size: 20px !important; } 
    /* 메트릭(수치) 폰트 크기 확대 */
    [data-testid="stMetricValue"] { font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. 이미지 오류 방지 함수
def safe_image(path, width=None, use_container_width=False): 
    try: 
        st.image(path, width=width, use_container_width=use_container_width) 
    except Exception:
        st.warning(f"이미지를 불러올 수 없습니다. 경로를 확인하세요: {path}")

# [핵심] PDF 생성 함수
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

# [핵심] 핵심 계산 로직 함수 (오리지널 로직 완벽 원복 유지)
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

# 로그인 화면 함수
def login_screen(): 
    st.markdown("<h1>더블유에셋 성남센터 로그인</h1>", unsafe_allow_html=True) 
    with st.form("login_form"): 
        user_id = st.text_input("아이디") 
        password = st.text_input("비밀번호", type="password") 
        if st.form_submit_button("로그인", use_container_width=True): 
            valid_users = {"admin": "1234", "wa230962": "wa230962", "guest": "guest", "center_fc3": "pass3333"} 
            if user_id in valid_users and valid_users[user_id] == password: 
                st.session_state['logged_in'] = True 
                st.session_state['current_user'] = user_id 
                st.rerun() 
            else: 
                st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

# 로그인 완료 후 노출될 연금 시뮬레이터 함수
def show_simulator():
    # 사이드바 (입력부)
    with st.sidebar: 
        st.title("고객 정보 입력") 
        gender = st.selectbox("▶ 성별", ["남", "여"], index=1) 
        st.markdown(" ▶ 생년 월 입력 ") 
        col1, col2 = st.columns(2) 
        today = datetime.date.today() 
        
        with col1: 
            birth_year = st.number_input("출생 연도", min_value=1940, max_value=today.year, value=1994, step=1) 
        with col2: 
            birth_month = st.number_input("출생 월", min_value=1, max_value=12, value=4, step=1) 
            
        current_age = today.year - birth_year 
        if today.month < birth_month: 
            current_age -= 1 
            
        st.success(f"고객님의 현재 나이는 만 {current_age}세 입니다.") 
        
        monthly_pay = st.number_input("▶ 월 납입 금액 (만원)", min_value=10, max_value=500, value=50, step=10) 
        pay_years = st.selectbox("▶ 납입 기간 (년)", [5, 7, 10, 12, 15, 20, 25], index=2) 
        
        min_retire_age = current_age + pay_years + 5 
        st.info(f"최소 연금개시 가능 나이는 {min_retire_age}세 입니다.") 
        
        target_r_age = st.slider("▶ 상세 분석할 연금 개시 나이", min_value=min_retire_age, max_value=90, value=max(65, min_retire_age))
        st.markdown("---") 
        compare_range = st.slider(
            "▶ 비교할 개시 연령 범위 선택", 
            min_value=min_retire_age, 
            max_value=90, 
            value=(max(60, min_retire_age), min(max(60, min_retire_age) + 10, 90)), 
            step=1 
        )
        
        # 로그아웃 버튼 (편의를 위해 추가)
        st.markdown("---")
        if st.button("로그아웃", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['current_user'] = "게스트"
            st.rerun()

    # 메인 화면 대시보드
    st.title("최저보증 변액종신연금 시뮬레이터") 
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
    
    st.markdown("", unsafe_allow_html=True)

    # 1. 예상 연금 준비금 구성 비율
    st.subheader("1. 예상 연금 준비금 구성 비율") 
    st.caption("고객님이 납입한 원금이 시간과 보너스를 통해 어떻게 성장했는지 직관적으로 보여줍니다.") 
    df_pie = pd.DataFrame({ 
        "항목": ["순수 납입 원금", "누적 적립 이자", "장기유지 가산보너스"], 
        "금액": [t_prin, t_int, t_bonus] 
    }) 
    fig_pie = px.pie(df_pie, values="금액", names="항목", hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
    fig_pie.update_traces(textposition='inside', texttemplate='%{label}<br>%{value:,.0f} 만원(%{percent})') 
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # 2. 연금 개시 연령별 수령액 비교
    st.subheader("2. 연금 개시 연령별 수령액 비교") 
    st.caption("은퇴 시기를 1년 늦출 때마다 연금 수령액이 얼마나 극적으로 상승하는지 확인하세요.") 
    start_age, end_age = compare_range 
    compare_ages = list(range(start_age, end_age + 1)) 
    compare_data = [] 
    for age in compare_ages: 
        _, _, _, _, a_pen = calculate_details(current_age, gender, monthly_pay, pay_years, age) 
        compare_data.append({"개시 연령": f"{age}세", "월 수령액 (만원)": a_pen/12}) 
        
    df_bar = pd.DataFrame(compare_data) 
    fig_bar = px.bar(df_bar, x="개시 연령", y="월 수령액 (만원)", text_auto='.0f', color="월 수령액 (만원)", color_continuous_scale="Blues")
    fig_bar.update_layout(showlegend=False, xaxis_title="연금 개시 연령", yaxis_title="월 수령액 (만원)") 
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")

    # 3. 생존 연령별 연금 누계액 및 납입원금
    st.subheader(f"3. 생존 연령별 연금 누계액 및 납입원금 ({target_r_age}세 개시 기준)") 
    st.caption("붉은색 영역은 납입하신 원금이며, 파란색 영역은 원금 위로 쌓이는 연금 수익의 총액입니다.") 
    survival_ages = list(range(80, 131)) 
    cumulative_data = [] 
    for s_age in survival_ages: 
        received_years = max(0, s_age - target_r_age + 1) 
        acc_pension = ann_pen * received_years 
        pension_profit = max(0, acc_pension - t_prin) 
        cumulative_data.append({ 
            "생존 나이": s_age, 
            "납입 원금": t_prin, 
            "연금 누적 수익": pension_profit 
        })
        
    df_cum = pd.DataFrame(cumulative_data)

    fig_cum = px.area(df_cum, x="생존 나이", y=["납입 원금", "연금 누적 수익"], 
                      labels={"value": "금액 (만원)", "생존 나이": "생존 연령 (세)", "variable": "항목"}, 
                      color_discrete_map={"납입 원금": "#E74C3C", "연금 누적 수익": "#2E86C1"})

    fig_cum.update_layout( 
        xaxis=dict(tickmode='linear', dtick=5, title="생존 연령 (세)"), 
        yaxis=dict(title="금액 (만원)"), 
        hovermode="x unified", 
        legend_title_text="비교 항목",
        barmode='stack'
    )
    st.plotly_chart(fig_cum, use_container_width=True)

    st.markdown("---") 
    
    # 4. 기대여명으로 보는 예상 수익
    st.subheader("4. 기대여명으로 보는 예상 수익")
    base_life = 92 if gender == "남" else 98 
    mid_life = int(base_life + (target_r_age - current_age) * 0.25) 
    life_range_start = mid_life - 2 
    life_range_end = mid_life + 10 
    
    st.write(f"AI가 최근 통계를 바탕으로 한 고객님의 예상 기대수명은 {life_range_start}세 ~ {life_range_end}세 입니다.") 
    st.caption("※ 개인에 따라 건강관리와 의학 발달에 따라 기대수명은 더욱 늘어날 수 있으며, 장수하실수록 연금의 가치는 극대화됩니다.")

    roi_range_data = pd.DataFrame([ 
        {"구간": "기대수명 하단", "나이": life_range_start, "수익률": (max(0, ann_pen * (life_range_start - target_r_age + 1) - t_prin) / t_prin) * 100}, 
        {"구간": "기대수명 중단", "나이": mid_life, "수익률": (max(0, ann_pen * (mid_life - target_r_age + 1) - t_prin) / t_prin) * 100}, 
        {"구간": "기대수명 상단", "나이": life_range_end, "수익률": (max(0, ann_pen * (life_range_end - target_r_age + 1) - t_prin) / t_prin) * 100} 
    ]) 
    
    fig_roi_range = px.bar(roi_range_data, x="구간", y="수익률", text_auto='.1f', color="수익률", color_continuous_scale="Viridis") 
    fig_roi_range.update_layout(yaxis_title="원금 대비 수익률 (%)", xaxis_title="") 
    st.plotly_chart(fig_roi_range, use_container_width=True)

    st.success(f"고객님께서 {life_range_end}세까지 생존하실 경우, 원금 대비 최대 {roi_range_data.iloc[2]['수익률']:.1f}%의 수익을 기대할 수 있습니다.")

# 메인 홈페이지 실행 함수
def main_app(): 
    inject_custom_css()
    if not st.session_state['logged_in']:
        login_screen()
    else:
        show_simulator()

# 앱 실행
main_app()
