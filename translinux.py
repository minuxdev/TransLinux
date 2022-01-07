import os, shutil, sys
from pathlib import Path
from tkinter import filedialog
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
file_names = []

index = 0

current_file = ''

start = False
copied_event = False
home_dir = Path.home()


def drop_hendler(event):
    if event.data.startswith('{'):
        parent_folder = event.data[1:3]
    else:
        parent_folder = event.data[0:3]
    x = event.data.count(parent_folder)
    
    data = event.data
    
    if x > 1:
        select_multiple(event)
    
    elif data.startswith('{'):
        data = data[1:-1]
        collected_dirs.append(data)
        
    else:
        collected_dirs.append(data)
        
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
        _dir = dirs[i].strip()
        home = _dir[:3]
        c = _dir.count(home)
        
        if c > 1:
            print(_dir)
            splited_path = _dir.split(home)

            for j in range(len(splited_path)):
                if splited_path[j].endswith('}'):
                    file_path = f'{home}{splited_path[j][:-1]}'
                else:
                    if j == 0:
                        continue
                    file_path = f'{home}{splited_path[j]}' 
                collected_dirs.append(file_path)
        else:
            if _dir.endswith('}'):
                _dir = _dir[:-1].strip()
                collected_dirs.append(_dir)


def filter_path():
    global collected_dirs, unique_dirs
    
    for i in range(len(collected_dirs)):
        pass
    
    
    for path in collected_dirs:
        name = path.split(r'/')[-1]
        if name.endswith('}'):
            name = name[:-1]
        
        if path not in unique_dirs:
            unique_dirs.append(path.strip())
            file_names.append(name)            


def append_to_list_box():
    list_box.delete(0, 'end')
    
    for files in file_names:
        list_box.insert('end', files)


def make_dst_path():    
    try:
        dst_path = filedialog.askdirectory(initialdir=home_dir)

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


def copy_hendler(dst_path):
    global copied_event, current_file,start, collected_dirs, unique_dirs,index
    
    start = True

    for file in unique_dirs:
        name = file.split(r'/')[-1]
        if os.path.isdir(file):
            try:
                current_file = name
                index = file.index(file)
                print('dir name: ', current_file)
                shutil.copytree(src=str(file).strip(), dst=str(dst_path)+name)
            except Exception as ex:
                continue
        else:
            try:
                current_file = name
                print('file name: ', current_file)
                # index = file.index(file)
                shutil.copy(src=str(file).strip(), dst=(dst_path)+name)
            except Exception as ex:
                print(ex)
                # print('Error with: ', file)
                
    copied_event = True
    print('Done Copying...\n\n\n')
    reset_program()


def reset_program():
    global collected_dirs, unique_dirs, file_names, copied_event
    
    list_box.delete(0, 'end')    
    collected_dirs = []
    unique_dirs = []
    file_names = []
    copied_event = False


def show_percentage():
    global copied_event, current_file, index
    
    p_bar = ProgressBar()
    progress_bar = p_bar.prog_bar
    label = p_bar.label
    
    percent = 0
    
    print('Before: ', copied_event)

    while not copied_event:
        print('Copying file: ', current_file)
        progress_bar['value'] = percent
        label['text'] = current_file

        if percent == 100:
            progress_bar['value'] = 100
            percent = 0
            continue
        
        percent += 10
        sleep(0.2)
    print('After: ', copied_event)
    progress_bar['value'] = 100
    sleep(0.2)
    p_bar.destroy()


def start_process():
    global start
    
    t1 = Thread(target=copy_hendler, args=(make_dst_path()+r'/',))
    t1.daemon = True
    t1.start()
    
    if start:
        t2 = Thread(target=show_percentage)
        t2.daemon = True
        t2.start()


def stop_process():
    sys.exit()


list_box.drop_target_register(DND_FILES)
list_box.dnd_bind('<<Drop>>', drop_hendler)

run.config(command=start_process)
cancel.config(command=stop_process)


root.mainloop()
