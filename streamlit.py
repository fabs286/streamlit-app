import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Title of the app
st.title('Concentración vs Absorbancia')

# Calibration data
absorbancia_cal = np.array([0.011, 0.071, 0.237, 0.474, 0.963, 2.524])
concentracion_cal = np.array([0, 5, 25, 50, 100, 300])

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
        # Properly manage session state when input changes
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
    if absorbancia_input > max(absorbancia_cal):
        # Linear extrapolation for values above the maximum calibration point
        slope = (concentracion_cal[-1] - concentracion_cal[-2]) / (absorbancia_cal[-1] - absorbancia_cal[-2])
        return slope * (absorbancia_input - absorbancia_cal[-1]) + concentracion_cal[-1]
    else:
        # Use linear interpolation for values within or below the calibration range
        return np.interp(absorbancia_input, absorbancia_cal, concentracion_cal)

# Calculate the corresponding concentrations for each input absorbance
concentraciones = [calculate_concentration(absorbancia) for absorbancia in st.session_state.absorbancias_input]

# Show calculated concentrations
for i, (absorbancia, concentracion) in enumerate(zip(st.session_state.absorbancias_input, concentraciones), start=1):
    st.write(f"La concentración correspondiente a la absorbancia {absorbancia:.3f} (Resultado {i}) es: {concentracion:.2f} µIU/mL")

# Plotting
fig, ax = plt.subplots()

# Calculate max values for axis limits
max_concentracion_input = max(concentraciones) if concentraciones else 0
max_absorbancia_input = max(st.session_state.absorbancias_input)

# Determine the extent of the calibration curve, using 20% margin only for values greater than the minimum
min_concentracion_input = min(concentraciones) if concentraciones else 0
min_absorbancia_input = min(st.session_state.absorbancias_input)

# Adjust the axis limits dynamically based on the minimum and maximum values of user input and calibration
min_concentracion_plot = min(min_concentracion_input * 0.8, concentracion_cal[0])
min_absorbancia_plot = min(min_absorbancia_input * 0.8, absorbancia_cal[0])

max_concentracion_plot = max(max_concentracion_input * 1.2, concentracion_cal[-1])
max_absorbancia_plot = max(max_absorbancia_input * 1.2, absorbancia_cal[-1])

# Set dynamic axis limits
ax.set_xlim([min_concentracion_plot, max_concentracion_plot])
ax.set_ylim([min_absorbancia_plot, max_absorbancia_plot])

# Generate calibration curve
x_vals_cal = np.linspace(min_concentracion_plot, max_concentracion_plot, 1000)
y_vals_cal = np.interp(x_vals_cal, concentracion_cal, absorbancia_cal)

# Extend the calibration curve for high values
slope = (absorbancia_cal[-1] - absorbancia_cal[-2]) / (concentracion_cal[-1] - concentracion_cal[-2])
y_vals_extended = np.where(x_vals_cal > concentracion_cal[-1], 
                           absorbancia_cal[-1] + slope * (x_vals_cal - concentracion_cal[-1]), 
                           y_vals_cal)

# Plot the calibration curve
ax.plot(x_vals_cal, y_vals_extended, label='Curva de Calibración', color='blue')

# Plot user results
for absorbancia, concentracion in zip(st.session_state.absorbancias_input, concentraciones):
    ax.scatter(concentracion, absorbancia, color='red')
    ax.plot([concentracion, concentracion], [0, absorbancia], 'k--')
    ax.plot([0, concentracion], [absorbancia, absorbancia], 'k--')

# Labels and legend
ax.set_xlabel('Concentración (µIU/mL)')
ax.set_ylabel('Absorbancia (D.O)')
ax.legend(['Curva de Calibración', 'Resultados'])
ax.grid(True)

# Show plot
st.pyplot(fig)

# Display calibration control values
st.write("### Controles")
st.write(f"- **Absorbancia**: {absorbancia_cal}")
st.write(f"- **Concentración**: {concentracion_cal}")
