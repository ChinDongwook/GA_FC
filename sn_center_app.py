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
    
    with st.form("login_form"):
        user_id = st.text_input("아이디를 입력하세요")
        password = st.text_input("비밀번호를 입력하세요", type="password")
        submit_button = st.form_submit_button("로그인", use_container_width=True)

        if submit_button:
            # 💡 [여기서 직원 아이디/비밀번호를 관리합니다]
            valid_users = {
                "admin": "1234",
                "wa230962": "wa230962",
                "guest": "guest",
                "center_fc3": "pass3333"
            }
            
            if user_id in valid_users and valid_users[user_id] == password:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = user_id
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 일치하지 않습니다. 다시 확인해 주세요.")

# 4. 메인 홈페이지 함수
def main_app():
    def inject_custom_css():
        st.markdown("""
        <style>
        /* Pretendard 폰트 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        html, body, [class*="st-"] { font-family: 'Pretendard', sans-serif !important; }

        /* 히어로 섹션 */
        .hero-container { background-color: #002147; color: #FFFFFF; padding: 40px; border-radius: 15px; margin-bottom: 30px; }
        
        /* 버튼 */
        div.stLinkButton > a { background-color: #002147 !important; color: white !important; font-weight: 600 !important; }
        
        /* 사이드바 라디오 버튼 텍스트 크기 키우기 */
        div[role="radiogroup"] label { font-size: 18px !important; font-weight: 600 !important; padding-top: 10px; padding-bottom: 10px; }
        </style>
        """, unsafe_allow_html=True)
    
    inject_custom_css()

    # 이미지 오류 방지 함수
    def safe_image(path, width=None, use_container_width=False):
        try:
            st.image(path, width=width, use_container_width=use_container_width)
        except Exception:
            st.warning(f"이미지를 불러올 수 없습니다. 경로를 확인하세요: {path}")

    # --- 왼쪽 사이드바 구성 ---
    with st.sidebar:
        # 환영 메시지 및 로그아웃
        current_user = st.session_state.get('current_user', '직원')
        st.write(f"반갑습니다, **{current_user}**님!")
        if st.button("로그아웃", use_container_width=True):
            st.session_state['logged_in'] = False
            st.rerun()
            
        st.markdown("---")
        
        # 💡 왼쪽 메뉴바 (라디오 버튼 활용)
        selected_menu = st.radio(
            "📌 **센터 메뉴 이동**",
            [
                "🏢 센터 소개", 
                "🚀 연금 시뮬레이터", 
                "📊 재무 설계", 
                "📈 투자 전략", 
                "🛡️ 보장 분석", 
                "📰 금융 자료실", 
                "📞 고객 센터"
            ]
        )

    # --- 메인 화면 상단 (모든 메뉴에서 공통으로 보이는 부분) ---
    safe_image("images/logo.png", width=100)
    st.markdown("""
    <div class="hero-container">
        <h1>WASSET 성남센터</h1>
        <p style="font-size: 20px;">고객님의 성공적인 자산 관리를 위해 최선을 다하는 파트너입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 선택된 메뉴에 따라 메인 화면 내용 변경 (기존 탭 역할) ---
    if selected_menu == "🏢 센터 소개":
        safe_image("images/main_banner.jpg", use_container_width=True)
        st.header("성남센터에 오신 것을 환영합니다")
        st.info("💡 전문적인 금융 컨설팅과 함께 안정적인 노후를 준비하세요.")
        
    elif selected_menu == "🚀 연금 시뮬레이터":
        st.header("프리미엄 연금 시뮬레이터")
        sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
        st.link_button("연금 시뮬레이터 시작하기", sim_url, use_container_width=True)

    elif selected_menu == "📊 재무 설계":
        st.header("맞춤형 재무 설계")
        st.write("고객님의 라이프사이클에 맞춘 종합 재무 설계 서비스를 제공합니다.")
        st.link_button("재무 설계 페이지로 이동", "https://example.com", use_container_width=True)

    elif selected_menu == "📈 투자 전략":
        st.header("최적의 투자 전략")
        st.write("시장 트렌드를 반영한 포트폴리오 및 투자 전략을 확인하세요.")
        st.link_button("투자 전략 페이지로 이동", "https://example.com", use_container_width=True)

    elif selected_menu == "🛡️ 보장 분석":
        st.header("빈틈없는 보장 분석")
        st.write("현재 가입하신 보험을 분석하고 최적의 보장 플랜을 제안합니다.")
        st.link_button("보장 분석 페이지로 이동", "https://example.com", use_container_width=True)

    elif selected_menu == "📰 금융 자료실":
        st.header("핵심 금융 자료실")
        st.write("자산 관리에 도움이 되는 다양한 금융 정보와 칼럼을 읽어보세요.")
        st.link_button("금융 자료실로 이동", "https://example.com", use_container_width=True)

    elif selected_menu == "📞 고객 센터":
        st.header("고객 센터")
        st.write("궁금하신 점이 있다면 언제든 성남센터로 문의해 주세요.")
        st.link_button("상담 예약 및 문의하기", "https://example.com", use_container_width=True)

# 5. 로그인 상태에 따른 화면 분기
if st.session_state['logged_in']:
    main_app()
else:
    login_screen()
