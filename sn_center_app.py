import streamlit as st

# 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide", page_icon="🏢")

def inject_custom_css():
    st.markdown("""
        <style>
        /* Pretendard 폰트 */
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        html, body, [class*="st-"] { font-family: 'Pretendard', sans-serif !important; }
        
        /* 탭 가독성 강제 수정 */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #f0f2f6; /* 탭 목록 배경색을 밝게 */
            padding: 10px;
            border-radius: 10px;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-size: 20px !important;
            font-weight: 800 !important;
            color: #000000 !important; /* 글자색을 검은색으로 강제 */
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
safe_image("images/logo.png", width=150)

st.markdown("""
    <div class="hero-container">
        <h1>WASSET 성남센터</h1>
        <p style="font-size: 20px;">고객님의 성공적인 자산 관리를 위해 최선을 다하는 파트너입니다.</p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🏢 센터 소개", "🚀 연금 시뮬레이터"])

with tab1:
    safe_image("images/main_banner.jpg", use_container_width=True)
    st.header("성남센터에 오신 것을 환영합니다")
    st.info("💡 전문적인 금융 컨설팅과 함께 안정적인 노후를 준비하세요.")

with tab2:
    st.header("프리미엄 연금 시뮬레이터")
    sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    st.link_button("연금 시뮬레이터 시작하기", sim_url, use_container_width=True)
