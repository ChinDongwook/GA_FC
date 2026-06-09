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

# 3. 통합 CSS 스타일링
def inject_custom_css(): 
    st.markdown("""
    <style>
    /* 콘텐츠 컨테이너 너비 제한 */ 
    .block-container { max-width: 1200px !important; margin: 0 auto !important; } 
    /* 사이드바 폭 축소 */ 
    [data-testid="stSidebar"] { min-width: 200px !important; max-width: 270px !important; }
    /* 텍스트 크기 일괄 확대 및 타이틀(h1) 조절 */ 
    .stApp { font-size: 18px !important; } 
    h1 { font-size: 28px !important; font-weight: 700 !important; } 
    h2, h3 { font-weight: 700 !important; font-size: 20px !important; } 
    /* 메트릭(수치) 폰트 크기 확대 */
    [data-testid="stMetricValue"] { font-size: 28px !important; }
    </style>
    """, unsafe_allow_html=True)

# [핵심] 핵심 계산 로직 함수 (오리지널 유지)
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

# 로그인 화면
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

# 페이지: 홈 화면
def show_home():
    st.title("더블유에셋 성남센터 포털")
    st.markdown("---")
    st.info(f"환영합니다! **{st.session_state['current_user']}**님, 성공적으로 로그인되었습니다.")
    st.write("왼쪽 메뉴 탭에서 원하시는 업무를 선택하여 진행해 주세요.")

# 페이지: 업무 매뉴얼
def show_manual():
    st.title("성남센터 업무 매뉴얼")
    st.markdown("---")
    st.write("여기에 공지사항, 영업 지원 자료, 보험사별 약관 등 센터 운영에 필요한 내용을 추가하실 수 있습니다.")

# 페이지: 연금 시뮬레이터 (로직 보호 영역)
def show_simulator():
    with st.sidebar: 
        st.subheader("💡 고객 정보 입력") 
        gender = st.selectbox("▶ 성별", ["남", "여"], index=1) 
        col1, col2 = st.columns(2) 
        today = datetime.date.today() 
        
        with col1: 
            birth_year = st.number_input("출생 연도", min_value=1940, max_value=today.year, value=1994, step=1) 
        with col2: 
            birth_month = st.number_input("출생 월", min_value=1, max_value=12, value=4, step=1) 
            
        current_age = today.year - birth_year 
        if today.month < birth_month: current_age -= 1 
            
        st.success(f"현재 나이: 만 {current_age}세") 
        
        monthly_pay = st.number_input("▶ 월 납입 (만원)", min_value=10, max_value=500, value=50, step=10) 
        pay_years = st.selectbox("▶ 납입 기간 (년)", [5, 7, 10, 12, 15, 20, 25], index=2) 
        min_retire_age = current_age + pay_years + 5 
        st.info(f"최소 개시: {min_retire_age}세") 
        
        target_r_age = st.slider("▶ 개시 나이 분석", min_value=min_retire_age, max_value=90, value=max(65, min_retire_age))
        compare_range = st.slider("▶ 비교 연령 범위", min_value=min_retire_age, max_value=90, value=(max(60, min_retire_age), min(max(60, min_retire_age) + 10, 90)), step=1)

    st.title("최저보증 변액종신연금 시뮬레이터") 
    st.markdown("---") 
    
    t_prin, t_int, t_bonus, f_res, ann_pen = calculate_details(current_age, gender, monthly_pay, pay_years, target_r_age) 
    month_pen = ann_pen / 12

    col1, col2, col3 = st.columns(3) 
    with col1: st.metric("총 납입 원금", f"{t_prin:,.0f} 만원") 
    with col2: st.metric(f"최종 준비금 ({target_r_age}세)", f"{f_res:,.0f} 만원", f"수익 +{(t_int+t_bonus):,.0f} 만원") 
    with col3: st.metric("예상 월 수령액", f"{month_pen:,.0f} 만원/월", f"연 {ann_pen:,.0f} 만원")
    
    st.markdown("", unsafe_allow_html=True)

    st.subheader("1. 예상 연금 준비금 구성 비율") 
    df_pie = pd.DataFrame({"항목": ["순수 납입 원금", "누적 적립 이자", "장기유지 보너스"], "금액": [t_prin, t_int, t_bonus]}) 
    fig_pie = px.pie(df_pie, values="금액", names="항목", hole=0.4, color_discrete_sequence=px.colors.sequential.Teal)
    fig_pie.update_traces(textposition='inside', texttemplate='%{label}<br>%{value:,.0f} 만원(%{percent})') 
    st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")
    st.subheader("2. 연금 개시 연령별 수령액 비교") 
    compare_data = [] 
    for age in range(compare_range[0], compare_range[1] + 1): 
        _, _, _, _, a_pen = calculate_details(current_age, gender, monthly_pay, pay_years, age) 
        compare_data.append({"개시 연령": f"{age}세", "월 수령액 (만원)": a_pen/12}) 
        
    fig_bar = px.bar(pd.DataFrame(compare_data), x="개시 연령", y="월 수령액 (만원)", text_auto='.0f', color="월 수령액 (만원)", color_continuous_scale="Blues")
    fig_bar.update_layout(showlegend=False) 
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    st.subheader(f"3. 생존 연령별 연금 누계 및 수익 ({target_r_age}세 개시)") 
    cumulative_data = [] 
    for s_age in range(80, 131): 
        pension_profit = max(0, (ann_pen * max(0, s_age - target_r_age + 1)) - t_prin) 
        cumulative_data.append({"생존 나이": s_age, "납입 원금": t_prin, "연금 누적 수익
