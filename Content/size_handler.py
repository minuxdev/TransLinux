import os
import shutil 



class SizeHandler:
    def __init__(self):
        self.total_size = 0
    
    
    def get_size(self, directory=None):
        if directory:
            try:
                for file in os.scandir(directory):
                    if file.is_file():
                        self.total_size += file.stat().st_size
                    elif file.is_dir():
                        self.get_size(file)
            except FileNotFoundError as e:
                return -1
            return self.total_size
    
    
    def size_converter(self, size=None):
        if size:
            base = 1024
            kilo = base
            mega = base ** 2
            giga = base ** 3
            terra = base ** 4
            
            if size < kilo:
                size = size
                texto = 'B'
            elif size < mega:
                size /= kilo
                texto = 'Kb'
            elif size < giga:
                size /= mega
                texto = 'Mb'
            elif size < terra:
                size /= giga
                texto = 'Gb'
            size = round(size, 2)
            return f'{size}{texto}'.replace('.', ',')
    
    
    def check_free_space(self, directory=None):
        if directory:
            stat = shutil.disk_usage(directory)
            return stat.free


