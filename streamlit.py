import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Title of the app
st.title('Concentración vs Absorbancia')

# Calibration data
absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

# Create a smooth interpolation function
f = interp1d(absorbancia_cal, concentracion_cal, kind='cubic', fill_value='extrapolate')

# Generate more reference points (1000 points) for a smoother curve
x_vals_cal = np.linspace(min(absorbancia_cal), max(absorbancia_cal), 1000)
y_vals_cal = f(x_vals_cal)

# Initialize session state for input fields if not exists
if 'absorbancias_input' not in st.session_state:
    st.session_state.absorbancias_input = [0.001]  # Default initial value

# Function to add a new input field
def agregar_campo():
    st.session_state.absorbancias_input.append(0.001)  # Add a new field

# Function to delete an input field
def eliminar_campo(indice):
    if len(st.session_state.absorbancias_input) > 1:
        st.session_state.absorbancias_input.pop(indice)

# Button to add a new result
if st.button('Agregar nuevo resultado'):
    agregar_campo()

# Ensure we have a local copy of absorbancias_input for updating
absorbancias_actualizadas = list(st.session_state.absorbancias_input)

# Display input fields with delete button
for i, absorbancia in enumerate(absorbancias_actualizadas):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        absorbancia_input = st.number_input(
            f'Absorbancia {i+1}:', 
            min_value=0.001, 
            max_value=10.0, 
            value=absorbancia, 
            step=0.001, 
            format="%.3f", 
            key=f'abs_input_{i}'
        )
        absorbancias_actualizadas[i] = absorbancia_input  # Update the local copy

    with col2:
        if st.button('🗑️', key=f'delete_{i}'):
            eliminar_campo(i)

# Update the session state only after all inputs are handled
st.session_state.absorbancias_input = absorbancias_actualizadas

# Function to handle interpolation and extrapolation
def calculate_concentration(absorbancia_input):
    return float(f(absorbancia_input))

# Calculate the corresponding concentrations for each input absorbance
concentraciones = [calculate_concentration(absorbancia) for absorbancia in st.session_state.absorbancias_input]

# Show calculated concentrations
for i, (absorbancia, concentracion) in enumerate(zip(st.session_state.absorbancias_input, concentraciones), start=1):
    st.write(f"La concentración correspondiente a la absorbancia {absorbancia:.3f} (Resultado {i}) es: {concentracion:.2f} µIU/mL")

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Plot smooth calibration curve
ax.plot(x_vals_cal, y_vals_cal, label='Curva de Calibración', color='blue')

# Plot user results
for absorbancia, concentracion in zip(st.session_state.absorbancias_input, concentraciones):
    ax.scatter(absorbancia, concentracion, color='red')
    ax.plot([absorbancia, absorbancia], [0, concentracion], 'k--')
    ax.plot([0, absorbancia], [concentracion, concentracion], 'k--')

# Labels and legend
ax.set_ylabel('Concentración (µIU/mL)')
ax.set_xlabel('Absorbancia (D.O)')
ax.legend(['Curva de Calibración', 'Resultados'])
ax.grid(True)

# Dynamic scaling for small values and expansion for larger values
min_absorbancia = min(min(st.session_state.absorbancias_input), min(absorbancia_cal))
max_absorbancia = max(max(st.session_state.absorbancias_input), max(absorbancia_cal))
min_concentracion = min(min(concentraciones), min(concentracion_cal))
max_concentracion = max(max(concentraciones), max(concentracion_cal))

if min_absorbancia < 0.1:
    ax.set_xlim(0, max(0.1, max_absorbancia * 1.1))
else:
    ax.set_xlim(0, max_absorbancia * 1.1)

ax.set_ylim(0, max_concentracion * 1.1)

# Show plot
st.pyplot(fig)

# Display calibration control values
st.write("### Controles")
st.write(f"- **Absorbancia**: {absorbancia_cal}")
st.write(f"- **Concentración**: {concentracion_cal}")
