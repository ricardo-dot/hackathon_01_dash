import pandas as pd
import seaborn as sns
import streamlit as st
from lib import catesian_format

df = pd.read_csv('dw_vendas.csv')

df['dim_tem_ano'] = df['dim_tem_ano'].astype(str)
df['dim_tem_mes'] = df['dim_tem_mes'].astype(str)
df['dim_tem_dia'] = df['dim_tem_dia'].astype(str)
df['date'] = pd.to_datetime(df['dim_tem_ano'] + '-' + df['dim_tem_mes'] + '-' + df['dim_tem_dia'])
df['dim_tem_mes_ano'] = df['date'].dt.strftime('%m/%Y')

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
table_cat1_ba.head()
st.table(table_cat1_ba)

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
st.table(table_1999_ba)


sns.lineplot(data=df_cat1_ba,
             x='dim_tem_mes_ano',
             y='fat_ven_faturamento',
             hue='dim_loj_nome',
             palette='mako')

st.line_chart(data=df_cat1_ba)