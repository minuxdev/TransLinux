from email import message
from enum import unique
from math import remainder
import os, shutil, sys, platform
from re import U
from pathlib import Path
from tkinter import filedialog, messagebox
from TkinterDnD2 import DND_FILES, TkinterDnD
from threading import Thread
from time import sleep

# from Content.multiples import size_converter
# from Content.get_size import get_size
# from Content.gui import ProgressBar, TransGui

from multiples import size_converter
from size_handler import SizeHandler
from gui import ProgressBar, TransGui


root = TkinterDnD.Tk()
root.minsize(650,400)
root.title('One-Go Multicopy ver:0.2')


gui = TransGui(root=root)
list_box = gui.list_box
show_required_space = gui.required_space
show_free_space = gui.free_space
run = gui.run_btn
clear = gui.clear_btn

sh = SizeHandler()
dir_size = sh.total_size

collected_paths = []
unique_paths = []
unsupported_chars = []
file_names = []
path_sizes = []

required_space = 0
remaining_bytes = 0
free_device_space = 0

current_file = ''
destination_path = ''

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
    
    global collected_paths, unique_paths, path_sizes, required_space
    
    for path in collected_paths:
        directory_size = 0
        sh.total_size = 0
        
        name = path.split(r'/')[-1]
        
        if name.endswith('}'):
            name = name[:-1]
            
        if path not in unique_paths and path not in unsupported_chars:
            if os.path.isfile(path):
                file_size = os.path.getsize(path)
                if file_size:
                    path_sizes.append(file_size)
                    unique_paths.append(path.strip())
                    file_names.append(name)
                    required_space += file_size
            
            elif os.path.isdir(path):
                directory_size = sh.get_size(path)
                
                if directory_size != -1:
                    path_sizes.append(directory_size)
                    required_space += directory_size
                    unique_paths.append(path.strip())
                    file_names.append(name)
                else:
                    messagebox.showerror(
                        'Encode Error', 'Unsupported character in file name!')
                    unsupported_chars.append(path)
            show_required_space['text'] = f"Required Space: {sh.size_converter(required_space)}"


def append_to_list_box():
    list_box.delete(0, 'end')
    print(path_sizes)
    
    for item in file_names:
        index = file_names.index(item)
        list_box.insert('end', f"{item}    -   {sh.size_converter(path_sizes[index])}")


def get_destination_path():  
    global destination_path, free_device_space
    try:
        destination_path = filedialog.askdirectory(initialdir=home_dir)
        free_device_space = sh.check_free_space(destination_path)
        show_free_space['text'] = f"Free Space: {sh.size_converter(free_device_space)}"

        os.mkdir(destination_path)
    except OSError as error:
        pass
    
    return destination_path


def copy_hendler(dst_path):
    global current_file,start, collected_paths, \
            unique_paths
    
    start = True

    for file in unique_paths:
        name = file.split(r'/')[-1]
        index = unique_paths.index(file)
        
        if not os.path.exists(dst_path+name):
            if os.path.isdir(file):
                try:
                    current_file = name
                    shutil.copytree(src=str(file).strip(), dst=str(dst_path)+name)
                except Exception as ex:
                    print(ex)
                    continue
            else:
                try:
                    current_file = name
                    shutil.copy(src=str(file).strip(), dst=(dst_path)+name)
                except Exception as ex:
                    print(ex)
                    continue
            # required_space -= path_sizes[index]
            # remaining_bytes += path_sizes[index]
        else:
            current_file = f'{name} \nAlready exist in destination.'
            sleep(3)

    print('Done Copying...\n')
    reset_program()


def reset_program(event=None):
    global collected_paths, unique_paths, file_names,\
        required_space, remaining_bytes, destination_path
    
    list_box.delete(0, 'end')    
    collected_paths = []
    unique_paths = []
    file_names = []
    sh.total_size = 0
    required_space = 0
    remaining_bytes = 0
    destination_path = ''
    show_free_space['text'] = f'Free Space: 0,00kb'
    show_required_space['text'] = f'Required Space: 0,00kb'


def exclude_selcted_files(event):
    for i in list_box.curselection():
        try:
            unique_paths.pop(i)
            file_names.pop(i)
            collected_paths.pop(i)
            path_sizes.pop(i)
        except IndexError as ie:
            pass    
        append_to_list_box()
        

def show_percentage():
    global copied_event, current_file, required_space, \
        remaining_bytes, destination_path
    
    p_bar = ProgressBar()
    progress_bar = p_bar.prog_bar
    label = p_bar.label

    print('Started')
    destination_path += r'/' + current_file
    
    while len(unique_paths) != 0:
        if os.path.isdir(destination_path):
            print("Is dir...")
            percents = (sh.get_size(destination_path) * 100) / required_space
        else:
            print("Is file")
            percents = (sh.size_converter(destination_path) * 100) / required_space
        progress_bar['value'] = percents
        
        label['text'] = current_file + "\t{:.2f}%".format(percents)
        sleep(1)
        
    print('Finished...')
    progress_bar['value'] = 100
    sleep(0.2)
    p_bar.destroy()


def start_process():
    global start, required_space, free_device_space
    destination = get_destination_path()
    print(required_space)
    
    if required_space < free_device_space:    
        if unique_paths:
            t1 = Thread(target=copy_hendler, args=(destination+r'/',))
            t1.daemon = True
            t1.start()
        else:
            messagebox.showwarning("No content", "The listbox is empty!")
            
        if start:
            t2 = Thread(target=show_percentage)
            t2.daemon = True
            t2.start()
    else:
        messagebox.showerror('No space', 'No enough space in device,\
            try to delete some files.')


def stop_process():
    sys.exit()


list_box.drop_target_register(DND_FILES)
list_box.dnd_bind('<<Drop>>', drop_event_handler)
list_box.bind('<Shift-D>', exclude_selcted_files)
list_box.bind('<Control-k>', reset_program)

run.config(command=start_process)
clear.config(command=reset_program)


root.mainloop()
