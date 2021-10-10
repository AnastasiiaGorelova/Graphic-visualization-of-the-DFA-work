import matplotlib.pyplot as plt
import ply.lex as lex
import sys
import networkx as nx

import machine_parser
import visualization
import validation

fin = open(sys.argv[1], 'r').read()
fout = open(sys.argv[1] + '.out', 'w')
machine = machine_parser.analyse(fin, fout)

visualization.draw_graph(machine, sys.argv[1] + '.out', 0)

string = input("Write string to validate it: ")
v = validation.validation(string, int(machine_parser.start_vertex), 0)

if v != 0:
    visualization.draw_graph(machine, sys.argv[1] + 'validate.out', 1)

