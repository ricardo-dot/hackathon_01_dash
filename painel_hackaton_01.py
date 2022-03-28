import numpy as np
import pandas as pd
from sqlalchemy import create_engine

import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

query_join = '''SELECT 
                dim_loja.dim_loj_nome, dim_loja.dim_loj_estado,              
                dim_produto.dim_pro_nome, dim_produto.dim_pro_categoria, dim_produto.dim_pro_familia,
                dim_tempo.dim_tem_dia, dim_tempo.dim_tem_mes, dim_tempo.dim_tem_ano,
                fat_vendas.fat_ven_quantidade, fat_vendas.fat_ven_faturamento
                FROM fat_vendas JOIN dim_loja
                ON fat_vendas.dim_loj_id = dim_loja.dim_loj_id
                JOIN dim_produto
                ON fat_vendas.dim_pro_id = dim_produto.dim_pro_id
                JOIN dim_tempo
                ON fat_vendas.dim_tem_id = dim_tempo.dim_tem_id
                '''
alchemyEngine = create_engine('postgresql+psycopg2://postgres:postgres@127.0.0.1:5433/test', pool_recycle=3600)
dbConnection = alchemyEngine.connect();
df = pd.read_sql(query_join, dbConnection)

loja1 = df.query('dim_loj_nome == "LOJA1" and dim_pro_categoria == "CAT1"')\
          .sort_values(by=['dim_tem_ano', 'dim_tem_mes', 'dim_tem_dia'])\
          .groupby(['dim_tem_ano', 'dim_tem_mes', 'dim_tem_dia'])\
          ['fat_ven_faturamento'].sum()
loja2 = df.query('dim_loj_nome == "LOJA2" and dim_pro_categoria == "CAT1"')\
          .sort_values(by=['dim_tem_ano', 'dim_tem_mes', 'dim_tem_dia'])\
          .groupby(['dim_tem_ano', 'dim_tem_mes', 'dim_tem_dia'])\
          ['fat_ven_faturamento'].sum()
loja3 = df.query('dim_loj_nome == "LOJA3" and dim_pro_categoria == "CAT1"')\
          .sort_values(by=['dim_tem_ano', 'dim_tem_mes', 'dim_tem_dia'])\
          .groupby(['dim_tem_ano', 'dim_tem_mes', 'dim_tem_dia'])\
          ['fat_ven_faturamento'].sum()

data_table1 = np.vstack([loja1.to_numpy(), loja2.to_numpy()])
data_table1 = np.hstack([data_table1,data_table1.sum(axis=1).reshape(2, 1)])
data_table1 = np.vstack([data_table1,data_table1.sum(axis=0)])

tb = pd.DataFrame(columns=["Nome da Loja"] + [str(i).strip('()') for i in loja1.keys()] + ["Total"])
tb = tb.append(pd.DataFrame([['Loja1'] + data_table1[0].tolist()], columns=tb.columns.to_list()), ignore_index = True)
tb = tb.append(pd.DataFrame([['Loja2'] + data_table1[1].tolist()], columns=tb.columns.to_list()), ignore_index = True)
tb = tb.append(pd.DataFrame([['Total'] + data_table1[2].tolist()], columns=tb.columns.to_list()), ignore_index = True)

fig_tabela1 = go.Figure(data=[go.Table(header=dict(values=list(tb.columns)),
                               cells=dict(values=[tb['Nome da Loja'], tb['1999, 1, 15'], tb['1999, 2, 15'], 
                               tb['2000, 1, 15'], tb['2000, 2, 15'], tb['Total']])) ])
fig_tabela1.update_layout(title_text='Faturamento BA Categoria 1', title_x=0.5)

loja1_cat1 = df.query('dim_loj_nome == "LOJA1" and dim_pro_categoria == "CAT1" and dim_loj_estado == "BA" and dim_tem_ano == 1999')['fat_ven_faturamento'].sum()
loja1_cat2 = df.query('dim_loj_nome == "LOJA1" and dim_pro_categoria == "CAT2" and dim_loj_estado == "BA" and dim_tem_ano == 1999')['fat_ven_faturamento'].sum()
loja2_cat1 = df.query('dim_loj_nome == "LOJA2" and dim_pro_categoria == "CAT1" and dim_loj_estado == "BA" and dim_tem_ano == 1999')['fat_ven_faturamento'].sum()
loja2_cat2 = df.query('dim_loj_nome == "LOJA2" and dim_pro_categoria == "CAT2" and dim_loj_estado == "BA" and dim_tem_ano == 1999')['fat_ven_faturamento'].sum()

tb2 = pd.DataFrame(columns=["Nome da Loja", "CAT1", "CAT2"])
tb2 = tb2.append(pd.DataFrame([["Loja1", loja1_cat1, loja1_cat2]], columns=tb2.columns.to_list()), ignore_index = True)
tb2 = tb2.append(pd.DataFrame([["Loja2", loja2_cat1, loja2_cat2]], columns=tb2.columns.to_list()), ignore_index = True)
tb2 = tb2.append(pd.DataFrame([["Total", loja1_cat1 + loja2_cat1, loja1_cat2 + loja2_cat2]], columns=tb2.columns.to_list()), ignore_index = True)

