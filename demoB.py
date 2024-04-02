# Computing the Shortest Path from two places

# You will need to install scikit-learn for this one
# conda install scikit-learn

import osmnx as ox
import networkx as nx #python's standard graph module needed by osmnx

## Copied from demoA

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
# ox.plot_graph(ox.project_graph(G),ax=ax,node_size=3) #check to see if this is the graph we want

## New Code
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

# Deprecated way of doing it
args = {'color':'#AA1111','width':3}
m=ox.plot_route_folium(G, route, popup_attribute='name', tiles='openstreetmap',**args)
m.save('map2.html')

# Poor Replacement to above
# ox.graph_to_gdfs(G, nodes=False).explore()
