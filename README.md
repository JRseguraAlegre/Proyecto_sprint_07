# Proyecto_sprint_07 Car Sales Dashboard
Este proyecto es una aplicación web construida con **Streamlit** y **Plotly Express**.  
La cual permite explorar un conjunto de datos de anuncios de venta de coches.  
El usuario puede aplicar filtros (año, precio, fabricante, condición) y visualizar:  
- Histogramas de distribución.  
- Gráficos de dispersión (precio vs. kilometraje).  
- KPIs con información resumida (promedio de precio, año, kilometraje).  
Además, la app permite descargar los datos filtrados en formato CSV.

##  Cómo ejecutar en local
1. Clonar este repositorio:
   ```bash
   git clone <url-del-repo>
   cd PROYECTO_SPRINT_07

python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

## Instalar dependencias:
pip install -r requirements.txt

## Ejecutar la app:
streamlit run "Notebook app.py"

##  Estructura
- `Notebook app.py`: aplicación principal de Streamlit.
- `vehicles_us.csv`: dataset de anuncios de coches.
- `EDA.ipynb`: notebook de análisis exploratorio.
- `requirements.txt`: librerías necesarias.
- `.gitignore`, `README.md`: configuración y documentación.

## Despliegue
Este proyecto puede desplegarse fácilmente en [Streamlit Cloud]()
1. Sube el repo a GitHub.
2. En Streamlit Cloud crea una nueva app desde el repo.
3. Indica como archivo principal: `Notebook app.py`.
4. Listo, tendrás un enlace público a tu dashboard.
