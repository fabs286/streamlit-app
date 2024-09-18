import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Título de la aplicación
st.title('Cálculo de Concentración Basado en Absorbancia')

# Datos del calibrador (Reactivo A por defecto)
absorbancia_cal = np.array([0.1, 0.2, 0.4, 0.6, 0.8, 1.0])
concentracion_cal = np.array([10, 20, 40, 60, 80, 100])

# Crear un input numérico para ingresar el valor de absorbancia
absorbancia_input = st.number_input('Ingresa el valor de absorbancia:', min_value=0.1, max_value=3.0, step=0.01, value=0.275)

# Crear la función de interpolación
interp_func = interpolate.interp1d(absorbancia_cal, concentracion_cal, kind='linear', fill_value='extrapolate')

# Calcular la concentración correspondiente
concentracion = interp_func(absorbancia_input)

# Mostrar el resultado
st.write(f"La concentración correspondiente a la absorbancia {absorbancia_input} es: {concentracion:.2f} µIU/mL")

# Generar la gráfica
fig, ax = plt.subplots()

# Limitar los ejes según los datos
ax.set_xlim([0, max(concentracion_cal) * 1.1])
ax.set_ylim([0, max(absorbancia_cal) * 1.1])

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
