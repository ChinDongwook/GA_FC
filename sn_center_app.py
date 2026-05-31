import streamlit as st
import Pansion_Simulation_app

# 코드 최상단에 추가
st.markdown("""
    <style>
    /* 메인 폰트와 배경색을 더 고급스럽게 */
    .main { background-color: #f5f7f9; }
    h1 { color: #003366 !important; font-weight: 700 !important; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="더블유에셋 성남센터", layout="wide")

st.title("🏢 더블유에셋 성남센터")
st.markdown("---")

tab1, tab2 = st.tabs(["🏢 센터 소개", "🚀 연금 시뮬레이터"])

with tab1:
    st.header("성남센터에 오신 것을 환영합니다")
    st.write("전문적인 금융 컨설팅을 경험하세요.")

with tab2:
    st.header("프리미엄 연금 시뮬레이터")
    st.write("아래 버튼을 누르면 연금 시뮬레이터가 새 창으로 열립니다.")
    
    # URL이 확실하게 지정된 안전한 버튼 (새 창에서 열림)
    sim_url = "https://chindongwook-ga-fc-pansion-simulation-app-yr83kb.streamlit.app/"
    
    st.link_button("연금 시뮬레이터 앱 실행하기", sim_url)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("이동하신 후 시뮬레이션을 진행해 주세요.")
