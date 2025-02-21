#Mapa con separacion por comunas, region y provincias
import folium
from folium import GeoJson
geojson_data = open('Comunas_RMaule.geojson').read()
geojson_data1 = open('Region_Maule.geojson').read()
geojson_data2 = open('Provincias_RMaule.geojson').read()
    # Agrega más tipos y colores según sea necesario
# Crea el mapa
mapa_maule = folium.Map(location=[-35.426666666667, -71.671666666667], zoom_start=8)
GeoJson('Comunas_RMaule.geojson', style_function=lambda x: {"fillColor": "red", "color": "red"}).add_to(mapa_maule)
GeoJson('Region_Maule.geojson', style_function=lambda x: {"fillColor": "blue", "color": "red", "weight":2}).add_to(mapa_maule)
GeoJson('Provincias_RMaule.geojson', style_function=lambda x: {"fillColor": "white", "color": "white"}).add_to(mapa_maule)
# Itera sobre el DataFrame y agrega marcadores con colores según el tipo de centro
GeoJson(geojson_data).add_to(mapa_maule)
GeoJson(geojson_data1).add_to(mapa_maule)
GeoJson(geojson_data2).add_to(mapa_maule)
# Muestra el mapa
mapa_maule