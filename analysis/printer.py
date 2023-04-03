import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import dill as pickle

# Retrieving data_graph from file
data_graph_file = "./data_graph_try.txt"
data_graph = nx.read_adjlist(data_graph_file)

# Setting figure to show
plt.figure(figsize=(10,8))
#pos = nx.kamada_kawai_layout(data_graph)
pos = nx.random_layout(data_graph)
node_options = {"node_color": "blue", "node_size": 5}
edge_options = {"width": .20, "alpha": .3, "edge_color": "black"}

# Printing nodes and edges
nx.draw_networkx_nodes(data_graph, pos, **node_options)
nx.draw_networkx_edges(data_graph, pos, **edge_options)
plt.show()