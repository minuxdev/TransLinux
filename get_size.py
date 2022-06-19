import os 
directory_size = 0

def get_size(directory):
    global directory_size
    try:
        for file in os.scandir(directory):
            if file.is_file():
                directory_size += file.stat().st_size
            elif file.is_dir():
                get_size(file)
    except FileNotFoundError as e:
        return -1
    return directory_size


if __name__ == "__main__":
    directory = input('dir: ')
    directory_size = get_size(directory=directory[1:-1])
    print(directory_size)