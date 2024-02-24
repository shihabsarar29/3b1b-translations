# FileUtils Class Documentation

## Overview
The `FileUtils` class contains methods to get the paths of files and directories easily.

## Attributes
- `root_directory`: **str**:
    - The root directory of the files you want to access.
- `target_directory`: **str**:
    - The direct parent directory in while files that end with `json_filename` are located.
- `json_filename`: **str**:
    - The name of the files whose paths you want to access.

## Methods
### get_json_files
- **Description**: Get the paths of all the files in the `target_directory`s that are in the `root_directory`s that end with `json_filename`.
- **Parameters**: 
    - ```None```

#### **Returns**:
- ```list```: A list of the `json_filename` files founds