fig_tabela2 = go.Figure(data=[go.Table(header=dict(values=list(tb2.columns)),
                               cells=dict(values=[tb2['Nome da Loja'], 
                                                  tb2['CAT1'], tb2['CAT2']])) ])
fig_tabela2.update_layout(title_text='Faturamento Total - BA 1999', title_x=0.5)

BA_1999 = df.query('dim_loj_estado == "BA" and dim_tem_ano == 1999')['fat_ven_faturamento'].sum()
BA_2000 = df.query('dim_loj_estado == "BA" and dim_tem_ano == 2000')['fat_ven_faturamento'].sum()
PB_1999 = df.query('dim_loj_estado == "PB" and dim_tem_ano == 1999')['fat_ven_faturamento'].sum()
PB_2000 = df.query('dim_loj_estado == "PB" and dim_tem_ano == 2000')['fat_ven_faturamento'].sum()

pc_BA = 100*(BA_2000 - BA_1999) / BA_1999
pc_PB = 100*(PB_2000 - PB_1999) / PB_1999

tb3 = pd.DataFrame(columns=["Estado", "1999", "2000", "Total"])
tb3 = tb3.append(pd.DataFrame([["BA", BA_1999, BA_2000, BA_1999 + BA_2000]], columns=tb3.columns.to_list()), ignore_index = True)
tb3 = tb3.append(pd.DataFrame([["PB", PB_1999, PB_2000, PB_1999 + PB_2000]], columns=tb3.columns.to_list()), ignore_index = True)

fig_tabela3 = go.Figure(data=[go.Table(header=dict(values=list(tb3.columns)),
                               cells=dict(values=[tb3['Estado'], tb3['1999'], tb3['2000'], tb3['Total']])) ])
fig_tabela3.update_layout(title_text='Faturamento YoY%', title_x=0.5)

tb4 = pd.DataFrame(columns=["Estado", "Faturamento YoY%"])
tb4 = tb4.append(pd.DataFrame([["BA", pc_BA]], columns=tb4.columns.to_list()), ignore_index = True)
tb4 = tb4.append(pd.DataFrame([["PB", pc_PB]], columns=tb4.columns.to_list()), ignore_index = True)

fig_tabela4 = go.Figure(data=[go.Table(header=dict(values=list(tb4.columns)),
                               cells=dict(values=[tb4['Estado'], tb4['Faturamento YoY%']])) ])
fig_tabela4.update_layout(title_text='Faturamento por Estado e Ano%', title_x=0.5)

fig_plot1 = px.line(x=[str(i).strip('()') for i in loja1.keys()], y=[loja1.values, loja2.values], 
        labels={'x': 'Data', 'value': 'Faturamento'}, title="Faturamento por Mensal por Loja da Bahia para a Categoria 01")

estado_BA = df.query('dim_loj_estado == "BA"').groupby(['dim_tem_ano'])['fat_ven_faturamento'].sum()
estado_PB = df.query('dim_loj_estado == "PB"').groupby(['dim_tem_ano'])['fat_ven_faturamento'].sum()

fig_plot2 = px.line(y=[estado_BA.values, estado_PB.values], x=[str(i).strip('()') for i in estado_BA.keys()],
        labels={'x': 'Ano', 'value': 'Faturamento'}, title="Faturamento estado por Ano")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = px.data.stocks()

app.layout = html.Div(id = 'parent', children = [

    # Cabeçalho - HACKATON DSBR
    html.H1(id='Titulo', children='HACKATON DSBR', 
            style = {'textAlign':'center', 'marginTop':100,'marginBottom':50}),

    html.Div([
        html.H3(id='PASSO VII', children='PASSO VII', 
                style = {'textAlign':'center', 'marginTop':50,'marginBottom':50}, 
                className="six columns"), 
        html.H3(id='H3', children='PASSO IX', style = {'textAlign':'center', \
                'marginTop':50,'marginBottom':50}, 
                className="six columns")                                                               
    ], className="row"),

    html.Div([

        html.Div([
            dcc.Graph(figure=fig_tabela1)
        ], className="four columns"),

        html.Div([
            dcc.Graph(figure=fig_tabela2)
        ], className="two columns"),

        html.Div([
            dcc.Graph(figure=fig_tabela3)
        ], className="two columns"),

        html.Div([
            dcc.Graph(figure=fig_tabela4)
        ], className="four columns"),


    ], className="row"),

    html.Div([
        html.Div([
            dcc.Graph(figure=fig_plot1)
        ], className="six columns"),
        html.Div([
            dcc.Graph(figure=fig_plot2)
        ], className="six columns"),
    ], className="row")
    ])

if __name__ == '__main__': 
    app.run_server(debug=True, threaded=True)