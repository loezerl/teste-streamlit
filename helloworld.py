import pandas as pd
import streamlit as st

st.write("Kasinao!!")

df = pd.read_csv("Relatorio_Estados_pr-rs-sc.csv", sep=';', infer_datetime_format=True, date_parser=['Data'])
df.set_index('Data', inplace=True)
st.write(df[['pcr-positivo', 'pcr-negativo']])
st.write("\nGRAFICAO!!")
st.bar_chart(df[['pcr-positivo', 'pcr-negativo']])