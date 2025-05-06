
import streamlit as st
import pandas as pd
from mongo import get_dataframe
from scraper import scraper_function

df = get_dataframe()
print(df.head())
def by_periodo(df, periodo_start, periodo_end):
    filtered_df = df[(df['data'] >= periodo_start) & (df['data'] <= periodo_end)]
    return filtered_df

def by_produto(df, produto):
    filtered_df = df[df['produto'] == produto]
    return filtered_df

def by_forma_pagamento(df, forma_pagamento):
    filtered_df = df[df['forma_pagamento'] == forma_pagamento]
    return filtered_df


st.title("Análise de Vendas")

#aff sidebar to add code
st.sidebar.title("Adicionar Nota")
st.sidebar.write("Adicione uma nova nota de venda")
produto = st.sidebar.text_input("chave")
if st.sidebar.button("Adicionar Nota"):
    if produto:
        produtos = scraper_function(produto)
        if produtos == None:
            st.sidebar.error("Nota já adicionada.")
        elif produtos == []:
            st.sidebar.error("Não foi possível adicionar produtos.")
        else:
            new_produtos = pd.DataFrame(produtos)
            new_produtos.rename(columns={'nome': 'produto',
                                        'data_hora':'data', 
                                        'forma_de_pagamento':'forma_pagamento'}, inplace=True)
            df = pd.concat([df, new_produtos], ignore_index=True)
            st.sidebar.success(f"Nota '{produto}' adicionada com sucesso!")
    else:
        st.sidebar.error("Por favor, insira uma chave para adicionar a nota.")

if df.empty:
    st.warning("Nenhum dado encontrado. Verifique a conexão com o banco de dados.")
else:
    #Gráfico de Produtos mais vendidos
    st.subheader("Produtos mais vendidos")
    produtos_mais_vendidos = df['produto'].value_counts()
    st.bar_chart(produtos_mais_vendidos)

    #Gráfico de Total de vendas por dia/semana/mês
    st.subheader("Total de vendas por dia/semana/mês")
    total_vendas = df.groupby(df['data'].dt.to_period('M')).agg({'total_da_venda': 'sum'}).reset_index()
    st.line_chart(total_vendas['total_da_venda'])

    #Gráfico de Comparativo entre formas de pagamento
    st.subheader("Comparativo entre formas de pagamento")
    formas_pagamento = df['forma_pagamento'].value_counts()
    st.bar_chart(formas_pagamento)

    #Gráfico de Valor médio por venda
    st.subheader("Valor médio por venda")
    valor_medio = df['total_da_venda'].mean()
    st.write(f"Valor médio por venda: R$ {valor_medio:.2f}")