import folium
import json
import sys
import pandas as pd
import os
from folium.plugins import MarkerCluster


# Cargar los datos de establecimientos

if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    print("No se proporcionó la ruta del archivo.")

#file_path = "Copia de edan_de_ejemplo.xlsx"
df = pd.read_excel(file_path)

# Convertir las coordenadas a float
df["latitud_establecimiento"] = df["latitud_establecimiento"].astype(str).str.replace(",", ".").astype(float)
df["longitud_establecimiento"] = df["longitud_establecimiento"].astype(str).str.replace(",", ".").astype(float)

# Convertir los estados de operatividad a minúsculas
df["operatividad_establecimiento"] = df["operatividad_establecimiento"].str.lower()

# Cargar las comunas de la Región del Maule desde el GeoJSON
geojson_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Comunas_RMaule.geojson')
with open(geojson_path, encoding="utf-8") as f:
    comunas_geojson = json.load(f)

# Crear el mapa centrado en la Región del Maule
mapa_maule = folium.Map(location=[-35.4267, -71.6717], zoom_start=8)

# Paleta de colores oscuros más diferenciados
colores_gris_oscuros = ["#101010", "#282828", "#404040", "#585858", "#707070", "#888888"]

# Obtener todas las provincias y asignarles un color más distintivo
provincias = sorted(set(feature["properties"]["PROVINCIA"] for feature in comunas_geojson["features"]))
colores_provincias = {provincia: colores_gris_oscuros[i % len(colores_gris_oscuros)] for i, provincia in enumerate(provincias)}

# Función para definir el color de cada comuna según la mayoría de sus establecimientos
def definir_color_comuna(comuna_nombre):
    establecimientos = df[df["COMUNA"].str.upper() == comuna_nombre.upper()]

    if establecimientos.empty:
        return "#AAAAAA"  # Gris claro si no hay datos

    # Contar la cantidad de establecimientos en cada estado
    conteo_estados = establecimientos["operatividad_establecimiento"].value_counts()

    # Si hay al menos un inoperativo, la comuna será negra
    if conteo_estados.get("inoperativo", 0) > 0:
        return "#ff0000"  # Rojo
    elif conteo_estados.get("semioperativo", 0) > 0:
        return "#ff9b00"  # naranja
    else:
        return "#05b100"  # Verde 

# Agregar los polígonos de las comunas con su color correcto y bordes más diferenciados
for feature in comunas_geojson["features"]:
    comuna_nombre = feature["properties"]["COMUNA"]
    provincia_nombre = feature["properties"]["PROVINCIA"]

    # Definir color basado en el estado de operatividad de la comuna
    color_comuna = definir_color_comuna(comuna_nombre)
    feature["properties"]["color"] = color_comuna  # Guardamos el color en las propiedades

    # Color del borde de la provincia (más diferenciados)
    color_borde = colores_provincias[provincia_nombre]

    folium.GeoJson(
        feature,
        name=comuna_nombre,
        style_function=lambda x, borde=color_borde: {
            "fillColor": x["properties"]["color"],  # Color de la comuna según operatividad
            "color": borde,  # Color del borde de la provincia (más variado)
            "weight": 3.5,  # Borde más grueso para distinguir provincias
            "fillOpacity": 0.6
        },
        highlight_function=lambda x: {
            "fillColor": "#DDDDDD",  # Gris más claro al resaltar
            "color": "white",
            "weight": 4,
            "fillOpacity": 0.9
        },
        tooltip=f"{comuna_nombre} - {provincia_nombre}"
    ).add_to(mapa_maule)

# Crear un grupo de marcadores con agrupamiento dinámico
cluster_marcadores = MarkerCluster().add_to(mapa_maule)

# Agregar marcadores de establecimientos con colores estándar
for _, row in df.iterrows():
    estado = row["operatividad_establecimiento"]

    if estado == "inoperativo":
        color_icono = "red"
    elif estado == "semioperativo":
        color_icono = "orange"
    else:
        color_icono = "green"

    folium.Marker(
        location=[row["latitud_establecimiento"], row["longitud_establecimiento"]],
        popup=f"{row['NOMBRE_ESTABLECIMIENTO']} ({estado})",
        icon=folium.Icon(color=color_icono)
    ).add_to(cluster_marcadores)

# Agregar control de capas
folium.LayerControl().add_to(mapa_maule)

current_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual
ruta_templates = os.path.join(current_dir, 'templates', 'mapa_interactivo.html')
print(f"Guardando mapa en: {ruta_templates}")  # Imprime la ruta absoluta correcta
mapa_maule.save(ruta_templates)  # Guarda el archivo en la ruta correcta
