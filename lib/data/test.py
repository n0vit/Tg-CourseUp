import os
import pprint

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
            
# queue_list [[gen_name, name_fold, [list_files_names], [list_path]]]
  
  
qe = DirScan.scan_dir(r"X:\Smi\Tsts")     
pprint.pprint(qe)


