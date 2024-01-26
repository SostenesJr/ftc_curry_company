# ==========================================================
# ===================== Libraries ==========================
# ==========================================================

import pandas as pd
import streamlit as st
import warnings
from PIL import Image
from limpeza import clean_cod
import utilites as ul

st.set_page_config( page_title="Visão Empresa", page_icon="📈", layout="wide")

# Devido a uma atualizaçao do plotly fica aparecendo um erro futuro esse import warnings e essa linha de codigo e pra suprimir esse erro
warnings.simplefilter("ignore", category=FutureWarning)

# import dataset
df = pd.read_csv(r"train.csv")

# fazendo limpeza do dataframe atravez de uma funçâo
df1 = clean_cod(df)

# =====================================================
# =================== barra lateral ===================
# =====================================================

# Titulo
st.header('Marketplace - Visão Cliente')
# Guardando dentro de uma variavel
image = Image.open("logo.png")
# Vizualizaçâo da imagem
st.sidebar.image(image, width=240)

# Titulo menor que vai diminuindo de acordo com #
st.sidebar.markdown('# Cury Company')
# Titulo menor
st.sidebar.markdown('## Fastest Delivery in Town')
# uma linha divisoria
st.sidebar.markdown("""---""")
# Titulo menor
st.sidebar.markdown('## Selecione uma data limite')

# Barra lateral para selecionar intervalo de datas

# Filtrar o DataFrame com base nas datas selecionadas
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.to_datetime('2022-04-13').to_pydatetime(),
    min_value=pd.to_datetime('2022-02-11').to_pydatetime(),
    max_value=pd.to_datetime('2022-04-06').to_pydatetime(),
    format='DD-MM-YYYY')

# Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# visualizaçco do Filtro de data
st.header(date_slider)
# uma linha divisoria
st.sidebar.markdown("""---""")
# Titulo menor
st.sidebar.markdown('## Selecione suas condiçôes de trânsito.')

# Filtrar o DataFrame com base no Trafego
traffic_options = st.sidebar.multiselect('Quais a condições do trânsito',
                                         ['Low', 'Medium', 'High', 'Jam'],
                                         default=['Low', 'Medium', 'High', 'Jam'])

# Filtro de Transito
l_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[l_selecionadas, :]

# uma linha divisoria
st.sidebar.markdown("""---""")
# Titulo do criador
st.sidebar.markdown('### Powered by Comunidade DS')


# =====================================================
# ================ Layout no Stremlit =================
# =====================================================

# Visualizaçâo do dataframe
st.dataframe(df1, use_container_width=True,)

# Criaçâo das abas que farma a divisao do conteudo [tabs]
tab1, tab2, tab3 = st.tabs(
    ['Visão Gerencial', 'Visão tática', 'Visão Geofráfrica'])

# chamando a variavel [tab1] cria-se uma divisao e todo conteudo vai para dentro da mesma.
with tab1:
    # container e pra deixar o assunto dentro de uma caixa
    with st.container():

        # função que chama da  libraries utilites
        fig = ul.Order_day(df1)

        # função do proprio streamlit feita para vizualização do grafico
        st.plotly_chart(fig, user_container_width=True)

    # container e pra deixar o assunto dentro de uma caixa
    with st.container():
        # Columns divide a aba em quantas parte quiser
        col1, col2 = st.columns(2)
        # a variavel col1 e a primeira divisoria dessa aba
        with col1:

            # função que chama da  libraries utilites
            fig = ul.Traffic_order_share(df1)

            # propria funçâo do streamlit para exibir o grafico
            st.plotly_chart(fig)

        # a variavel col2 e a segunda divisoria dessa aba
        with col2:

            # função que chama da  libraries utilites
            fig = ul.Traffic_order_city(df1)

            # propria funçâo do streamlit para exibir o grafico
            st.plotly_chart(fig)

# chamando a variavel [tab2] eu crio uma divisao e todo conteudo vai para dentro da mesma.
with tab2:
    # container e pra deixar o assunto dentro de uma caixa
    with st.container():
        # Columns divide a aba em quantas parte quiser
        col1, col2 = st.columns(2)
        # a variavel col1 e a primeira divisoria dessa aba
        with col1:

            # função que chama da  libraries utilites
            fig = ul.Order_week(df1)

            # propria funçâo do streamlit para exibir o grafico
            st.plotly_chart(fig, use_container_width=True)

        # a variavel col2 e a segunda divisoria dessa aba
        with col2:

            # função que chama da  libraries utilites
            fig = ul.Order_share_week(df1)

            # funçâo do streamlit de vizualizaçâo
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    # função que chama da  libraries utilites
    ul.Country_maps(df1)