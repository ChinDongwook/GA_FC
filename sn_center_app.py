import streamlit as st

# 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

st.title("🏢 더블유에셋 성남센터")
st.markdown("---")

# 탭 구성
tab1, tab2, tab3 = st.tabs(["1. 센터 소개", "2. 금융/자산관리 칼럼", "3. 연금 시뮬레이터 이동"])

with tab1:
    st.header("신뢰와 전문성으로 자산을 설계합니다")
    st.write("더블유에셋 성남센터는 데이터에 기반한 전문적인 컨설팅을 제공합니다.")
    st.info("📍 위치: 성남시 분당구/중원구 일대 | 📞 문의: 센터로 문의주세요.")

with tab2:
    st.header("금융/자산관리 전문 지식")
    st.markdown("---")
    st.subheader("💡 박곰희 노후준비 매니지먼트")
    st.write("퇴직연금(DC형) 운용 팁: 현금으로 방치하지 말고 증권사 계좌로 시스템화하세요.")
    st.subheader("💰 ISA 계좌 활용법")
    st.write("전 금융기관 1인 1계좌, 절세의 핵심입니다.")

with tab3:
    st.header("연금 시뮬레이터 실행")
    st.write("아래 버튼을 클릭하시면 연금 시뮬레이션 페이지로 즉시 이동합니다.")
    
    # 새 창 띄우지 않고 현재 창에서 이동
    url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    st.markdown(f"""
        <a href="{url}" 
           target="_self" 
           style="background-color: #ff4b4b; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px;">
           👉 연금 시뮬레이터 실행하기 (클릭)
        </a>
    """, unsafe_allow_html=True)
