import ply.lex as lex
import sys
import re
from tkinter import *
from tkinter import messagebox


class Graph:
    alphabet = []
    vertex_cnt = ""
    start_vertex = ""
    terminal_vertexes = []
    edges = []
    max_vert = 0


one_start_vertex = True
passed_checkers = True
correct_input = True
passed_checkers_for_validation = True

tokens = [
    'alphabet',
    'Q',
    'start',
    'T',
    'function'
]


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    global correct_input
    correct_input = False
    messagebox.showinfo("INCORRECT INPUT!", "Incorrect input format")
    t.lexer.skip(1)


def t_alphabet(t):
    r'alphabet:.+ \|\|'
    s = t.value[9:-3]
    for i in s:
        Graph.alphabet.append(i)
    return t


def t_Q(t):
    r'Q:\(.+ s'
    Graph.vertex_cnt = t.value[3:-3]
    return t


def t_start(t):
    r'tart:.+ T'
    str = t.value[6:-3]
    for i in str:
        if i != ')':
            Graph.start_vertex = Graph.start_vertex + i
        else:
            global one_start_vertex
            one_start_vertex = False
            break
    return t


def t_T(t):
    r':\(.+ f'
    str = t.value[1:-2]
    сur = ""
    for i in str:
        if i == ')':
            Graph.terminal_vertexes.append(cur)
        elif i == '(':
            cur = ""
        else:
            cur = cur + i
    return t


def t_function(t):
    r'unction:.+'
    str = t.value[8:]
    сur = ""
    cnt = 0
    current_edge = ["", "", ""]  # [start,finish,transition]
    for i in str:
        if i == ')':
            if cnt != 2:
                current_edge[cnt] = cur
                cnt += 1
            else:
                current_edge[cnt] = current_edge[cnt] + Graph.alphabet[int(cur) - 1]
        elif i == '(':
            cur = ""
        elif i == '.':
            Graph.edges.append(current_edge)
            Graph.max_vert = max(Graph.max_vert, int(current_edge[0]), int(current_edge[1]))  # НОВОЕ
            current_edge = ["", "", ""]
            cnt = 0
        else:
            cur = cur + i
    return t


def clear():
    Graph.alphabet = []
    Graph.vertex_cnt = ""
    Graph.start_vertex = ""
    Graph.terminal_vertexes = []
    Graph.edges = []
    Graph.max_vert = 0
    global one_start_vertex, passed_checkers, correct_input
    one_start_vertex = True
    passed_checkers = True
    correct_input = True


def alphabet_checking():
    global passed_checkers
    if len(Graph.alphabet) != len(set(Graph.alphabet)):
        passed_checkers = False
        messagebox.showinfo("INCORRECT AUTOMATON!", "Alphabet elements are not unique")


def start_vertex_checking():
    global passed_checkers
    if Graph.start_vertex == "":
        passed_checkers = False
        messagebox.showinfo("INCORRECT AUTOMATON!", "Initial state does not found :(")
    elif one_start_vertex == False:
        passed_checkers = False
        messagebox.showinfo("INCORRECT AUTOMATON!", "Initial state is not the only one")


def automaton_states_checking():
    global passed_checkers
    if len(Graph.terminal_vertexes) != len(set(Graph.terminal_vertexes)):
        passed_checkers = False
        messagebox.showinfo("INCORRECT AUTOMATON!", "States are not unique")


def determinism_and_completeness_checking():
    global passed_checkers, passed_checkers_for_validation
    l = []
    for i in range(int(Graph.vertex_cnt)):
        l.append("")
    for i in Graph.edges:
        l[int(i[0])] = l[int(i[0])] + i[2]
    for i in l:
        if len(i) != len(set(i)):
            passed_checkers = False
            passed_checkers_for_validation = False
            messagebox.showinfo("INCORRECT AUTOMATON!", "automaton is not determenistic")
            break
    for i in l:
        if len(set(i)) < len(Graph.alphabet):
            passed_checkers = False
            messagebox.showinfo("INCORRECT AUTOMATON!", "automaton is not complete")
            break


def test_automaton():
    alphabet_checking()
    start_vertex_checking()
    automaton_states_checking()
    determinism_and_completeness_checking()


def analyse(fin):
    clear()
    lexer = lex.lex()
    lexer.input(fin)
    while True:
        tok = lexer.token()
        if not tok:
            break
    test_automaton()
    return Graph
