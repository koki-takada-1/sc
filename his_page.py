import streamlit as st

def history_page_display(csv,html,year,month,day):
    
    st.markdown(f'### {year}年{month}月{day}日の為替相場')
    st.download_button(
        label="CSVダウンロード",
        data=csv,
        file_name='table.csv',
        mime='text/csv',
        key="download-tools-csv"
    )
    if st.button('ホームに戻る ダブルクリック',key='back-home'):
        st.session_state.home_page = 'visible'
        
        
    st.markdown(html,unsafe_allow_html=True)

    
    