import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Título de la aplicación
st.title('Concentración vs Absorbancia')

# Nuevos valores del calibrador (Reactivo de control)
absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

# Estado para los resultados de absorbancia
if 'absorbancias_input' not in st.session_state:
    st.session_state.absorbancias_input = [0.0]  # Inicializamos con un valor por defecto

# Función para agregar un nuevo campo de absorbancia
def agregar_campo():
    st.session_state.absorbancias_input.append(0.0)  # Agregar un nuevo campo con valor por defecto

# Función para eliminar un campo de absorbancia
def eliminar_campo(indice):
    st.session_state.absorbancias_input.pop(indice)  # Eliminar el campo por su índice

# Botón para agregar un nuevo resultado
st.button('Agregar nuevo resultado', on_click=agregar_campo)

# Mostrar los campos de absorbancia con un botón de eliminar al lado
for i in range(len(st.session_state.absorbancias_input)):
    col1, col2 = st.columns([4, 1])
    with col1:
        # Guardar el valor actualizado de cada campo
        st.session_state.absorbancias_input[i] = st.number_input(
            f'Absorbancia {i+1}:', min_value=0.001, max_value=10.0, step=0.001, value=st.session_state.absorbancias_input[i], format="%.3f", key=f'abs_input_{i}')
    with col2:
        if st.button('🗑️', key=f'delete_{i}', on_click=eliminar_campo, args=(i,)):
            break  # Salir del bucle si se elimina un campo para evitar problemas de indexado

# Botón para graficar los resultados
if st.button('Graficar'):
    # Crear la función de interpolación
    interp_func = interpolate.interp1d(absorbancia_cal, concentracion_cal, kind='linear', fill_value='extrapolate')

    # Calcular las concentraciones correspondientes a cada absorbancia
    concentraciones = [interp_func(absorbancia) for absorbancia in st.session_state.absorbancias_input]

    # Mostrar las concentraciones correspondientes
    st.write("### Concentraciones Calculadas")
    for i, (absorbancia, concentracion) in enumerate(zip(st.session_state.absorbancias_input, concentraciones), start=1):
        st.write(f"Absorbancia {absorbancia:.3f} = Concentración {concentracion:.2f} µIU/mL")

    # Generar la gráfica
    fig, ax = plt.subplots()

    # Limitar los ejes según los valores de entrada, dejando un margen del 20% más allá del mayor resultado
    if st.session_state.absorbancias_input:
        max_concentracion = max(concentraciones)
        max_absorbancia = max(st.session_state.absorbancias_input)
    else:
        max_concentracion = max(concentracion_cal)
        max_absorbancia = max(absorbancia_cal)

    ax.set_xlim([0, max_concentracion * 1.2])  # Dejar un margen del 20% en el eje X
    ax.set_ylim([0, max_absorbancia * 1.2])  # Dejar un margen del 20% en el eje Y

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
