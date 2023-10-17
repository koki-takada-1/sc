import pandas as pd
import plotly.express as px
import streamlit as st


def main_page(rate,spread,img,update):
    df = pd.read_csv('usd.csv')
    # tableの参照方法参考に
    update = df['date'][len(df['date'])-1]
    with st.container():
        st.markdown(f'### 最終更新日時：{update}')
        # st.markdown('## 米ドルTTS リアルタイムレート')
        # st.markdown(f'<p style= "color:black;\
        #             font-size:40px;\
        #             border: 0.15rem solid;\
        #             writing-mode: horizontal-tb;\
        #             text-align: center;\
        #             border-radius: 10px; \
        #             "p>{rate}\
        #             </p>',unsafe_allow_html=True
        # )
        
        # st.markdown(f'## スプレッド')
        # st.markdown(f'<p style= "color:black;\
        #             font-size:40px;\
        #             border: 0.15rem solid;\
        #             writing-mode: horizontal-tb;\
        #             text-align: center;\
        #             border-radius: 10px; \
        #             "p>{spread}\
        #             </p>',unsafe_allow_html=True
        # )
    
    with st.container():
        
        fig = px.line(df,x='date',y=['tts','ttb'],title="USD 4-Moth Chart")
        st.plotly_chart(fig, use_container_width=True)
