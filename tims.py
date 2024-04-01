# brew install spatialindex
# pip install osmnx
# pip install folium

'''
This is an old, unfinished attempt at solving the "closest Tim Hortons" problem. It combines our voronoi
project with an underlying structure that is a map, rather than an image.
'''
import osmnx as ox
import networkx as nx
import folium

file = 'timmap.html'

# get the region of interest
place_names = ['UBC','Pacific Spirit Regional Park, BC', 'Vancouver, BC']
local = ox.geocode_to_gdf(place_names)

parks = ox.geocode_to_gdf('Parks, Vancouver, BC')

print(tims)
print(type(tims))


# show the region (project to avoid skew, but leave in latlong for computation)
#toshow = ox.project_gdf(local)
#fig, ax = ox.plot_shape(toshow)

# combine regions explicitly so we capture the roads that go between them.
unified = local.unary_union.convex_hull

print(type(unified))

tim_mask = tims.within(unified)
timUnified = tims.loc[tim_mask]

print(timUnified)
print(len(timUnified))

print(tims.head())

''' 
# grab the parts of the graph that fall within the region
G = ox.graph_from_polygon(unified, network_type='drive', truncate_by_edge=True,
                                     clean_periphery=False, simplify=True)

ox.plot_graph(ox.project_graph(G))



origin = ox.utils.geocode('2366 Main Mall, Vancouver, BC')
destination = ox.utils.geocode('Stanley Park, Vancouver, BC')

origin_node = ox.get_nearest_node(G,origin)
destination_node = ox.get_nearest_node(G,destination)

route = nx.shortest_path(G, origin_node, destination_node)


ox.plot_graph_route(G,route)
'''

m2= folium.Map()

m=ox.plot_route_folium(G, route, route_width=3, route_color='#AA1111',
                     tiles='openstreetmap', popup_attribute='name', edge_width=2, tiles='openstreetmap')

#----------------------------
parishroads2 = ox.graph_from_polygon(shp, network_type='drive', truncate_by_edge=True,
                                     clean_periphery=False, simplify=True)
m2=folium.Map()
folium.GeoJson(gj, name='geojson').add_to(m2)
m2=ox.plot_graph_folium(parishroads2, graph_map=m2,popup_attribute='name', edge_width=2, tiles='openstreetmap')

m2
#----------------------------


m.save(file)

'''