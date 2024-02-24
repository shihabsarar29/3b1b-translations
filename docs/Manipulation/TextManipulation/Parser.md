# Parser Class Documentation

## Overview
The `Parser` class contains methods to extract commonly used information from transcripts. For how a transcript might look, refer to this [repository]()

## Initialization Parameters
- `file_path`: **str**
    - The file path to the transcript data in JSON format.
- `json_encoding`: **str** (default: **utf-8**)
    -  The encoding to use when reading the JSON file.

## Attributes
- `json_list`: **dict**:
    - The transcript data in dictionary format. Read in from `file_path` with `json_encoding`.

## Methods
### get_translated_texts
- **Description**: Get the translated texts from the transcript data.
- **Parameters**
    - ```None```
- **Returns**
    - ```str```: A string where all translated texts are concatenated together, separated by a space: ' '.

### get_translated_texts_list
- **Description**: Get the translated texts from the transcript data as a list.
- **Parameters**
    - ```None```
- **Returns**
    - ```list```: A list of the translated texts.

### get_original_texts
- **Description**: Get the original texts from the transcript data.
- **Parameters**
    - ```None```
- **Returns**
    - ```str```: A string where all original (English) texts are concatenated together, separated by a space: ' '.

### get_original_texts_list
- **Description**: Get the original texts from the transcript data as a list.
- **Parameters**
    - ```None```
- **Returns**
    - ```list```: A list of the original (English) texts.

### get_start_timestamps
- **Description**: Get the start timestamps from the transcript data.
- **Parameters**
    - ```None```
- **Returns**
    - ```list```: A list of the start timestamps of the texts.

### get_end_timestamps
- **Description**: Get the end timestamps from the transcript data.
- **Parameters**
    - ```None```
- **Returns**
    - ```list```: A list of the end timestamps of the texts.

### get_interval
- **Description**: Get the interval between the start and end timestamps from the transcript data.
- **Parameters**
    - ```None```
- **Returns**
    - ```list```: A list of the intervals between the start and end timestamps of the texts.