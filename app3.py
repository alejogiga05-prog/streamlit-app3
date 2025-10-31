import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN ---
st.title("🤖 Monitoreo Predictivo Industrial con Métodos de Análisis")
st.write("""
Simulación de sensores industriales con **detección de anomalías**, 
**análisis predictivo** y **acciones preventivas automáticas**.
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

# --- ESTADÍSTICAS GENERALES ---
st.subheader("📈 Promedios, Mínimos y Máximos de cada Variable")
estadisticas = []
for col in df.columns[1:6]:
    estadisticas.append({
        "Variable": col,
        "Promedio": round(df[col].mean(), 2),
        "Mínimo": round(df[col].min(), 2),
        "Máximo": round(df[col].max(), 2)
    })
st.table(pd.DataFrame(estadisticas))

# --- MÉTODO PREDICTIVO ---
st.subheader("🔮 Análisis Predictivo (Promedios Móviles + Regresión Lineal)")

predicciones = []
for col in df.columns[1:6]:
    # Promedio móvil (ventana de 3 días)
    df[f"Promedio Móvil {col}"] = df[col].rolling(window=3).mean()

    # Regresión lineal simple para pronóstico
    x = np.arange(len(df))
    y = df[col].values
    coef = np.polyfit(x, y, 1)  # Ajuste lineal
    tendencia = coef[0]         # Pendiente
    proximo_valor = coef[0] * (len(df)) + coef[1]

    # Clasificar tendencia
    if tendencia > 0.2:
        tendencia_texto = "⬆️ En aumento"
    elif tendencia < -0.2:
        tendencia_texto = "⬇️ En descenso"
    else:
        tendencia_texto = "➡️ Estable"

    predicciones.append({
        "Variable": col,
        "Tendencia": tendencia_texto,
        "Predicción Próximo Día": round(proximo_valor, 2)
    })

st.table(pd.DataFrame(predicciones))

# --- MOSTRAR TENDENCIAS ---
st.subheader("📉 Gráficos de Tendencias y Suavizado")
for col in df.columns[1:6]:
    st.line_chart(df.set_index("Día")[[col, f"Promedio Móvil {col}"]])

# --- ANÁLISIS DE ANOMALÍAS ---
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
st.subheader("🧠 Diagnóstico y Acciones Preventivas")

anomalias_totales = {col: df[f"Anómalo {col}"].sum() for col in df.columns[1:6]}
riesgo = 0
recomendaciones = []

for col, n in anomalias_totales.items():
    if n > 2:
        st.warning(f"⚠️ Alta cantidad de anomalías en **{col}** → posible riesgo futuro.")
        riesgo += 1
        if "Temperatura" in col:
            recomendaciones.append("Revisar ventilación y limpiar filtros del motor.")
        elif "Humedad" in col:
            recomendaciones.append("Verificar sellado y humedad del ambiente.")
        elif "Vibración" in col:
            recomendaciones.append("Inspeccionar rodamientos y alineación del eje.")
        elif "Corriente" in col:
            recomendaciones.append("Comprobar cableado y consumo de energía.")
        elif "Voltaje" in col:
            recomendaciones.append("Revisar estabilidad de alimentación eléctrica.")
    elif n > 0:
        st.info(f"ℹ️ Variaciones leves detectadas en **{col}**.")
    else:
        st.success(f"✅ {col} dentro del rango normal.")

# --- ESTADO GLOBAL ---
st.markdown("---")
if riesgo >= 3:
    st.error("🚨 Alta probabilidad de falla próxima. Revisión técnica urgente.")
elif riesgo == 2:
    st.warning("⚠️ Posible deterioro del sistema. Revisión preventiva recomendada.")
else:
    st.success("✅ Sistema estable. Sin señales de falla inminente.")

# --- RECOMENDACIONES ---
if recomendaciones:
    st.subheader("🛠️ Acciones Preventivas Sugeridas")
    for rec in recomendaciones:
        st.write(f"- {rec}")
else:
    st.write("💡 No se requieren acciones preventivas por el momento.")

st.caption("Desarrollado por Alejandro Giraldo — Sistema Predictivo con Promedios Móviles y Regresión Lineal")

