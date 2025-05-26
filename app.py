
import streamlit as st
import pandas as pd
import plotly.express as px
from mongo import get_dataframe
from scraper import scraper_function
import datetime
from datetime import datetime, timedelta


df = get_dataframe()

df.loc[df['forma_pagamento'] == '', 'forma_pagamento'] = 'Outros'

def by_periodo(df, periodo_start, periodo_end):
    filtered_df = df[(df['data'] >= periodo_start) & (df['data'] <= periodo_end)]
    return filtered_df

def by_produto(df, produto):
    filtered_df = df[df['produto'] == produto]
    return filtered_df

def by_forma_pagamento(df, forma_pagamento):
    filtered_df = df[df['forma_pagamento'] == forma_pagamento]
    return filtered_df


st.title("Análise de Compras")
st.write("Disciplina de Business Intelligence - Luiz Felipe, Matheus Iverson, Paulo Vitor, Pedro Paulo Carvalho e Rodrigo Santana")
#aff sidebar to add code
st.sidebar.title("Adicionar Nota")
st.sidebar.write("Adicione uma nova nota de compra")
produto = st.sidebar.text_input("Código da Nota Fiscal:", "")
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

# Filtro de produto na sidebar
st.sidebar.title("Filtrar Produtos")
produto_busca = st.sidebar.text_input("Buscar produto pelo nome (contém):")
if produto_busca:
    df = df[df['produto'].str.contains(produto_busca, case=False, na=False)]

# Certifique-se de que a coluna de data está no formato correto
df['data'] = pd.to_datetime(df['data'], errors='coerce')

# Certifique-se de que a coluna de data está no formato datetime
df['data'] = pd.to_datetime(df['data'], errors='coerce')

if df.empty:
    st.warning("Nenhum dado encontrado. Verifique a conexão com o banco de dados ou filtros aplicados.")
else:
    # Filtro de data na sidebar
    st.sidebar.title("Filtrar por Data")

    # Definir limites com base nos dados reais
    data_min = df['data'].min().date()
    data_max = df['data'].max().date()

    periodo_start = st.sidebar.date_input("Data Inicial", value=data_min, min_value=data_min, max_value=data_max)
    periodo_end = st.sidebar.date_input("Data Final", value=data_max, min_value=data_min, max_value=data_max)

    if periodo_start > periodo_end:
        st.sidebar.error("A data inicial não pode ser maior que a data final.")
    else:
        # Converter para datetime completo para o filtro funcionar corretamente
        periodo_start = pd.to_datetime(periodo_start)
        periodo_end = pd.to_datetime(periodo_end) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

        df = by_periodo(df, periodo_start, periodo_end)


if df.empty:
    st.warning("Nenhum dado encontrado. Verifique a conexão com o banco de dados.")
else:
        # Gráfico de Produtos mais comprados
    st.subheader("Produtos mais comprados")

    produtos_mais_comprados = df['produto'].value_counts().head(15).reset_index()
    produtos_mais_comprados.columns = ['Produto', 'Quantidade']

    fig = px.bar(
        produtos_mais_comprados,
        x='Quantidade',
        y='Produto',
        orientation='h',
        color='Quantidade',
        color_continuous_scale='Viridis',
        labels={'Quantidade': 'Quantidade Comprada', 'Produto': 'Produto'},
        title='Top 15 Produtos Mais Comprados'
    )

    # Ordenar y pelo total
    fig.update_layout(yaxis={'categoryorder': 'total descending'})

    # Aplicar fonte Calibri negrito nos ticks e títulos dos eixos
    fig.update_layout(
        xaxis=dict(
            tickfont=dict(
                family='Calibri',
                size=12,
                color='black'
            ),
            title_font=dict(
                family='Calibri',
                size=14,
                color='black'
            )
        ),
        yaxis=dict(
            tickfont=dict(
                family='Calibri',
                size=12,
                color='black'
            ),
            title_font=dict(
                family='Calibri',
                size=14,
                color='black'
            )
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    #Gráfico de Produtos menos comprados
    st.subheader("Produtos menos comprados")
    produtos_menos_comprados = df['produto'].value_counts().tail(15).reset_index()
    produtos_menos_comprados.columns = ['Produto', 'Quantidade']
    fig = px.bar(
        produtos_menos_comprados,
        x='Quantidade',
        y='Produto',
        orientation='h',
        color='Quantidade',
        color_continuous_scale='Viridis',
        labels={'Quantidade': 'Quantidade Comprada', 'Produto': 'Produto'},
        title='Top 15 Produtos Menos Comprados'
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})

    # Aplicar fonte Calibri negrito nos ticks e títulos dos eixos
    fig.update_layout(
        xaxis=dict(
            tickfont=dict(
                family='Calibri',
                size=12,
                color='black'
            ),
            title_font=dict(
                family='Calibri',
                size=14,
                color='black'
            )
        ),
        yaxis=dict(
            tickfont=dict(
                family='Calibri',
                size=12,
                color='black'
            ),
            title_font=dict(
                family='Calibri',
                size=14,
                color='black'
            )
        )
    )
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de Total de compras por dia/semana/mês
    st.subheader("Total de Compras por dia/semana/mês")
    periodo = st.selectbox(
        "Selecione o período:",
        ["Dia", "Mês"]
    )
    if periodo == "Dia":
        total_compras = df.groupby(df['data'].dt.to_period('D')).agg({'total_da_venda': 'sum'}).reset_index()
    elif periodo == "Mês":
        total_compras = df.groupby(df['data'].dt.to_period('M')).agg({'total_da_venda': 'sum'}).reset_index()
    # Converter Period para string para o gráfico
    total_compras['data'] = total_compras['data'].astype(str)

    # Exibir o gráfico
    st.bar_chart(total_compras.set_index('data')['total_da_venda'])

    #Gráfico de Comparativo entre formas de pagamento
    st.subheader("Comparativo entre formas de pagamento")
    formas_pagamento = df['forma_pagamento'].value_counts()
    st.bar_chart(formas_pagamento)

    st.subheader("Valor médio por compra")
    valor_medio = df['total_da_venda'].mean()
    # Exibir texto com fonte Calibri negrito via HTML
    st.markdown(
        f"<p style='font-family:Calibri; font-weight:bold; font-size:20px;'>"
        f"Valor médio por compra: R$ {valor_medio:.2f}"
        f"</p>",
        unsafe_allow_html=True
    )


    tabela_produtos = (
        df.groupby('produto')
        .size()
        .reset_index(name='Quantidade')
        .sort_values(by='Quantidade', ascending=False)
    )

    # Exibe a tabela
    st.subheader("Todos os Produtos Vendidos (Ordenados por Quantidade)")

    st.dataframe(
        tabela_produtos.style.format({'Quantidade': '{:,}'}),
        use_container_width=True
    )
