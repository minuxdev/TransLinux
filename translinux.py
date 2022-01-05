import os 
import shutil
from tkinter import filedialog
from tkinter.constants import E, END
from tkinter.ttk import Treeview
from TkinterDnD2 import DND_FILES, TkinterDnD
from gui import ProgressBar, TransGui
from threading import Thread
from time import sleep



root = TkinterDnD.Tk()
root.minsize(600,400)
root.title('Translinux ver:0.1')

gui = TransGui(root=root)


list_box = gui.list_box
run = gui.run_btn
cancel = gui.cancel_btn



collected_dirs = []
unique_dirs = []


def drop_hendler(event):
    
    if event.data.startswith('{'):
        parent_folder = event.data[1:3]
    else:
        parent_folder = event.data[0:3]
    x = event.data.count(parent_folder)
    
    if x > 1:
        select_multiple(event)
    
    elif event.data.startswith('{'):
        collected_dirs.append(event.data[1:-1])
    else:
        collected_dirs.append(event.data)
        
    filter_path()
    
    append_to_list_box()
    


def select_multiple(event):
    dirs = []
    
    if '{' in event.data:
        dirs = event.data.replace('{','')
        dirs = dirs.split('} ')
    else:
        dirs = event.data.split(' ')
    
    for i in range(len(dirs)):
        _dir = dirs[i]
        home = _dir[:3]
        c = _dir.count(home)
        
        if c > 1:
            splited_path = _dir.split(home)

            for j in range(len(splited_path)):
                if splited_path[j].endswith('}'):
                    file_path = f'{_dir[:3]}{splited_path[j][:-1]}'
                else:
                    if j == 0:
                        continue
                    file_path = f'{_dir[:3]}{splited_path[j]}'   
                collected_dirs.append(file_path)
        else:
            if _dir.endswith('}'):
                collected_dirs.append(_dir[:-1])
            else:
                collected_dirs.append(_dir)


def filter_path():
    global collected_dirs, unique_dirs
    
    for k in range(len(collected_dirs)):
        path = collected_dirs[k]
        
        if path not in unique_dirs:
            unique_dirs.append(path)



def append_to_list_box():
    list_box.delete(0, END)
    
    for files in unique_dirs:
        list_box.insert(END, files)


def make_dst_path():    
    try:
        dst_path = filedialog.askdirectory(initialdir='/home/minux/Desktop/')
        dst_path += '/TRANSLINUX/'
        os.mkdir(dst_path)
    except OSError as error:
        pass
    
    return dst_path


def get_len_files():
    global unique_dirs
    collect_files = []
    
    for link in unique_dirs:    
        if os.path.isdir(link):
            for root, dirs, files in os.walk(link):
                for file in files:
                    collect_files.append(file)
        else:
            collect_files.append(link)
    return len(collect_files)


def progress_value():
    num = get_len_files()
    return 100 / num, num
    


def copy_hendler():
    dst_path = make_dst_path()
    # percent, num = progress_value()
    
    Thread(target=show_percentage).start()
    # p_bar = ProgressBar()
    # pg_bar = p_bar.prog_bar
    # label = p_bar.label
    # pg_bar.start(1000)
    
    for l in range(len(unique_dirs)):
        file = unique_dirs[l]
        name = file.split(r'/')[-1]

        
        if os.path.isdir(file):
            try:
                shutil.copytree(src=str(file).strip(), dst=str(dst_path)+name)
                # pg_bar.start(1000)
                # print(pg_bar['value'])
                        
            except Exception as ex:
                continue
        else:
            try:
                shutil.copy(src=str(file).strip(), dst=(dst_path)+name)
                # pg_bar['value'] += percent
                # print(pg_bar['value'])
            except Exception as ex:
                print(ex)
                
        # pg_bar.stop()            



def show_percentage():
    global percent, num
    percent, num = progress_value()    
    
    p_bar = ProgressBar()
    pg_bar = p_bar.prog_bar
    label = p_bar.label
    
    for x in range(num):
        if x == num-1:
            pg_bar['value'] = 100
        else:
            pg_bar['value'] += int(percent)
            root.update_idletasks()
        sleep(0.2)
    
    p_bar.destroy()




list_box.drop_target_register(DND_FILES)
list_box.dnd_bind('<<Drop>>', drop_hendler)

run.config(command=copy_hendler)


root.mainloop()
