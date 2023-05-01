import os

class fs_helper:
    
    def get_all_filepaths(root_dir):
        file_paths = []

        for root, dirs, files in os.walk(root_dir):
            for file in files:
                # print(root, file)
                file_paths.append(os.path.join(root, file))
            for dir in dirs:
                # print(os.path.join(root, dir))
                file_paths.append(os.path.join(root, dir))

        
        return file_paths


    def relativize_file_path(fpath):
        return fpath.replace(os.path.dirname(os.path.abspath(__file__)), '.') 


    def relativize_file_paths(fpaths):
        relativized_fpaths = []

        for fpath in fpaths:
            relativized_fpaths.append(fs_helper.relativize_file_path(fpath))


        return relativized_fpaths    
