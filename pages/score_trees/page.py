import tkinter as tk
from tkinter import ttk

from pages.score_trees.script import ScoresScript
from general.progress_bar import ProgressBar

class ScoresPage(ttk.Frame):
    def __init__(self, master, root, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.root = root

        self.script = ScoresScript(root)
        
        ## Settings
        frm_settings = ttk.Frame(self)
        lbl_namespace      = ttk.Label(frm_settings,text='Namespace: ')
        self.ent_namespace = ttk.Entry(frm_settings)
        self.ent_namespace.insert(0, 'my_namespace')
        lbl_folder         = ttk.Label(frm_settings,text='Folder: ')
        self.ent_folder    = ttk.Entry(frm_settings)
        self.ent_folder.insert(0, 'path/to/tree')
        lbl_player         = ttk.Label(frm_settings,text='Player: ')
        self.ent_player    = ttk.Entry(frm_settings)
        self.ent_player.insert(0, '.index')
        lbl_objective      = ttk.Label(frm_settings,text='Objective: ')
        self.ent_objective = ttk.Entry(frm_settings)
        self.ent_objective.insert(0, 'my_scoreboard')
        lbl_start          = ttk.Label(frm_settings,text='Start: ')
        self.ent_start     = ttk.Entry(frm_settings)
        self.ent_start.insert(0, '1')
        lbl_end            = ttk.Label(frm_settings,text='End: ')
        self.ent_end       = ttk.Entry(frm_settings)
        self.ent_end.insert(0, '128')

        frm_settings.pack      (pady=10)
        lbl_namespace.grid     (row=0,column=0)
        self.ent_namespace.grid(row=0,column=1)
        lbl_folder.grid        (row=0,column=2)
        self.ent_folder.grid   (row=0,column=3)
        lbl_player.grid        (row=1,column=0)
        self.ent_player.grid   (row=1,column=1)
        lbl_objective.grid     (row=1,column=2)
        self.ent_objective.grid(row=1,column=3)
        lbl_start.grid         (row=2,column=0)
        self.ent_start.grid    (row=2,column=1)
        lbl_end.grid           (row=2,column=2)
        self.ent_end.grid      (row=2,column=3)

        ## Code Block Text Field
        frm_code = ttk.Frame(self)
        frm_code.pack(pady=10)
        self.txt_code = tk.Text(frm_code, wrap="none")
        self.txt_code.insert("end", "if score < 64:\n   a = score/25\nelse:\n   a = 0\nout = f'say X={a}'")
        vsb = ttk.Scrollbar(frm_code, command=self.txt_code.yview, orient="vertical")
        hsb = ttk.Scrollbar(frm_code, command=self.txt_code.xview, orient="horizontal")
        self.txt_code.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        frm_code.grid_rowconfigure(0, weight=1)
        frm_code.grid_columnconfigure(0, weight=1)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        self.txt_code.grid(row=0, column=0, sticky="nsew")

        self.btn_generate = ttk.Button(self,text='Generate',command=self.generate)
        self.btn_generate.pack()

        # create a progress bar
        self.pb = ProgressBar(self)

    def generate(self):
        self.btn_generate.config(state='disabled')
        self.pb.pack(pady=10)
        self.pb.update(0)
        self.script.generate(self,self.master)

        self.btn_generate.config(state='normal')
        self.pb.pack_forget()
