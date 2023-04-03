import matplotlib.pyplot as plt


    
plt.figure(figsize=(10,8))
#pos = nx.kamada_kawai_layout(data_graph)
pos = nx.random_layout(data_graph)
node_options = {"node_color": "blue", "node_size": 20}
edge_options = {"width": .50, "alpha": .5, "edge_color": "black"}
nx.draw_networkx_nodes(data_graph, pos, **node_options)
nx.draw_networkx_edges(data_graph, pos, **edge_options)
#nx.draw(data_graph)
plt.show()