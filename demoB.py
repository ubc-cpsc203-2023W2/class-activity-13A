# Computing the Shortest Path from two places using OSMnx and NetworkX.

import osmnx as ox
import networkx as nx #python's standard graph module needed by osmnx

# get the region of interest
place_names = ['UBC', 'Pacific Spirit Regional Park, BC', 'Vancouver, BC']
local = ox.geocode_to_gdf(place_names)
print("Checking first few rows of GDF:")
print(local.head())

# show the region (project to avoid skew, but leave data in latlong for computation)
toshow = ox.projection.project_gdf(local) #move the coordinates to something that looks nice
ax = toshow.plot(fc='gray', ec='none')

# combine regions explicitly so we capture the roads that go between them.
unified = local.union_all().convex_hull

# grab the parts of the graph that fall within the region
G = ox.graph_from_polygon(unified, network_type='drive', truncate_by_edge=True,
                                    simplify=True)
# check to see if this is the graph we want
ox.plot_graph(ox.project_graph(G),ax=ax,node_size=3)

# Plan a path.
origin = ox.geocode('UBC, Vancouver, BC')
destination = ox.geocode('Stanley Park, Vancouver, BC')

origin_node = ox.nearest_nodes(G, origin[1], origin[0])
print(f"Origin coordinates: {origin}")
print(f"Origin node: {origin_node}")

destination_node = ox.nearest_nodes(G, destination[1], destination[0])
print(f"Destination coordinates: {destination}")
print(f"Destination node: {destination_node}")

# Use NetworkX path planner.
route = nx.shortest_path(G, origin_node, destination_node, weight='length')
print(f"Route nodes: {route}")

# Plot using OSMnx.
ox.plot_graph_route(G,route,node_size=3)

# Create interactive map using GDFs and GeoPandas explore().
m = ox.routing.route_to_gdf(G, route).explore(color='blue', style_kwds=dict(weight=5))

#kwargs = { 'style_kwds': dict(opacity=0.5), 'color': 'pink'}
#nodes, edges = ox.convert.graph_to_gdfs(G)
#m = edges.explore(**kwargs)
#m = nodes.explore(m=m, **kwargs)

m.save('mapB.html')
