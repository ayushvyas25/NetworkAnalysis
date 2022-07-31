import networkx as nx
import osmnx as ox
import pandas as pd

%matplotlib inline
ox.__version__

# get the network for Piedmont, calculate its basic stats, then show the average circuity
stats = ox.basic_stats(ox.graph_from_place("Paris, France"))
stats["circuity_avg"]

#change place from here and save it accordingly
place = "Paris, France"
gdf = ox.geocode_to_gdf(place)
area = ox.project_gdf(gdf).unary_union.area
G = ox.graph_from_place(place, network_type="drive")
fig, ax = ox.plot_graph(G, node_size=1, save=True, filepath="./images/Paris.png")


# calculate basic and extended network stats, merge them together, and display
stats = ox.basic_stats(G, area=area)
pd.Series(stats)



# unpack dicts into individiual keys:values
stats = ox.basic_stats(G, area=area)
for k, count in stats["streets_per_node_counts"].items():
    stats["{}way_int_count".format(k)] = count
for k, proportion in stats["streets_per_node_proportions"].items():
    stats["{}way_int_prop".format(k)] = proportion

# delete the no longer needed dict elements
del stats["streets_per_node_counts"]
del stats["streets_per_node_proportions"]

# load as a pandas dataframe
pd.DataFrame(pd.Series(stats, name="value")).round(3)



# calculate betweenness with a digraph of G (ie, no parallel edges)
bc = nx.betweenness_centrality(ox.get_digraph(G), weight="length")
max_node, max_bc = max(bc.items(), key=lambda x: x[1])
max_node, max_bc

nc = ["r" if node == max_node else "w" for node in G.nodes]
ns = [80 if node == max_node else 3 for node in G.nodes]
fig, ax = ox.plot_graph(G, node_size=ns, node_color=nc, node_zorder=10,save=True, filepath="./images/Paris2.png")


# add the betweenness centraliy values as new node attributes, then plot

nx.set_node_attributes(G, bc, "bc")
nc = ox.plot.get_node_colors_by_attr(G, "bc", cmap="plasma")
ns = [80 if node == max_node else 10 for node in G.nodes]
fig, ax = ox.plot_graph(
    G,
    node_color=nc,
    node_size=ns,
    node_zorder=50,
    edge_linewidth=0.2,
    edge_color="w",
    save=True, filepath="./images/Paris3.png"
)

# Coded with the help of OSMNx https://github.com/gboeing/osmnx
