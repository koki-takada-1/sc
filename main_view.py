
import pandas as pd
import plotly.express as px
import streamlit as st
import datetime


def main_page(df):
    with st.container():
        df['usd_id'] = pd.to_datetime(df['usd_id'])
        date = df['usd_id'][len(df['usd_id'])-1]
        st.markdown(f'### 最終更新日時：{date.year}年{date.month}月{date.day}日')
    
    with st.container():
        fig = px.line(df,x='usd_id',y=['tts','ttb'],title="USD 4-Moth Chart")
        st.plotly_chart(fig, use_container_width=True)

    