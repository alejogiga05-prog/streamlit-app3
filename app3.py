import streamlit as st
import pandas as pd
import numpy as np

# --- Configuración general ---
st.title("🏭 Monitoreo Industrial de Sensores - Simulación")

st.write("""
Este tablero muestra datos simulados de diferentes sensores industriales: 
temperatura, humedad, vibración, aceleración, corriente, voltaje, velocidad y producción.
""")

# --- Generar datos simulados ---
dias = pd.date_range("2025-01-01", periods=10)

# Simulación de variables (valores coherentes)
temperatura = np.random.uniform(18, 40, size=10)
humedad = np.random.uniform(30, 95, size=10)
vibracion = np.random.uniform(0.2, 3.0, size=10)
aceleracion = np.random.uniform(0.5, 4.0, size=10)
corriente = np.random.uniform(2, 10, size=10)
voltaje = np.random.uniform(210, 240, size=10)
rpm = np.random.uniform(800, 1800, size=10)
produccion = np.random.uniform(100, 500, size=10)

# Crear DataFrame
df = pd.DataFrame({
    "Día": dias,
    "Temperatura (°C)": temperatura,
    "Humedad (%)": humedad,
    "Vibración (mm/s)": vibracion,
    "Aceleración (m/s²)": aceleracion,
    "Corriente (A)": corriente,
    "Voltaje (V)": voltaje,
    "Velocidad (RPM)": rpm,
    "Producción (unid/h)": produccion
})

# --- Mostrar tabla de datos ---
st.subheader("📋 Datos simulados de sensores")
st.dataframe(df, use_container_width=True)

# --- Gráficos individuales ---
st.subheader("📈 Gráficos de variables industriales")

st.line_chart(df.set_index("Día")[["Temperatura (°C)"]])
st.line_chart(df.set_index("Día")[["Humedad (%)"]])
st.line_chart(df.set_index("Día")[["Vibración (mm/s)"]])
st.line_chart(df.set_index("Día")[["Aceleración (m/s²)"]])
st.line_chart(df.set_index("Día")[["Corriente (A)"]])
st.line_chart(df.set_index("Día")[["Voltaje (V)"]])
st.line_chart(df.set_index("Día")[["Velocidad (RPM)"]])
st.line_chart(df.set_index("Día")[["Producción (unid/h)"]])

# --- Promedios ---
st.subheader("📊 Promedios de la semana")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Temp. promedio", f"{df['Temperatura (°C)'].mean():.2f} °C")
col2.metric("Humedad promedio", f"{df['Humedad (%)'].mean():.2f} %")
col3.metric("Vibración promedio", f"{df['Vibración (mm/s)'].mean():.2f}")
col4.metric("Aceleración promedio", f"{df['Aceleración (m/s²)'].mean():.2f}")

col5, col6, col7, col8 = st.columns(4)
col5.metric("Corriente promedio", f"{df['Corriente (A)'].mean():.2f} A")
col6.metric("Voltaje promedio", f"{df['Voltaje (V)'].mean():.2f} V")
col7.metric("Velocidad promedio", f"{df['Velocidad (RPM)'].mean():.0f} RPM")
col8.metric("Producción promedio", f"{df['Producción (unid/h)'].mean():.0f} unid/h")

# --- Evaluación automática simple ---
st.subheader("🧠 Diagnóstico automático")

if df["Vibración (mm/s)"].mean() > 2.0:
    st.warning("🚨 Nivel de vibración elevado: posible desbalanceo o daño en el motor.")
else:
    st.success("✅ Vibración dentro del rango normal.")

if df["Temperatura (°C)"].mean() > 35:
    st.warning("🌡️ Temperatura excesiva: revisar sistema de enfriamiento.")
else:
    st.success("✅ Temperatura estable.")

if df["Corriente (A)"].mean() > 8:
    st.warning("⚡ Corriente alta: posible sobrecarga en el motor.")
else:
    st.success("✅ Corriente dentro de valores normales.")

if df["Producción (unid/h)"].mean() < 200:
    st.warning("📉 Producción baja: posible ralentización o falla en el proceso.")
else:
    st.success("✅ Producción dentro del rango esperado.")

# --- Pie ---
st.write("---")
st.caption("Simulación de monitoreo industrial desarrollada en Streamlit (by Alejandro Giraldo)")


