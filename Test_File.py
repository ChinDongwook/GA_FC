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
        height: 1px
