from tkinter import ttk

from pages.bsc.script import BSCScript
from general.progress_bar import ProgressBar

class BSCPage(ttk.Frame):
    def __init__(self, master, root, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.root = root

        self.script = BSCScript(root)
        
        self.frm_blocks    = ttk.Frame (self)
        self.ent_version   = ttk.Entry (self.frm_blocks)
        self.ent_version.insert(0, '1.19')
        self.lbl_version   = ttk.Label (self.frm_blocks,text='Version:')
        self.btn_getBlocks = ttk.Button(self.frm_blocks,command=self.getBlocks,text='➤')
        self.lbl_blockinfo = ttk.Label (self,text='')

        self.frm_blocks.pack()
        self.lbl_version.pack(side='left')
        self.ent_version.pack(side='left')
        self.btn_getBlocks.pack(side='left')
        self.lbl_blockinfo.pack()
        
        self.btn_generate = ttk.Button(self,text='Generate',command=self.generate)
        self.btn_generate.pack()

        # create a progress bar
        self.pb = ProgressBar(self)

    def getBlocks(self):
        feedback = self.script.fetchBlocks(self.ent_version.get())
        self.lbl_blockinfo.configure(text=feedback)

    def generate(self):
        self.btn_generate.config(state='disabled')
        self.pb.pack(pady=10)
        self.pb.update(0)
        self.script.generate(self.pb,self.master)

        self.btn_generate.config(state='normal')
        self.pb.pack_forget()
