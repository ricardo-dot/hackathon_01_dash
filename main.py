import pandas as pd
import streamlit as st
from lib import catesian_format, calculate_yoy
import plotly.express as px


df = pd.read_csv('data/dw_vendas.csv')

# Criando uma tabela de data
df['dim_tem_ano'] = df['dim_tem_ano'].astype(str)
df['dim_tem_mes'] = df['dim_tem_mes'].astype(str)
df['dim_tem_dia'] = df['dim_tem_dia'].astype(str)
df['date'] = pd.to_datetime(df['dim_tem_ano'] + '-' + df['dim_tem_mes'] + '-' + df['dim_tem_dia'])


# Criando a coluna mês/ano
df['dim_tem_mes_ano'] = df['date'].dt.strftime('%m/%Y')


# Tabela categoria 1 e estado Bahia
keys = ['dim_loj_nome', 'dim_pro_categoria',
        'dim_loj_estado', 'fat_ven_faturamento',
        'dim_tem_mes_ano', 'date']

df_cat1_ba = (
    df.loc[:, keys]
        .query("dim_pro_categoria == 'CAT1' & dim_loj_estado == 'BA'")
        .groupby(['dim_loj_nome', 'dim_tem_mes_ano', 'date'], as_index=False)
        .sum()
        .sort_values(by='date')
)

table_cat1_ba = catesian_format(df_cat1_ba, 'dim_tem_mes_ano')
table_cat1_ba['TOTAL'] = table_cat1_ba.sum(axis=1)
table_cat1_ba.loc[len(table_cat1_ba.index)] = table_cat1_ba.sum()
table_cat1_ba['Nome da Loja'] = ['LOJA1', 'LOJA2', 'TOTAL']
table_cat1_ba = table_cat1_ba[['Nome da Loja', '01/1999', '02/1999', '01/2000', '02/2000', 'TOTAL']]


# Tabela estado Bahia e ano 1999
keys = ['dim_loj_nome', 'dim_tem_ano',
        'dim_pro_categoria', 'dim_loj_estado',
        'fat_ven_faturamento']
df_1999_ba = (
    df.loc[:, keys]
    .query("dim_tem_ano == '1999' & dim_loj_estado == 'BA'")
    .groupby(['dim_loj_nome', 'dim_pro_categoria'], as_index=False)
    .sum()
    .sort_values(by='fat_ven_faturamento')
)

table_1999_ba = catesian_format(df_1999_ba, 'dim_pro_categoria')
table_1999_ba.loc[len(table_1999_ba.index)] = table_1999_ba.sum()
table_1999_ba['Nome da Loja'] = ['LOJA1', 'LOJA2', 'TOTAL']
table_1999_ba = table_1999_ba[['Nome da Loja', 'CAT1', 'CAT2']]

st.markdown("<h1 style='text-align: center;'>Passo VII</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

col1.table(table_cat1_ba)
col2.empty()
col3.table(table_1999_ba)

# Gráfico faturamento por mês/ano a partir da tabela categoria 1 e estado Bahia
st.plotly_chart(
px.line(data_frame=df_cat1_ba,
        x='dim_tem_mes_ano', 
        y='fat_ven_faturamento',
        color='dim_loj_nome')
)

st.markdown("<h1 style='text-align: center;'>Passo IX</h1>", unsafe_allow_html=True)


table_faturamento_estado = pd.DataFrame(
    {'Estados': ['BA', 'PB'], 
     'Faturamento yoy %': [
           calculate_yoy(df, "dim_loj_estado == 'BA'") * 100,
           calculate_yoy(df, "dim_loj_estado == 'PB'") * 100
       ]}
).round(2)

year_states = (
    df.loc[:, keys]
    .groupby(['dim_tem_ano', 'dim_loj_estado'],as_index=False)
    .sum()
)

table_year_states = catesian_format(year_states, key="dim_tem_ano")
table_year_states['TOTAL'] = table_year_states.sum(axis=1)
table_year_states['Estados'] = ['BA', 'PB']
table_year_states = table_year_states[['Estados', '1999', '2000', 'TOTAL']]

col1, col2, col3 = st.columns(3)

col1.table(table_faturamento_estado)
col2.empty()
col3.table(table_year_states)

st.plotly_chart(
px.line(data_frame=year_states, 
              x='dim_tem_ano', 
              y='fat_ven_faturamento', 
              color='dim_loj_estado')
)