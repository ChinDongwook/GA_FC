import streamlit as st

# 페이지 환경 설정 (넓은 레이아웃과 아이콘)
st.set_page_config(page_title="더블유에셋 성남센터", page_icon="🏢", layout="wide")

# 고급스러운 디자인을 위한 CSS 삽입
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    h1 { color: #003366 !important; font-weight: 800 !important; }
    .stTabs [data-baseweb="tab-list"] { background-color: #ffffff; padding: 10px; border-radius: 10px; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; border: 1px solid #e0e0e0; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    .css-1r6slp0 { font-size: 1.2rem; }
    </style>
""", unsafe_allow_html=True)

# 메인 헤더
st.title("🏢 더블유에셋 성남센터")
st.markdown("### 데이터 기반의 스마트 재무 설계 파트너")
st.markdown("---")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["센터 소개", "금융 전문 칼럼", "연금 시뮬레이터"])

with tab1:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.header("신뢰 그 이상의 가치")
        st.write("더블유에셋 성남센터는 투명한 수수료 체계와 전문적인 자산 관리 솔루션을 제공합니다.")
    with col2:
        st.info("📍 위치: 성남시 분당구/중원구 일대\n📞 상담: 031-000-0000")

with tab2:
    st.header("💡 금융 인사이트")
    # 아코디언 방식으로 깔끔하게 정리
    with st.expander("퇴직연금(DC형) 운용 핵심 팁"):
        st.write("방치된 현금은 물가 상승률을 따라가지 못합니다. 시스템화된 자산 운용이 필요합니다.")
    with st.expander("절세의 핵심, ISA 계좌 활용법"):
        st.write("1인 1계좌, 절세 혜택을 극대화하는 성남센터만의 포트폴리오 전략을 확인하세요.")

with tab3:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("고객님의 노후 자산을 미리 계산해 보세요.")
    
    # 시뮬레이터 앱 주소
    sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    
    # 세련된 버튼 스타일링
    st.markdown(f"""
        <div style="padding: 20px;">
            <a href="{sim_url}" target="_blank" 
               style="background-color: #003366; color: white; padding: 15px 30px; 
               text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 18px;">
               🚀 시뮬레이터 앱 실행하기 (새 창)
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    st.warning("이동 후 고객님의 연금 정보를 입력하여 시뮬레이션을 완료하세요.")
