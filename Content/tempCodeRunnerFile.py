    # for path in collected_paths:
    #     directory_size = 0
        
    #     name = path.split(r'/')[-1]
    #     if name.endswith('}'):
    #         name = name[:-1]
            
    #     if path not in unique_paths and path not in unsupported_chars:
    #         if os.path.isfile(path):
    #             print(path)
    #             file_size = os.path.getsize(path)
    #             if file_size:
    #                 print(file_size)
    #                 sizes.append(size_converter(file_size))
    #                 unique_paths.append(path.strip())
    #                 file_names.append(name)
            
    #         elif os.path.isdir:
    #             # print('directory size is : ' + str(directory_size))
    #             directory_size = get_size(path)
    #             print('=====> directory size is : ' + str(directory_size))
                
    #             if directory_size != -1:
    #                 sizes.append(size_converter(directory_size))
    #                 unique_paths.append(path.strip())
    #                 file_names.append(name)
    #             else:
    #                 messagebox.showerror(
    #                     'Encode Error', 'Unsupported character in file name!')
    #                 unsupported_chars.append(path)
