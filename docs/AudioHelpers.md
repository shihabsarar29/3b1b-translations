# AudioManipulation Class

The `AudioManipulation` class provides methods for manipulating audio files. It's particularly useful when trying to match translated audio with visuals.

## Methods:

##### adjust_speed_based_on_json
Adjusts the speed of an audio file based on the data from a JSON file.

###### Args:
- `translated_file_path` **str**: 
  - The path to the translated audio file.
- `json_file_path` **str**: 
  - The path to the JSON file containing the data for speed adjustment.
- `output_file_path` **str**: 
  - The path where the adjusted audio file will be saved.

###### Returns:
- `None`

##### create_pause_audio
Creates pause audio files based on the given start timestamps and duration.

###### Args:
- `start_timestamps` **list[int]**: 
  - The start timestamps for the pauses.
- `output_directory` **str**: 
  - The directory where the pause audio files will be saved.
- `duration` **float**: 
  - The duration of the pauses.

###### Returns:
- `None`

##### join_audios
Joins pause audio files and translated audio files together.

###### Args:
- `pause_audio_files` **list[str]**: 
  - The pause audio files to be joined.
- `translated_audio_files` **list[str]**: 
  - The translated audio files to be joined.
- `output_file_path` **str**: 
  - The path where the final audio file will be saved.

###### Returns:
- `None`
