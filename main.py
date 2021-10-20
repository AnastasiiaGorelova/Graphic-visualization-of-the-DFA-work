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
    validation_entry.delete(0, END)


def display_automate():
    try:
        fin = open(automate_entry.get(), 'r').read()
        machine = machine_parser.analyse(fin)

        ready_image = visualization.draw_graph(machine, automate_entry.get() + '-automaton', 0)

        r = Toplevel()
        r.title("Displaying automaton")

        my_image = PhotoImage(file=str(ready_image), master=root)
        canvas_width = max(my_image.width(), 300)
        canvas_height = my_image.height()
        canvas = Canvas(r, height=canvas_height, width=canvas_width)
        canvas.pack()
        canvas.create_image(canvas_width / 2, 0, anchor=N, image=my_image)
        r.mainloop()
    except FileNotFoundError:
        messagebox.showinfo("ERROR", "File not found")
    except Exception:
        messagebox.showinfo("ERROR", "wtf?!")


def display_validation():
    try:
        fin = open(automate_entry.get(), 'r').read()
        machine = machine_parser.analyse(fin)
        if machine_parser.passed_checkers_for_validation == True:
            v = validation.validation(validation_entry.get(), int(machine_parser.Graph.start_vertex), 0)

            if v != 0:
                ready_image = visualization.draw_graph(machine, automate_entry.get() + '-validation', 1)
                r = Toplevel()
                r.title("Displaying validation of: \"" + str(validation_entry.get()) + "\"")

                my_image = PhotoImage(file=str(ready_image), master=root)
                canvas_width = max(my_image.width(), 300)
                canvas_height = my_image.height()
                canvas = Canvas(r, height=canvas_height, width=canvas_width)
                canvas.pack()
                canvas.create_image(canvas_width / 2, 0, anchor=N, image=my_image)
                r.mainloop()
            else:
                messagebox.showinfo("UpS", "\"" + validation_entry.get() + "\" is not in our language")


    except FileNotFoundError:
        messagebox.showinfo("ERROR", "File not found")
    except Exception:
        messagebox.showinfo("ERROR", "wtf?!")


###########
root = Tk()
root.title("Graphic-visualization-of-the-DFA-work")

automate_label = Label(text="Enter a file with automaton:")
validation_label = Label(text="Enter a string:")

automate_label.grid(row=0, column=0, sticky="w")
validation_label.grid(row=1, column=0, sticky="w")

automate_entry = Entry()
validation_entry = Entry()

automate_entry.grid(row=0, column=1, padx=5, pady=5)
validation_entry.grid(row=1, column=1, padx=5, pady=5)

display_automate_button = Button(text="Show automaton", command=display_automate)
display_validation_button = Button(text="Show string matching with automaton", command=display_validation)
clear_button = Button(text="Clear", command=clear)

display_automate_button.grid(row=2, column=0, padx=5, pady=5, sticky="e")
display_validation_button.grid(row=2, column=1, padx=5, pady=5, sticky="e")
clear_button.grid(row=2, column=2, padx=5, pady=5, sticky="e")

root.mainloop()  # запускает цикл обработки событий окна
##########
