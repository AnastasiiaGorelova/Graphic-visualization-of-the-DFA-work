import networkx as nx
import matplotlib.pyplot as plt

import machine_parser

def add_vertex(G, pos, machine):
    colour_map = []
    for i in G.nodes:
        if i == machine.start_vertex:
            colour_map.append('red')
        elif str(i) in machine.terminal_vertexes:
            colour_map.append('blue')
        else:
            colour_map.append('green')
    nx.draw_networkx(G, pos, node_color=colour_map, node_size=1000)  # node lables

def add_edges(G, pos, machine):
    labels = {}
    for i in machine.edges:
        labels[(int(i[0]),int(i[1]))] = i[2]
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=20)


def draw_graph(machine):

    # nx.draw_circular(G,
    #                  node_color='red',
    #                  node_size=1000,
    #                  with_labels=True)

    G = nx.MultiDiGraph()

    G.add_nodes_from(list(range(machine.vertex_cnt)))
    edges = []
    for i in machine.edges:
        edges.append((int(i[0]),int(i[1])))
    G.add_edges_from(edges)

    pos = nx.spring_layout(G)
    nx.draw(G, pos)


    add_vertex(G, pos, machine)
    add_edges(G, pos, machine)



    plt.savefig("graph.png")
    return G