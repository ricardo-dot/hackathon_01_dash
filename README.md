# 1º Hackathon DSBR

<img src="https://datascibr.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F1e2981f8-e996-4b65-bc32-dd43c6c13d0d%2Fhackathon1.png?table=block&id=69f5ee7f-c32d-49cb-b2b8-fa475342c579&spaceId=b0ad94d1-b13d-42e8-93ff-04ffcc74dc68&width=2000&userId=&cache=v2" style=" width: 100%" />

# Relatório de Execução
## Equipe CyberChase
**Integrantes:** Mariana Farias, Paulo Ricardo F. Neves, Vagner Rocha e Sarah Barbosa.

### ➡ Regras
- Cada equipe só poderá ter no máximo três componentes
- A cada etapa concluída a equipe deverá notificar os facilitadores  (gestores da dinâmica)
- Os facilitadores poderão solicitar reuniões a qualquer momento para que as equipes apresentem a sua etapa atual
- Não existe uma concorrência entre equipes
- As orientações do 1ª Hackthon estão disponíveis nesta página, mas caso tenham alguma dúvida os facilitadores podem ser consultados

### ➡ Desafio
O desafio será criar o DW de Vendas clássico de Kimball no formato Star Schema no Postges e
importá-lo para o Power BI. Posteriormente serão resolvidos um conjunto de consultas na linguagem Data Analysis Expressions (DAX). No final do desafio, essas consultas serão apresentas em um painel no Power BI que deverá considerar a comunicação visual e a experiência do usuário.

### ➡ Projeto Arquitetural
<img src="https://datascibr.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fe2645143-cffb-4c6d-ba10-ab1953017e13%2FUntitled.png?table=block&id=44ed2a6e-26df-461c-9a46-1f5c4b0743a5&spaceId=b0ad94d1-b13d-42e8-93ff-04ffcc74dc68&width=2000&userId=&cache=v2"/>

### ➡ Resolução das Etapas

#### Etapa 01 - Download das ferramentas
Orientação:
> Instalar o Postgres, Instalar o Power BI Desktop, Instalar o Dax Studio, Instalar o Tabular Editor.

Resolução:
Foram feitas as instalações das ferramentas Postgres, Power Bi, Dax Studio e Tabular Editor.

#### Etapa 02 - Conexão POSTGRES-POWER BI
Orientação:
> Criar o Banco de Dados DW_VENDAS no Postgres e executar o script e consumir o modelo no Power BI.
> Use a opção de import do modelo no Power BI

Resolução:

Resultado final após a importação da base de dados no Power BI:

