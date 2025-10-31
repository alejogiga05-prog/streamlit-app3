iimport streamlit as st
import pandas as pd
import numpy as np

# Título principal
st.title("Monitoreo de Temperatura")

st.write("Esta aplicación muestra temperaturas simuladas durante una semana.")

# Crear datos simulados
dias = pd.date_range("2025-01-01", periods=7)
temperaturas = np.random.uniform(18, 35, size=7)

# Crear tabla
df = pd.DataFrame({
    "Día": dias,
    "Temperatura (°C)": temperaturas
})

# Mostrar tabla
st.subheader("Datos de Temperatura")
st.dataframe(df)

# Gráfico simple de Streamlit
st.subheader("Gráfico de Temperatura")
st.line_chart(df.set_index("Día"))

# Calcular promedio
promedio = df["Temperatura (°C)"].mean()
st.subheader("Promedio de Temperatura")
st.write(f"**{promedio:.2f} °C**")

# Mensaje según rango
if promedio > 30:
    st.warning("⚠️ La temperatura promedio es muy alta.")
elif promedio < 20:
    st.info("❄️ La temperatura promedio es baja.")
else:
    st.success("✅ Temperatura dentro del rango normal.")
