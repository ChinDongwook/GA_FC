import streamlit as st

# 1. 페이지 레이아웃 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

# 2. 메인 타이틀
st.title("🏢 더블유에셋 성남센터")
st.markdown("전문성과 신뢰로 고객님의 자산을 관리합니다.")
st.markdown("---")

# 3. 탭 구성
tab1, tab2, tab3 = st.tabs(["센터 소개", "금융 정보 칼럼", "연금 시뮬레이터"])

with tab1:
    st.header("더블유에셋 성남센터")
    st.write("고객의 라이프사이클에 최적화된 재무 설계를 제공합니다.")
    st.info("📍 위치: 성남시 분당/중원구 일대 | 📞 문의: 센터로 문의 바랍니다.")

with tab2:
    st.header("금융 정보 칼럼")
    st.subheader("💡 박곰희 노후준비 매니지먼트")
    st.write("퇴직연금(DC형)을 방치하지 말고 시스템화하세요.")
    st.subheader("💰 ISA 계좌 활용법")
    st.write("1인 1계좌, 절세의 핵심입니다.")

with tab3:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("고객님의 노후 자금을 미리 계산해 보세요.")
    
    # 시뮬레이터 주소 (연결할 앱 주소를 넣으세요)
    sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    
    # 이동 버튼
    if st.button("🚀 시뮬레이터로 이동하기"):
        st.write(f"아래 링크를 클릭하세요: [{sim_url}]({sim_url})")
        st.link_button("시뮬레이터 실행", sim_url)
