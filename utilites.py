
import streamlit as st
import plotly.express as px
import pandas as pd
import folium as fl
from streamlit_folium import folium_static
import numpy as np
import plotly.graph_objects as go
from haversine import haversine


def Order_day(df1):
       # Quantidade de pedidos por dia.
        st.markdown(' # Orders by Day') 
        # linha de codigo pra extrair em tabela e agrupamento o resultado da pergunta
        cols = ['ID', 'Order_Date']
        df_aux = df1.loc[:, cols].groupby( 'Order_Date' ).count().reset_index()
        # Mudando o nome que vai aparecer no grafico
        df_aux.columns = ['Dia', 'Quantidade']
        #vizualização do resultado em grafico de barras
        fig = px.bar(df_aux, x='Dia', y='Quantidade', color='Dia') 
        return fig
    
def Traffic_order_share(df1): 
    # divisao dos pedidos por tipo de trafego
    st.header('Traffic Order Share')
    #Selecionando as colunas que vao ser analisadas
    cols1 = [ 'ID', 'Road_traffic_density']
    #Agrupando e contando cada tipo de entrega
    df_aux = df1.loc [:, cols1].groupby('Road_traffic_density').count().reset_index()
    #fazendo a divsao para achar a porcetagem de cada tipo de pedido
    calc = df_aux['ID'] / df_aux['ID'].sum()
    # Criando uma dova variavel e colocando o resultado anterior nela
    df_aux [ 'Deliveries_perc'] = calc
    # criando uma variavel para colocar a vizualizaçâo do resultado em grafico de pizza
    fig = px.pie(df_aux, values= 'Deliveries_perc', names = 'Road_traffic_density',) 
    return fig

def Traffic_order_city(df1):
    # divisao dos pedidos por tipo de cidade
    st.header('Traffic Order City')
    #Selecionando as colunas que vao ser analisadas
    cols1 = [ 'ID' , 'City' , 'Road_traffic_density']
    cols2 = ['City', 'Road_traffic_density']
    #Agrupando
    df_aux = df1.loc[:, cols1 ].groupby(cols2).count().reset_index()
    # Exibiçao em grafico de dispersâo
    fig =px.scatter(df_aux, x= 'City', y= 'Road_traffic_density', size='ID', color= 'ID', size_max= 60)
    return fig


def Order_week(df1):
    # Pedidos por final de semana
    st.header('Order by Week')
    # leitura de cada semana
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime('%U')
    # agrupamento
    cols = [ 'ID', 'Week_of_year',]
    # fazendo a contagem do agrupamento e jogando isso na coluna wee_of_year
    df_aux = df1.loc[: , cols].groupby('Week_of_year').count().reset_index()
    # varial que recebe a funçâo de vizualiçao do plotly
    fig = px.line(df_aux, x='Week_of_year', y='ID')
    return fig

def Order_share_week(df1):
    # Ordem dos pedidos por semana
    st.header('Order Share by Week')
    # Seleção de colunas para ser analisadas
    cols1 = [ 'ID', 'Week_of_year']
    cols2 = [ 'Delivery_person_ID', 'Week_of_year' , ]
    # criando variaveis para armazenar o resultado do agrupamento
    df_aux_1 = df1.loc[:,cols1].groupby('Week_of_year').count().reset_index()
    df_aux_2 = df1.loc[:,cols2].groupby('Week_of_year').nunique().reset_index()
    # calculo
    df_aux = pd.merge(df_aux_1, df_aux_2, how='inner')
    calc = df_aux[ 'ID'] / df_aux[ 'Delivery_person_ID']
    df_aux[ 'Order_by_delivery'] = calc
    # exibiçcão em grafico de linha
    fig = px.line(df_aux, x='Week_of_year', y='Order_by_delivery') 
    return fig

def Country_maps(df1):
    # Mapa das cidades
    st.header(' Country Map')
    # colunas quem tem as coordenadas
    cols1 = ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']
    cols2 = [ 'City', 'Road_traffic_density']
    # Agrupamento
    df_aux = df1.loc[:, cols1].groupby(cols2).median().reset_index()
    # funçcao que tras o mapa mundial
    map = fl.Map(control_scale = True, tiles="OpenStreetMap",)
    # loop para passar em cada coordenada
    for index, location_info in df_aux.iterrows():
        lct = [location_info['Delivery_location_latitude'], location_info['Delivery_location_longitude']]
        fl.Marker(lct).add_to(map)
    # funçâo para exibir no streamlit
    folium_static(map, width=1024, height=600)
    return None

#========================================================================
#========================================================================

