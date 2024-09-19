import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# ... (keep the existing code up to the 'Graficar' button) ...

# Botón para graficar los resultados
if st.button('Graficar'):
    # Crear la función de interpolación
    interp_func = interpolate.interp1d(absorbancia_cal, concentracion_cal, kind='linear', fill_value='extrapolate')
    
    # Calcular las concentraciones correspondientes a cada absorbancia
    concentraciones = [float(interp_func(absorbancia)) for absorbancia in st.session_state.absorbancias_input]
    
    # Mostrar las concentraciones correspondientes
    st.write("### Concentraciones Calculadas")
    for i, (absorbancia, concentracion) in enumerate(zip(st.session_state.absorbancias_input, concentraciones), start=1):
        st.write(f"Absorbancia {absorbancia:.3f} = Concentración {concentracion:.2f} µIU/mL")
    
    # Generar la gráfica
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Calcular los límites de los ejes
    max_concentracion = max(max(concentraciones), max(concentracion_cal))
    max_absorbancia = max(max(st.session_state.absorbancias_input), max(absorbancia_cal))
    
    # Añadir un 20% de margen
    x_margin = max_concentracion * 0.2
    y_margin = max_absorbancia * 0.2
    
    x_max = max_concentracion + x_margin
    y_max = max_absorbancia + y_margin
    
    # Crear puntos para la curva de calibración
    x_cal = np.linspace(0, x_max, 1000)
    y_cal = np.interp(x_cal, concentracion_cal, absorbancia_cal)
    
    # Gráfica de la curva de calibración
    ax.plot(x_cal, y_cal, label='Curva de Calibración (Calibrador)', color='blue')
    
    # Graficar cada punto de resultado
    for absorbancia, concentracion in zip(st.session_state.absorbancias_input, concentraciones):
        ax.scatter(concentracion, absorbancia, color='red')
        ax.plot([concentracion, concentracion], [0, absorbancia], 'k--')
        ax.plot([0, concentracion], [absorbancia, absorbancia], 'k--')
    
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    
    ax.set_xlabel('Concentración (µIU/mL)')
    ax.set_ylabel('Absorbancia (D.O)')
    ax.legend(['Curva de Calibración (Calibrador)', 'Resultados'])
    ax.grid(True)
    
    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)

# ... (keep the rest of the code as is) ...
