import streamlit as st

# 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide", page_icon="🏢")

def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
        html, body, [class*="st-"] { font-family: 'Pretendard', sans-serif !important; }
        
        /* 히어로 섹션 */
        .hero-container { background-color: #002147; color: #FFFFFF; padding: 40px; border-radius: 15px; margin-bottom: 30px; }
        
        /* 탭 글자 색상을 확실하게 지정 (어떤 테마에서도 보이도록) */
        .stTabs [data-baseweb="tab"] { 
            font-size: 20px !important; 
            font-weight: 700 !important; 
            color: #002147 !important; 
        }
        
        /* 버튼 스타일 */
        div.stLinkButton > a { background-color: #002147 !important; color: white !important; font-weight: 600 !important; }
        div.stLinkButton > a:hover { background-color: #d4af37 !important; color: #000 !important; }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# 이미지 오류 방지용 함수
def safe_image(path, width=None, use_container_width=False):
    try:
        st.image(path, width=width, use_container_width=use_container_width)
    except Exception:
        st.error(f"이미지를 불러올 수 없습니다: {path}. 경로와 파일명을 확인해주세요.")

# 1. 로고 배치
safe_image("images/logo.png", width=150)

# 메인 헤더
st.markdown("""
    <div class="hero-container">
        <h1>WASSET 성남센터</h1>
        <p style="font-size: 20px;">고객님의 성공적인 자산 관리를 위해 최선을 다하는 파트너입니다.</p>
    </div>
""", unsafe_allow_html=True)

# 탭 구성
tab1, tab2 = st.tabs(["🏢 센터 소개", "🚀 연금 시뮬레이터"])

with tab1:
    safe_image("images/main_banner.jpg", use_container_width=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("성남센터에 오신 것을 환영합니다")
        st.write("전문적인 금융 컨설팅과 함께 안정적인 노후를 준비하세요.")
        st.info("💡 센터에 대한 더 자세한 정보나 상담 예약은 언제든 문의해 주세요.")
    with col2:
        st.metric(label="전문 상담사 수", value="45명+", delta="고객과 함께 성장 중")

with tab2:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("안정적인 미래를 위한 첫걸음, 아래 시뮬레이터를 통해 확인해 보세요.")
    
    sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    st.link_button("연금 시뮬레이터 시작하기", sim_url, use_container_width=True)
    st.warning("이동 후 고객님의 정보를 입력하여 시뮬레이션을 진행하세요.")

st.markdown("---")
st.caption("© 2026 더블유에셋 성남센터 | 전문 금융 컨설팅")
