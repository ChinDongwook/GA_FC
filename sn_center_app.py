import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide", page_icon="🏢")

# 2. 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. CSS 스타일링 (폰트 및 레이아웃 최적화)
def inject_custom_css():
    st.markdown("""
    <style>
    /* Pretendard 폰트 적용 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, p, div, span, h1, h2, h3, h4, h5, h6, label { 
        font-family: 'Pretendard', sans-serif !important; 
    }

    /* 사이드바 토글 버튼 복원 */
    [data-testid="collapsedControl"] { display: flex !important; }

    /* 타이틀 크기 조정 (기존보다 축소) */
    h1 { font-size: 28px !important; margin-bottom: 10px !important; }
    h2 { font-size: 22px !important; }

    /* 메인 텍스트 겹침 방지: 크기 축소 및 여백 조정 */
    .stMarkdown, .stWrite, p { 
        font-size: 16px !important; 
        line-height: 1.5 !important; 
    }

    /* 라디오 버튼 텍스트 최적화 */
    div.stRadio > label { font-size: 16px !important; font-weight: 700 !important; }
    div.stRadio p { font-size: 15px !important; }

    /* 히어로 섹션 크기 조정 */
    .hero-container { 
        background-color: #002147; 
        color: #FFFFFF; 
        padding: 25px; 
        border-radius: 10px; 
        margin-bottom: 20px; 
    }
    
    /* 버튼 크기 조정 */
    div.stLinkButton > a { font-size: 14px !important; padding: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. 로그인 및 메인 화면 구성
def login_screen():
    st.markdown("<h2 style='text-align: center;'>더블유에셋 성남센터 로그인</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        user_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        if st.form_submit_button("로그인", use_container_width=True):
            if user_id == "admin" and password == "1234":
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = user_id
                st.rerun()
            else:
                st.error("로그인 실패")

def main_app():
    inject_custom_css()
    
    with st.sidebar:
        st.write(f"반갑습니다, **{st.session_state.get('current_user')}**님!")
        if st.button("로그아웃"):
            st.session_state['logged_in'] = False
            st.rerun()
        selected_menu = st.radio("📌 메뉴", ["🏢 센터 소개", "🚀 연금 시뮬레이터", "📊 재무 설계", "📈 투자 전략", "🛡️ 보장 분석"])

    st.markdown('<div class="hero-container"><h1>WASSET 성남센터</h1><p>성공적인 자산 관리를 위한 파트너</p></div>', unsafe_allow_html=True)
    
    # 각 메뉴 내용
    if selected_menu == "🏢 센터 소개":
        st.header("성남센터 소개")
        st.write("전문적인 금융 컨설팅을 제공합니다.")
    elif selected_menu == "🚀 연금 시뮬레이터":
        st.header("연금 시뮬레이터")
        st.link_button("시뮬레이터 시작", "https://example.com")
    else:
        st.header(selected_menu)
        st.write("관련 서비스를 준비 중입니다.")

if st.session_state['logged_in']:
    main_app()
else:
    login_screen()
