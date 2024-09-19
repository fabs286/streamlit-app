import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Título de la aplicación
st.title('Concentración vs Absorbancia')

# Nuevos valores del calibrador (Reactivo de control)
absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

# Crear una lista para almacenar múltiples resultados de absorbancia
absorbancias_input = []

# Función para agregar nuevos campos de absorbancia
def agregar_resultado():
    absorbancia_input = st.number_input(
        f'Ingresa el valor de absorbancia {len(absorbancias_input) + 1}:', 
        min_value=0.001, 
        max_value=10.0, 
        step=0.001, 
        value=0.275, 
        format="%.3f"
    )
    absorbancias_input.append(absorbancia_input)

# Botón para agregar más resultados
if st.button('Agregar nuevo resultado'):
    agregar_resultado()

# Botón para quitar el último resultado
if st.button('Quitar último resultado'):
    if absorbancias_input:
        absorbancias_input.pop()

# Mostrar la lista actual de absorbancias
if absorbancias_input:
    st.write(f"Resultados actuales de absorbancia: {absorbancias_input}")

# Crear la función de interpolación
interp_func = interpolate.interp1d(absorbancia_cal, concentracion_cal, kind='linear', fill_value='extrapolate')

# Calcular las concentraciones correspondientes a cada absorbancia
concentraciones = [interp_func(absorbancia) for absorbancia in absorbancias_input]

# Mostrar los resultados en la interfaz
for i, (absorbancia, concentracion) in enumerate(zip(absorbancias_input, concentraciones), start=1):
    st.write(f"Absorbancia {absorbancia:.3f} = Concentración {concentracion:.2f} µIU/mL")

# Generar la gráfica
fig, ax = plt.subplots()

# Limitar los ejes según los valores de entrada, dejando un margen del 20% más allá del mayor resultado
if absorbancias_input:
    max_concentracion = max(concentraciones)
    max_absorbancia = max(absorbancias_input)
else:
    max_concentracion = max(concentracion_cal)
    max_absorbancia = max(absorbancia_cal)

# Ensure the blue line extends to cover all input values + 20%
concentracion_extendida = np.linspace(0, max(max_concentracion, max(concentracion_cal)) * 1.2, 100)
absorbancia_extendida = interp_func(concentracion_extendida)

# Ajustar los límites de los ejes con el margen del 20%
ax.set_xlim([0, max_concentracion * 1.2])  # Dejar un margen del 20% en el eje X
ax.set_ylim([0, max_absorbancia * 1.2])    # Dejar un margen del 20% en el eje Y

# Gráfica de la curva de calibración extendida
ax.plot(concentracion_extendida, absorbancia_extendida, label='Curva de Calibración (Calibrador)', color='blue')

# Graficar cada punto de resultado
for absorbancia, concentracion in zip(absorbancias_input, concentraciones):
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
