import ply.lex as lex
import sys
import re


class graph:
    alphabet = []
    vertex_cnt = ""
    start_vertex = ""
    terminal_vertexes = []
    edges = []


one_start_vertex = True
passed_checkers = True
correct_input = True

tokens = [
    'alphabet',
    'Q',
    'start',
    'T',
    'function'
]

<<<<<<< HEAD
=======
global_alphabet = []
vertex_cnt = ""
start_vertex = ""
terminal_vertexes = []
edges = []
one_start_vertex = True
passed_checkers = True
correct_input = True
max_vert = 0

>>>>>>> validation

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    global correct_input
    correct_input = False
    t.lexer.skip(1)


def t_alphabet(t):
    r'alphabet:.+ \|\|'
    s = t.value[9:-3]
    for i in s:
        graph.alphabet.append(i)
    return t


def t_Q(t):
    r'Q:\(.+ s'
    graph.vertex_cnt = t.value[3:-3]
    return t


def t_start(t):
    r'tart:.+ T'
    str = t.value[6:-3]
    for i in str:
        if i != ')':
            graph.start_vertex = graph.start_vertex + i
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
            graph.terminal_vertexes.append(cur)
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
                current_edge[cnt] = current_edge[cnt] + graph.alphabet[int(cur) - 1]
        elif i == '(':
            cur = ""
        elif i == '.':
            graph.edges.append(current_edge)
            current_edge = ["", "", ""]
            cnt = 0
        else:
            cur = cur + i
    return t


def alphabet_checking(graph):
    global passed_checkers
    if len(graph.alphabet) == len(set(graph.alphabet)):
        return "PASSED: Alphabet elements are unique"
    else:
        passed_checkers = False
        return "NOT PASSED: Alphabet elements are not unique"


def start_vertex_checking(graph):
    global passed_checkers
    if graph.start_vertex == "":
        passed_checkers = False
        return "NOT PASSED: Initial state does not found"
    elif one_start_vertex == False:
        passed_checkers = False
        return "NOT PASSED: Initial state is not the only one"
    else:
        return "RASSED: Initial state is the only one"


def machine_states_checking(graph):
    global passed_checkers
    if len(graph.terminal_vertexes) == len(set(graph.terminal_vertexes)):
        return "PASSED: States are unique"
    else:
        passed_checkers = False
        return "NOT PASSED: States are not unique"


def determinism_and_completeness_checking(fout, graph):
    global passed_checkers
    l = []
    checker = True
    for i in range(int(graph.vertex_cnt)):
        l.append("")
    for i in graph.edges:
        l[int(i[0])] = l[int(i[0])] + i[2]
    for i in l:
        if len(i) != len(set(i)):
            passed_checkers = False
            fout.write("NOT PASSED: machine is not determenistic\n")
            checker = False
            break
    if checker:
        fout.write("PASSED: machine is deterministic\n")
    checker = True
    for i in l:
        if len(set(i)) < len(graph.alphabet):
            passed_checkers = False
            fout.write("NOT PASSED: machine is not complete\n")
            checker = False
            break
    if checker:
        fout.write("PASSED: machine is complete\n")


def print_analysis(fout):
    if correct_input == False:
        fout.write("Incorrect input format" + "\n")
    fout.write("Analyzing the machine...\nAlphabet:\n")
    for s in graph.alphabet:
        fout.write(s + ' ')
    fout.write("\nVertex count:\n" + str(graph.vertex_cnt) + "\nStart state: \n" + str(
        graph.start_vertex) + "\nTerminal states: \n")
    for i in graph.terminal_vertexes:
        fout.write(i + ' ')
    fout.write("\nEdges: \n")
    for i in graph.edges:
        fout.write("transition from " + i[0] + " to " + i[1] + " by \"" + i[2] + "\"\n")


def test_machine(fout):
    fout.write("\nTesting the machine...\n")
    fout.write(alphabet_checking(graph) + "\n")
    fout.write(start_vertex_checking(graph) + "\n")
    fout.write(machine_states_checking(graph) + "\n")
    determinism_and_completeness_checking(fout, graph)
    if passed_checkers:
        fout.write("Well done!\n")


def analyse(fin, fout):
    lexer = lex.lex()
    lexer.input(fin)
    while True:
        tok = lexer.token()
        if not tok:
            break
    print_analysis(fout)
    test_machine(fout)
    return graph
