import streamlit as st
import pandas as pd
import json
import os

def cargar_datos_desde_archivo(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Ocurrió un error al cargar el JSON: {e}")
        return None

def mostrar_datos_agentes(datos):
    st.title("Agentes FIFA con licencia oficial")
    if datos:
        agentes_data = {
            'Nombre': [f"{agente['firstName']} {agente['lastName']}" for agente in datos['content']],
            'Estado de licencia': [agente['licenseStatus'] for agente in datos['content']],
            'Número de licencia': [agente['licenseNumber'] for agente in datos['content']],
            'Minors autorizados': [agente['authorisedMinors'] for agente in datos['content']]
        }
        df_agentes = pd.DataFrame(agentes_data)
        filtro_nombre = st.sidebar.text_input("Buscar por Nombre")
        filtro_licencia = st.sidebar.text_input("Buscar por Número de Licencia")
        if filtro_nombre:
            df_agentes = df_agentes[df_agentes['Nombre'].str.contains(filtro_nombre, case=False)]
        if filtro_licencia:
            df_agentes = df_agentes[df_agentes['Número de licencia'].str.contains(filtro_licencia, case=False)]
        filtro_busqueda = st.sidebar.text_input("Buscar en los registros")
        if filtro_busqueda:
            df_agentes = df_agentes[df_agentes.astype(str).apply(lambda x: x.str.contains(filtro_busqueda, case=False)).any(axis=1)]
        page_number = st.number_input("Ir a la página", min_value=1, max_value=len(df_agentes)//100+1, step=1, value=1)
        start_idx = (page_number - 1) * 100
        end_idx = min(len(df_agentes), page_number * 100)
        df_display = df_agentes.iloc[start_idx:end_idx]
        st.write(df_display)

# Banner promocional
banner_style = """
    <div style="background-color: #f1c40f; padding: 10px; border-radius: 5px; margin-bottom: 20px; text-align: center;">
        <h3 style="color: black;">¡Oferta Especial!</h3>
        <p style="color: black;">Plataforma FIFA de exámenes ahora con un descuento anual de 80€</p>
        <a href="https://examenes-agente-fifa.streamlit.app/" target="_blank" style="color: #2980b9; text-decoration: none; font-weight: bold;">
            Haz clic aquí para más información
        </a>
    </div>
"""
st.markdown(banner_style, unsafe_allow_html=True)

st.sidebar.title("Navegación")
st.sidebar.subheader("Seleccione una página")

page = st.sidebar.selectbox("Páginas", ["Buscar Agentes"])

if page == "Buscar Agentes":
    file_path = os.path.join(os.path.dirname(__file__), 'config.json')
    datos = cargar_datos_desde_archivo(file_path)
    if datos:
        mostrar_datos_agentes(datos)
