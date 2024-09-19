import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Title of the app
st.title('Concentración vs Absorbancia')

# Calibration data
absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

# Input absorbance value
absorbancia_input = st.number_input('Ingrese la absorbancia (3 decimales):', min_value=0.001, max_value=10.0, step=0.001, format="%.3f")

# Function to handle interpolation and extrapolation
def calculate_concentration(absorbancia_input):
    if absorbancia_input > max(absorbancia_cal):
        # Linear extrapolation for values above the maximum calibration point
        slope = (concentracion_cal[-1] - concentracion_cal[-2]) / (absorbancia_cal[-1] - absorbancia_cal[-2])
        return slope * (absorbancia_input - absorbancia_cal[-1]) + concentracion_cal[-1]
    else:
        # Use linear interpolation for values within the calibration range
        return np.interp(absorbancia_input, absorbancia_cal, concentracion_cal)

# Calculate concentration
concentracion = calculate_concentration(absorbancia_input)
st.write(f'La concentración correspondiente a la absorbancia {absorbancia_input:.3f} es: {concentracion:.2f} µIU/mL')

# Plotting
fig, ax = plt.subplots()

# Generate more points for a smoother blue curve
x_vals_cal = np.linspace(0, max(concentracion_cal) * 1.2, 500)
y_vals_cal = np.interp(x_vals_cal, concentracion_cal, absorbancia_cal)

# Set axis limits to adjust dynamically, starting small and growing as needed
x_max = max(concentracion * 1.2, 10)
y_max = max(absorbancia_input * 1.2, 1.0)

ax.set_xlim([0, x_max])
ax.set_ylim([0, y_max])

# Plot the calibration curve
ax.plot(x_vals_cal, y_vals_cal, label='Curva de Calibración', color='blue')

# Plot the result as a red point
ax.scatter(concentracion, absorbancia_input, color='red')
ax.plot([concentracion, concentracion], [0, absorbancia_input], 'k--')
ax.plot([0, concentracion], [absorbancia_input, absorbancia_input], 'k--')

# Labels and legend
ax.set_xlabel('Concentración (µIU/mL)')
ax.set_ylabel('Absorbancia (D.O)')
ax.legend(['Curva de Calibración', 'Resultado'])
ax.grid(True)

# Show plot
st.pyplot(fig)

# Display calibration control values
st.write("### Controles")
st.write(f"- **Absorbancia**: {absorbancia_cal}")
st.write(f"- **Concentración**: {concentracion_cal}")