def top_delivery(df1, operation):
    if operation == "max":     
        cols1 = ['Delivery_person_ID', 'City', 'Time_taken(min)']
        cols2 = ['City', 'Delivery_person_ID']
        # Calculando a maior duração de entrega agrupada por City e Delivery_person_ID
        df_mean_std_2 = df1.loc[:, cols1].groupby(cols2).max().reset_index()
        # Ordenando os resultados com base em City e Time_taken(min)
        df_mean_std_2 = df_mean_std_2.sort_values(by='City', ascending=False).sort_values(by='Time_taken(min)', ascending=False)
        # pegando so 10 primeiros de cada coluna
        df_aux01 = df_mean_std_2.loc[df_mean_std_2['City'] == 'Metropolitian', :].head(10)
        df_aux02 = df_mean_std_2.loc[df_mean_std_2['City'] == 'Urban', :].head(10)
        df_aux03 = df_mean_std_2.loc[df_mean_std_2['City'] == 'Semi-Urban', :].head(10)
        df003 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
        df003.columns = ['Cidade', 'Identificaçâo' , 'Tempo'] 
        return df003
    
    elif operation == "min":
        cols1 = ['Delivery_person_ID', 'City', 'Time_taken(min)']
        cols2 = ['City', 'Delivery_person_ID']
        # Calculando a menor duração de entrega agrupada por City e Delivery_person_ID
        df_mean_std_2 = df1.loc[:, cols1].groupby(cols2).min().reset_index()
        # Ordenando os resultados com base em City e Time_taken(min)
        df_mean_std_2 = df_mean_std_2.sort_values(by='City').sort_values(by='Time_taken(min)')
        # pegando so 10 primeiros de cada coluna
        df_aux01 = df_mean_std_2.loc[df_mean_std_2['City'] == 'Metropolitian', :].head(10)
        df_aux02 = df_mean_std_2.loc[df_mean_std_2['City'] == 'Urban', :].head(10)
        df_aux03 = df_mean_std_2.loc[df_mean_std_2['City'] == 'Semi-Urban', :].head(10)
        df003 = pd.concat([df_aux01, df_aux02, df_aux03]).reset_index(drop=True)
        df003.columns = ['Cidade', 'Identificaçâo' , 'Tempo']

        return df003

#========================================================================
#========================================================================

def Festival(df1, operation_1, operation_2 ):
    # Operation_1, é a opção se que marca se estava ocorrendo o festival ou não, as opções sao: "Yes" ou "No"
    # Operation_2, é a opçao se marca que se quer ou desvio padrao ["Std_time"] ou a media ["Avg_time"]
    
    cols=['Time_taken(min)','Festival']
    df_aux = (df1.loc[:, cols]
                .groupby( 'Festival' )
                .agg( {'Time_taken(min)' : [ 'mean', 'std']} ) )         
    df_aux.columns = ['Avg_time', 'Std_time']
    df_aux = df_aux.reset_index()
    linhas_selecionadas = df_aux['Festival'] == operation_1
    df_aux = np.round( df_aux.loc[linhas_selecionadas, operation_2], 2) 
    return df_aux

def Time_mean_city(df1):
    cols1 = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    df1['Distance'] = df1.loc[:, cols1].apply( lambda x:  haversine( ( x[cols1[0]], x[cols1[1]] ), (x[cols1[2]], x[cols1[3]]) ), axis=1)
    avg_distance = df1.loc[:,['City','Distance']].groupby( 'City').mean().reset_index()
    fig = go.Figure(data=[ go.Pie(labels= avg_distance['City'], values= avg_distance['Distance'], pull=[0.05, 0.05, 0.05], marker_colors=['#8B0000', '#ADD8E6', '#FFD700'])])  
    return fig

def Std_city_traffic(df1):
    cols=['City','Time_taken(min)', 'Road_traffic_density' ]
    df_aux = df1.loc[:, cols].groupby( ['City','Road_traffic_density'] ).agg( {'Time_taken(min)' : [ 'mean', 'std']} )       
    df_aux.columns = ['avg_time', 'std_time']      
    df_aux = df_aux.reset_index()        
    fig= px.sunburst(df_aux, path=['City', 'Road_traffic_density'], 
                            values='avg_time',color='std_time', 
                            color_continuous_scale='Solar', 
                            color_continuous_midpoint=np.average(df_aux['std_time']))
    return fig

def Time_std_mean_city_traffic(df1):
    cols = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby( 'City' ).agg( {'Time_taken(min)' : [ 'mean', 'std']} )
    df_aux.columns = ['Avg_time','Std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar( name= 'Control', x= df_aux['City'], y=df_aux['Avg_time'], error_y=dict( type='data', array=df_aux['Std_time'])))
    fig.update_layout(barmode='group')
    return fig

def Time_mean_std_city_food(df1):
    cols=['City', 'Type_of_order' , 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby( ['City','Type_of_order'] ).agg( {'Time_taken(min)' : [ 'mean', 'std']} )  
    df_aux.columns = ['avg_time', 'std_time']
    df_aux.reset_index()
    return df_aux