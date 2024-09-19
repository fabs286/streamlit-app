import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

# Title of the app
st.title('Concentración vs Absorbancia')

# Calibration data
absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

# Initialize session state for input fields
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

# Display input fields with delete button
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

# Update session state with the new input values
st.session_state.absorbancias_input = absorbancias_actualizadas

# Linear interpolation within the calibration range
interp_func = interpolate.interp1d(absorbancia_cal, concentracion_cal, kind='linear', bounds_error=False, fill_value="extrapolate")

# Function to handle extrapolation manually beyond the calibration range
def manual_extrapolation(absorbancia_input):
    if absorbancia_input > max(absorbancia_cal):
        # Calculate the slope from the last two calibration points
        slope = (concentracion_cal[-1] - concentracion_cal[-2]) / (absorbancia_cal[-1] - absorbancia_cal[-2])
        # Extrapolate concentration based on this slope
        extra_concentration = slope * (absorbancia_input - absorbancia_cal[-1]) + concentracion_cal[-1]
        return extra_concentration
    elif absorbancia_input < min(absorbancia_cal):
        # Extrapolate for values below the minimum calibration point
        slope = (concentracion_cal[1] - concentracion_cal[0]) / (absorbancia_cal[1] - absorbancia_cal[0])
        extra_concentration = slope * (absorbancia_input - absorbancia_cal[0]) + concentracion_cal[0]
        return extra_concentration
    else:
        # Use interpolation for values within the calibration range
        return interp_func(absorbancia_input)

# Calculate the corresponding concentrations for each input absorbance using interpolation or extrapolation
concentraciones = [manual_extrapolation(absorbancia) for absorbancia in st.session_state.absorbancias_input]

# Show calculated concentrations
for i, (absorbancia, concentracion) in enumerate(zip(st.session_state.absorbancias_input, concentraciones), start=1):
    st.write(f"La concentración correspondiente a la absorbancia {absorbancia:.3f} (Resultado {i}) es: {concentracion:.2f} µIU/mL")

# Plotting
fig, ax = plt.subplots()

# Set dynamic axis limits with 20% margin beyond max input values
max_concentracion = max(concentraciones + [max(concentracion_cal)])
max_absorbancia = max(st.session_state.absorbancias_input + [max(absorbancia_cal)])

ax.set_xlim([0, max_concentracion * 1.2])
ax.set_ylim([0, max_absorbancia * 1.2])

# Plot the original calibration curve
ax.plot(concentracion_cal, absorbancia_cal, label='Curva de Calibración (Original)', color='blue')

# Generate extended calibration curve based on manual extrapolation
x_vals_extendido = np.linspace(0, max_concentracion * 1.2, 100)
y_vals_extendido = [manual_extrapolation(x) for x in x_vals_extendido]

# Plot the extended calibration curve
ax.plot(x_vals_extendido, y_vals_extendido, color='blue', linestyle='dashed')

# Plot user results
for absorbancia, concentracion in zip(st.session_state.absorbancias_input, concentraciones):
    ax.scatter(concentracion, absorbancia, color='red')
    ax.plot([concentracion, concentracion], [0, absorbancia], 'k--')
    ax.plot([0, concentracion], [absorbancia, absorbancia], 'k--')

# Labels and legend
ax.set_xlabel('Concentración (µIU/mL)')
ax.set_ylabel('Absorbancia (D.O)')
ax.legend(['Curva de Calibración (Original)', 'Curva Extendida', 'Resultados'])
ax.grid(True)

# Show plot
st.pyplot(fig)

# Display calibration control values
st.write("### Controles")
st.write(f"- **Absorbancia**: {absorbancia_cal}")
st.write(f"- **Concentración**: {concentracion_cal}")
