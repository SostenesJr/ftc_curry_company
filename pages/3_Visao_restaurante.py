#==========================================================
#===================== Libraries ==========================
#==========================================================

import pandas as pd
import plotly.express as px
from haversine import haversine
import streamlit as st
import warnings
from PIL import Image
import numpy as np
from limpeza import clean_cod
import plotly.graph_objects as go
import utilites as ul

st.set_page_config( page_title="Visão Empresa", page_icon="🚚", layout="wide")

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
st.header('Marketplace - Visão Restaurantes')
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

st.dataframe(df1)
#=====================================================
#================ Layout no Stremlit =================
#=====================================================

# Visualizaçâo do dataframe
st.dataframe(df1, use_container_width=True,)

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', '-', '-'] )

with tab1:
    with st.container():
        st.title( 'Overal Metrics')
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            
            cols = ['Delivery_person_ID']
            df_aux = df1.loc[:, cols].nunique()
            col1.metric('Entregadores Unicos', df_aux, 'quant')
            
        with col2:  
            cols1 = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
            df1['Distance'] = df1.loc[:, cols1].apply( lambda x:  haversine( ( x[cols1[0]], x[cols1[1]] ), (x[cols1[2]], x[cols1[3]]) ), axis=1)
            avg_distance = np.round( df1['Distance'].mean(), 2)
            col2.metric('Distancia Media', avg_distance, 'km')
            
        with col3:
            
            df_aux = ul.Festival(df1, "Yes", "Avg_time")
            col3.metric('Tempo Médio Festival [ON]', df_aux , 'min')
            
        with col4:
            
            df_aux = ul.Festival(df1, "Yes", "Std_time")     
            col4.metric('Desvio Padrão Festival [ON]', df_aux , 'min')
            
        with col5:

            df_aux = ul.Festival(df1, "No", "Avg_time")            
            col5.metric('Tempo Médio Festival [OFF]', df_aux , 'min')
            
        with col6:

            df_aux = ul.Festival(df1, "No", "Std_time")            
            col6.metric('Desvio Padrão Festival [OFF]', df_aux , 'min')
                      
        st.markdown("""---""")
        
    with st.container():
        st.title( 'Time Metrics')
        col1, col2 = st.columns(2)
        
        with col1:
            col1.markdown('### O tempo médio de entrega por cidade.')             
            fig = ul.Time_mean_city(df1)
            col1.plotly_chart(fig)
        
        with col2:
            col2.markdown('### O desvio padrão de entrega por cidade e tipo de trafego.')
            fig = ul.Std_city_traffic(df1)
            col2.plotly_chart(fig,use_container_width=True)
                 
        st.markdown("""---""")
          
    with st.container():
        st.title( 'Time distribution')
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                col1.markdown('### O tempo médio e o desvio padrão de entrega por cidade e tipo de tráfego')
                fig = ul.Time_std_mean_city_traffic(df1)
                col1.plotly_chart(fig)

            with col2:
                
                col2.markdown('### O tempo médio e o desvio padrão de entrega por cidade e tipo de pedido.')
                df_aux = ul.Time_mean_std_city_food(df1)
                col2.dataframe(df_aux)
                   
        st.markdown("""---""")     
