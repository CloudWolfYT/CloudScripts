# Build using "python3.9 -m PyInstaller --noconsole --onefile -i"assets\icon.ico" --collect-data TKinterModernThemes root.py"

from tkinter import ttk
import TKinterModernThemes as TKMT

from pages.bsc.page import BSCPage
from pages.score_trees.page import ScoresPage

class App:
    def __init__(self, master):
        self.master = master
        self.master.geometry('800x800')
        self.master.title('Cloud\'s Scripts')
        
        self.output_path = "generated"

        # create a notebook widget to hold the pages
        self.notebook = ttk.Notebook(self.master)
        self.notebook.pack(fill='both', expand=True)
        
        self.page_bsc = BSCPage(self.notebook, self)
        self.notebook.add(self.page_bsc, text='Block Converter')
        self.page_scores = ScoresPage(self.notebook, self)
        self.notebook.add(self.page_scores, text='Scoreboard Trees')

window = TKMT.ThemedTKinterFrame("%yourProjectName","azure","dark")

window.root.tk.call("set_theme", "light")
window.root.tk.call("set_theme", "dark")
app = App(window.root)
window.root.mainloop()