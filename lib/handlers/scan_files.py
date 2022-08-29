import os




class DirScan:
 
  
    def scan_dir(directory: str):
        if directory is None:
            return
        if not os.path.exists: 
            return
        directory = os.path.normpath(directory)

        queue = []
        gen_folders_names =[]
        for address, dirs, files in os.walk(directory):

            foldname = os.path.split(address)[-1]
            
            if dirs and not files and address == directory:
                gen_folders_names.extend(dirs)
              
            paths = [os.path.join(address, xx) for xx in files]
            names = [name for name in files]
            if paths and names:
                for gen in gen_folders_names:
                    if gen in paths[0]:
                        queue.append([gen,foldname,names,paths])
                
        return queue










# class DirScan:
   
#     def scan_dir(directory: str):
#         if directory is None:
#             return
#         if not os.path.exists: 
#             return
#         Folders_names =[]
#         Files_names =[]
#         Path = []
#         for address, dirs, files in os.walk(directory):
#             for name in files:
#                 Path.append(os.path.join(address, name))
#                 Files_names.append(name)
#             if dirs:
#                 Folders_names.append(dirs)
#         return [Folders_names,Files_names, Path]
            
  
  



class DataQueue:
    def create_queue(data_list:list):
        folders = data_list[0]
        names_files = data_list[1]
        list_path = data_list[2]
        queue_list = []
        gen_names= folders[0]
        
        for gen in gen_names:
            for fold_list in folders[1:]:
                for fold in fold_list:
                    path_in_folder =  set()
                    file_names = set()
                    for name in names_files:
                        for path in list_path:                 
                            if name in path and fold in path and gen in path:
                                name_fold = fold
                                file_names.add(name)        
                                path_in_folder.add(path) 
                                
                    if  file_names and  path_in_folder:
                        file_names = list(file_names)
                        path_in_folder = list(path_in_folder)
                        file_names.sort()
                        path_in_folder.sort()
                        queue = [gen, name_fold, file_names, path_in_folder]    
                        queue_list.append(queue)
        return queue_list
    

# dat_list = DirScan.scan_dir('X:\Smi\PLS')        
# queu = DataQueue.create_queue(data_list=dat_list)

# with open('X:\\Smi\\PLS\\queue.txt',  'w', encoding="utf-8") as fp:
     
#     for items in queue:         
#         fp.write(f"MODULE: {items[0]} \n")      
#         fp.write(f"FOLD: {items[1]} \n")      
#         for item in items[2]: 
#             fp.write(f"FileName: {item} \n")   
                
#         for item in items[3]: 
#             fp.write(f"Path: {item} \n")   
#     print('Done')