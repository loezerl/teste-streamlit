import pandas as pd
import streamlit as st
import numpy as np
import altair as alt

st.title("[e-SUS Notifica] PCR-Positivo Sul do Brasil")
st.write("""
Esse relatório consiste em mostrar os testes positivos para covid-19 listados na API [e-SUS Notifica].
As informações contidas no relatório são:
- Quantidade de RT-PCR positivos por dia
- Quantidade de RT-PCR negativos por dia.
- Quantidade de RT-PCR positivos nas faixas etárias: [0, 4], [5, 9], [10, 14], [15, 19] [20, 29], [30, 39], [40, 49], [50, 59] [60, 69], [70, 79], [80, 999].
- Quantidade de óbitos para RT-PCR positivos.

Com base nessas informações é possível analisar graficamente quais faixas etárias estão testando positivo para o novo coronavírus.
Por enquanto, o gráfico é apenas gerado para a região Sul do país. Contendo assim, apenas os dados dos estados PR, RS e SC.
""")
st.write("Abaixo o percentual de PCR-Positivo distribuído por data e faixas etárias")

option = st.selectbox(
    'Deseja gerar o relatório para qual região?',
    ('Sul', 'Paraná', 'Santa Catarina', 'Rio Grande do Sul'))

if option == "Sul":
    st.write("Carregando dados do Sul..")
    df = pd.read_csv("Relatorio_Estados_pr-rs-sc.csv", sep=';')
    st.write("carregado!")
elif option == "Paraná":
    st.write("Carregando dados do Paraná..")
    df = pd.read_csv("Relatorio_pr.csv", sep=';')
    st.write("carregado!")
elif option == "Santa Catarina":
    st.write("Carregando dados de Santa Catarina..")
    df = pd.read_csv("Relatorio_sc.csv", sep=';')
    st.write("carregado!")
elif option == "Rio Grande do Sul":
    st.write("Carregando dados do Rio Grande do Sul..")
    df = pd.read_csv("Relatorio_rs.csv", sep=';')
    st.write("carregado!")

df.replace(np.nan, 0, inplace=True)
df['Data'] = pd.to_datetime(df['Data'], format="%Y-%m-%d")


st.write("Deseja filtrar por algum período específico?")
d3 = st.date_input("Período selecionado", [])
if len(d3) > 0:
    df = df[df['Data'] >= str(d3[0])]
    df = df[df['Data'] <= str(d3[1])]
    st.write("Início: {} | Fim: {}".format(str(d3[0]), str(d3[1])))

df = df[df['pcr-positivo'] != 0]
ignore_columns = [
    'pcr-positivo',
    'pcr-negativo',
    'Data',
    'obitos'
]
st.write(df.head())
drop_columns = []
plot_columns = []
for c in df.columns.values:
    if not(c in ignore_columns):
        df[c + "_percent"] = ((df[c]/df['pcr-positivo'])*100).round(3)
        drop_columns.append(c)
        plot_columns.append(c + "_percent")
df.drop(drop_columns, axis=1, inplace=True)

df.set_index('Data', inplace=True)
st.subheader("Gráfico")
st.area_chart(df[plot_columns])
