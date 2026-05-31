import streamlit as st

# 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

st.title("🏢 더블유에셋 성남센터")
st.markdown("더블유에셋 성남센터는 고객님의 성공적인 자산 관리를 위해 최선을 다합니다.")
st.markdown("---")

# 탭 구성
tab1, tab2 = st.tabs(["🏢 센터 소개", "🚀 연금 시뮬레이터로 이동"])

with tab1:
    st.header("성남센터에 오신 것을 환영합니다")
    st.write("전문적인 금융 컨설팅과 함께 안정적인 노후를 준비하세요.")
    st.info("센터에 대한 더 자세한 정보나 상담 예약은 언제든 문의해 주세요.")

with tab2:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("아래 버튼을 클릭하시면 연금 시뮬레이션 페이지로 즉시 이동합니다.")
    
    # URL 주소
    sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    
    # 버튼 형태의 링크 (target="_self"는 현재 창에서 이동)
    st.markdown(
        f'<a href="{sim_url}" target="_self" style="background-color: #ff4b4b; color: white; padding: 15px 25px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 18px;">연금 시뮬레이터 시작하기</a>',
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.warning("이동 후 고객님의 정보를 입력하여 시뮬레이션을 진행하세요.")
