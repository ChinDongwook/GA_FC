import streamlit as st

# 페이지 설정
st.set_page_config(page_title="더블유에셋 성남센터 업무포털", layout="wide", page_icon="🏢")

def main():
    st.title("🏢 더블유에셋 성남센터 업무포털")
    
    # 탭 구성
    tabs = st.tabs(["🏢 센터 소개", "🚀 연금 시뮬레이터", "📖 업무 매뉴얼", "📞 센터 연락처"])
    
    with tabs[0]:
        st.header("센터 소개")
        st.write("성남센터에 오신 것을 환영합니다.")
        
    with tabs[1]:
        st.header("연금 시뮬레이터")
        st.write("연금 시뮬레이션 기능이 여기에 구현됩니다.")
        
    with tabs[2]:
        st.header("📖 업무 매뉴얼")
        # 매뉴얼 항목을 확장 가능한 형태로 구성
        with st.expander("신규 계약 등록 방법"):
            st.write("1. 시스템 접속\n2. 고객 정보 입력...")
        with st.expander("보험금 청구 절차"):
            st.write("필요 서류 안내 및 접수처...")
            
    with tabs[3]:
        st.header("📞 센터 연락처")
        # 연락처 테이블 구성
        st.table({
            "부서/직함": ["센터장", "매니저", "지원팀"],
            "성명": ["홍길동", "김철수", "이영희"],
            "내선번호": ["101", "102", "103"]
        })

if __name__ == "__main__":
    main()
