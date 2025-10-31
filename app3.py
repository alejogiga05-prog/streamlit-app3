import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DEL DASHBOARD ---
st.title("🤖 Monitoreo Predictivo y Descripción de Anomalías")
st.write("""
Sistema de simulación industrial que **detecta**, **describe** y **previene** fallas futuras 
a partir de datos de sensores: **temperatura, humedad, vibración, corriente y voltaje**.
""")

# --- SIMULACIÓN DE DATOS ---
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

# --- DETECCIÓN DE ANOMALÍAS ---
def detectar_anomalias(columna):
    media = df[columna].mean()
    std = df[columna].std()
    limite_inf = media - 2 * std
    limite_sup = media + 2 * std
    df[f"Anómalo {columna}"] = (df[columna] < limite_inf) | (df[columna] > limite_sup)
    return limite_inf, limite_sup

limites = {}
for col in df.columns[1:]:
    limites[col] = detectar_anomalias(col)

# --- MOSTRAR DATOS SIMULADOS ---
st.subheader("📊 Datos de Sensores Simulados")
st.dataframe(df)

# --- ESTADÍSTICAS GENERALES ---
st.subheader("📈 Promedios, Mínimos y Máximos de cada Variable")

estadisticas = []
for col in df.columns[1:6]:
    promedio = df[col].mean()
    minimo = df[col].min()
    maximo = df[col].max()
    estadisticas.append({
        "Variable": col,
        "Promedio": round(promedio, 2),
        "Mínimo": round(minimo, 2),
        "Máximo": round(maximo, 2)
    })

stats_df = pd.DataFrame(estadisticas)
st.table(stats_df)

# --- TENDENCIAS ---
st.subheader("📉 Tendencias de Sensores (últimos días)")
for col in df.columns[1:6]:
    st.line_chart(df.set_index("Día")[[col]])

# --- DESCRIPCIÓN DETALLADA DE ANOMALÍAS ---
st.subheader("⚠️ Descripción de Anomalías Detectadas")

anomaly_details = []
for col in df.columns[1:6]:
    anom_rows = df[df[f"Anómalo {col}"]]
    if not anom_rows.empty:
        limite_inf, limite_sup = limites[col]
        for _, row in anom_rows.iterrows():
            valor = row[col]
            dia = row["Día"].strftime("%Y-%m-%d")

            if valor > limite_sup:
                tipo = "por encima del rango"
                impacto = "posible sobrecarga o exceso térmico"
            else:
                tipo = "por debajo del rango"
                impacto = "posible fallo de sensor o baja eficiencia"

            anomaly_details.append({
                "Fecha": dia,
                "Variable": col,
                "Valor": round(valor, 2),
                "Rango Normal": f"{limite_inf:.2f} – {limite_sup:.2f}",
                "Descripción": f"Valor {tipo}, {impacto}."
            })

if anomaly_details:
    st.table(pd.DataFrame(anomaly_details))
else:
    st.success("✅ No se detectaron anomalías en las lecturas recientes.")

# --- DIAGNÓSTICO Y PREVENCIÓN ---
st.subheader("🧠 Diagnóstico y Prevención de Fallas")

anomalias_totales = {col: df[f"Anómalo {col}"].sum() for col in df.columns[1:6]}
riesgo = 0
recomendaciones = []

for col, n in anomalias_totales.items():
    if n > 2:
        st.warning(f"⚠️ Alta cantidad de anomalías en **{col}** → posible riesgo futuro.")
        riesgo += 1

        if "Temperatura" in col:
            recomendaciones.append("Revisar ventilación y limpieza del motor.")
        elif "Humedad" in col:
            recomendaciones.append("Verificar sellado de la cabina y control ambiental.")
        elif "Vibración" in col:
            recomendaciones.append("Inspeccionar rodamientos y alineación del motor.")
        elif "Corriente" in col:
            recomendaciones.append("Revisar cableado y consumo de cargas conectadas.")
        elif "Voltaje" in col:
            recomendaciones.append("Verificar estabilidad de alimentación eléctrica.")
    elif n > 0:
        st.info(f"ℹ️ Variaciones leves detectadas en **{col}**.")
    else:
        st.success(f"✅ {col} dentro del rango normal.")

# Estado global del sistema
st.markdown("---")
if riesgo >= 3:
    st.error("🚨 Alta probabilidad de falla próxima. Revisión técnica urgente.")
elif riesgo == 2:
    st.warning("⚠️ Posible deterioro del sistema. Revisión preventiva recomendada.")
else:
    st.success("✅ Sistema estable. Sin señales de falla inminente.")

# --- ACCIONES PREVENTIVAS ---
if recomendaciones:
    st.subheader("🛠️ Acciones Preventivas Sugeridas")
    for rec in recomendaciones:
        st.write(f"- {rec}")
else:
    st.write("💡 No se requieren acciones preventivas por el momento.")

st.caption("Desarrollado por Alejandro Giraldo — Sistema Predictivo con descripción automática de anomalías")
