import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide", page_icon="🏢")

# 2. 로그인 상태 초기화
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 3. CSS 스타일링 (테마 설정창 겹침 방지 및 범위 한정)
def inject_custom_css():
    st.markdown("""
    <style>
    /* 콘텐츠 컨테이너 너비 제한 */
    .block-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
    /* 사이드바 폭 축소 (모바일 및 데스크탑 대응) */
    [data-testid="stSidebar"] {
        min-width: 200px !important;
        max-width: 250px !important;
    }
    
    /* 메인 화면 컨테이너로 범위 한정 (테마 설정창 겹침 방지) */
    [data-testid="stAppViewContainer"] { 
        font-family: 'Pretendard', sans-serif !important; 
    }
    
    /* 사이드바 토글 버튼 보호 */
    [data-testid="collapsedControl"] { display: flex !important; color: #002147 !important; }

    /* 히어로 섹션 */
    .hero-container { background-color: #002147; color: #FFFFFF; padding: 25px; border-radius: 10px; margin-bottom: 20px; }
    
    /* 타이틀 및 헤더 */
    [data-testid="stAppViewContainer"] h1 { font-size: 26px !important; margin-bottom: 10px !important; }
    [data-testid="stAppViewContainer"] h2 { font-size: 20px !important; }
    
    /* 본문 텍스트 */
    [data-testid="stAppViewContainer"] .stMarkdown, 
    [data-testid="stAppViewContainer"] .stWrite, 
    [data-testid="stAppViewContainer"] p { 
        font-size: 15px !important; 
        line-height: 1.4 !important; 
    }

    /* 사이드바 메뉴 */
    [data-testid="stSidebar"] div.stRadio > label { font-size: 17px !important; font-weight: 800 !important; color: #002147 !important; }
    [data-testid="stSidebar"] div.stRadio p { font-size: 14px !important; }

    /* 버튼 스타일 */
    div.stLinkButton > a { font-size: 14px !important; background-color: #002147 !important; color: white !important; font-weight: 600 !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. 이미지 오류 방지 함수
def safe_image(path, width=None, use_container_width=False):
    try:
        st.image(path, width=width, use_container_width=use_container_width)
    except Exception:
        st.warning(f"이미지를 불러올 수 없습니다. 경로를 확인하세요: {path}")

# 5. 업무 매뉴얼 페이지 렌더링 함수
def show_manual_page():
    st.header("📖 성남센터 업무 매뉴얼")
    
    tab_names = [
        "공지사항", "신규 계약", "보험금 청구", "고객 관리", "상품 정보",
        "수수료/평가", "교육 일정", "지원 서식", "센터 연락처", "FAQ"
    ]
    tabs = st.tabs(tab_names)
    
    for i, tab in enumerate(tabs):
        with tab:
            if tab_names[i] == "센터 연락처":
                st.subheader("📞 센터 내 주요 연락처")
                st.table({
                    "부서/직함": ["센터장", "매니저", "지원팀"],
                    "성명": ["홍길동", "김철수", "이영희"],
                    "내선번호": ["101", "102", "103"]
                })
            else:
                st.subheader(f"{tab_names[i]}")
                with st.expander(f"📌 {tab_names[i]} 관련 핵심 요약 및 지침 클릭"):
                    st.write(f"이곳에 {tab_names[i]}에 대한 세부 업무 매뉴얼 내용을 작성 및 업데이트하세요.")
                    st.info("필요 시 다운로드 링크나 세부 가이드를 텍스트로 보완할 수 있습니다.")

# 6. 로그인 화면 함수
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

# 7. 메인 홈페이지 함수
def main_app():
    inject_custom_css()
    
    with st.sidebar:
        st.write(f"반갑습니다, **{st.session_state.get('current_user')}**님!")
        if st.button("로그아웃"):
            st.session_state['logged_in'] = False
            st.rerun()
        selected_menu = st.radio("📌 센터 메뉴 이동", ["🏢 센터 소개", "🚀 연금 시뮬레이터", "📖 업무 매뉴얼", "📊 재무 설계", "📈 투자 전략", "🛡️ 보장 분석"])

    # 로고 및 헤더
    safe_image("images/logo.png", width=100)
    st.markdown('<div class="hero-container"><h1>WASSET 성남센터</h1><p>성공적인 자산 관리를 위한 파트너</p></div>', unsafe_allow_html=True)
    
    # 메뉴별 내용
    if selected_menu == "🏢 센터 소개":
        safe_image("images/main_banner.jpg", use_container_width=True)
        st.header("성남센터에 오신 것을 환영합니다")
        st.write("전문적인 금융 컨설팅과 함께 안정적인 노후를 준비하세요.")
        
        # 스마트폰 앱 설치 안내 섹션 추가 (텍스트 크기 제어 적용)
        st.markdown("---")
        st.markdown("<h3 style='font-size: 18px; font-weight: bold;'>📱 스마트폰에 1초 만에 센터 앱 설치하기</h3>", unsafe_allow_html=True)
        st.markdown("<div style='font-size: 14px; background-color: #e8f4f8; padding: 15px; border-radius: 8px; color: #002147; margin-bottom: 15px;'>💡 이 홈페이지를 스마트폰 바탕화면에 추가해두면 어플처럼 터치 한 번으로 접속할 수 있습니다.</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div style='font-size: 15px; font-weight: bold; margin-bottom: 8px;'>🍎 아이폰 (Safari)</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 13px; line-height: 1.6;'>1. 화면 하단의 <b>공유</b>(네모에 화살표) 버튼 터치<br>2. 메뉴를 위로 올려 <b>'홈 화면에 추가'</b> 선택<br>3. 우측 상단 <b>'추가'</b> 버튼 터치</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div style='font-size: 15px; font-weight: bold; margin-bottom: 8px;'>🤖 안드로이드 (Chrome)</div>", unsafe_allow_html=True)
            st.markdown("<div style='font-size: 13px; line-height: 1.6;'>1. 우측 상단의 <b>메뉴</b>(점 3개) 버튼 터치<br>2. <b>'홈 화면에 추가'</b> 선택<br>3. 팝업창에서 <b>'추가'</b> 버튼 터치</div>", unsafe_allow_html=True)
            
    elif selected_menu == "🚀 연금 시뮬레이터":
        st.header("프리미엄 연금 시뮬레이터")
        st.link_button("시뮬레이터 시작하기", "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/")
    elif selected_menu == "📖 업무 매뉴얼":
        show_manual_page()
    else:
        st.header(selected_menu)
        st.write("관련 서비스를 준비 중입니다.")

if st.session_state['logged_in']:
    main_app()
else:
    login_screen()
