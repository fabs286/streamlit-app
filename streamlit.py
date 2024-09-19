import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Add this at the beginning of your script
st.set_option('deprecation.showPyplotGlobalUse', False)

# Wrap the main content in a try-except block
try:
    # Título de la aplicación
    st.title('Concentración vs Absorbancia')

    # Nuevos valores del calibrador (Reactivo de control)
    absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
    concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

    # Inicializar el estado de la sesión si no existe
    if 'absorbancias_input' not in st.session_state:
        st.session_state.absorbancias_input = [0.001]

    # Función para agregar un nuevo campo de absorbancia
    def agregar_campo():
        st.session_state.absorbancias_input.append(0.001)

    # Función para eliminar un campo de absorbancia
    def eliminar_campo(indice):
        if len(st.session_state.absorbancias_input) > 1:
            st.session_state.absorbancias_input.pop(indice)

    # Botón para agregar un nuevo resultado
    if st.button('Agregar nuevo resultado'):
        agregar_campo()

    # Mostrar los campos de absorbancia con un botón de eliminar al lado
    absorbancias_actualizadas = []
    for i, absorbancia in enumerate(st.session_state.absorbancias_input):
        col1, col2 = st.columns([4, 1])
        with col1:
            nueva_absorbancia = st.number_input(
                f'Absorbancia {i+1}:', 
                min_value=0.001, 
                max_value=10.0, 
                value=float(absorbancia),
                step=0.001, 
                format="%.3f", 
                key=f'abs_input_{i}'
            )
            absorbancias_actualizadas.append(nueva_absorbancia)
        with col2:
            if st.button('🗑️', key=f'delete_{i}'):
                eliminar_campo(i)
                st.experimental_rerun()

    # Actualizar el estado con los nuevos valores
    st.session_state.absorbancias_input = absorbancias_actualizadas

    # ... (rest of your code)

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.exception(e)
