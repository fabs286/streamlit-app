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

    # Crear la función de interpolación
    interp_func = interpolate.interp1d(absorbancia_cal, concentracion_cal, kind='linear', fill_value='extrapolate')

    # Calcular las concentraciones correspondientes a cada absorbancia
    concentraciones = [interp_func(absorbancia) for absorbancia in st.session_state.absorbancias_input]

    # Mostrar los resultados en la interfaz
    for i, (absorbancia, concentracion) in enumerate(zip(st.session_state.absorbancias_input, concentraciones), start=1):
        st.write(f"La concentración correspondiente a la absorbancia {absorbancia:.3f} (Resultado {i}) es: {concentracion:.2f} µIU/mL")

    # Generate extrapolated calibration points to extend the blue line
    max_absorbancia_input = max(absorbancias_actualizadas)
    if max_absorbancia_input > absorbancia_cal[-1]:
        # Extend the calibration curve beyond the last known point
        # Using the slope between the last two points
        slope = (concentracion_cal[-1] - concentracion_cal[-2]) / (absorbancia_cal[-1] - absorbancia_cal[-2])
        new_absorbancias = np.linspace(absorbancia_cal[-1], max_absorbancia_input, num=50)
        new_concentraciones = concentracion_cal[-1] + slope * (new_absorbancias - absorbancia_cal[-1])

        absorbancia_cal = np.concatenate((absorbancia_cal, new_absorbancias[1:]))
        concentracion_cal = np.concatenate((concentracion_cal, new_concentraciones[1:]))

    # Generar la gráfica
    fig, ax = plt.subplots()

    # Limitar los ejes según los valores de entrada, dejando un margen del 20% más allá del mayor resultado
    max_concentracion = max(max(concentraciones), max(concentracion_cal))
    max_absorbancia = max(max(absorbancias_actualizadas), max(absorbancia_cal))

    ax.set_xlim([0, max_concentracion * 1.2])
    ax.set_ylim([0, max_absorbancia * 1.2])

    # Gráfica de la curva de calibración
    ax.plot(concentracion_cal, absorbancia_cal, label='Curva de Calibración (Calibrador)', color='blue')

    # Graficar cada punto de resultado
    for absorbancia, concentracion in zip(st.session_state.absorbancias_input, concentraciones):
        ax.scatter(concentracion, absorbancia, color='red', label='Resultado')
        ax.plot([concentracion, concentracion], [0, absorbancia], 'k--')
        ax.plot([0, concentracion], [absorbancia, absorbancia], 'k--')

    ax.set_xlabel('Concentración (µIU/mL)')
    ax.set_ylabel('Absorbancia (D.O)')
    ax.legend()
    ax.grid(True)

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

    # Agregar el disclaimer con los valores del reactivo de control
    st.write("### Controls")
    st.write(f"- **Absorbancia**: {absorbancia_cal}")
    st.write(f"- **Concentración**: {concentracion_cal}")

except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.exception(e)
