import ply.lex as lex
import sys
import re


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


def alphabet_checking():
    global passed_checkers
    if len(Graph.alphabet) == len(set(Graph.alphabet)):
        return "PASSED: Alphabet elements are unique"
    else:
        passed_checkers = False
        return "NOT PASSED: Alphabet elements are not unique"


def start_vertex_checking():
    global passed_checkers
    if Graph.start_vertex == "":
        passed_checkers = False
        return "NOT PASSED: Initial state does not found"
    elif one_start_vertex == False:
        passed_checkers = False
        return "NOT PASSED: Initial state is not the only one"
    else:
        return "RASSED: Initial state is the only one"


def machine_states_checking():
    global passed_checkers
    if len(Graph.terminal_vertexes) == len(set(Graph.terminal_vertexes)):
        return "PASSED: States are unique"
    else:
        passed_checkers = False
        return "NOT PASSED: States are not unique"


def determinism_and_completeness_checking(fout):
    global passed_checkers
    l = []
    checker = True
    for i in range(int(Graph.vertex_cnt)):
        l.append("")
    for i in Graph.edges:
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
        if len(set(i)) < len(Graph.alphabet):
            passed_checkers = False
            fout.write("NOT PASSED: machine is not complete\n")
            checker = False
            break
    if checker:
        fout.write("PASSED: machine is complete\n")


def print_analysis(fout):
    if not correct_input:
        fout.write("Incorrect input format" + "\n")
    fout.write("Analyzing the machine...\nAlphabet:\n")
    for s in Graph.alphabet:
        fout.write(s + ' ')
    fout.write("\nVertex count:\n" + str(Graph.vertex_cnt) + "\nStart state: \n" + str(
        Graph.start_vertex) + "\nTerminal states: \n")
    for i in Graph.terminal_vertexes:
        fout.write(i + ' ')
    fout.write("\nEdges: \n")
    for i in Graph.edges:
        fout.write("transition from " + i[0] + " to " + i[1] + " by \"" + i[2] + "\"\n")


def test_machine(fout):
    fout.write("\nTesting the machine...\n")
    fout.write(alphabet_checking() + "\n")
    fout.write(start_vertex_checking() + "\n")
    fout.write(machine_states_checking() + "\n")
    determinism_and_completeness_checking(fout)
    if passed_checkers:
        fout.write("Well done!\n")


def analyse(fin, fout):
    clear()
    print(Graph.edges)
    lexer = lex.lex()
    lexer.input(fin)
    while True:
        tok = lexer.token()
        if not tok:
            break
    print_analysis(fout)
    test_machine(fout)
    print(Graph.edges)
    return Graph
