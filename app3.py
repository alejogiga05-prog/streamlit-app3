import streamlit as st
import pandas as pd
import numpy as np

# Título principal
st.title("🌡️ Monitoreo de Temperatura y Humedad")

st.write("Aplicación sencilla para visualizar datos simulados de temperatura y humedad durante una semana.")

# Crear datos simulados
dias = pd.date_range("2025-01-01", periods=7)
temperaturas = np.random.uniform(18, 35, size=7)
humedad = np.random.uniform(40, 90, size=7)

# Crear DataFrame
df = pd.DataFrame({
    "Día": dias,
    "Temperatura (°C)": temperaturas,
    "Humedad (%)": humedad
})

# Mostrar tabla
st.subheader("📋 Datos simulados")
st.dataframe(df)

# Gráfico de temperatura
st.subheader("🌡️ Gráfico de Temperatura")
st.line_chart(df.set_index("Día")["Temperatura (°C)"])

# Gráfico de humedad
st.subheader("💧 Gráfico de Humedad")
st.line_chart(df.set_index("Día")["Humedad (%)"])

# Calcular promedios
prom_temp = df["Temperatura (°C)"].mean()
prom_hum = df["Humedad (%)"].mean()

st.subheader("📊 Promedios semanales")
col1, col2 = st.columns(2)
col1.metric("Temperatura promedio", f"{prom_temp:.2f} °C")
col2.metric("Humedad promedio", f"{prom_hum:.2f} %")

# Mensajes según condiciones
if prom_temp > 30:
    st.warning("⚠️ Temperatura alta: revise sistemas de enfriamiento.")
elif prom_temp < 20:
    st.info("❄️ Temperatura baja: posible ahorro energético.")
else:
    st.success("✅ Temperatura dentro del rango normal.")

if prom_hum > 80:
    st.warning("💦 Humedad muy alta: riesgo de condensación.")
elif prom_hum < 40:
    st.info("🌵 Humedad baja: revise sistemas de ventilación.")
else:
    st.success("✅ Humedad dentro del rango recomendado.")

