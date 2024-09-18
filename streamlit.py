import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Título de la aplicación
st.title('Cálculo de Concentración Basado en Absorbancia')

# Nuevos valores del calibrador (Reactivo de control)
absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

# Crear un input numérico para ingresar el valor de absorbancia con 3 decimales
absorbancia_input = st.number_input('Ingresa el valor de absorbancia:', min_value=0.001, max_value=3.0, step=0.001, value=0.275, format="%.3f")

# Crear la función de interpolación
interp_func = interpolate.interp1d(absorbancia_cal, concentracion_cal, kind='linear', fill_value='extrapolate')

# Calcular la concentración correspondiente
concentracion = interp_func(absorbancia_input)

# Mostrar el resultado
st.write(f"La concentración correspondiente a la absorbancia {absorbancia_input:.3f} es: {concentracion:.2f} µIU/mL")

# Generar la gráfica
fig, ax = plt.subplots()

# Limitar los ejes según los valores de entrada
ax.set_xlim([0, concentracion * 1.1])  # Ajusta el eje X según la concentración calculada
ax.set_ylim([0, absorbancia_input * 1.1])  # Ajusta el eje Y según la absorbancia ingresada

# Gráfica de la curva de calibración
ax.plot(concentracion_cal, absorbancia_cal, label='Curva de Calibración (Calibrador)', color='blue')

# Punto del resultado ingresado
ax.scatter(concentracion, absorbancia_input, color='red', label='Resultado')
ax.plot([concentracion, concentracion], [0, absorbancia_input], 'k--')
ax.plot([0, concentracion], [absorbancia_input, absorbancia_input], 'k--')

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
