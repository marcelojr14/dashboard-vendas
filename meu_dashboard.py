import streamlit as st
import pandas as pd

st.title('Dashboard de Vendas')

@st.cache_data
def carregar_dados():
    return pd.read_csv('vendas.csv')

df = carregar_dados()

df['Data'] = pd.to_datetime(df['Data'])

st.sidebar.title('Filtros')

lista_de_categorias = df['Categoria'].unique()

categorias_selecionadas = st.sidebar.multiselect(
    'Selecione as Categorias',
    options=lista_de_categorias,
    default=lista_de_categorias
)

df_filtrado = df[df['Categoria'].isin(categorias_selecionadas)]

receita_calculada = df_filtrado['Valor'].sum()
total_pedidos = len(df_filtrado)

col1, col2 = st.columns([1, 1])

with col1:
    st.metric(
        label='Receita Total',
        value=f'R$ {receita_calculada:,.2f}'
    )

with col2:
    st.metric(
        label='Total de Pedidos',
        value=total_pedidos
    )

aba1, aba2 = st.tabs(['Evolução Mensal', 'Tabela de Dados'])

with aba1:
    dados_agrupados = (
        df_filtrado
        .set_index('Data')
        .resample('ME')['Valor']
        .sum()
    )

    st.area_chart(dados_agrupados)

with aba2:
    st.dataframe(df_filtrado)

    csv = df_filtrado.to_csv(index=False).encode('utf-8')

    st.download_button(
        label='Baixar dados filtrados em CSV',
        data=csv,
        file_name='vendas_filtradas.csv',
        mime='text/csv'
    )
