import streamlit as st
import pandas as pd
import numpy as np

# Título y descripción
st.title("🤖 Monitoreo Predictivo y Prevención de Fallas")
st.write("""
Sistema inteligente de monitoreo industrial que simula lecturas de sensores, 
detecta anomalías y genera recomendaciones preventivas para evitar fallas futuras.
""")

# --- Simulación de datos de sensores ---
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

# Agregar columnas de anomalías
for col in df.columns[1:]:
    df[f"Anómalo {col}"] = detectar_anomalias(col)

# --- Mostrar datos simulados ---
st.subheader("📊 Datos de Sensores Simulados")
st.dataframe(df)

# --- Promedios ---
st.subheader("📈 Promedios Generales")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Temperatura", f"{df['Temperatura (°C)'].mean():.2f} °C")
col2.metric("Humedad", f"{df['Humedad (%)'].mean():.2f} %")
col3.metric("Vibración", f"{df['Vibración (mm/s)'].mean():.2f} mm/s")
col4.metric("Corriente", f"{df['Corriente (A)'].mean():.2f} A")
col5.metric("Voltaje", f"{df['Voltaje (V)'].mean():.2f} V")

# --- Gráficos ---
st.subheader("📉 Gráficos de Variables")
for col in df.columns[1:6]:
    st.line_chart(df.set_index("Día")[[col]])

# --- Resumen de anomalías ---
st.subheader("⚠️ Resumen de Anomalías")
anomalias_totales = {col: df[f"Anómalo {col}"].sum() for col in df.columns[1:6]}
anom_df = pd.DataFrame(list(anomalias_totales.items()), columns=["Variable", "N° de anomalías"])
st.table(anom_df)

# --- Diagnóstico y prevención ---
st.subheader("🧠 Diagnóstico Predictivo y Prevención")

riesgo = 0
recomendaciones = []

for col, n in anomalias_totales.items():
    if n > 2:
        st.warning(f"⚠️ Alta cantidad de anomalías en **{col}** → posible falla futura.")
        riesgo += 1

        # Recomendaciones preventivas según tipo de variable
        if "Temperatura" in col:
            recomendaciones.append("Revisar ventilación y limpieza del motor.")
        elif "Humedad" in col:
            recomendaciones.append("Verificar sellado de la cabina y control ambiental.")
        elif "Vibración" in col:
            recomendaciones.append("Inspeccionar rodamientos, alineación y fijaciones del motor.")
        elif "Corriente" in col:
            recomendaciones.append("Revisar cableado, aislamiento y consumo de cargas conectadas.")
        elif "Voltaje" in col:
            recomendaciones.append("Verificar estabilidad de alimentación y filtros eléctricos.")

    elif n > 0:
        st.info(f"ℹ️ Variaciones leves en **{col}**. Monitorear periódicamente.")
    else:
        st.success(f"✅ {col} dentro del rango normal.")

# --- Evaluación general ---
st.markdown("---")
if riesgo >= 3:
    st.error("🚨 Predicción: Alta probabilidad de falla próxima. Requiere revisión técnica urgente.")
elif riesgo == 2:
    st.warning("⚠️ Predicción: Posible deterioro del sistema. Revisión preventiva recomendada.")
else:
    st.success("✅ Sistema estable. No se detectan señales de falla inminente.")

# --- Recomendaciones preventivas ---
if recomendaciones:
    st.subheader("🛠️ Acciones Preventivas Sugeridas")
    for rec in recomendaciones:
        st.write(f"- {rec}")
else:
    st.write("💡 No se requieren acciones preventivas en este momento.")

st.caption("Desarrollado por Alejandro Giraldo — Sistema Predictivo de Mantenimiento en Streamlit")




