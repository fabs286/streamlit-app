import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Título de la aplicación
st.title('Concentración vs Absorbancia')

# Valores del calibrador (Reactivo de control)
absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

# Inicializar el estado de la sesión si no existe
if 'absorbancias_input' not in st.session_state:
    st.session_state.absorbancias_input = [0.001]  # Valor inicial por defecto

# Función para agregar un nuevo campo de absorbancia
def agregar_campo():
    st.session_state.absorbancias_input.append(0.001)  # Añadir nuevo campo

# Función para eliminar un campo de absorbancia
def eliminar_campo(indice):
    if len(st.session_state.absorbancias_input) > 1:
        st.session_state.absorbancias_input.pop(indice)  # Eliminar campo sin usar rerun

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

# Actualizar el estado con los nuevos valores
st.session_state.absorbancias_input = absorbancias_actualizadas

# Crear la función de interpolación
interp_func = interpolate.interp1d(absorbancia_cal, concentracion_cal, kind='linear', fill_value='extrapolate')

# Calcular las concentraciones correspondientes a cada absorbancia
concentraciones = [interp_func(absorbancia) for absorbancia in st.session_state.absorbancias_input]

# Mostrar los resultados de las concentraciones calculadas
for i, (absorbancia, concentracion) in enumerate(zip(st.session_state.absorbancias_input, concentraciones), start=1):
    st.write(f"La concentración correspondiente a la absorbancia {absorbancia:.3f} (Resultado {i}) es: {concentracion:.2f} µIU/mL")

# Generar la gráfica
fig, ax = plt.subplots()

# Limitar los ejes según los valores de entrada, dejando un margen del 20% más allá del mayor resultado
max_concentracion = max(concentraciones + [max(concentracion_cal)])
max_absorbancia = max(st.session_state.absorbancias_input + [max(absorbancia_cal)])

ax.set_xlim([0, max_concentracion * 1.2])  # Dejar un margen del 20% en el eje X
ax.set_ylim([0, max_absorbancia * 1.2])  # Dejar un margen del 20% en el eje Y

# Gráfica de la curva de calibración extendida
x_vals_extendido = np.linspace(0, max_concentracion * 1.2, 100)  # Extender la curva
y_vals_extendido = interp_func(x_vals_extendido)

ax.plot(concentracion_cal, absorbancia_cal, label='Curva de Calibración (Calibrador)', color='blue')  # Línea original
ax.plot(x_vals_extendido, y_vals_extendido, color='blue', linestyle='dashed')  # Extender línea

# Graficar cada punto de resultado
for absorbancia, concentracion in zip(st.session_state.absorbancias_input, concentraciones):
    ax.scatter(concentracion, absorbancia, color='red')
    ax.plot([concentracion, concentracion], [0, absorbancia], 'k--')
    ax.plot([0, concentracion], [absorbancia, absorbancia], 'k--')

ax.set_xlabel('Concentración (µIU/mL)')
ax.set_ylabel('Absorbancia (D.O)')
ax.legend(['Curva de Calibración (Calibrador)', 'Resultados'])
ax.grid(True)

# Mostrar la gráfica en Streamlit
st.pyplot(fig)

# Agregar el disclaimer con los valores del reactivo de control
st.write("### Controls")
st.write(f"- **Absorbancia**: {absorbancia_cal}")
st.write(f"- **Concentración**: {concentracion_cal}")
