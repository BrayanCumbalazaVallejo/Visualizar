import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

st.set_page_config(page_title="Mapa de Ciudades y Estudiantes", layout="wide")

st.title("📍 Mapa interactivo: Ciudades y Estudiantes")

# ======================
# DATOS DEL MAPA
# ======================
data = [
    {"CODIGOCIUDAD": 5, "NOMBRECIUDAD": "Barranquilla", "ESTUDIANTES": 188},
    {"CODIGOCIUDAD": 1, "NOMBRECIUDAD": "Bogotá", "ESTUDIANTES": 148},
    {"CODIGOCIUDAD": 2, "NOMBRECIUDAD": "Medellín", "ESTUDIANTES": 138},
    {"CODIGOCIUDAD": 14, "NOMBRECIUDAD": "Villavicencio", "ESTUDIANTES": 69},
    {"CODIGOCIUDAD": 7, "NOMBRECIUDAD": "Santa Marta", "ESTUDIANTES": 68},
    {"CODIGOCIUDAD": 6, "NOMBRECIUDAD": "Manizales", "ESTUDIANTES": 67},
    {"CODIGOCIUDAD": 12, "NOMBRECIUDAD": "Pasto", "ESTUDIANTES": 67},
    {"CODIGOCIUDAD": 4, "NOMBRECIUDAD": "Cartagena", "ESTUDIANTES": 65},
    {"CODIGOCIUDAD": 15, "NOMBRECIUDAD": "Rioacha", "ESTUDIANTES": 65},
    {"CODIGOCIUDAD": 10, "NOMBRECIUDAD": "Popayán", "ESTUDIANTES": 64},
    {"CODIGOCIUDAD": 8, "NOMBRECIUDAD": "Pereira", "ESTUDIANTES": 61},
    {"CODIGOCIUDAD": 3, "NOMBRECIUDAD": "Cali", "ESTUDIANTES": 0},
    {"CODIGOCIUDAD": 9, "NOMBRECIUDAD": "Neiva", "ESTUDIANTES": 0},
    {"CODIGOCIUDAD": 11, "NOMBRECIUDAD": "Armenia", "ESTUDIANTES": 0},
    {"CODIGOCIUDAD": 13, "NOMBRECIUDAD": "Valledupar", "ESTUDIANTES": 0},
]

df = pd.DataFrame(data)
df["NOMBRECIUDAD"] = df["NOMBRECIUDAD"].replace({"Rioacha": "Riohacha"})

# Coordenadas aproximadas
coords = {
    "Barranquilla": (10.9685, -74.7813),
    "Bogotá": (4.7110, -74.0721),
    "Medellín": (6.2442, -75.5812),
    "Villavicencio": (4.1420, -73.6266),
    "Santa Marta": (11.2408, -74.1990),
    "Manizales": (5.0703, -75.5138),
    "Pasto": (1.2136, -77.2811),
    "Cartagena": (10.3910, -75.4794),
    "Riohacha": (11.5444, -72.9070),
    "Popayán": (2.4448, -76.6147),
    "Pereira": (4.8133, -75.6961),
    "Cali": (3.4516, -76.5320),
    "Neiva": (2.9386, -75.2819),
    "Armenia": (4.5339, -75.6811),
    "Valledupar": (10.4631, -73.2532),
}

df["lat"] = df["NOMBRECIUDAD"].map(lambda x: coords.get(x, (None, None))[0])
df["lon"] = df["NOMBRECIUDAD"].map(lambda x: coords.get(x, (None, None))[1])

# Filtros del mapa
with st.sidebar:
    st.header("Filtros")
    min_est = int(df["ESTUDIANTES"].min())
    max_est = int(df["ESTUDIANTES"].max())
    rango = st.slider("Estudiantes (mín - máx)", min_value=min_est, max_value=max_est,
                      value=(min_est, max_est), step=1)
    ocultar_ceros = st.checkbox("Ocultar ciudades con 0 estudiantes", value=False)

fdf = df[(df["ESTUDIANTES"] >= rango[0]) & (df["ESTUDIANTES"] <= rango[1])]
if ocultar_ceros:
    fdf = fdf[fdf["ESTUDIANTES"] > 0]

# Escalas visuales del mapa
base_radius = 5000
scale_radius = 200
fdf = fdf.copy()
fdf["radius"] = base_radius + fdf["ESTUDIANTES"] * scale_radius

