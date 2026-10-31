# RADAR ODDS 2.0 — móvil + nube

Esta versión ofrece una interfaz web adaptada a móvil y preparada para desplegarse
en Streamlit Community Cloud. El panel se puede abrir desde el navegador del móvil.

## Qué necesitas
- Una cuenta GitHub.
- Una cuenta Streamlit Community Cloud.
- Este ZIP descomprimido en tu ordenador (para subir los archivos a GitHub).
- No necesitas introducir contraseñas de casas de apuestas.

## Publicación en la nube
1. Descomprime este ZIP.
2. Entra en GitHub y crea un repositorio nuevo, por ejemplo `radar-odds`.
3. Sube todos los archivos y carpetas de esta versión al repositorio.
4. Entra en https://share.streamlit.io/ e inicia sesión con GitHub.
5. Pulsa **Create app** y selecciona tu repositorio.
6. En **Main file path**, escribe `app.py`.
7. Pulsa **Deploy**.
8. Cuando termine, abre la URL que te proporcione Streamlit desde tu móvil.
9. En el navegador del móvil, usa “Añadir a pantalla de inicio” si quieres un acceso directo.

## Qué funciona ahora
- Panel web responsive para móvil.
- Importación manual de cuotas mediante CSV.
- Comparación de cuotas y detección preliminar de desviaciones.
- Descarga de alertas CSV.
- Datos ficticios de ejemplo para probar el panel.

## Qué NO funciona todavía
- No hay conexión automática con casas ni con un proveedor de cuotas.
- No hay vigilancia 24/7 ni alertas Telegram en esta versión.
- Los datos de demostración no son reales.
- No se debe considerar una alerta como una oportunidad confirmada.

## Formato de importación
Columnas obligatorias:
`event_id,sport,event_name,market,selection,bookmaker,odds,observed_at`

Usa timestamps ISO-8601, preferiblemente UTC. Los nombres de mercado y selección
deben estar normalizados para comparar resultados equivalentes.

## Siguiente etapa técnica
Añadir un proveedor que autorice el uso de sus datos y cubra operadores españoles,
persistencia externa (por ejemplo, PostgreSQL gestionado) y un recolector programado.
El plan gratuito de un hosting no garantiza procesos permanentes ni ejecución exacta
cada pocos segundos. Antes de prometer monitorización continua, hay que validar
límites, cobertura, licencia y frecuencia de actualización del proveedor.

No se realizan apuestas automáticas, no se accede a cuentas de operadores y no se
intenta eludir controles o restricciones de sus plataformas.
