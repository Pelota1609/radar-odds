import streamlit as st
import pandas as pd
from detector import detect_stale_odds, load_sample_data

st.set_page_config(page_title="RADAR ODDS", page_icon="📡", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
.block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1100px;}
[data-testid="stMetric"] {background: rgba(120,120,120,.08); padding: 12px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("📡 RADAR ODDS")
st.caption("Mobile Cloud · Detector experimental de cuotas desactualizadas")

with st.expander("⚙️ Filtros", expanded=False):
    threshold = st.slider("Desviación mínima (%)", 1.0, 30.0, 8.0, 0.5)
    min_books = st.slider("Casas mínimas para consenso", 2, 5, 3)

uploaded = st.file_uploader("📥 Importar cuotas CSV", type=["csv"])
try:
    raw = pd.read_csv(uploaded) if uploaded else load_sample_data()
except Exception as exc:
    st.error(f"No se pudo leer el CSV: {exc}")
    st.stop()

required = {"event_id","sport","event_name","market","selection","bookmaker","odds","observed_at"}
missing = required - set(raw.columns)
if missing:
    st.error("Faltan columnas obligatorias: " + ", ".join(sorted(missing)))
    st.stop()

alerts = detect_stale_odds(raw, threshold_pct=threshold, min_books=min_books)
source = "CSV importado" if uploaded else "Datos de demostración"
m1, m2, m3 = st.columns(3)
m1.metric("Registros", len(raw))
m2.metric("Eventos", raw["event_id"].nunique())
m3.metric("Alertas", len(alerts))

st.info(f"Fuente actual: {source}. La demostración contiene datos inventados; no son cuotas reales.")
st.subheader("🚨 Posibles anomalías")
if alerts.empty:
    st.success("No hay anomalías que superen el umbral.")
else:
    st.warning("Estas detecciones son indicios, no confirmaciones de cuotas congeladas.")
    for _, r in alerts.iterrows():
        with st.container(border=True):
            st.markdown(f"**{r['evento']}** · {r['deporte']}")
            st.write(f"{r['mercado']} · {r['seleccion']}")
            x, y = st.columns(2)
            x.metric("Cuota observada", f"{r['cuota']:.2f}")
            y.metric("Mediana comparativa", f"{r['mediana_otras_casas']:.2f}")
            st.caption(f"Casa: {r['casa']} · Diferencia: {r['diferencia_pct']:+.2f}%")
            st.caption(f"Estado: {r['estado']}")

st.subheader("📋 Datos recibidos")
with st.expander("Ver tabla completa"):
    st.dataframe(raw, use_container_width=True, hide_index=True)

st.download_button("⬇️ Descargar alertas CSV",
                   alerts.to_csv(index=False).encode("utf-8"),
                   file_name="radar_odds_alertas.csv", mime="text/csv",
                   use_container_width=True)

with st.expander("ℹ️ Qué significa una alerta"):
    st.write("El sistema compara la cuota de una casa con la mediana de otras casas para el mismo evento, mercado y selección. Una diferencia puede deberse a retrasos, márgenes, reglas distintas, límites o errores de identificación. Verifica siempre la disponibilidad y las reglas del operador.")
