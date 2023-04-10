import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import dill as pickle
from argparse import ArgumentParser
import sys

parser = ArgumentParser()
parser.add_argument("-d", "--date", dest="date", type=str, help="date")
args = parser.parse_args()

if args.date:
    date = args.date
else:
    sys.exit("Please give a date")

# Retrieving data_graph from file
# e.g. ./graphs/data_graph_2023-04-01.txt
data_graph_file = "./graphs/data_graph_" + date + ".txt"
data_graph = nx.read_adjlist(data_graph_file)

# Setting figure to show
plt.figure(figsize=(10,8))
# pos = nx.kamada_kawai_layout(data_graph)
pos = nx.random_layout(data_graph)
node_options = {"node_color": "blue", "node_size": 0.1}
edge_options = {"width": .05, "alpha": .3, "edge_color": "black"}

# Printing nodes and edges
nx.draw_networkx_nodes(data_graph, pos, **node_options)
nx.draw_networkx_edges(data_graph, pos, **edge_options)
plt.show()