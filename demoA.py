# How many Blenz' are there in Vancouver?

import osmnx as ox
import networkx as nx

# get the region of interest
place_names = ['UBC','Pacific Spirit Regional Park, BC', 'Vancouver, BC']
local = ox.geocode_to_gdf(place_names)
print("Checking first few rows of GDF:")
print(local.head())

# check if the region looks right (project to avoid skew, but leave data in latlong for computation)
toshow = ox.projection.project_gdf(local) #move the coordinates to something that looks nice
ax = toshow.plot(fc='gray', ec='none')

# combine regions explicitly so we capture the roads that go between them.
unified = local.union_all().convex_hull

# grab the parts of the graph that fall within the region
G = ox.graph_from_polygon(unified, network_type='drive', truncate_by_edge=True, simplify=True)
# check to see if this is the graph we want
ox.plot_graph(ox.project_graph(G),ax=ax,node_size=3)

# assemble the list of Blenz in vancouver
tags = {'amenity':'cafe'}
cafe_gdf = ox.features_from_polygon(unified, tags)

# Let's work with a Canadian owned brand.
blenz = cafe_gdf[cafe_gdf['name'] == 'Blenz Coffee']
print("Vancouver has " + str(len(blenz)) + " Blenz!")

# Display those locations on an interactive map.
m = blenz.explore(color = 'green', marker_kwds = dict(radius=10))
m.save('mapA.html')