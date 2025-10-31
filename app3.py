import streamlit as st
import pandas as pd
import numpy as np
import time

# Configuración general
st.set_page_config(page_title="Sistema Predictivo Industrial", layout="wide")
st.title("🤖 Sistema Predictivo Industrial 2.0")
st.write("Monitoreo en tiempo real de temperatura, humedad, vibración, corriente y voltaje.")

# Actualización automática cada 10 segundos
st_autorefresh = st.experimental_rerun
st_autorefresh_interval = 10  # segundos

# Generar datos simulados (20 lecturas)
dias = pd.date_range("2025-01-01", periods=20)
np.random.seed(int(time.time()) % 10000)  # datos diferentes en cada actualización

data = {
    "Día": dias,
    "Temperatura (°C)": np.random.normal(30, 3, 20),
    "Humedad (%)": np.random.normal(60, 10, 20),
    "Vibración (mm/s)": np.random.normal(1.5, 0.4, 20),
    "Corriente (A)": np.random.normal(6, 1, 20),
    "Voltaje (V)": np.random.normal(230, 5, 20)
}
df = pd.DataFrame(data)

# --- Detección de anomalías ---
def detectar_anomalias(col):
    media = df[col].mean()
    std = df[col].std()
    lim_inf, lim_sup = media - 2 * std, media + 2 * std
    df[f"Anómalo {col}"] = (df[col] < lim_inf) | (df[col] > lim_sup)
    return lim_inf, lim_sup

limites = {}
for col in df.columns[1:]:
    limites[col] = detectar_anomalias(col)

# --- Mostrar datos y promedios ---
st.subheader("📊 Datos de sensores")
st.dataframe(df)

st.subheader("📈 Promedios")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Temperatura", f"{df['Temperatura (°C)'].mean():.2f} °C")
col2.metric("Humedad", f"{df['Humedad (%)'].mean():.2f} %")
col3.metric("Vibración", f"{df['Vibración (mm/s)'].mean():.2f} mm/s")
col4.metric("Corriente", f"{df['Corriente (A)'].mean():.2f} A")
col5.metric("Voltaje", f"{df['Voltaje (V)'].mean():.2f} V")

# --- Semáforo global ---
anomalias_totales = {col: df[f"Anómalo {col}"].sum() for col in df.columns[1:6]}
nivel_riesgo = sum(n > 2 for n in anomalias_totales.values())

st.markdown("## 🚦 Estado del Sistema")

if nivel_riesgo >= 3:
    color, estado = "🔴", "CRÍTICO — Falla inminente detectada"
elif nivel_riesgo == 2:
    color, estado = "🟠", "PREVENTIVO — Revisar pronto el sistema"
else:
    color, estado = "🟢", "ESTABLE — Operación normal"

st.markdown(f"### {color} **{estado}**")
st.progress((nivel_riesgo / 3))

# --- Descripción de anomalías ---
st.subheader("⚠️ Descripción de anomalías")

detalles = []
for col in df.columns[1:6]:
    anoms = df[df[f"Anómalo {col}"]]
    if not anoms.empty:
        lim_inf, lim_sup = limites[col]
        for _, row in anoms.iterrows():
            valor, fecha = row[col], row["Día"].strftime("%Y-%m-%d")
            if valor > lim_sup:
                tipo = "por encima del rango"
                impacto = "posible sobrecarga o recalentamiento"
            else:
                tipo = "por debajo del rango"
                impacto = "posible falla del sensor o baja eficiencia"
            detalles.append({
                "Fecha": fecha,
                "Variable": col,
                "Valor": round(valor, 2),
                "Rango Normal": f"{lim_inf:.2f} – {lim_sup:.2f}",
                "Descripción": f"{tipo}, {impacto}."
            })







