import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Título principal ---
st.title("🌡️ Monitoreo Industrial de Temperatura")

st.write("Esta aplicación muestra datos simulados de temperatura industrial para pruebas de digitalización.")

# --- Generar datos simulados ---
dias = pd.date_range("2025-01-01", periods=7)
temperaturas = np.random.uniform(18, 35, size=7)
df = pd.DataFrame({"Fecha": dias, "Temperatura (°C)": temperaturas})

# --- Mostrar tabla de datos ---
st.subheader("📋 Datos de temperatura simulados")
st.dataframe(df, use_container_width=True)

# --- Crear gráfico con Matplotlib ---
st.subheader("📈 Gráfico de temperatura semanal")

fig, ax = plt.subplots()
ax.plot(df["Fecha"], df["Temperatura (°C)"], marker="o", linestyle="-", color="blue")
ax.set_xlabel("Fecha")
ax.set_ylabel("Temperatura (°C)")
ax.set_title("Evolución de la temperatura industrial")
plt.xticks(rotation=45)

st.pyplot(fig)

# --- Calcular promedio ---
promedio = df["Temperatura (°C)"].mean()
st.metric("Temperatura promedio", f"{promedio:.2f} °C")

# --- Evaluar condiciones ---
if promedio > 30:
    st.warning("⚠️ La temperatura promedio es alta, revise los sistemas de enfriamiento.")
elif promedio < 20:
    st.info("❄️ Temperatura baja, posible ahorro energético.")
else:
    st.success("✅ Temperatura dentro del rango normal de operación.")

# --- Pie de página ---
st.write("---")
st.caption("Aplicación desarrollada como proyecto de digitalización industrial.")
