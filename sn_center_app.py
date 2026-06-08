import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide", page_icon="🏢")

# 2. 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. CSS 스타일링 (사이드바 폭 축소 및 디자인 최적화)
def inject_custom_css():
    st.markdown("""
        <style>
        /* 모바일 및 웹 환경에서 사이드바 폭을 약 20% 수준으로 제한 */
        [data-testid="stSidebar"] {
            min-width: 200px !important;
            max-width: 250px !important;
        }
        /* 메인 화면 컨테이너 스타일 */
        [data-testid="stAppViewContainer"] {
            font-family: 'Pretendard', sans-serif !important;
        }
        /* 사이드바 토글 버튼 보호 */
        [data-testid="collapsedControl"] {
            color: #002147 !important;
            z-index: 9999 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# 4. 이미지 오류 방지 함수
def safe_image(path, width=None, use_container_width=False):
    try:
        st.image(path, width=width, use_container_width=use_container_width)
    except Exception:
        st.warning(f"이미지를 불러올 수 없습니다. 경로를 확인하세요: {path}")

# 5. 로그인 화면 함수
def login_screen():
    st.markdown("### 🏢 더블유에셋 성남센터 로그인")
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

# 6. 메인 홈페이지 함수
def main_app():
    inject_custom_css()
    with st.sidebar:
        st.write(f"반갑습니다, **{st.session_state.get('current_user', '직원')}**님!")
        if st.button("로그아웃"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.markdown("---")
        selected_menu = st.radio("📌 센터 메뉴 이동", ["🏢 센터 소개", "🚀 연금 시뮬레이터"])
    
    st.title("더블유에셋 성남센터")
    if selected_menu == "🏢 센터 소개":
        safe_image("images/main_banner.jpg", use_container_width=True)
        st.write("성남센터에 오신 것을 환영합니다.")
    elif selected_menu == "🚀 연금 시뮬레이터":
        st.header("프리미엄 연금 시뮬레이터")
        sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
        st.link_button("연금 시뮬레이터 시작하기", sim_url, use_container_width=True)

# 7. 실행 분기
if st.session_state['logged_in']:
    main_app()
else:
    login_screen()
