import pandas as pd
import streamlit as st
import numpy as np
import altair as alt

FAIXA_ETARIA = {
    "0 a 4 anos": [False, 'pcr-positivo-0a4'],
    "5 a 9 anos": [False, 'pcr-positivo-5a9'],
    "10 a 14 anos": [False, 'pcr-positivo-10a14'],
    "15 a 19 anos": [False, 'pcr-positivo-15a19'],
    "20 a 29 anos": [False, 'pcr-positivo-20a29'],
    "30 a 39 anos": [False, 'pcr-positivo-30a39'],
    "40 a 49 anos": [False, 'pcr-positivo-40a49'],
    "50 a 59 anos": [False, 'pcr-positivo-50a59'],
    "60 a 69 anos": [False, 'pcr-positivo-60a69'],
    "70 a 79 anos": [False, 'pcr-positivo-70a79'],
    "Maior que 80 anos": [False, 'pcr-positivo-80a999']
}

st.title("[e-SUS Notifica] PCR-Positivo Sul do Brasil")
st.write("""
Esse relatório consiste em mostrar os testes positivos para covid-19 listados na API [e-SUS Notifica].
As informações contidas no relatório são:
- Quantidade de RT-PCR positivos por dia
- Quantidade de RT-PCR negativos por dia.
- Quantidade de RT-PCR positivos nas faixas etárias: [0, 4], [5, 9], [10, 14], [15, 19], 
[20, 29], [30, 39], [40, 49], [50, 59] [60, 69], [70, 79], [80, 999].
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
    st.write("carregado!\n")
elif option == "Paraná":
    st.write("Carregando dados do Paraná..")
    df = pd.read_csv("Relatorio_pr.csv", sep=';')
    st.write("carregado!\n")
elif option == "Santa Catarina":
    st.write("Carregando dados de Santa Catarina..")
    df = pd.read_csv("Relatorio_sc.csv", sep=';')
    st.write("carregado!\n")
elif option == "Rio Grande do Sul":
    st.write("Carregando dados do Rio Grande do Sul..")
    df = pd.read_csv("Relatorio_rs.csv", sep=';')
    st.write("carregado!\n")

df.replace(np.nan, 0, inplace=True)
df['Data'] = pd.to_datetime(df['Data'], format="%Y-%m-%d")

st.subheader("Deseja filtrar por algum período específico?")
d3 = st.date_input("Período selecionado", [])
if len(d3) > 0:
    df = df[df['Data'] >= str(d3[0])]
    df = df[df['Data'] <= str(d3[1])]
    st.write("Início: {} | Fim: {}".format(str(d3[0]), str(d3[1])))

st.subheader("Deseja filtrar por alguma faixa etária?")
for k in FAIXA_ETARIA:
    FAIXA_ETARIA[k][0] = st.checkbox(k)

filtro_idades = []
for k in FAIXA_ETARIA:
    if FAIXA_ETARIA[k][0]:
        filtro_idades.append(FAIXA_ETARIA[k][1])

df['pcr'] = df['pcr-positivo'] + df['pcr-negativo']
df = df[df['pcr-positivo'] != 0]
ignore_columns = [
    'Data',
    'pcr-positivo',
    'pcr-negativo',
    'pcr',
    'obitos'
]
df = df[ignore_columns + filtro_idades]
st.write(df.head())
drop_columns = []
plot_columns = []
## Percentual de positividade por faixa etária
for c in df.columns.values:
    if not(c in ignore_columns):
        df[c + "_percent"] = ((df[c]/df['pcr-positivo'])*100).round(3)
        drop_columns.append(c)
        plot_columns.append(c + "_percent")
## Percentual de positividade por teste realizado
df["positividade"] = ((df['pcr-positivo'] / df['pcr']) * 100).round(3)
df.set_index('Data', inplace=True)
st.subheader("Gráfico de positivos (%) por faixa etária")
st.area_chart(df[plot_columns])

st.subheader("Gráfico de positividade (%)")
st.line_chart(df['positividade'])
