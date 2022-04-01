# 1º Hackathon DSBR
<img src="https://datascibr.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F1e2981f8-e996-4b65-bc32-dd43c6c13d0d%2Fhackathon1.png?table=block&id=69f5ee7f-c32d-49cb-b2b8-fa475342c579&spaceId=b0ad94d1-b13d-42e8-93ff-04ffcc74dc68&width=2000&userId=&cache=v2" style=" width: 100%" />

### Equipe CyberChase
## Relatório de Execução

**Integrantes:** Mariana Farias, Paulo Ricardo F. Neves, Vagner Rocha e Sarah Barbosa.




### Resolução das Etapas

#### ➡ Etapa 01
> Foi feito o download das ferramentas Postgres, Power Bi, Dax Studio e Tabular Editor.

#### ➡ Etapa 02 - Conexão POSTGRES-POWER BI
> Resultado final após a importação da base de dados no Power BI:
> ![image](https://user-images.githubusercontent.com/48892066/161325017-5399432c-5ed0-4485-a902-6eabb9e964ca.png)

### Etapa 03 - Criar Consultas no Dax Studio

#### DAX 1
> Listar os estados da dimensão DIM_LOJA
![image](https://user-images.githubusercontent.com/48892066/161325244-a67546d4-5d86-42f9-a4e7-0a4c91d30be3.png)

> Código Dax:
```
EVALUATE
'public dim_loja'
```

#### DAX 2
> Listar os estados sem repetição da dimensão DIM_LOJA

![image](https://user-images.githubusercontent.com/48892066/161325699-4c8d62b0-5a83-4420-a93b-e2dc6b8e178c.png)

> Código Dax:

```
EVALUATE
DISTINCT ( 'public dim_loja'[dim_loj_estado] )
```

#### DAX 3
> Listar o campus da dimensão DIM_LOJA filtrados pelo estado BA

![image](https://user-images.githubusercontent.com/48892066/161326032-936635e1-6a53-43f0-bb2b-11256550acb4.png)

> Código Dax

```
EVALUATE
FILTER(
'public dim_loja',
'public dim_loja'[dim_loj_estado] = "BA"
)
```

### ➡ Projeto Arquitetural
<img src="https://datascibr.notion.site/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fe2645143-cffb-4c6d-ba10-ab1953017e13%2FUntitled.png?table=block&id=44ed2a6e-26df-461c-9a46-1f5c4b0743a5&spaceId=b0ad94d1-b13d-42e8-93ff-04ffcc74dc68&width=2000&userId=&cache=v2"/>
