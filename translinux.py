import os, shutil, sys, platform
from pathlib import Path
from tkinter import filedialog, messagebox
from TkinterDnD2 import DND_FILES, TkinterDnD
from get_size import get_size
from gui import ProgressBar, TransGui
from threading import Thread
from time import sleep
from multiples import size_converter


root = TkinterDnD.Tk()
root.minsize(650,400)
root.title('One-Go Multicopy ver:0.2')


gui = TransGui(root=root)
list_box = gui.list_box
run = gui.run_btn
clear = gui.clear_btn

collected_paths = []
unique_paths = []
unsupported_chars = []
file_names = []
sizes = []
current_file = ''

start = False
home_dir = Path.home()


def drop_event_handler(event):
    """Extract data (path) form event.

    Args:
        event (drop): TkinterDnD2
    """
    
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
        collected_paths.append(data)
    else:
        collected_paths.append(data)
        
    filter_path()
    append_to_list_box()
    
    
def select_multiple(event):
    """Split data from event to generate separated paths
    when multiple files are selected.

    Args:
        event (drop): TkinterDnD2
    """
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
            splited_path = _dir.split(home)
            
            for j in range(len(splited_path)):
                if splited_path[j].endswith('}'):
                    file_path = f'{home}{splited_path[j][:-1]}'
                else:
                    if j == 0:
                        continue
                    file_path = f'{home}{splited_path[j]}'.strip() 
                
                if file_path not in collected_paths:
                    collected_paths.append(file_path)
        else:
            if _dir.endswith('}'):
                _dir = _dir[:-1].strip()
            collected_paths.append(_dir)


def filter_path():
    """Filter duplicated paths in collected_paths"""
    
    global collected_paths, unique_paths, sizes

    for path in collected_paths:
        directory_size = 0
        
        name = path.split(r'/')[-1]
        if name.endswith('}'):
            name = name[:-1]
            
        if path not in unique_paths and path not in unsupported_chars:
            if os.path.isfile(path):
                sizes.append(size_converter(os.path.getsize(path)))
            elif os.path.isdir:
                directory_size = get_size(path)

                if directory_size != -1:
                    sizes.append(size_converter(directory_size))
                    unique_paths.append(path.strip())
                    file_names.append(name)
                else:
                    messagebox.showerror(
                        'Encode Error', 'Unsupported character in file name!')
                    unsupported_chars.append(path)


def append_to_list_box():
    list_box.delete(0, 'end')
    
    for item in file_names:
        index = file_names.index(item)
        list_box.insert('end', f"{item}    -   {sizes[index]}")


def get_destination_path():    
    try:
        destination_path = filedialog.askdirectory(initialdir=home_dir)

        os.mkdir(destination_path)
    except OSError as error:
        pass
    
    return destination_path


def copy_hendler(dst_path):
    global current_file,start, collected_paths, unique_paths, total_size
    
    start = True

    for file in unique_paths:
        name = file.split(r'/')[-1]
        
        if not os.path.exists(dst_path+name):
            
            if os.path.isdir(file):
                total_size += get_size(file)
                try:
                    current_file = name
                    shutil.copytree(src=str(file).strip(), dst=str(dst_path)+name)
                except Exception as ex:
                    print(ex)
            else:
                total_size += os.path.getsize(file)
                try:
                    current_file = name
                    shutil.copy(src=str(file).strip(), dst=(dst_path)+name)
                except Exception as ex:
                    print(ex)
        else:
            current_file = f'{name} \nAlready exist in destination.'
            sleep(3)

    print('Done Copying...\n')
    reset_program()


def reset_program(event=None):
    global collected_paths, unique_paths, file_names
    
    list_box.delete(0, 'end')    
    collected_paths = []
    unique_paths = []
    file_names = []


def exclude_selcted_files(event):
    for i in list_box.curselection():
        try:
            unique_paths.pop(i)
            file_names.pop(i)
            collected_paths.pop(i)
        except IndexError as ie:
            pass    
        append_to_list_box()
        

def show_percentage():
    global copied_event, current_file
    
    p_bar = ProgressBar()
    progress_bar = p_bar.prog_bar
    label = p_bar.label
    
    percents = 0

    print('Started')
    
    while len(unique_paths) != 0:
        progress_bar['value'] = percents
        label['text'] = f"{current_file}"

        if percents == 100:
            progress_bar['value'] = 100
            percents = 0
            continue
        
        percents += 10
        label['text'] = current_file + f"\t{percents}"
        sleep(0.2)
    print('Finished...')
    progress_bar['value'] = 100
    sleep(0.2)
    p_bar.destroy()


def start_process():
    global start
    
    t1 = Thread(target=copy_hendler, args=(get_destination_path()+r'/',))
    t1.daemon = True
    t1.start()
    
    if start:
        t2 = Thread(target=show_percentage)
        t2.daemon = True
        t2.start()


def stop_process():
    sys.exit()


list_box.drop_target_register(DND_FILES)
list_box.dnd_bind('<<Drop>>', drop_event_handler)
list_box.bind('<Shift-D>', exclude_selcted_files)
list_box.bind('<Control-k>', reset_program)

run.config(command=start_process)
clear.config(command=reset_program)


root.mainloop()
