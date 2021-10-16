import networkx as nx
import numpy as npy
import matplotlib.pyplot as plt

import machine_parser
import visualization


class Edge:
    def __init__(self, to, frm):
        self.to = to
        self.frm = frm


valide_edges = []


def make_adjacency():
    adjacency = [[] for _ in range(machine_parser.Graph.max_vert + 1)]
    for e in machine_parser.Graph.edges:
        adjacency[int(e[0])].append([e[1], e[2]])
    return adjacency


def validation_dfs(string, start, n, adjacency):
    global valide_edges
    for j in range(len(adjacency[start])):
        to = adjacency[start][j][0]
        func = adjacency[start][j][1]
        if n == len(string):
            return start
        if func.find(string[n]) == -1:
            continue
        elif func.find(string[n]) != -1:
            valide_edges.append(Edge(start, int(to)))
            return validation_dfs(string, int(to), n + 1, adjacency)
    return start


def validation(string, start, n):
    term = validation_dfs(string, start, n, make_adjacency())
    if str(term) in machine_parser.Graph.terminal_vertexes:
        # print("OK")
        return 1
    else:
        # print("NO")
        return 0
