from tkinter import ttk

class ProgressBar:
    def __init__(self, parent):
        
        self.frame = ttk.Frame(parent)
        self.pb = ttk.Progressbar(self.frame, orient='horizontal', length=200, mode='determinate')
        self.pb.pack()

    def update(self, value):
        self.pb['value'] = value
    
    def pack(self, *args, **kwargs):
        self.frame.pack(*args, **kwargs)
    
    def pack_forget(self, *args, **kwargs):
        self.frame.pack_forget(*args, **kwargs)