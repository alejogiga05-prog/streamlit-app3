import streamlit as st
import pandas as pd
import numpy as np

# Configuración general
st.title("🤖 Monitoreo Inteligente y Detección de Anomalías")
st.write("Simulación de sensores industriales con detección automática de anomalías y predicción de posibles fallas.")

# --- Simulación de datos ---
dias = pd.date_range("2025-01-01", periods=20)
np.random.seed(42)

data = {
    "Día": dias,
    "Temperatura (°C)": np.random.normal(30, 3, 20),
    "Humedad (%)": np.random.normal(60, 10, 20),
    "Vibración (mm/s)": np.random.normal(1.5, 0.4, 20),
    "Corriente (A)": np.random.normal(6, 1, 20),
    "Voltaje (V)": np.random.normal(230, 5, 20)
}

df = pd.DataFrame(data)

# --- Función para detectar anomalías ---
def detectar_anomalias(columna):
    media = df[columna].mean()
    std = df[columna].std()
    limite_inferior = media - 2*std
    limite_superior = media + 2*std
    return (df[columna] < limite_inferior) | (df[columna] > limite_superior)

# Marcar anomalías
for col in df.columns[1:]:
    df[f"Anómalo {col}"] = detectar_anomalias(col)

# --- Mostrar tabla de datos ---
st.subheader("📊 Datos simulados")
st.dataframe(df)

# --- Mostrar promedios ---
st.subheader("📈 Promedios generales")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Temperatura promedio", f"{df['Temperatura (°C)'].mean():.2f} °C")
col2.metric("Humedad promedio", f"{df['Humedad (%)'].mean():.2f} %")
col3.metric("Vibración promedio", f"{df['Vibración (mm/s)'].mean():.2f} mm/s")
col4.metric("Corriente promedio", f"{df['Corriente (A)'].mean():.2f} A")
col5.metric("Voltaje promedio", f"{df['Voltaje (V)'].mean():.2f} V")

# --- Mostrar gráficos simples ---
st.subheader("📉 Gráficos de sensores")
for col in df.columns[1:6]:
    st.line_chart(df.set_index("Día")[[col]])

# --- Calcular resumen de anomalías ---
st.subheader("⚠️ Resumen de anomalías detectadas")
anomalias_totales = {col: df[f"Anómalo {col}"].sum() for col in df.columns[1:6]}
anom_df = pd.DataFrame(list(anomalias_totales.items()), columns=["Variable", "N° de anomalías"])
st.table(anom_df)

# --- Diagnóstico automático ---
st.subheader("🧠 Diagnóstico predictivo")

riesgo = 0
for col, n in anomalias_totales.items():
    if n > 2:
        st.warning(f"⚠️ Alta cantidad de anomalías en **{col}** → posible riesgo futuro.")
        riesgo += 1
    elif n > 0:
        st.info(f"ℹ️ Se detectaron algunas variaciones inusuales en **{col}**.")
    else:
        st.success(f"✅ {col} sin anomalías significativas.")

# --- Predicción general ---
st.markdown("---")
if riesgo >= 3:
    st.error("🚨 Predicción: **Alta probabilidad de falla próxima.** Requiere revisión técnica.")
elif riesgo == 2:
    st.warning("⚠️ Predicción: **Posible deterioro del sistema.** Monitorear con más frecuencia.")
else:
    st.success("✅ Sistema en condiciones normales. Sin señales de falla.")

st.caption("Simulación predictiva desarrollada en Streamlit – Alejandro Giraldo")



