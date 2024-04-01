# brew install spatialindex
# pip install osmnx
# pip install folium
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
                                     clean_periphery=False, simplify=True)
ox.plot_graph(ox.project_graph(G),ax=ax,node_size=3) #check to see if this is the graph we want

# assemble the list of starbucks in vancouver
tags = {'amenity':'cafe'}
cafe_gdf = ox.geometries_from_polygon(unified, tags)

sb = cafe_gdf[ cafe_gdf['name'] == 'Starbucks']
print("Vancouver has " + str(len(sb)) + " Starbucks!")




#-----------------------------------------------------------
# make a folium map

kwargs = {'opacity':0}
m = ox.plot_graph_folium(G, tiles='openstreetmap',**kwargs)

# function to create a marker for each starbucks, and add it to the map
def buildMarker(row):
    if row['geometry'].geom_type == 'Point':
        folium.CircleMarker((row['geometry'].y,row['geometry'].x),
                            color='green',radius=5,fill=True).add_to(m)
    else:
        x, y = row['geometry'].exterior.coords.xy
        folium.CircleMarker((y[0],x[0]),
                      color='red',radius=5,fill=True).add_to(m)

sb.apply(buildMarker,axis=1) # consider each row from the data frame as input to the function

m.save('map.html')

#shortest path computation (just an example)-------------------------------------

origin = ox.geocode('UBC, Vancouver, BC')
destination = ox.geocode('Stanley Park, Vancouver, BC')

origin_node = ox.nearest_nodes(G,origin[1],origin[0])
print(*origin)
print(origin_node)

destination_node = ox.nearest_nodes(G,destination[1],destination[0])
print(*destination)
print(destination_node)

route = nx.shortest_path(G, origin_node, destination_node, weight='length')
print(route)

ox.plot_graph_route(G,route,node_size=3)

args = {'color':'#AA1111','width':3}
m=ox.plot_route_folium(G, route, route_map=m, popup_attribute='name', tiles='openstreetmap',**args)

m.save('map2.html')
