# GUI for SUN Lab Access System

import tkinter as tk
from tkinter import ttk

class AdminGUI:

    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        self.root.title("SUN Lab Access System - Admin")
        # Add GUI components here

    def run(self):
        self.root.mainloop()
