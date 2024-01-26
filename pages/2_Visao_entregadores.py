#==========================================================
#===================== Libraries ==========================
#==========================================================

import pandas as pd
import plotly.express as px
from haversine import haversine
import streamlit as st
import warnings
from PIL import Image
from limpeza import clean_cod
import utilites as ul

st.set_page_config( page_title="Visão Empresa", page_icon="🍽️", layout="wide")


#Devido a uma atualizaçao do plotly fica aparecendo um erro futuro esse import warnings e essa linha de codigo e pra suprimir esse erro
warnings.simplefilter("ignore", category=FutureWarning)

# import dataset
df = pd.read_csv(r"train.csv")
# fazendo limpeza do dataframe atravez de uma funçâo
df1 = clean_cod(df)


#=====================================================
#=================== barra lateral ===================
#=====================================================

# Titulo
st.header('Marketplace - Visão Entregadores')
# Guardando dentro de uma variavel
image = Image.open("logo.png")
# Vizualizaçâo da imagem
st.sidebar.image(image, width = 240)

# Titulo menor que vai diminuindo de acordo com #
st.sidebar.markdown('# Cury Company')
# Titulo menor
st.sidebar.markdown('## Fastest Delivery in Town')
# uma linha divisoria
st.sidebar.markdown("""---""")
# Titulo menor
st.sidebar.markdown( '## Selecione uma data limite' )

# Barra lateral para selecionar intervalo de datas

# Filtrar o DataFrame com base nas datas selecionadas
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value=pd.to_datetime('2022-04-13').to_pydatetime(),
    min_value=pd.to_datetime('2022-02-11').to_pydatetime(),
    max_value=pd.to_datetime('2022-04-06').to_pydatetime(),
    format='DD-MM-YYYY')

#Filtro de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas,:]

# visualizaçco do Filtro de data
st.header(date_slider)
# uma linha divisoria
st.sidebar.markdown("""---""")
# Titulo menor
st.sidebar.markdown( '## Selecione suas condiçôes de trânsito.' )

# Filtrar o DataFrame com base no Trafego
traffic_options = st.sidebar.multiselect('Quais a condições do trânsito', 
                     ['Low', 'Medium', 'High', 'Jam'],
                     default=['Low', 'Medium', 'High', 'Jam'])

# Filtro de Transito
l_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[l_selecionadas,:]
# uma linha divisoria
st.sidebar.markdown("""---""")
# Titulo do criador
st.sidebar.markdown('### Powered by Comunidade DS')

#=====================================================
#================ Layout no Stremlit =================
#=====================================================

# Visualizaçâo do dataframe
st.dataframe(df1, use_container_width=True,)

# Criaçâo das abas que farma a divisao do conteudo [tabs]
tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '-', '-'] )

with tab1:
    with st.container():
        st.title(' Overall Metrics')
        col1, col2, col3, col4 = st.columns( 4, gap= 'large')
        with col1:
            # A Maior idade entregadores
            df_aux = df1.loc[:, ['Delivery_person_Age']].max()
            col1.metric('Maior de idade', df_aux)

        with col2:
            # Menor idade entregadores
            df_aux = df1.loc[:, ['Delivery_person_Age']].min()
            col2.metric('Menor de idade', df_aux)

        with col3:
            # Melhor condição de veículos.
            df_aux = df1.loc[:, ['Vehicle_condition']].max()
            col3.metric('Melhor condiçâo do veiculos',df_aux)

        with col4:
            # Pior condição de veículos.
            df_aux = df1.loc[:, ['Vehicle_condition']].min()
            col4.metric('Pior condiçâo do veiculos',df_aux)
            
with st.container():
    st.markdown("""---""")
    st.title(  ' Avaliaçôes')

    col1, col2 = st.columns( 2 )
    with col1:
        st.write('<h4> Avaliaçâo media por entregador </h4>', unsafe_allow_html=True)
        
        cols1 = ['Delivery_person_ID','Delivery_person_Ratings']
        df_aux = df1.loc[:, cols1].groupby('Delivery_person_ID').mean().reset_index()
        df_aux.columns = ['Identificaçâo', 'Media']
        
        st.dataframe(df_aux)
    
    with col2:
        st.write('<h4> Avaliaçâo media por Trafego </h4>', unsafe_allow_html=True)
        
        cols1 = [ 'Road_traffic_density', 'Delivery_person_Ratings']
        df_mean = df1.loc[:,cols1].groupby('Road_traffic_density').mean().reset_index()
        df_mean.columns = [ 'Trafego' , 'Media']
        st.dataframe(df_mean)
        st.write('<h4> Avaliaçâo media por clima </h4>', unsafe_allow_html=True)
        cols1 = [ 'Delivery_person_Ratings', 'Weatherconditions']
        df_mean = df1.loc[:,cols1].groupby('Weatherconditions').mean().reset_index()
        df_mean.columns = [ 'Clima' , 'Media']
        
        st.dataframe(df_mean)

with st.container():
    st. markdown("""---""")
    st.title('Velocidade de entrega')

    col1, col2 = st.columns (2)
    with col1:
        st.write('<h4> Top entregadores mais rapidos </h4>', unsafe_allow_html=True)
        df003 = ul.top_delivery(df1,"min")
        st.dataframe(df003)
    with col2:
        st.write('<h4> Top entregadores mais lentos </h4>', unsafe_allow_html=True)
        df003 =ul.top_delivery(df1,"max")
        st.dataframe(df003)