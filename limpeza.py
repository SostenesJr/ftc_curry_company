#==========================================================
#===================== Libraries ==========================
#==========================================================
import pandas as pd
import warnings

#Devido a uma atualizaçao do plotly fica aparecendo um erro futuro esse import warnings e essa linha de codigo e pra suprimir esse erro
warnings.simplefilter("ignore", category=FutureWarning)

#==========================================================
#=================== Limpeza do Dataset ===================
#==========================================================

def clean_cod(df1):
    """
    Esta função tem a responsabilidade de limpar o dataframe
    
    Remoçâo dos dados Nan
    Mundança do tipo da coluna de dados
    Remoçâo dos espaços das variaveis
    formataçâo da coluna
    limpeza da coluna de tempo( remoçâo do texto da variavel numerica)
    
    input: Dataframe    
    Output: Dataframe    
    """
    #resetando o index
    df1 = df1.reset_index(drop=True)

    # Limpeza da coluna Delivery_person_Age de NaN
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    # Mudando o tipo da coluna Delivery_person_Age para int
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype( int )

    # Limpeza da coluna Delivery_person_Ratings de NaN
    linhas_selecionadas = df1['Delivery_person_Ratings'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    # Mudando o tipo da coluna Delivery_person_Ratings para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype( float )

    # Limpeza da coluna multiple_deliveries de NaN
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN ' 
    df1 = df1.loc[linhas_selecionadas, :].copy()
    # Mudando o tipo da coluna multiple_deliveries para int
    df1['multiple_deliveries'] = df1['multiple_deliveries'].fillna(0).astype(int)

    # Mudando o tipo da coluna Order_Date para datetime[ns]
    df1['Order_Date'] = df1['Order_Date'].astype('datetime64[ns]')

    # Limpeza da coluna City de NaN e nan
    linhas_selecionadas = df1[ 'City'] != 'NaN '
    df1 = df1.loc[ linhas_selecionadas, :].copy()
    linhas_selecionadas = df1[ 'City'] != 'nan'
    df1 = df1.loc[ linhas_selecionadas, :].copy()
    # Mudando o tipo da coluna City para str
    df1['City'] = df1['City'].astype( str )

    # Limpeza da coluna time_Orderd de NaN
    linhas_selecionadas = df1[ 'Time_Orderd'] != 'NaN '
    df1 = df1.loc[ linhas_selecionadas, :].copy()

    # Limpeza da coluna Festival de NaN
    linhas_selecionadas = df1[ 'Festival'] != 'NaN '
    df1 = df1.loc[ linhas_selecionadas, :].copy()
    # Mudando o tipo da coluna Festival para str
    df1['Festival'] = df1['Festival'].astype( str )

    # Limpeza da coluna Road_traffic_density de NaN e nan
    linhas_selecionadas = df1[ 'Road_traffic_density'] != 'NaN '
    df1 = df1.loc[ linhas_selecionadas, :].copy()
    linhas_selecionadas = df1['Road_traffic_density'] != 'nan '
    df1 = df1.loc[ linhas_selecionadas, :].copy()
    # Mudando o tipo da coluna Road_traffic_density para str
    df1['Road_traffic_density'] = df1['Road_traffic_density'].astype( str )

    # Limpeza da coluna Type_of_order de NaN
    linhas_selecionadas = df1['Type_of_order'] != 'nan '
    df1 = df1.loc[ linhas_selecionadas, :].copy()
    # Mudando o tipo da coluna Type_of_order para str
    df1['Type_of_order'] = df1['Type_of_order'].astype( str )

    # Mudando o tipo da coluna Type_of_vehicle para str
    df1['Type_of_vehicle'] = df1['Type_of_vehicle'].astype( str )
    
    # Limpeza da coluna Time_taken(min) de NaN
    linhas_selecionadas = df1[ 'Time_taken(min)'] != 'NaN '
    df1 = df1.loc[ linhas_selecionadas, :].copy()

    #resetando o index
    df1 = df1.reset_index(drop=True)

    # tirando os espaços vazios das linhas e colunas
    for i in range(len( df1.ID)):
        df1.loc[i,'ID'] = df1.loc[ i, 'ID'].strip()
        df1.loc[i,'Delivery_person_ID'] = df1.loc[ i, 'Delivery_person_ID'].strip()
        df1.loc[i,'Type_of_order'] = df1.loc[ i, 'Type_of_order'].strip()
        df1.loc[i,'Type_of_vehicle'] = df1.loc[ i, 'Type_of_vehicle'].strip()
        df1.loc[i,'Festival'] = df1.loc[ i, 'Festival'].strip()
        df1.loc[i,'City'] = df1.loc[ i, 'City'].strip()
        df1.loc[i,'Road_traffic_density'] = df1.loc[ i, 'Road_traffic_density'].strip()

    #resetando o index
    df1 = df1.reset_index(drop=True)

    #limpeza da coluna Time_taken(min), para tirar a string e deixa o numero
    df1['Time_taken(min)'] = pd.to_numeric(df1['Time_taken(min)'].str.replace('(min)', ''), errors='coerce')

    #resetando o index
    df1 = df1.reset_index(drop=True)

    return df1