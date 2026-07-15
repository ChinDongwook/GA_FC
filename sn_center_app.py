import streamlit as st
import streamlit.components.v1 as components
import datetime

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

if "menu_page" not in st.session_state:
    st.session_state["menu_page"] = "🏢 센터 소개"

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
        transition: transform 0.2s ease, border-color 0.2s ease;
        height: 100%;
    }
    .card:hover {
        border-color: #C9A84C;
        transform: translateY(-2px);
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
        라이트 모드 — body.light-mode 클래스 기반
    ══════════════════════════════════════ */
    body.light-mode .stApp,
    body.light-mode [data-testid="stAppViewContainer"] {
        background-color: #F4F1EA !important;
    }
    body.light-mode [data-testid="stHeader"] {
        background-color: #F4F1EA !important;
        border-bottom: 1px solid #D4C5A0 !important;
    }
    body.light-mode [data-testid="stHeader"] button svg,
    body.light-mode [data-testid="stHeader"] span {
        color: #001330 !important;
        fill: #001330 !important;
    }
    body.light-mode [data-testid="stDecoration"] {
        background: linear-gradient(90deg, #001330, #C9A84C, #001330) !important;
    }
    /* 사이드바는 항상 네이비 유지 */
    body.light-mode [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001330 0%, #0A2342 100%) !important;
    }
    body.light-mode .card {
        background: #FFFFFF !important;
        border-color: #E0D9CC !important;
        box-shadow: 0 2px 16px rgba(0,19,48,0.08) !important;
    }
    body.light-mode .card-title { color: #001330 !important; }
    body.light-mode .card-body  { color: #4A5568 !important; }
    body.light-mode .login-card {
        background: #FFFFFF !important;
        border-color: #E0D9CC !important;
    }
    body.light-mode .login-logo-text { color: #001330 !important; }
    body.light-mode [data-testid="stAppViewContainer"] h1,
    body.light-mode [data-testid="stAppViewContainer"] h2 {
        color: #001330 !important;
    }
    body.light-mode [data-testid="stAppViewContainer"] p {
        color: #2E3A4E !important;
    }
    body.light-mode [data-testid="stExpander"] {
        background: #FFFFFF !important;
        border-color: #E0D9CC !important;
    }
    body.light-mode [data-testid="stExpander"] summary {
        color: #001330 !important;
    }
    body.light-mode [data-testid="stTabs"] button {
        color: #4A5568 !important;
    }
    body.light-mode [data-testid="stTabs"] button[aria-selected="true"] {
        color: #001330 !important;
    }
    body.light-mode [data-testid="stAppViewContainer"] table thead tr {
        background: #001330 !important;
    }
    body.light-mode [data-testid="stAppViewContainer"] tbody tr:nth-child(even) {
        background: #F8F5EE !important;
    }
    body.light-mode [data-testid="stAppViewContainer"] td,
    body.light-mode [data-testid="stAppViewContainer"] th {
        border-bottom-color: #E0D9CC !important;
        color: #2E3A4E !important;
    }
    body.light-mode [data-testid="stInfoBox"] {
        background: #FFF8EC !important;
    }
    body.light-mode .install-banner {
        background: #001330 !important;
    }
    body.light-mode .hero-container {
        background: linear-gradient(135deg, #001330 0%, #0A2342 60%, #001a3a 100%) !important;
    }
    body.light-mode .gold-divider {
        background: linear-gradient(90deg, #C9A84C, #C9A84C88, transparent) !important;
    }
    
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# JS: Streamlit 테마 감지 → body 클래스 토글 (components.html 우회 방식 적용)
# ─────────────────────────────────────────────
def inject_theme_detector():
    components.html(r"""
    <script>
    (function() {
        try {
            // 부모 DOM(Streamlit 앱 본체)에 접근
            const parentDoc = window.parent.document;
            if (!parentDoc) return;

            function applyTheme() {
                // Streamlit이 설정한 실제 배경색 변수 감지
                let bgColor = window.parent.getComputedStyle(parentDoc.documentElement).getPropertyValue('--background-color').trim()
                           || window.parent.getComputedStyle(parentDoc.body).getPropertyValue('--background-color').trim();
                
                if (!bgColor) return;

                let r, g, b;
                if (bgColor.startsWith('#')) {
                    let hex = bgColor.replace('#', '');
                    if (hex.length === 3) hex = hex.split('').map(x => x + x).join('');
                    r = parseInt(hex.substr(0, 2), 16);
                    g = parseInt(hex.substr(2, 2), 16);
                    b = parseInt(hex.substr(4, 2), 16);
                } else {
                    const rgb = bgColor.match(/\d+/g);
                    if (rgb && rgb.length >= 3) {
                        r = parseInt(rgb[0], 10);
                        g = parseInt(rgb[1], 10);
                        b = parseInt(rgb[2], 10);
                    } else {
                        return;
                    }
                }

                // 밝기 공식 적용
                const brightness = (r * 299 + g * 587 + b * 114) / 1000;
                
                // 테마 클래스 토글
                if (brightness > 128) {
                    parentDoc.body.classList.add('light-mode');
                } else {
                    parentDoc.body.classList.remove('light-mode');
                }
            }

            // 초기 강제 적용 및 주기적 감시 (Streamlit 메뉴 전환 실시간 포착)
            applyTheme();
            setInterval(applyTheme, 500);

        } catch(e) {
            console.error("테마 전환 스크립트 오류:", e);
        }
    })();
    </script>
    """, height=0, width=0)

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
                    "부서 / 직함": ["센터장", "성남센터", "지원팀"],
                    "성명":       ["진동욱", "김철수", "이영희"],
                    "내선번호":   ["010-5717-1402",   "031-722-2223",   "103"],
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
            save_info = st.checkbox("✅ 아이디/비밀번호 저장")
            submitted = st.form_submit_button("로그인", use_container_width=True)

        if submitted:
            valid_users = {
                "admin":      "1234",
                "wa230962":   "wa230962",
                "guest":      "guest",
                "center_fc3": "pass3333",
                "wa22014":   "wa22014", "wa221132":   "wa221132", "wa140867":   "wa140867", "wa211014":   "wa211014", 
            }
            if user_id in valid_users and valid_users[user_id] == password:
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = user_id
                
                # 저장 옵션 선택 여부에 따라 세션에 임시 플래그 저장
                if save_info:
                    st.session_state["save_creds"] = {"id": user_id, "pw": password}
                else:
                    st.session_state["clear_creds"] = True
                    
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 일치하지 않습니다.")

        # 로그인 폼 하단에 추가 안내 문구 배치
        st.info("💡 아이디/비번은 사번과 동일합니다. 사번으로 로그인 후 업무메뉴 이용 가능합니다.")

    # [핵심] 로그인 화면이 렌더링될 때 로컬 스토리지에 저장된 자격증명이 있다면 자동 입력
    components.html("""
    <script>
    (function() {
        setTimeout(() => {
            try {
                const parentDoc = window.parent.document;
                const id = window.parent.localStorage.getItem('wa_id');
                const pw = window.parent.localStorage.getItem('wa_pw');
                
                if (id && pw) {
                    const idInput = parentDoc.querySelector('input[placeholder="아이디를 입력하세요"]');
                    const pwInput = parentDoc.querySelector('input[placeholder="비밀번호를 입력하세요"]');
                    const checkbox = parentDoc.querySelector('input[type="checkbox"]');

                    // React 기반의 Streamlit 입력창에 값을 강제로 주입하고 이벤트를 발생시키는 함수
                    function setReactValue(element, value) {
                        const valueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        valueSetter.call(element, value);
                        element.dispatchEvent(new Event('input', { bubbles: true }));
                    }

                    if (idInput && idInput.value === '') setReactValue(idInput, id);
                    if (pwInput && pwInput.value === '') setReactValue(pwInput, pw);
                    
                    // 체크박스 자동 선택
                    if (checkbox && !checkbox.checked) checkbox.click();
                }
            } catch(e) {}
        }, 300);
    })();
    </script>
    """, height=0, width=0)

# ─────────────────────────────────────────────
# 7. 메인 앱
# ─────────────────────────────────────────────
def main_app():
    inject_custom_css()
    inject_theme_detector()

    # ─────────────────────────────────────────────
    # [핵심] 로그인 성공 직후 로컬 스토리지 처리 로직
    # ─────────────────────────────────────────────
    if st.session_state.get("save_creds"):
        id_val = st.session_state["save_creds"]["id"]
        pw_val = st.session_state["save_creds"]["pw"]
        components.html(f"""
            <script>
                window.parent.localStorage.setItem('wa_id', '{id_val}');
                window.parent.localStorage.setItem('wa_pw', '{pw_val}');
            </script>
        """, height=0, width=0)
        del st.session_state["save_creds"]

    if st.session_state.get("clear_creds"):
        components.html("""
            <script>
                window.parent.localStorage.removeItem('wa_id');
                window.parent.localStorage.removeItem('wa_pw');
            </script>
        """, height=0, width=0)
        del st.session_state["clear_creds"]

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
            
            # 사이드바에서 혼동을 주던 임시 메뉴를 제거하고 본질적인 메뉴만 남김
            menu_options = ["🏢 센터 소개", "🚀 연금 시뮬레이터", "📖 업무 매뉴얼"]
        else:
            st.markdown('<div style="font-size:12px; color:#8B9BB4; padding:0 4px; margin-bottom:12px;">게스트 접속 중</div>', unsafe_allow_html=True)
            st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
            menu_options = ["🏢 센터 소개", "🚀 연금 시뮬레이터", "🔐 로그인"]

        # 로그인/로그아웃으로 인해 선택되었던 메뉴가 사라질 경우를 대비한 안전 장치
        if st.session_state["menu_page"] not in menu_options:
            st.session_state["menu_page"] = menu_options[0]

        # key 속성을 지정하여 테마 변경 등의 리프레시에도 상태를 보존
        selected_menu = st.radio("MENU", menu_options, key="menu_page")

        # 사이드바 하단 현재 시간 표시 (한국 표준시 기준)
        now_kst = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
        time_str = now_kst.strftime("%Y년 %m월 %d일 %H:%M")

        # 메뉴와 겹치지 않도록 absolute 속성을 제거하고 위쪽 여백(margin-top)을 부여, 폰트 크기(14px) 상향
        st.markdown(f"""
        <div style="margin-top:60px; text-align:center;">
            <div style="font-size:14px; color:#8B9BB4; letter-spacing:0.05em; font-weight:500;">{time_str}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── 히어로 배너 ───────────────────────────
    safe_image("images/logo.png", width=80)
    st.markdown("""
    <div class="hero-container">
        <div class="hero-eyebrow">WASSET SEUNGNAM CENTER</div>
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

        # 서비스 카드 (변경 사항 적용부)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 기본 3개 카드
        cards = [
            ("💻", "더블유에셋 New전산", "W-ASSET 통합 영업지원 및 고객관리 전산 시스템으로 이동합니다.", "https://wasset.kr/main"),
            ("📊", "보험료비교", "손보.생보 보험사별 보험료 비교, OK마이보험 보장 내역을 한눈에 비교 분석합니다.", "https://wasset.bojang114.com/index.html"),
            ("📞", "성남센터 담당자 연락처", "성남센터 업무 지원 담당자들의 직통 연락처를 확인합니다.", "https://docs.google.com/spreadsheets/d/1pspaAVWQlx7ypp878z6PZPwk27TybUfKoGmybvaiBOU/edit?gid=0#gid=0")
        ]
        
        is_logged_in = st.session_state.get("logged_in", False)

        # 로그인 시 6개의 추가 카드 메뉴 확장
        if is_logged_in:
            cards.extend([
                ("📂", "모든 보험사 전산설치", "모든 보험사 전살설치 및 설계요청 각보험사 정보. 카드납. 소식지 .", "https://wasset-info.com/insurance"),
                ("📑", "영업 자료", "손생보 소식지, 시책, 카드뉴스, 상품비교, 가이드북, 질병통계, 각종 금융 자료", "https://drive.google.com/drive/folders/1Oq1MjqWxCqhEt9808ejD6ult0H-ng3Ts"),
                ("🛡️", "보장 분석 리포트", "한화손보, KB손보, DB손보 보장분석PDF 등록으로 전문적인 보장분석 리포트를 만들어보세요", "https://wasset.bojang114.com/uiFitbojang/index.html?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb25zdWx0YW50aWQiOiJXQTIzMDk2MiIsImNvbnN1bHRhbnRfbmFtZSI6IuynhOuPmeyasSIsImNvbXB5X2NkIjoiQTIzOCIsImNvbXB5X25hbWUiOiLrjZTruJTsnKDsl5DshYsiLCJicmFuY2hfbmFtZSI6IuuNlOu4lOycoOyXkOyFiyIsImV4cCI6MTc4MzU2NDE1MiwiY29uc3VsdGFudF9pZCI6IldBMjMwOTYyIiwibmFtZSI6IuynhOuPmeyasSIsImNsaWVudF9pZCI6IkEyMzgiLCJtZG4iOiJBMjM4Iiwicm9sZSI6IiIsImNsaWVudF9pcCI6IjIyMi45OC4xNzEuMjMzIn0.LKGm8lUGYR8gUhGt9xXiswN1UVIoDOKPPlR_DxVq_gY"),
                ("🎓", "더블유에셋 와인프로", "더블유에셋 구전산 와인프로 인트라넷.", "https://wain.pro/main/login.php"),
                ("👥", "고객 관리 툴", "서비스 준비중입니다.", ""),
                ("🏆", "우수사례 공유", "서비스 준비중입니다.", "")
            ])

        # 전체 카드 목록을 3개씩 끊어서 열(column)을 생성하고 배치 (그리드 구현)
        for i in range(0, len(cards), 3):
            cols = st.columns(3)
            # 슬라이싱된 카드를 각 열에 매핑
            for col, card in zip(cols, cards[i:i+3]):
                icon, title, body, link = card
                with col:
                    if is_logged_in:
                        # 로그인 성공 상태: <a> 태그를 이용해 카드 클릭 시 새 창에서 열리도록 구현
                        st.markdown(f"""
                        <a href="{link}" target="_blank" style="text-decoration: none;">
                            <div class="card" style="cursor: pointer;">
                                <div class="card-icon">{icon}</div>
                                <div class="card-title" style="color: #C9A84C;">{title} ↗</div>
                                <div class="card-body">{body}</div>
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                    else:
                        # 미로그인 상태: 클릭 시 가장 간결한 JS 팝업(alert) 알림 처리
                        st.markdown(f"""
                        <a href="javascript:void(0);" onclick="alert('로그인 후 이용해주세요');" style="text-decoration: none;">
                            <div class="card" style="opacity: 0.75; cursor: pointer;">
                                <div class="card-icon">{icon}</div>
                                <div class="card-title">{title}</div>
                                <div class="card-body">{body}<br><br><span style="color:#C9A84C; font-size:12px; font-weight:600;">🔒 로그인 후 이용 가능</span></div>
                            </div>
                        </a>
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
