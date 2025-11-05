# Recursos utilitzats per crear el cartograma
# https://gadm.org/download_country.html --> mapes i dades espacials (gadm41_AND.shp.zip)
# https://ca.wikipedia.org/wiki/Parr%C3%B2quies_d%27Andorra --> dades parroquia-poblacio 2023

import geopandas as gpd
import pandas as pd
import cartogram
import matplotlib.pyplot as plt
import folium
import branca.colormap as cm
from branca.element import Element

# Carregar shapefile
gdf = gpd.read_file("gadm41_AND_1.shp")

# Carregar csv amb les dades
df = pd.read_csv("andorra_population.csv")

# Comparar camps csv shp
gdf = gdf.rename(columns={"NAME_1": "parishes"})

# Unir les dades tabulars amb geografiques
gdf = gdf.merge(df, on="parishes")

# reprojectar a CRS
gdf = gdf.to_crs(epsg=3857)

# Crear cartograma basat en la població de les parroquies
c = cartogram.Cartogram(gdf, "population")

# Exportar a gpkg (Geopackage)
c.to_file("cartogram_andorra.gpkg")

# Carregar fitxer gpkg
carto_gdf = gpd.read_file("cartogram_andorra.gpkg")

# Visualitzar cartograma
fig, ax = plt.subplots(figsize=(10, 8))

# Ocultar eixos (escales horitzontal y vertical)
ax.set_axis_off()

carto_gdf.plot(
    column="population",
    ax=ax,
    legend=True,
    cmap="YlGn",
    edgecolor="black",
    linewidth=0.5,
)

# Exportar cartograma a png - test de prova
plt.savefig("cartograma.png")

# Coordenades centrals d'Andorra (aprox)
m = folium.Map(location=[42.5, 1.5], zoom_start=10, tiles="cartodbpositron")

# Calcular min i max per a la escala de colors
min_pop = carto_gdf["population"].min()
max_pop = carto_gdf["population"].max()


# Funció per assignar colors segons la població
def style_function(feature):
    population = feature["properties"]["population"]
    # Normalitzar entre 0 i 1
    normalized = (population - min_pop) / (max_pop - min_pop)
    # Convertir a color YlGn (del groc al verd)
    import matplotlib.cm as cm
    import matplotlib.colors as mcolors

    cmap = plt.colormaps["YlGn"]
    rgba = cmap(normalized)
    hex_color = mcolors.rgb2hex(rgba)

    return {"fillColor": hex_color, "fillOpacity": 0.5, "color": "black", "weight": 0.5}


# Afegir GeoJSON al mapa amb popups de nom de parroquia i total poblacio
folium.GeoJson(
    carto_gdf,
    name="Cartograma poblacional",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["parishes", "population"], aliases=["Parroquia:", "Població:"]
    ),
).add_to(m)

# Crear la paleta de colors manualment
colormap = cm.LinearColormap(
    colors=["#ffffe5", "#78c679", "#238443"],  # color aproximats de la paleta YlGn
    vmin=min_pop,
    vmax=max_pop,
    caption="Població en milers d'habitants",
)


def style_function(feature):
    population = feature["properties"]["population"]
    return {
        "fillColor": colormap(population),
        "fillOpacity": 0.5,
        "weight": 0.5,
        "color": "black",
    }


colormap.add_to(m)

# Afegir un element html amb el titol al document
titol_html = """
<h3 style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
    z-index: 9999; background-color: white; padding: 10px; border: 2px solid grey;">
    Població d'Andorra per parrròquies al 2023
</h3>
"""

h3_element = Element(titol_html)
m.get_root().html.add_child(h3_element)

# Creacio index.html
m.save("./public/index.html")
