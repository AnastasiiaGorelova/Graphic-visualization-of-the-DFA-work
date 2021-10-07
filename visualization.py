import networkx as nx
import matplotlib.pyplot as plt

import machine_parser

# def add_edge():
#

def draw_graph(graph):
    #G = nx.Graph()

    #G.add_nodes_from(list(range(graph.vertex_cnt)))
    #G.add_edge(0,1,graph=G)
    #G.add_edges_from(graph.edges)


    # nx.draw_circular(G,
    #                  node_color='red',
    #                  node_size=1000,
    #                  with_labels=True)

    G = nx.DiGraph()
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(1, 3)

    labels = {(0, 1): 'foo', (2, 3): 'bar'}

    pos = nx.spring_layout(G)

    nx.draw(G, pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=20)

    #nx.draw(G)

    plt.savefig("graph.png")
    return G