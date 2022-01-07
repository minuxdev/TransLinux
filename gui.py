from tkinter import *
from tkinter import ttk
import os, platform


if platform.system == 'Linux':
    os.system('xrdb -load /dev/null')
    os.system('xrdb -query')


class TransGui():
    def __init__(self, root = None):
        self.root = root

        self.create_frames()
        self.create_widgets()
        self.resize_control()
        self.place_widgets()
        # self.crate_menubar()


    def create_frames(self):
        self.top = Frame(self.root)
        self.control = Frame(self.root)
        self.output = Frame(self.root)
        self.buttons = Frame(self.root)
    
    
    def create_widgets(self):
        label = Label(self.top, text = 'Drag and Drop on here...',
                    justify='center')
        label.grid(column=1, row=0, sticky='we', padx=4, pady=4)
        
        self.scroll_v = Scrollbar(self.control, orient='vertical')
        self.scroll_h = Scrollbar(self.control, orient='horizontal')
        
        self.list_box = Listbox(self.control, font='Poppins 9',
                        yscrollcommand=self.scroll_v.set,
                        xscrollcommand=self.scroll_h.set)
        
        self.scroll_v.config(command=self.list_box.yview)
        self.scroll_h.config(command=self.list_box.xview)
        
        self.run_btn = Button(self.buttons, text='Run', width=12)

        self.cancel_btn = Button(self.buttons, text='Cancel', width=12)


    def resize_control(self):
        Grid.columnconfigure(self.root, 0, weight=1)
        Grid.rowconfigure(self.root, 1, weight=1)
        
        Grid.columnconfigure(self.control, 0, weight=1)
        Grid.rowconfigure(self.control, 0, weight=1)
        
    
    def place_widgets(self):
        self.top.grid(row=0, column=0, sticky='we', padx=4, pady=4)
        self.control.grid(row=1, column=0, sticky='news', padx=4, pady=4)
        self.output.grid(row=2, column=0, sticky='we', padx=4, pady=4)
        self.buttons.grid(row=3, column=0, sticky='news', padx=1, pady=1)
        
        self.list_box.grid(column=0, row=0,  columnspan=1,
                        sticky='news', padx=4, pady=4)
        self.scroll_v.grid(column=1, row=0,  rowspan=2,
                        sticky='ns', padx=0, pady=4)
        self.scroll_h.grid(column=0, row=1,  columnspan=2,
                        sticky='we', padx=4, pady=0)
        
        self.run_btn.grid(row=2, column=2, sticky='news',
                        padx=4, pady=4)
        self.cancel_btn.grid(row=2, column=3, sticky='news',
                        padx=4, pady=4)
        

class ProgressBar(Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Copying data')
        self.geometry('600x100')
        self.resizable(False, False)
        
        # self.grab_set()
        
        self.main_functions()
        
    def main_functions(self):
        self.create_frame()
        self.create_widgets()
        self.place_widgets()

    def create_frame(self):
        self.progress = Frame(self)
        self.label = Label(self, anchor=CENTER)
    
    
    def create_widgets(self):
        
        self.prog_bar = ttk.Progressbar(self.progress,
                                        orient=HORIZONTAL,
                                        length=580, mode='determinate')
        
        self.file_name = Label(self.label, justify=CENTER, font='monospace')
    
    
    def place_widgets(self):
        self.progress.grid(column=0, row=0, 
                        sticky='news', padx=4, pady=5)

        self.label.grid(column=0, row=1, 
                        sticky='news', padx=4, pady=2)
        
        self.prog_bar.grid(column=0, row=0, columnspan=2,
                        sticky='news', padx=4, pady=4)
        self.file_name.grid(column=0, row=1, columnspan=2,
                        sticky='news', padx=4, pady=4)


if __name__ == "__main__":
    root = Tk()
    root.title('Transfer')
    root.minsize(500,200)
    app = TransGui(root=root)
    pg = ProgressBar()
    pg.label['text'] = 'aldjfa;lsdjf;lakdjfkalsd,mxcnzv,mcnvoiewfsdaksdfkjasdnfnasm,dnf,'
    root.mainloop()
    
    