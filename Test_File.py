import streamlit as st

# ─────────────────────────────────────────────
# 1. 페이지 설정
# ─────────────────────────────────────────────
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide", page_icon="🏢")

# ─────────────────────────────────────────────
# 2. 로그인 상태 초기화
# ─────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["current_user"] = "게스트"

# ─────────────────────────────────────────────
# 3. CSS — 다크 네이비 + 골드 고급 금융사 테마
# ─────────────────────────────────────────────
def inject_custom_css():
    st.markdown("""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap');
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css');

    /* ── 전체 배경 ── */
    .stApp, [data-testid="stApp"] {
        background-color: #070B11 !important;
    }
    [data-testid="stAppViewContainer"] {
        background-color: #070B11 !important;
        font-family: 'Pretendard', sans-serif !important;
    }
    /* ── 상단 헤더 & 툴바 (다크 테마) ── */
    [data-testid="stHeader"] {
        background-color: #070B11 !important;
        border-bottom: 1px solid #1E2D42 !important;
    }
    /* 햄버거/점세개 메뉴 아이콘 */
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] svg,
    [data-testid="stHeader"] span {
        color: #8B9BB4 !important;
        fill: #8B9BB4 !important;
    }
    [data-testid="stHeader"] button:hover svg,
    [data-testid="stHeader"] button:hover span {
        color: #C9A84C !important;
        fill: #C9A84C !important;
    }
    /* Streamlit 상단 툴바 (Deploy 버튼 등) */
    [data-testid="stToolbar"],
    .stToolbar {
        background-color: #070B11 !important;
    }
    [data-testid="stToolbar"] * {
        color: #8B9BB4 !important;
    }
    /* 상단 데코 바 제거 */
    #MainMenu, header[data-testid="stHeader"]::before {
        background-color: #070B11 !important;
    }
    /* Streamlit 기본 상단 컬러 바 (빨간/주황 그라디언트) 덮기 */
    [data-testid="stDecoration"],
    .stDecoration {
        background: linear-gradient(90deg, #001330, #C9A84C, #001330) !important;
        height: 2px !important;
    }

    /* ── 사이드바 ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001330 0%, #0A2342 100%) !important;
        min-width: 220px !important;
        max-width: 260px !important;
        border-right: 1px solid #C9A84C33 !important;
    }
    [data-testid="stSidebar"] * {
        color: #E8E0D0 !important;
    }
    /* 사이드바 유저 안내 */
    [data-testid="stSidebar"] .stMarkdown p {
        font-size: 13px !important;
        color: #8B9BB4 !important;
        letter-spacing: 0.02em;
    }
    /* 라디오 그룹 라벨 (메뉴 제목) */
    [data-testid="stSidebar"] div.stRadio > label {
        font-family: 'Pretendard', sans-serif !important;
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        color: #C9A84C !important;
        margin-bottom: 12px !important;
    }
    /* 라디오 항목 */
    [data-testid="stSidebar"] div[role="radiogroup"] > label {
        padding: 10px 14px !important;
        margin-bottom: 4px !important;
        border-radius: 6px !important;
        border-left: 2px solid transparent !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
        background-color: #ffffff0d !important;
        border-left: 2px solid #C9A84C !important;
    }
    [data-testid="stSidebar"] div.stRadio p {
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #E8E0D0 !important;
    }
    /* 사이드바 divider */
    [data-testid="stSidebar"] hr {
        border-color: #C9A84C33 !important;
        margin: 16px 0 !important;
    }
    /* 로그아웃 버튼 */
    [data-testid="stSidebar"] div.stButton > button {
        background: transparent !important;
        color: #8B9BB4 !important;
        border: 1px solid #C9A84C55 !important;
        font-size: 12px !important;
        padding: 6px 12px !important;
        border-radius: 4px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stSidebar"] div.stButton > button:hover {
        background: #C9A84C22 !important;
        color: #C9A84C !important;
        border-color: #C9A84C !important;
    }
    /* 사이드바 토글 버튼 */
    [data-testid="collapsedControl"] {
        color: #C9A84C !important;
    }

    /* ── 메인 콘텐츠 영역 ── */
    .block-container {
        max-width: 1100px !important;
        padding: 2rem 2.5rem !important;
        margin: 0 auto !important;
    }

    /* ── 히어로 배너 ── */
    .hero-container {
        background: linear-gradient(135deg, #001330 0%, #0A2342 60%, #001a3a 100%);
        color: #D0D8E4;
        padding: 40px 48px;
        border-radius: 12px;
        margin-bottom: 32px;
        border: 1px solid #C9A84C44;
        position: relative;
        overflow: hidden;
    }
    .hero-container::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #C9A84C, transparent);
    }
    .hero-container::after {
        content: 'W';
        position: absolute;
        right: 40px;
        top: 50%;
        transform: translateY(-50%);
        font-family: 'Playfair Display', serif;
        font-size: 120px;
        font-weight: 700;
        color: #C9A84C0d;
        line-height: 1;
    }
    .hero-eyebrow {
        font-size: 11px;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #C9A84C;
        margin-bottom: 10px;
        font-weight: 600;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 36px;
        font-weight: 700;
        margin: 0 0 10px 0;
        line-height: 1.2;
        color: #D0D8E4;
    }
    .hero-sub {
        font-size: 15px;
        color: #8B9BB4;
        margin: 0;
        letter-spacing: 0.03em;
    }

    /* ── 섹션 헤딩 ── */
    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2 {
        font-family: 'Playfair Display', serif !important;
        color: #E8EDF2 !important;
    }
    [data-testid="stAppViewContainer"] h1 { font-size: 28px !important; }
    [data-testid="stAppViewContainer"] h2 { font-size: 22px !important; }
    [data-testid="stAppViewContainer"] h3 {
        font-family: 'Pretendard', sans-serif !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: #8B9BB4 !important;
    }
    [data-testid="stAppViewContainer"] p {
        font-size: 15px !important;
        color: #B8C4D0 !important;
        line-height: 1.65 !important;
    }

    /* ── 골드 구분선 ── */
    .gold-divider {
        height: 1px;
        background: linear-gradient(90deg, #C9A84C, #C9A84C55, transparent);
        margin: 24px 0;
        border: none;
    }

    /* ── 카드 ── */
    .card {
        background: #0D1520;
        border-radius: 10px;
        padding: 24px;
        border: 1px solid #1E2D42;
        border-top: 3px solid #C9A84C;
        box-shadow: 0 2px 16px rgba(0,19,48,0.06);
        margin-bottom: 16px;
    }
    .card-icon {
        font-size: 28px;
        margin-bottom: 10px;
    }
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 17px;
        font-weight: 600;
        color: #E8EDF2;
        margin-bottom: 6px;
    }
    .card-body {
        font-size: 14px;
        color: #7A90A8;
        line-height: 1.55;
    }

    /* ── 앱 설치 배너 ── */
    .install-banner {
        background: #001330;
        border-radius: 10px;
        padding: 22px 26px;
        border: 1px solid #C9A84C44;
        margin-top: 24px;
    }
    .install-banner-title {
        font-size: 12px;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #C9A84C;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .install-banner-desc {
        font-size: 13px;
        color: #8B9BB4;
        margin-bottom: 18px;
        line-height: 1.5;
    }
    .install-col-title {
        font-size: 13px;
        font-weight: 700;
        color: #E8E0D0;
        margin-bottom: 8px;
    }
    .install-col-body {
        font-size: 12px;
        color: #8B9BB4;
        line-height: 1.8;
    }

    /* ── 탭 스타일 ── */
    [data-testid="stTabs"] button {
        font-family: 'Pretendard', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        color: #7A90A8 !important;
        letter-spacing: 0.03em !important;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #E8EDF2 !important;
        border-bottom-color: #C9A84C !important;
    }
    [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
        background-color: #C9A84C !important;
    }

    /* ── expander ── */
    [data-testid="stExpander"] {
        border: 1px solid #1E2D42 !important;
        border-radius: 8px !important;
        background: #0D1520 !important;
    }
    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        font-size: 14px !important;
        color: #D0D8E4 !important;
    }

    /* ── 링크 버튼 ── */
    div.stLinkButton > a {
        background: linear-gradient(135deg, #C9A84C, #b8943d) !important;
        color: #E8EDF2 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border-radius: 6px !important;
        border: none !important;
        padding: 10px 24px !important;
        letter-spacing: 0.05em !important;
        transition: opacity 0.2s !important;
    }
    div.stLinkButton > a:hover {
        opacity: 0.88 !important;
    }

    /* ── 로그인 폼 ── */
    .login-card {
        max-width: 400px;
        margin: 60px auto;
        background: #0D1520;
        border-radius: 12px;
        padding: 48px 40px;
        border: 1px solid #1E2D42;
        border-top: 3px solid #C9A84C;
        box-shadow: 0 8px 40px rgba(0,19,48,0.10);
        text-align: center;
    }
    .login-logo-text {
        font-family: 'Playfair Display', serif;
        font-size: 22px;
        font-weight: 700;
        color: #E8EDF2;
        margin-bottom: 4px;
    }
    .login-sub {
        font-size: 12px;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #C9A84C;
        margin-bottom: 32px;
        font-weight: 600;
    }
    /* 로그인 제출 버튼 */
    div.stForm div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #001330, #0A2342) !important;
        color: #C9A84C !important;
        border: 1px solid #C9A84C55 !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        letter-spacing: 0.08em !important;
        width: 100% !important;
        padding: 12px !important;
        border-radius: 6px !important;
        transition: all 0.2s !important;
    }
    div.stForm div.stFormSubmitButton > button:hover {
        border-color: #C9A84C !important;
        background: #0A2342 !important;
    }

    /* ── 테이블 ── */
    [data-testid="stAppViewContainer"] table {
        border-collapse: collapse !important;
        width: 100% !important;
        font-size: 14px !important;
    }
    [data-testid="stAppViewContainer"] thead tr {
        background: #001330 !important;
        color: #C9A84C !important;
    }
    [data-testid="stAppViewContainer"] tbody tr:nth-child(even) {
        background: #0A1220 !important;
    }
    [data-testid="stAppViewContainer"] td, 
    [data-testid="stAppViewContainer"] th {
        padding: 10px 14px !important;
        border-bottom: 1px solid #1E2D42 !important;
    }

    /* ── info/warning 박스 ── */
    [data-testid="stInfoBox"] {
        background: #0D1A2E !important;
        border-left: 3px solid #C9A84C !important;
        border-radius: 6px !important;
    }

    /* ══════════════════════════════════════
       라이트 모드 오버라이드
       (Streamlit 설정창에서 Light 선택 시)
    ══════════════════════════════════════ */
    [data-theme="light"] .stApp,
    [data-theme="light"] [data-testid="stApp"],
    [data-theme="light"] [data-testid="stAppViewContainer"] {
        background-color: #F4F1EA !important;
    }
    [data-theme="light"] [data-testid="stHeader"] {
        background-color: #F4F1EA !important;
        border-bottom: 1px solid #D4C5A0 !important;
    }
    [data-theme="light"] [data-testid="stDecoration"] {
        background: linear-gradient(90deg, #001330, #C9A84C, #001330) !important;
    }
    [data-theme="light"] [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001330 0%, #0A2342 100%) !important;
    }
    [data-theme="light"] .card {
        background: #FFFFFF !important;
        border-color: #E0D9CC !important;
        box-shadow: 0 2px 16px rgba(0,19,48,0.08) !important;
    }
    [data-theme="light"] .card-title { color: #001330 !important; }
    [data-theme="light"] .card-body  { color: #4A5568 !important; }
    [data-theme="light"] .login-card {
        background: #FFFFFF !important;
        border-color: #E0D9CC !important;
    }
    [data-theme="light"] [data-testid="stAppViewContainer"] h1,
    [data-theme="light"] [data-testid="stAppViewContainer"] h2 {
        color: #001330 !important;
    }
    [data-theme="light"] [data-testid="stAppViewContainer"] p {
        color: #2E3A4E !important;
    }
    [data-theme="light"] [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border-color: #E0D9CC !important;
    }
    [data-theme="light"] [data-testid="stExpander"] summary {
        color: #001330 !important;
    }
    [data-theme="light"] [data-testid="stTabs"] button {
        color: #4A5568 !important;
    }
    [data-theme="light"] [data-testid="stTabs"] button[aria-selected="true"] {
        color: #001330 !important;
    }
    [data-theme="light"] [data-testid="stHeader"] button svg,
    [data-theme="light"] [data-testid="stHeader"] span {
        color: #001330 !important;
        fill: #001330 !important;
    }
    [data-theme="light"] table thead tr {
        background: #001330 !important;
    }
    [data-theme="light"] table tbody tr:nth-child(even) {
        background: #F8F5EE !important;
    }
    [data-theme="light"] table td,
    [data-theme="light"] table th {
        border-bottom-color: #E0D9CC !important;
        color: #2E3A4E !important;
    }
    [data-theme="light"] .install-banner {
        background: #001330 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. 이미지 오류 방지
# ─────────────────────────────────────────────
def safe_image(path, width=None, use_container_width=False):
    try:
        st.image(path, width=width, use_container_width=use_container_width)
    except Exception:
        pass  # 이미지 없으면 조용히 스킵

# ─────────────────────────────────────────────
# 5. 업무 매뉴얼 페이지
# ─────────────────────────────────────────────
def show_manual_page():
    st.markdown('<div class="hero-eyebrow" style="color:#C9A84C; font-size:11px; letter-spacing:0.2em; font-weight:700;">OPERATIONS</div>', unsafe_allow_html=True)
    st.markdown('<h2 style="font-family:Playfair Display,serif; color:#E8EDF2; margin-bottom:4px;">업무 매뉴얼</h2>', unsafe_allow_html=True)
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    tab_names = [
        "📢 공지사항", "📝 신규 계약", "💊 보험금 청구", "👥 고객 관리", "📦 상품 정보",
        "💰 수수료/평가", "📅 교육 일정", "📄 지원 서식", "📞 연락처", "❓ FAQ"
    ]
    tabs = st.tabs(tab_names)

    for i, tab in enumerate(tabs):
        with tab:
            name = tab_names[i]
            if name == "📞 연락처":
                st.markdown("##### 센터 내 주요 연락처")
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                st.table({
                    "부서 / 직함": ["센터장", "매니저", "지원팀"],
                    "성명":       ["홍길동", "김철수", "이영희"],
                    "내선번호":   ["101",   "102",   "103"],
                })
            else:
                st.markdown(f"##### {name.split(' ', 1)[-1]} 지침")
                st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
                with st.expander(f"📌 {name.split(' ', 1)[-1]} 핵심 요약 보기"):
                    st.write(f"이곳에 **{name.split(' ', 1)[-1]}** 관련 세부 업무 매뉴얼을 작성·업데이트하세요.")
                    st.info("필요 시 다운로드 링크나 세부 가이드를 추가할 수 있습니다.")

# ─────────────────────────────────────────────
# 6. 로그인 화면
# ─────────────────────────────────────────────
def login_screen():
    st.markdown("""
    <div class="login-card">
        <div class="login-logo-text">W ASSET</div>
        <div class="login-sub">성남센터 · 전용 포털</div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
        with st.form("login_form"):
            user_id  = st.text_input("아이디", placeholder="아이디를 입력하세요")
            password = st.text_input("비밀번호", type="password", placeholder="비밀번호를 입력하세요")
            submitted = st.form_submit_button("로그인", use_container_width=True)

        if submitted:
            valid_users = {
                "admin":      "1234",
                "wa230962":   "wa230962",
                "guest":      "guest",
                "center_fc3": "pass3333",
            }
            if user_id in valid_users and valid_users[user_id] == password:
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = user_id
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

# ─────────────────────────────────────────────
# 7. 메인 앱
# ─────────────────────────────────────────────
def main_app():
    inject_custom_css()

    # ── 사이드바 ──────────────────────────────
    with st.sidebar:
        # 로고 영역
        st.markdown("""
        <div style="padding: 20px 4px 16px 4px; border-bottom: 1px solid #C9A84C33; margin-bottom: 20px;">
            <div style="font-family:'Playfair Display',serif; font-size:20px; font-weight:700; color:#D0D8E4; letter-spacing:0.04em;">W ASSET</div>
            <div style="font-size:10px; color:#C9A84C; letter-spacing:0.18em; text-transform:uppercase; font-weight:600; margin-top:3px;">성남센터</div>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state["logged_in"]:
            st.markdown(f"""
            <div style="font-size:12px; color:#8B9BB4; margin-bottom:6px; padding:0 4px;">
                <span style="color:#C9A84C;">●</span>&nbsp;&nbsp;{st.session_state.get('current_user')}
            </div>
            """, unsafe_allow_html=True)
            if st.button("로그아웃"):
                st.session_state["logged_in"] = False
                st.session_state["current_user"] = "게스트"
                st.rerun()
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            menu_options = ["🏢 센터 소개", "🚀 연금 시뮬레이터", "📖 업무 매뉴얼", "📊 재무 설계", "📈 투자 전략", "🛡️ 보장 분석"]
        else:
            st.markdown('<div style="font-size:12px; color:#8B9BB4; padding:0 4px; margin-bottom:12px;">게스트 접속 중</div>', unsafe_allow_html=True)
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            menu_options = ["🏢 센터 소개", "🚀 연금 시뮬레이터", "🔐 로그인"]

        selected_menu = st.radio("MENU", menu_options)

        # 사이드바 하단 버전
        st.markdown("""
        <div style="position:absolute; bottom:24px; left:0; right:0; text-align:center;">
            <div style="font-size:10px; color:#3A4E6A; letter-spacing:0.1em;">© 2025 W ASSET</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 히어로 배너 ───────────────────────────
    safe_image("images/logo.png", width=80)
    st.markdown("""
    <div class="hero-container">
        <div class="hero-eyebrow">WASSET SUNGNAM CENTER</div>
        <div class="hero-title">더블유에셋 성남센터</div>
        <p class="hero-sub">신뢰와 전문성으로 함께하는 자산관리 파트너</p>
    </div>
    """, unsafe_allow_html=True)

    # ── 메뉴 분기 ──────────────────────────────
    if selected_menu == "🏢 센터 소개":
        safe_image("images/main_banner.jpg", use_container_width=True)

        st.markdown('<div class="hero-eyebrow" style="color:#C9A84C; font-size:11px; letter-spacing:0.2em; font-weight:700;">ABOUT US</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="font-family:Playfair Display,serif; color:#E8EDF2; margin-bottom:4px;">성남센터 소개</h2>', unsafe_allow_html=True)
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.write("전문적인 금융 컨설팅과 함께 안정적인 노후를 설계하세요. 더블유에셋 성남센터는 고객 한 분 한 분의 자산 목표에 맞춘 맞춤형 솔루션을 제공합니다.")

        # 서비스 카드
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        cards = [
            ("💼", "재무 설계", "고객의 생애 주기에 맞는 체계적인 자산 포트폴리오를 설계합니다."),
            ("📈", "투자 전략", "시장 분석을 바탕으로 리스크를 관리하며 수익을 극대화합니다."),
            ("🛡️", "보장 분석", "예상치 못한 위험으로부터 소중한 자산을 안전하게 지킵니다."),
        ]
        for col, (icon, title, body) in zip([col1, col2, col3], cards):
            with col:
                st.markdown(f"""
                <div class="card">
                    <div class="card-icon">{icon}</div>
                    <div class="card-title">{title}</div>
                    <div class="card-body">{body}</div>
                </div>
                """, unsafe_allow_html=True)

        # 앱 설치 안내
        st.markdown("""
        <div class="install-banner">
            <div class="install-banner-title">📱 스마트폰 앱처럼 사용하기</div>
            <div class="install-banner-desc">바탕화면에 추가하면 터치 한 번으로 바로 접속할 수 있습니다.</div>
        """, unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("""
            <div class="install-col-title">🍎 아이폰 (Safari)</div>
            <div class="install-col-body">
                1. 하단 공유(□↑) 버튼 터치<br>
                2. <b style='color:#E8E0D0;'>홈 화면에 추가</b> 선택<br>
                3. 우측 상단 <b style='color:#E8E0D0;'>추가</b> 버튼 터치
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            st.markdown("""
            <div class="install-col-title">🤖 안드로이드 (Chrome)</div>
            <div class="install-col-body">
                1. 우측 상단 메뉴(⋮) 버튼 터치<br>
                2. <b style='color:#E8E0D0;'>홈 화면에 추가</b> 선택<br>
                3. 팝업창에서 <b style='color:#E8E0D0;'>추가</b> 버튼 터치
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif selected_menu == "🚀 연금 시뮬레이터":
        st.markdown('<div class="hero-eyebrow" style="color:#C9A84C; font-size:11px; letter-spacing:0.2em; font-weight:700;">TOOLS</div>', unsafe_allow_html=True)
        st.markdown('<h2 style="font-family:Playfair Display,serif; color:#E8EDF2; margin-bottom:4px;">연금 시뮬레이터</h2>', unsafe_allow_html=True)
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card" style="max-width:520px;">
            <div class="card-icon">🚀</div>
            <div class="card-title">최저보증 변액종신연금 시뮬레이터</div>
            <div class="card-body" style="margin-bottom:18px;">납입 조건과 운용 시나리오를 직접 입력하여 예상 연금액을 확인하세요.</div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("시뮬레이터 시작하기 →", "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/")

    elif selected_menu == "📖 업무 매뉴얼":
        show_manual_page()

    elif selected_menu == "🔐 로그인":
        login_screen()

    else:
        st.markdown(f'<div class="hero-eyebrow" style="color:#C9A84C; font-size:11px; letter-spacing:0.2em; font-weight:700;">COMING SOON</div>', unsafe_allow_html=True)
        st.markdown(f'<h2 style="font-family:Playfair Display,serif; color:#E8EDF2;">{selected_menu}</h2>', unsafe_allow_html=True)
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="card" style="max-width:480px;">
            <div class="card-body">해당 서비스를 준비 중입니다. 빠른 시일 내에 제공할 예정입니다.</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 8. 앱 실행
# ─────────────────────────────────────────────
main_app()
