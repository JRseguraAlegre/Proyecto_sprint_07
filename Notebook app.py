# --- Notebook app.py ---
import os
import glob
import streamlit as st
import plotly.express as px
import pandas as pd

# =======================
# Configuración de página
# =======================
st.set_page_config(
    page_title="Car Sales Dashboard",
    layout="wide",
)

# =======================
# Utilidades en-línea
# =======================
@st.cache_data(show_spinner=False)
def load_data(paths_pattern: str) -> pd.DataFrame:
    """
    Busca el CSV que coincida con el patrón (vehicles_us*.csv) en la raíz,
    se lee y hace una limpieza ligera.
    """
    matches = glob.glob(paths_pattern)
    if not matches:
        raise FileNotFoundError(
            "No se encontro un archivo CSV que coincida con 'vehicles_us*.csv' "
            "en la carpeta actual."
        )
    path = matches[0]
    df = pd.read_csv(path)

    # Normaliza nombres de columnas a snake_case
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace("/", "_")
    )

    # Tipos numéricos clave (si aplican)
    for col in ["price", "model_year", "odometer"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Completa columnas categóricas comunes si faltan
    for col in ["manufacturer", "condition", "fuel", "transmission", "type", "model"]:
        if col not in df.columns:
            df[col] = None

    # Limpieza básica
    if "price" in df.columns:
        df = df[df["price"] > 0]
    if "model_year" in df.columns:
        df = df[df["model_year"].between(1950, 2035, inclusive="both")]
    if "odometer" in df.columns:
        df = df[df["odometer"] >= 0]

    df = df.dropna(subset=["price", "model_year", "odometer"])
    return df.reset_index(drop=True)

def number_format(x) -> str:
    """Formatea números (ej. 12345.6 -> $12,346)."""
    try:
        return f"${x:,.0f}"
    except Exception:
        return "-"

# =======================
# Carga de datos
# =======================
# Patrón que funciona con:
# - vehicles_us.csv
pattern = os.path.join(os.getcwd(), "vehicles_us*.csv")

try:
    df = load_data(pattern)
except Exception as e:
    st.error(
        " No se pudo cargar el dataset.\n\n"
        "Asegúrate de que el CSV esté en la **misma carpeta** que este archivo "
        "y que su nombre comience por **`vehicles_us`** "
    )
    st.stop()

# =======================
# Sidebar (Filtros)
# =======================
st.sidebar.header("Filtros")

year_min = int(df["model_year"].min())
year_max = int(df["model_year"].max())
years = st.sidebar.slider(
    "Año del modelo",
    year_min,
    year_max,
    (year_min, year_max),
)

price_min_all = int(df["price"].min())
price_max_all = int(df["price"].max())
price_min_default = int(df["price"].quantile(0.05))
price_max_default = int(df["price"].quantile(0.95))
price_min, price_max = st.sidebar.slider(
    "Rango de precio",
    price_min_all,
    price_max_all,
    (price_min_default, price_max_default),
)

manufacturer_opts = ["(todos)"] + sorted([x for x in df["manufacturer"].dropna().unique()])
manufacturer = st.sidebar.selectbox("Fabricante", manufacturer_opts, index=0)

condition_opts = ["(todas)"] + sorted([x for x in df["condition"].dropna().unique()])
condition = st.sidebar.selectbox("Condición", condition_opts, index=0)

# Aplicar filtros
mask = (
    (df["model_year"].between(years[0], years[1])) &
    (df["price"].between(price_min, price_max))
)
if manufacturer != "(todos)":
    mask &= df["manufacturer"] == manufacturer
if condition != "(todas)":
    mask &= df["condition"] == condition

df_f = df.loc[mask].copy()

# =======================
# Encabezado / KPIs
# =======================
st.title("Car Sales Dashboard")
st.caption("Demo con Streamlit + Plotly Express. Filtra en la barra lateral.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Registros", f"{len(df_f):,}")
with col2:
    st.metric("Precio medio", number_format(df_f["price"].mean()))
with col3:
    st.metric("Año medio", f"{df_f['model_year'].mean():.0f}")
with col4:
    st.metric("Km medio", number_format(df_f["odometer"].mean()))

st.divider()

# =======================
# Histograma de precios
# =======================
with st.expander("📊 Histograma de precios (plotly-express)", expanded=True):
    bins = st.slider("Número de bins", 10, 100, 40, key="bins_hist")
    fig_hist = px.histogram(
        df_f,
        x="price",
        nbins=bins,
        title="Distribución de precios",
        labels={"price": "Precio (USD)"},
    )
    fig_hist.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_hist, use_container_width=True)

# =======================
# Dispersión precio vs odómetro
# =======================
with st.expander("Gráfico de dispersión precio vs. odómetro", expanded=True):
    color_by = st.selectbox(
        "Color por",
        ["condition", "fuel", "transmission", "type", "manufacturer"],
        index=0,
        key="color_scatter",
    )
    fig_scatter = px.scatter(
        df_f,
        x="odometer",
        y="price",
        color=color_by,
        hover_data=["model_year", "model", "manufacturer"],
        labels={"odometer": "kilometraje", "price": "precio (USD)"},
        title="Precio vs. Kilometraje",
    )
    fig_scatter.update_traces(marker=dict(opacity=0.6))
    fig_scatter.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_scatter, use_container_width=True)

# =======================
# Tabla y descarga
# =======================
st.subheader("Datos filtrados")
st.dataframe(
    df_f.head(1000),
    use_container_width=True,
    hide_index=True,
)

csv_bytes = df_f.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Descargar CSV filtrado",
    data=csv_bytes,
    file_name="vehicles_filtered.csv",
    mime="text/csv",
)

car_data = pd.read_csv('vehicles_us.csv')
hist_button = st.button("Construir histograma")

if hist_button:
    st.write("Creación de un histograma para el conjunto de datos")

    fig = px.histogram(car_data, x="odometer", nbins=40,
                       title="Distribución de kilometraje")
    st.plotly_chart(fig, use_container_width=True)

# =======================
# Botón para gráfico de dispersión
# =======================
scatter_button = st.button("Construir gráfico de dispersión")

if scatter_button:
    st.write("Creación de un gráfico de dispersión")

    fig2 = px.scatter(car_data,
                      x="odometer",
                      y="price",
                      color="condition",
                      title="Precio vs Kilometraje")
    st.plotly_chart(fig2, use_container_width=True)
