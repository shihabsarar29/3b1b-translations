import os

class FileUtils:
    def __init__(self, root_directory, target_directory, json_filename='sentence_translations.json'):
        self.root_directory = root_directory
        self.target_directory = target_directory
        self.json_filename = json_filename

    def get_json_files(self):
        json_files = []
        
        # Walk through root_directory
        for dir_path, dir_names, filenames in os.walk(self.root_directory):
            # check if target_directory is a subdirectory of dir_path
            if self.target_directory in dir_path.split(os.sep):
                # iterate over every file in the current directory
                for filename in filenames:
                    # Check if the file is a JSON file
                    if filename.endswith(self.json_filename):
                        json_files.append(os.path.join(dir_path, filename))
        
        return json_files