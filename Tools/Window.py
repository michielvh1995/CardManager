import tkinter as tk
# import Tkinder as tk

class Window:
    def __init__(self):

        # Init Tkinter (the window itself)
        self.root = tk.Tk()

        w = tk.Label(self.root, text="Hello Tkinter!")
        w.pack() # Fit window to contained size

    def AddComponent(self, comp):
        w = tk.label()

    def Run(self):
        # The main loop
        self.root.mainloop()

a = Window()
a.Run()
