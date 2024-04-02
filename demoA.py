# How many Blenz' are there in Vancouver?

# You will probably need to install some packages for today's class:

# - `conda install --conda-forge osmnx`
# - `conda install --conda-forge networkx`
# - `conda install --conda-forge folium`

# brew install spatialindex
# pip install nominatim (for geocoding)

import osmnx as ox
import networkx as nx #python's standard graph module needed by osmnx
import folium #needed by osmnx

# get the region of interest
place_names = ['UBC','Pacific Spirit Regional Park, BC', 'Vancouver, BC']
local = ox.geocode_to_gdf(place_names)
print(local.head())

# show the region (project to avoid skew, but leave data in latlong for computation)
toshow = ox.project_gdf(local) #move the coordinates to something that looks nice
ax = toshow.plot(fc='gray', ec='none')

# combine regions explicitly so we capture the roads that go between them.
unified = local.unary_union.convex_hull

# grab the parts of the graph that fall within the region
G = ox.graph_from_polygon(unified, network_type='drive', truncate_by_edge=True,
                                     simplify=True)
ox.plot_graph(ox.project_graph(G),ax=ax,node_size=3) #check to see if this is the graph we want

# assemble the list of Blenz in vancouver
tags = {'amenity':'cafe'}
cafe_gdf = ox.geometries_from_polygon(unified, tags)

blenz = cafe_gdf[ cafe_gdf['name'] == 'Blenz Coffee']
print("Vancouver has " + str(len(blenz)) + " Blenz!")

#-----------------------------------------------------------
# make a folium map

kwargs = {'opacity':0}
m = ox.plot_graph_folium(G, tiles='openstreetmap',**kwargs)

# function to create a marker for each Blenz, and add it to the map
def buildMarker(row):
    if row['geometry'].geom_type == 'Point':
        folium.CircleMarker((row['geometry'].y,row['geometry'].x),
                            color='green',radius=5,fill=True).add_to(m)
    else:
        x, y = row['geometry'].exterior.coords.xy
        folium.CircleMarker((y[0],x[0]),
                      color='red',radius=5,fill=True).add_to(m)

blenz.apply(buildMarker,axis=1) # consider each row from the data frame as input to the function

m.save('map.html')

