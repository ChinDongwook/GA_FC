import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide", page_icon="🏢")

# 2. 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. CSS 스타일링 (텍스트 크기 최적화 및 겹침 방지)
def inject_custom_css():
    st.markdown("""
    <style>
    /* Pretendard 폰트 적용 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    
    /* 전체 폰트 및 테마 설정창 대응을 위해 !important 사용 최소화 */
    html, body, [class*="st-"] { 
        font-family: 'Pretendard', sans-serif !important; 
    }

    /* 사이드바 토글 버튼 강제 표시 */
    [data-testid="collapsedControl"] { display: flex !important; color: #002147 !important; }

    /* 히어로 섹션 */
    .hero-container { background-color: #002147; color: #FFFFFF; padding: 30px; border-radius: 12px; margin-bottom: 20px; }

    /* 타이틀 크기 조정 (기존보다 조금 더 컴팩트하게) */
    h1 { font-size: 24px !important; margin-bottom: 5px !important; }
    h2 { font-size: 18px !important; }

    /* 본문 텍스트 겹침 방지 (폰트 크기 및 줄 높이 축소) */
    .stMarkdown, .stWrite, p { 
        font-size: 14px !important; 
        line-height: 1.4 !important; 
        margin-bottom: 5px !important;
    }

    /* 사이드바 메뉴 폰트 및 정렬 */
    div.stRadio > label { font-size: 16px !important; font-weight: 700 !important; color: #002147 !important; }
    div.stRadio p { font-size: 14px !important; }

    /* 버튼 스타일 */
    div.stLinkButton > a { font-size: 13px !important; background-color: #002147 !important; color: white !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 4. 로그인 화면 함수
def login_screen():
    st.markdown("<h2 style='text-align: center;'>더블유에셋 성남센터 로그인</h2>", unsafe_allow_html=True)
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

# 5. 메인 홈페이지 함수
def main_app():
    with st.sidebar:
        st.write(f"반갑습니다, **{st.session_state.get('current_user')}**님!")
        if st.button("로그아웃"):
            st.session_state['logged_in'] = False
            st.rerun()
        selected_menu = st.radio("📌 센터 메뉴 이동", ["🏢 센터 소개", "🚀 연금 시뮬레이터", "📊 재무 설계", "📈 투자 전략", "🛡️ 보장 분석"])

    st.image("images/logo.png", width=100)
    st.markdown('<div class="hero-container"><h1>WASSET 성남센터</h1><p>성공적인 자산 관리를 위한 파트너</p></div>', unsafe_allow_html=True)
    
    if selected_menu == "🏢 센터 소개":
        st.header("성남센터에 오신 것을 환영합니다")
        st.write("전문적인 금융 컨설팅과 함께 안정적인 노후를 준비하세요.")
    elif selected_menu == "🚀 연금 시뮬레이터":
        st.header("프리미엄 연금 시뮬레이터")
        st.link_button("시뮬레이터 시작하기", "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/")
    else:
        st.header(selected_menu)
        st.write("관련 서비스를 준비 중입니다.")

if st.session_state['logged_in']:
    main_app()
else:
    login_screen()
