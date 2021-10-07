import matplotlib.pyplot as plt
import ply.lex as lex
import sys
import networkx as nx

import machine_parser
import visualization

fin = open(sys.argv[1], 'r').read()
fout = open(sys.argv[1] + '.out', 'w')
machine = machine_parser.analyse(fin, fout)

G = visualization.draw_graph(machine)
