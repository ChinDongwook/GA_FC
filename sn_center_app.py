import streamlit as st

# 페이지 레이아웃 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

# 사이드바 (문의 및 위치 정보)
with st.sidebar:
    st.image("https://www.w-asset.co.kr/assets/images/logo.png") # 더블유에셋 로고 사용 가능
    st.title("📞 상담 문의")
    st.write("전문 컨설턴트와의 1:1 상담")
    st.info("📍 성남시 분당구/중원구 일대\n\n📞 031-000-0000")

# 메인 페이지 타이틀
st.title("🏢 더블유에셋 성남센터")
st.markdown("---")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["센터 소개", "금융/자산관리 전문 칼럼", "연금 시뮬레이터"])

with tab1:
    st.header("신뢰와 전문성으로 자산을 설계합니다")
    st.write("더블유에셋 성남센터는 객관적인 데이터를 바탕으로 고객의 라이프사이클에 최적화된 자산관리 솔루션을 제공합니다.")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("우리의 원칙")
        st.write("✅ 투명한 수수료 체계 및 데이터 기반 분석")
        st.write("✅ 고객 중심의 맞춤형 은퇴 설계")
    with col2:
        st.subheader("전문 컨설팅 분야")
        st.write("- 연금저축/IRP/ISA 자산운용 전략")
        st.write("- 법인/개인 절세 및 세금 컨설팅")

with tab2:
    st.header("금융/자산관리 전문 지식")
    st.markdown("---")
    
    st.subheader("💡 현금으로 썩히지 마세요: 퇴직연금 시스템화")
    st.write("DC형 퇴직연금 계좌는 방치하는 순간 물가 상승률에 의해 자산이 깎입니다. 증권사 계좌로 시스템화하여 자산을 관리하세요.")
    
    st.subheader("💰 절세의 핵심: ISA 계좌 활용법")
    st.write("1인당 1개만 가능한 ISA 계좌, 어떻게 활용하느냐에 따라 10년 후 자산 차이가 달라집니다.")
    st.info("자세한 상담은 센터 상담 신청을 통해 확인하세요.")

with tab3:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("더블유에셋 성남센터가 제공하는 최적의 연금 설계 툴입니다.")
    st.write("아래 버튼을 클릭하시면 새 창 열림 없이 현재 창에서 바로 계산을 시작합니다.")
    
    # 현재 창에서 시뮬레이터로 이동
    st.markdown("""
        <a href="https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/" 
           target="_self" 
           style="background-color: #ff4b4b; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px;">
           👉 연금 시뮬레이터 실행하기
        </a>
    """, unsafe_allow_html=True)
