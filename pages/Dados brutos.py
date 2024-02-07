import streamlit as st
from Dashboard import load_data
import requests
import pandas as pd
import time

@st.cache_data
def converte_csv(df):
    return df.to_csv( index=False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!', icon="✅")
    time.sleep(5)
    sucesso.empty()




st.title('DADOS BRUTOS :shopping_trolley:')

query_string = {'regiao': '', 'ano': ''}
dados = load_data(query_string)
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'], format='%d/%m/%Y')

st.sidebar.title('Filtros')

with st.sidebar:

    with st.expander('Nome do Produto'):
        produtos = st.multiselect(
            'Selecione os produtos',
            dados['Produto'].unique(),
            dados['Produto'].unique())
        st.write('You selected:', produtos)

    with st.expander('Preço do Produto'):
        preco = st.slider('Selecione o preço', 0, int(dados['Preço'].max()), (0, int(dados['Preço'].max())))

    with st.expander('Data da Compra'):
        data_compra = st.date_input('Selecione a data', (dados['Data da Compra'].min(), dados['Data da Compra'].max()))
        # st.write('You selected:', data_compra)

    with st.expander('Categoria do produto'):
        categorias = st.multiselect('Selecione as categorias', dados['Categoria do Produto'].unique(),
                                   dados['Categoria do Produto'].unique())
    
    with st.expander('Frete da venda'):
        frete = st.slider('Frete', 0, 250, (0, 250))
    
    with st.expander('Vendedor'):
        vendedores = st.multiselect('Selecione os vendedores', dados['Vendedor'].unique(), dados['Vendedor'].unique())
    
    with st.expander('Local da compra'):
        local_compra = st.multiselect('Selecione o local da compra', dados['Local da compra'].unique(),
                                      dados['Local da compra'].unique())
    
    with st.expander('Avaliação da compra'):
        avaliacao = st.slider('Selecione a avaliação da compra', 1, 5, value=(1, 5))
    
    with st.expander('Tipo de pagamento'):
        tipo_pagamento = st.multiselect('Selecione o tipo de pagamento', dados['Tipo de pagamento'].unique(),
                                        dados['Tipo de pagamento'].unique())
    
    with st.expander('Quantidade de parcelas'):
        qtd_parcelas = st.slider('Selecione a quantidade de parcelas', 1, 24, (1, 24))


with st.expander('Colunas visíveis'):
    colunas = st.multiselect(
        'Escolha as colunas a serem analisadas',
        list(dados.columns),
        list(dados.columns))
    # st.write('You selected:', options)

query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
`Categoria do Produto` in @categorias and \
@frete[0] <= Frete <= @frete[1] and \
Vendedor in @vendedores and \
`Local da compra` in @local_compra and \
@avaliacao[0] <= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@qtd_parcelas[0] <= `Quantidade de parcelas` <= @qtd_parcelas[1]
 '''
dados_filtrados = dados.query(query)
dados_filtrados = dados_filtrados[colunas]

st.dataframe(dados_filtrados)
st.markdown(f'linhas : :blue[{dados_filtrados.shape[0]}]  colunas: :blue[{dados_filtrados.shape[1]}]')

st.markdown('Escreve um nome para o arquivo')

coluna1, coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('', label_visibility='collapsed', value='dados')
    nome_arquivo += '.csv'
with coluna2:
    st.download_button('Download CSV'
                       , data= converte_csv(dados_filtrados)
                       , file_name=nome_arquivo
                       , mime='text/csv'
                       , on_click = mensagem_sucesso
                       )
