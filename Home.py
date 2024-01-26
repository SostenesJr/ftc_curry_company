import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Home",
    page_icon="🍲"
)
image = Image.open('logo.png')
st.sidebar.image(image, width =240)

st.sidebar.markdown('# Cury Company')

st.sidebar.markdown('## Fastest Delivery in Town')

st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi construido para acmponhar as metricas de crescimento dos entregadores e restaurantes.
    ### Como utilizar esses Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Metricas gerais de comportamento
        - Visão Tática: Indicadores semanais de crescimento
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregadores:
        - Acompnhamento dos indicadores semanais de crescimento
    - Visão Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes
        
    ### Ask for Help
    - Time de Data Science no Discord
        @maigaron
    """
)