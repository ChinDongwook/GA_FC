import streamlit as st

# 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

st.title("🏢 더블유에셋 성남센터")

# 탭 구성
tab1, tab2 = st.tabs(["1. 센터 소개", "2. 연금 시뮬레이터로 이동"])

with tab1:
    st.header("성남센터에 오신 것을 환영합니다")
    st.markdown("전문적인 금융 컨설팅을 경험하세요.")
    st.info("센터에 대한 더 자세한 정보는 아래로 문의해 주세요.")

with tab2:
    st.header("프리미엄 연금 시뮬레이터로 이동")
    st.write("아래 버튼을 클릭하면 연금 시뮬레이션 페이지로 즉시 이동합니다.")
    
    # ✅ 여기서 버튼을 클릭하면 시뮬레이터 주소로 이동합니다
    st.link_button("연금 시뮬레이터 시작하기", "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/")

    st.warning("이동 후 고객님의 정보를 입력하여 시뮬레이션을 진행하세요.")