![image](https://user-images.githubusercontent.com/48892066/161325017-5399432c-5ed0-4485-a902-6eabb9e964ca.png)

### Etapa 03 - Criar Consultas no Dax Studio

Orientações:
> DAX 1: Listar os estados da dimensão DIM_LOJA
> 
> DAX 2: Listar os estados sem repetição da dimensão DIM_LOJA
> 
> DAX 3: Listar o campus da dimensão DIM_LOJA filtrados pelo estado BA
> 
> DAX 4: Calcular o faturamento total da tabela de fatos FAT_VENDAS

Resolução:

![image](https://user-images.githubusercontent.com/48892066/161325244-a67546d4-5d86-42f9-a4e7-0a4c91d30be3.png)

Código Dax:
```
EVALUATE
'public dim_loja'
```

![image](https://user-images.githubusercontent.com/48892066/161325699-4c8d62b0-5a83-4420-a93b-e2dc6b8e178c.png)

Código Dax:

```
EVALUATE
DISTINCT ( 'public dim_loja'[dim_loj_estado] )
```


![image](https://user-images.githubusercontent.com/48892066/161326032-936635e1-6a53-43f0-bb2b-11256550acb4.png)

Código Dax:

```
EVALUATE
FILTER(
'public dim_loja',
'public dim_loja'[dim_loj_estado] = "BA"
)
```

![image](https://user-images.githubusercontent.com/48892066/161326269-f31a5f84-ff1e-45c3-8374-33fc7b7f9bcb.png)

Código Dax:

```
EVALUATE ROW(
	"Total vendas", SUM('public fat_vendas'[fat_ven_faturamento])
) 
```

### Etapa 04 - Criar uma nova coluna de tempo (mês/ano) no Power BI

Orientações:

> No Power BI criar uma nova coluna na tabela de dimensão DIM_TEMPO DIM_TEM_MES_ANO_PW

Resolução:

No Power Query foi adicionada uma coluna personalizada a partir do seguinte código:

```
= Text.From([dim_tem_mes]) & "/" & Text.From([dim_tem_ano])
```
Resultado final no Power BI:

![image](https://user-images.githubusercontent.com/48892066/161332812-bbb98fa0-919c-4bee-8b0b-7788a6efb53b.png)


### Etapa 05 - Encontrar faturamento no Dax Studio I

> DAX 5: Criar a consulta DAX para retornar o total do faturamento das vendas referentes a Categoria=“CAT1” (DIM_PRODUTO) e do Estado=“BA” (DIM_LOJA)

Resolução:

![image](https://user-images.githubusercontent.com/48892066/161333597-22a36bac-3d45-4b98-b599-9ad63f2a38ff.png)

Código Dax:

```
EVALUATE
SUMMARIZECOLUMNS (
	'public dim_tempo'[dim_tem_mes_ano_pw],
	'public dim_loja'[dim_loj_nome],
	FILTER('public dim_loja', 'public dim_loja'[dim_loj_estado] = "BA"),
	FILTER('public dim_produto', 'public dim_produto'[dim_pro_categoria]= "CAT1"),
    "Total Sales", SUM ( 'public fat_vendas'[fat_ven_faturamento] )
)
```

### Etapa 06 - Encontrar faturamento no Dax Studio II

Orientações:

> Criar a consulta DAX para retornar o total do faturamento das vendas referente ao ano de 1999 do estado “BA”. Usar a função TREATAS para filtrar o estado “BA”

Resolução:

![image](https://user-images.githubusercontent.com/48892066/161326772-a3ee905b-ed53-4823-ac87-e4fcf308ba9a.png)

Código dax:

```
EVALUATE
SUMMARIZECOLUMNS(
	'public dim_loja'[dim_loj_nome],
	'public dim_produto'[dim_pro_categoria],
	TREATAS({1999}, 'public dim_tempo'[dim_tem_ano]),
	TREATAS({"BA"}, 'public dim_loja'[dim_loj_estado]), 
	"Total Faturamento", SUM('public fat_vendas'[fat_ven_faturamento])
)
```

### Etapa 07 - Criar o Painel I no Power BI

![passoVII.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/2a5296be-e62e-4dbc-8d4f-1f4d74b6bb68/passoVII.png)

### Etapa 08 - Criar nova coluna no Power BI

Orientações: 
> Criar no Power BI uma  nova coluna do tipo data na tabela dimensão DIM_TEMPO – DIM_TEM_DIA_MES_ANO_PW

Resolução:

Foi utilizado o recurso de coluna calculada com a seguinte formula Dax:

```
dim_dia_mes_ano_pw = FORMAT(DATE('public dim_tempo'[dim_tem_ano], 'public dim_tempo'[dim_tem_mes], 'public dim_tempo'[dim_tem_dia]), "dddd, dd \de mmmm \de yyyy")
```
Resultado final no Power BI: 
![image](https://user-images.githubusercontent.com/48892066/161334034-aedf4e80-d99f-4bdc-acfe-5cefb1182e8d.png)


### Etapa 09 - Criar a Painel I com novos elementos no Power BI

Orientação:
> Criar uma medida para apresentar o crescimento percentual do faturamento dos estados “BA” e “PB” entre os anos 1999 e 2000.
> 
> Apresentar as tabelas com o componentes no Power BI (painel 1)

Resolução: 

![image](https://user-images.githubusercontent.com/48892066/161332008-37526b52-568a-4289-987c-68cd995ceed0.png)

Código Dax:
```
DEFINE
	MEASURE 'medidas_percentual_faturamento'[total_faturamento] = 
		SUM('public fat_vendas'[fat_ven_faturamento])

	MEASURE 'medidas_percentual_faturamento'[periodo_faturamento] = 
		CALCULATE([total_faturamento], SAMEPERIODLASTYEAR('public dim_tempo'[date]))

	MEASURE  'medidas_percentual_faturamento'[Yoy_faturamento] = 
		DIVIDE([total_faturamento]-[periodo_faturamento], [periodo_faturamento])-1
	EVALUATE{ [Yoy_faturamento] }
```

Resultado Final no Power BI

![image](https://user-images.githubusercontent.com/48892066/161332601-8d4331da-2bcf-4b74-8b73-b57d85edd56b.png)
