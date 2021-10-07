import ply.lex as lex
import sys
import re

class Graph:
    def __init__(self):
        self.alphabet = global_alphabet  #алфавит языка
        self.start_vertex = int(start_vertex)
        self.terminal_vertexes = terminal_vertexes
        self.edges = edges
        self.vertex_cnt = int(vertex_cnt)

tokens = [
    'alphabet',
    'Q',
    'start',
    'T',
    'function'
]

global_alphabet = []
vertex_cnt = ""
start_vertex = ""
terminal_vertexes = []
edges = []
one_start_vertex = True
passed_checkers = True
fout = None


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    fout.write("Incorrect input format '%s'" % t.value[0] + "\n")
    t.lexer.skip(1)


def t_alphabet(t):
    r'alphabet:.+ \|\|'
    s = t.value[9:-3]
    for i in s:
        global_alphabet.append(i)
    return t


def t_Q(t):
    r'Q:\(.+ s'
    global vertex_cnt
    vertex_cnt = t.value[3:-3]
    return t


def t_start(t):
    r'tart:.+ T'
    global start_vertex
    # start_vertex = t.value[6:-3]
    str = t.value[6:-3]
    for i in str:
        if i != ')':
            start_vertex = start_vertex + i
        else:
            global one_start_vertex
            one_start_vertex = False
            break
    return t


def t_T(t):
    r':\(.+ f'
    global terminal_vertexes
    str = t.value[1:-2]
    сur = ""
    for i in str:
        if i == ')':
            terminal_vertexes.append(cur)
        elif i == '(':
            cur = ""
        else:
            cur = cur + i
    return t


def t_function(t):
    r'unction:.+'
    global edges
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
                current_edge[cnt] = current_edge[cnt] + global_alphabet[int(cur) - 1]
        elif i == '(':
            cur = ""
        elif i == '.':
            edges.append(current_edge)
            current_edge = ["", "", ""]
            cnt = 0
        else:
            cur = cur + i
    return t


def alphabet_checking():
    global passed_checkers
    if len(global_alphabet) == len(set(global_alphabet)):
        return "PASSED: Alphabet elements are unique"
    else:
        passed_checkers = False
        return "NOT PASSED: Alphabet elements are not unique"


def start_vertex_checking():
    global passed_checkers
    if start_vertex == "":
        passed_checkers = False
        return "NOT PASSED: Initial state does not found"
    elif one_start_vertex == False:
        passed_checkers = False
        return "NOT PASSED: Initial state is not the only one"
    else:
        return "RASSED: Initial state is the only one"


def machine_states_checking():
    global passed_checkers
    if len(terminal_vertexes) == len(set(terminal_vertexes)):
        return "PASSED: States are unique"
    else:
        passed_checkers = False
        return "NOT PASSED: States are not unique"


def determinism_and_completeness_checking():
    global passed_checkers
    l = []
    checker = True
    for i in range(int(vertex_cnt)):
        l.append("")
    for i in edges:
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
        if len(set(i)) < len(global_alphabet):
            passed_checkers = False
            fout.write("NOT PASSED: machine is not complete\n")
            checker = False
            break
    if checker:
        fout.write("PASSED: machine is complete\n")

def analyse(fin, curfout):
    lexer = lex.lex()
    lexer.input(fin)
    global fout
    fout = curfout
    while True:
        tok = lexer.token()
        if not tok:
            break

    fout.write("Analyzing the machine...\nAlphabet:\n")
    for s in global_alphabet:
        fout.write(s + ' ')
    fout.write("\nVertex count:\n" + vertex_cnt + "\nStart state: \n" + start_vertex + "\nTerminal states: \n")
    for i in terminal_vertexes:
        fout.write(i + ' ')
    fout.write("\nEdges: \n")
    for i in edges:
        fout.write("transition from " + i[0] + " to " + i[1] + " by \"" + i[2] + "\"\n")

    fout.write("\nTesting the machine...\n")
    fout.write(alphabet_checking() + "\n")
    fout.write(start_vertex_checking() + "\n")
    fout.write(machine_states_checking() + "\n")
    determinism_and_completeness_checking()
    if passed_checkers:
        fout.write("Well done!\n")

    graph = Graph()
    return graph