min_v = fdf["ESTUDIANTES"].min() if not fdf.empty else 0
max_v = fdf["ESTUDIANTES"].max() if not fdf.empty else 1
def to_color(v, vmin=min_v, vmax=max_v):
    if vmax == vmin:
        return [200, 120, 120, 180]
    t = (v - vmin) / (vmax - vmin)
    r = int(80 + t * (255 - 80))
    g = int(120 + (1 - t) * 60)
    b = int(120 + (1 - t) * 60)
    return [r, g, b, 180]

fdf["color"] = fdf["ESTUDIANTES"].apply(to_color)

# Vista inicial del mapa
center_lat = fdf["lat"].mean() if not fdf.empty else df["lat"].mean()
center_lon = fdf["lon"].mean() if not fdf.empty else df["lon"].mean()
initial_view = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=5.2, pitch=30)

layer = pdk.Layer(
    "ScatterplotLayer",
    data=fdf.dropna(subset=["lat", "lon"]),
    get_position='[lon, lat]',
    get_radius="radius",
    get_fill_color="color",
    pickable=True,
    stroked=True,
    get_line_color=[0, 0, 0],
    line_width_min_pixels=1,
    radius_min_pixels=3,
)

tooltip = {
    "html": "<b>{NOMBRECIUDAD}</b><br/>Estudiantes: {ESTUDIANTES}<br/>Código: {CODIGOCIUDAD}",
    "style": {"backgroundColor": "white", "color": "black"}
}

# Mostrar mapa
st.pydeck_chart(
    pdk.Deck(
        map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
        initial_view_state=initial_view,
        layers=[layer],
        tooltip=tooltip,
    ),
    use_container_width=True,
)

st.caption("💡 Consejo: usa el panel de la izquierda para filtrar por número de estudiantes o ocultar los ceros.")

# ======================
# SELECCIÓN DE CIUDAD Y GRÁFICAS
# ======================
# Aquí se simula el "clic" en el mapa con un selector
with st.sidebar:
    ciudad_sel = st.selectbox("Selecciona una ciudad para ver sus gráficas:", fdf["NOMBRECIUDAD"].unique())

# Aquí deberías tener tu dataframe real de estudiantes
# df_Estudiante = pd.read_csv("...")  # ejemplo
# Para el ejemplo pongo un dataset simulado:
df_Estudiante = pd.DataFrame({
    "NOMBRECIUDAD": ["Bogotá", "Bogotá", "Bogotá", "Medellín", "Medellín", "Pasto", "Pasto"],
    "CARRERA": ["Ingeniería", "Medicina", "Derecho", "Ingeniería", "Derecho", "Medicina", "Derecho"],
    "MESES_TRANSCURRIDOS": [24, 30, 18, 20, 25, 28, 22]
})

if ciudad_sel:
    st.subheader(f"📊 Gráficas para {ciudad_sel}")

    # Cantidad de estudiantes por carrera en la ciudad
    estudiantes_por_carrera = df_Estudiante[df_Estudiante['NOMBRECIUDAD'] == ciudad_sel] \
        .groupby('CARRERA').size().reset_index(name='CANTIDAD_ESTUDIANTES') \
        .sort_values('CANTIDAD_ESTUDIANTES', ascending=True)

    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=estudiantes_por_carrera, x='CANTIDAD_ESTUDIANTES', y='CARRERA',
                palette='Blues', edgecolor='black', ax=ax1)
    ax1.set_title(f"Cantidad de estudiantes por carrera en {ciudad_sel}", fontweight='bold')
    for i, v in enumerate(estudiantes_por_carrera['CANTIDAD_ESTUDIANTES']):
        ax1.text(v + 0.3, i, str(v), va='center', fontweight='bold')
    st.pyplot(fig1)

    # Promedio de meses transcurridos por carrera en la ciudad
    promedio_ciudad = df_Estudiante[df_Estudiante['NOMBRECIUDAD'] == ciudad_sel] \
        .groupby('CARRERA')['MESES_TRANSCURRIDOS'].mean().reset_index() \
        .sort_values('MESES_TRANSCURRIDOS', ascending=True)

    fig2, ax2 = plt.subplots(figsize=(8, 5))
    sns.barplot(data=promedio_ciudad, x='MESES_TRANSCURRIDOS', y='CARRERA',
                palette='Blues_r', edgecolor='black', ax=ax2)
    ax2.set_title(f"Promedio de meses transcurridos por carrera en {ciudad_sel}", fontweight='bold')
    for i, v in enumerate(promedio_ciudad['MESES_TRANSCURRIDOS']):
        ax2.text(v + 0.3, i, f"{v:.1f}", va='center', fontweight='bold')
    st.pyplot(fig2)
