import streamlit as st

# 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

# 다크/라이트 테마에 반응하는 고급 CSS 스타일링
st.markdown("""
    <style>
    /* 탭 전체 폰트 크기 및 가독성 향상 */
    .stTabs [data-baseweb="tab"] { 
        font-size: 20px !important; 
        font-weight: 600 !important;
        padding: 10px 20px !important;
    }
    
    /* 본문 글자 크기 키우기 */
    .stMarkdown, .stWrite, .stInfo { 
        font-size: 18px !important; 
    }
    
    /* 다크 테마용 가독성 유지 스타일 */
    [data-testid="stAppViewContainer"] {
        color: inherit;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏢 더블유에셋 성남센터")
st.markdown("더블유에셋 성남센터는 고객님의 성공적인 자산 관리를 위해 최선을 다합니다.")
st.markdown("---")

# 탭 구성
tab1, tab2 = st.tabs(["🏢 센터 소개", "🚀 연금 시뮬레이터"])

with tab1:
    st.header("성남센터에 오신 것을 환영합니다")
    st.write("전문적인 금융 컨설팅과 함께 안정적인 노후를 준비하세요.")
    st.info("센터에 대한 더 자세한 정보나 상담 예약은 언제든 문의해 주세요.")

with tab2:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("아래 버튼을 클릭하시면 시뮬레이션 페이지가 새 창으로 열립니다.")
    
    sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    
    # 버튼 스타일링 (다크 테마에서도 잘 보이는 색상 선택)
    st.link_button("연금 시뮬레이터 시작하기", sim_url, use_container_width=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.warning("이동 후 고객님의 정보를 입력하여 시뮬레이션을 진행하세요.")
