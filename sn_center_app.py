import streamlit as st

# 1. 페이지 설정 (반드시 최상단에 위치해야 합니다)
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide", page_icon="🏢")

# 2. 로그인 상태 초기화 (Session State 활용)
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. 로그인 화면 함수
def login_screen():
    st.markdown("""
        <div style="background-color: #002147; padding: 30px; border-radius: 15px; text-align: center; color: white; margin-bottom: 30px;">
            <h2>더블유에셋 성남센터</h2>
            <p>직원 전용 시스템입니다. 로그인해 주세요.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 폼(Form)을 사용해 엔터키로도 로그인이 가능하도록 구성
    with st.form("login_form"):
        user_id = st.text_input("아이디를 입력하세요")
        password = st.text_input("비밀번호를 입력하세요", type="password")
        submit_button = st.form_submit_button("로그인", use_container_width=True)

        if submit_button:
            # ==========================================
            # 💡 [여기서 직원 아이디/비밀번호를 관리합니다]
            # "아이디": "비밀번호" 형태로 계속 추가하시면 됩니다.
            # ==========================================
            valid_users = {
                "admin": "1234",
                "wa230962": "wa230962",
                "guest": "guest",
                "center_fc2": "pass2222",
                "center_fc3": "pass3333"
            }
            
            # 입력한 아이디가 valid_users 목록에 있고, 비밀번호도 일치하는지 확인 [cite: 278]
            if user_id in valid_users and valid_users[user_id] == password:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = user_id # 접속한 사용자 아이디 저장
                st.rerun() # 상태 업데이트 후 페이지 새로고침
            else:
                st.error("아이디 또는 비밀번호가 일치하지 않습니다. 다시 확인해 주세요.")

# 4. 메인 홈페이지 함수
def main_app():
    # 사이드바 (로그아웃 버튼 및 환영 메시지)
    with st.sidebar:
        current_user = st.session_state.get('current_user', '직원')
        st.write(f"반갑습니다, **{current_user}**님!")
        if st.button("로그아웃", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()

    def inject_custom_css():
        st.markdown("""
        <style>
        /* Pretendard 폰트 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        html, body, [class*="st-"] { font-family: 'Pretendard', sans-serif !important; }

        /* 탭 가독성 강제 수정 */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f0f2f6; 
            padding: 10px;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 20px !important;
            font-weight: 800 !important;
            color: #000000 !important; 
            background-color: transparent !important;
        }
        
        /* 탭 선택 시 강조 */
        .stTabs [aria-selected="true"] {
            color: #002147 !important;
            border-bottom: 3px solid #002147 !important;
        }
        /* 히어로 섹션 */
        .hero-container { background-color: #002147; color: #FFFFFF; padding: 40px; border-radius: 15px; margin-bottom: 30px; }
        
        /* 버튼 */
        div.stLinkButton > a { background-color: #002147 !important; color: white !important; font-weight: 600 !important; }
        </style>
        """, unsafe_allow_html=True)
    
    inject_custom_css()

    # 이미지 오류 방지
    def safe_image(path, width=None, use_container_width=False):
        try:
            st.image(path, width=width, use_container_width=use_container_width)
        except Exception:
            st.warning(f"이미지를 불러올 수 없습니다. 경로를 확인하세요: {path}")

    # 로고 및 메인 구성
    safe_image("images/logo.png", width=100)
    st.markdown("""
    <div class="hero-container">
        <h1>WASSET 성남센터</h1>
        <p style="font-size: 20px;">고객님의 성공적인 자산 관리를 위해 최선을 다하는 파트너입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 탭 7개 구성 ---
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🏢 센터 소개", 
        "🚀 연금 시뮬레이터", 
        "📊 재무 설계", 
        "📈 투자 전략", 
        "🛡️ 보장 분석", 
        "📰 금융 자료실", 
        "📞 고객 센터"
    ])
    
    with tab1:
        safe_image("images/main_banner.jpg", use_container_width=True)
        st.header("성남센터에 오신 것을 환영합니다")
        st.info("💡 전문적인 금융 컨설팅과 함께 안정적인 노후를 준비하세요.")
        
    with tab2:
        st.header("프리미엄 연금 시뮬레이터")
        sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
        st.link_button("연금 시뮬레이터 시작하기", sim_url, use_container_width=True)

    with tab3:
        st.header("맞춤형 재무 설계")
        st.write("고객님의 라이프사이클에 맞춘 종합 재무 설계 서비스를 제공합니다.")
        st.link_button("재무 설계 페이지로 이동", "https://example.com", use_container_width=True)

    with tab4:
        st.header("최적의 투자 전략")
        st.write("시장 트렌드를 반영한 포트폴리오 및 투자 전략을 확인하세요.")
        st.link_button("투자 전략 페이지로 이동", "https://example.com", use_container_width=True)

    with tab5:
        st.header("빈틈없는 보장 분석")
        st.write("현재 가입하신 보험을 분석하고 최적의 보장 플랜을 제안합니다.")
        st.link_button("보장 분석 페이지로 이동", "https://example.com", use_container_width=True)

    with tab6:
        st.header("핵심 금융 자료실")
        st.write("자산 관리에 도움이 되는 다양한 금융 정보와 칼럼을 읽어보세요.")
        st.link_button("금융 자료실로 이동", "https://example.com", use_container_width=True)

    with tab7:
        st.header("고객 센터")
        st.write("궁금하신 점이 있다면 언제든 성남센터로 문의해 주세요.")
        st.link_button("상담 예약 및 문의하기", "https://example.com", use_container_width=True)

# 5. 로그인 상태에 따른 화면 분기
if st.session_state['logged_in']:
    main_app()
else:
    login_screen()
