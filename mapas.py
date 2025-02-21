import folium
import json
import sys
import pandas as pd
import os

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

# Diccionario de colores para cada estado de operatividad
estado_colores = {
    "operativo": "green",
    "semioperativo": "orange",
    "inoperativo": "red"
}

# Función para definir el color de cada comuna según la mayoría de sus establecimientos
def definir_color_comuna(comuna_nombre):
    establecimientos = df[df["COMUNA"].str.upper() == comuna_nombre.upper()]

    if establecimientos.empty:
        return "gray"  # No hay datos de establecimientos

    # Contar la cantidad de establecimientos en cada estado
    conteo_estados = establecimientos["operatividad_establecimiento"].value_counts()

    # Verificar la mayoría
    num_operativos = conteo_estados.get("operativo", 0)
    num_semioperativos = conteo_estados.get("semioperativo", 0)
    num_inoperativos = conteo_estados.get("inoperativo", 0)

    total_establecimientos = num_operativos + num_semioperativos + num_inoperativos

    if num_inoperativos > num_operativos + num_semioperativos:
        return "red"  # Mayoría inoperativo
    elif num_semioperativos > 0 or (num_inoperativos > 0 and num_operativos > 0):
        return "orange"  # Hay semioperativo o mezcla entre operativo/inoperativo
    elif num_operativos == total_establecimientos:
        return "green"  # Todos operativos

    return "gray"

# Agregar los polígonos de las comunas con su color correcto
for feature in comunas_geojson["features"]:
    comuna_nombre = feature["properties"]["COMUNA"]
    provincia_nombre = feature["properties"]["PROVINCIA"]

    # Definir color basado en el estado de operatividad de la comuna
    color_comuna = definir_color_comuna(comuna_nombre)
    feature["properties"]["color"] = color_comuna  # Guardamos el color en las propiedades

    folium.GeoJson(
        feature,
        name=comuna_nombre,
        style_function=lambda x: {
            "fillColor": x["properties"]["color"],  # Tomamos el color desde las propiedades
            "color": "black",
            "weight": 1,
            "fillOpacity": 0.6
        },
        highlight_function=lambda x: {
            "fillColor": "lightblue",
            "color": "black",
            "weight": 3,
            "fillOpacity": 0.8
        },
        tooltip=f"{comuna_nombre} - {provincia_nombre}"
    ).add_to(mapa_maule)

# Función para obtener el color del marcador de los establecimientos
def definir_color_marcador(estado):
    return estado_colores.get(estado.lower(), "gray")  # Convertimos a minúsculas por seguridad

# Agregar marcadores de centros de salud
for _, row in df.iterrows():
    folium.Marker(
        location=[row["latitud_establecimiento"], row["longitud_establecimiento"]],
        popup=f"{row['NOMBRE_ESTABLECIMIENTO']} ({row['operatividad_establecimiento']})",
        icon=folium.Icon(color=definir_color_marcador(row["operatividad_establecimiento"]))
    ).add_to(mapa_maule)

# Agregar control de capas
folium.LayerControl().add_to(mapa_maule)

current_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio del script actual
ruta_templates = os.path.join(current_dir, 'templates', 'mapa_interactivo.html')
print(f"Guardando mapa en: {ruta_templates}")  # Imprime la ruta absoluta correcta
mapa_maule.save(ruta_templates)  # Guarda el archivo en la ruta correcta
