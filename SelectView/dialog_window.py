import tkinter as tk
from tkinter import ttk
from pprint import pprint
import sys

class DialogWindow():
    def __init__(self, options):
        self.options = options
        self.selected_item = None
        self.window = tk.Tk()
        self.window.geometry('400x100')

        labelTop = ttk.Label(self.window, text="Select view")
        labelTop.grid(column=1, row=0)
        #pprint(dict(labelTop))
        
        self.combo = ttk.Combobox(self.window, values=self.options)
        self.combo.grid(column=2, row=1)
        self.combo.current(1)
        self.combo.bind('<<ComboboxSelected>>', self.print_selected)
        #pprint(dict(comboExample)) 

        button = ttk.Button(self.window, 
                            text="select", 
                            command=self.close_window
                            )
        button.grid(column=2, row=2)
        #pprint(dict(button))
        
        self.window.mainloop()

    def close_window(self):
        print(self.selected_item)
        self.window.destroy()

    def print_selected(self, event):
        self.selected_item = self.options.index(self.combo.get()) - 1

w = DialogWindow(sys.argv)
