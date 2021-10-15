import matplotlib.pyplot as plt
import ply.lex as lex
import sys
import networkx as nx

import machine_parser
import visualization
import validation
from tkinter import *
from tkinter import messagebox


def clear():
    automate_entry.delete(0, END)
    automate_entry.delete(0, END)


def display_automate():
    fin = open(automate_entry.get(), 'r').read()
    fout = open(automate_entry.get() + '-parser' + '.txt', 'w')
    machine = machine_parser.analyse(fin, fout)

    ready_image = visualization.draw_graph(machine, automate_entry.get() + '-automate', 0)

    r = Toplevel()
    r.title("Displaying automate")

    canvas = Canvas(r, height=500, width=500)
    canvas.pack()
    my_image = PhotoImage(file=str(ready_image), master=root)
    canvas.create_image(0, 0, anchor=NW, image=my_image)
    r.mainloop()


def display_validation():
    fin = open(automate_entry.get(), 'r').read()
    fout = open(automate_entry.get() + '.out', 'w')
    machine = machine_parser.analyse(fin, fout)

    v = validation.validation(validation_entry.get(), int(machine_parser.start_vertex), 0)

    if v != 0:
        ready_image = visualization.draw_graph(machine, automate_entry.get() + '-validation', 1)
        r = Toplevel()
        r.title("Displaying validation of: \"" + str(validation_entry.get()) + "\"")

        canvas = Canvas(r, height=500, width=500)
        canvas.pack()
        my_image = PhotoImage(file=str(ready_image), master=root)
        canvas.create_image(0, 0, anchor=NW, image=my_image)
        r.mainloop()
    else:
        messagebox.showinfo("UpS", validation_entry.get() + "is not in our language")


###########
root = Tk()
root.title("Graphic-visualization-of-the-DFA-work")

automate_label = Label(text="Введите файл где лежит автомат:")
validation_label = Label(text="Введите строчку:")

automate_label.grid(row=0, column=0, sticky="w")
validation_label.grid(row=1, column=0, sticky="w")

automate_entry = Entry()
validation_entry = Entry()

automate_entry.grid(row=0, column=1, padx=5, pady=5)
validation_entry.grid(row=1, column=1, padx=5, pady=5)

display_automate_button = Button(text="Show automate", command=display_automate)
display_validation_button = Button(text="Show validation", command=display_validation)
clear_button = Button(text="Clear", command=clear)

display_automate_button.grid(row=2, column=0, padx=5, pady=5, sticky="e")
display_validation_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
clear_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")

root.mainloop()  # запускает цикл обработки событий окна
##########
