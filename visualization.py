import networkx as nx
import numpy as npy
import matplotlib.pyplot as plt

import machine_parser


def build_graph(G, machine):
    G.add_nodes_from(list(range(int(machine.vertex_cnt))))
    edges = []
    for i in machine.edges:
        edges.append((int(i[0]), int(i[1])))
    G.add_edges_from(edges)


def set_node_labels(G):
    nx.set_node_attributes(G, {i: {'label': i} for i in G.nodes})


def set_edge_labels(G, machine):
    labelseee = {}
    for i in machine.edges:
        labelseee[(int(i[0]), int(i[1]))] = i[2]
    nx.set_edge_attributes(G, {(e[0], e[1]): {'label': labelseee[(e[0], e[1])]} for e in G.edges(data=True)})


def paint_vertices(G, machine, D):
    colour_map = {}
    for i in G.nodes:
        if i == int(machine.start_vertex):
            colour_map[i] = 'darkviolet'
        elif str(i) in machine.terminal_vertexes:
            colour_map[i] = 'grey'
        else:
            colour_map[i] = 'pink'

    for i in D.nodes():
        n = D.get_node(i)
        n.attr['color'] = 'black'
        n.attr['style'] = 'filled'
        n.attr['fillcolor'] = colour_map[int(n)]


def paint_edges(D):
    D.edge_attr.update(color='black', arrowsize=1)


def draw_graph(machine, filename):
    G = nx.DiGraph()

    build_graph(G, machine)

    set_node_labels(G)
    set_edge_labels(G, machine)

    D = nx.drawing.nx_agraph.to_agraph(G)  # makes graphiz graph from nx

    paint_vertices(G, machine, D)
    paint_edges(D)

    pos = D.layout('dot')

    # D.draw(filename + '.pdf')
    D.draw(filename + '.svg')  # тоже неплохо поддерживается
