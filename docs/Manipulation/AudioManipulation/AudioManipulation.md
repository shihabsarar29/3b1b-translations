# AudioManipulation Class

## Overview
This class provides methods for manipulating audio files. Useful when trying to match translated audio with visuals.

## Methods
### create_single_pause_audio
- **Description**: Creates a single pause audio file based on the given duration. Saves the audio file to the given path.
- **Parameters**
    - `duration`: **float**
        - The duration of the pause in seconds.
    - `output_file`: **str**
        - The path where the pause audio file will be saved to.
#### Returns:
- ```None```

### Output:
- A single ```.wav``` audio file saved to the given path.

### join_audios
- **Description**: Joins pause audio files and translated audio files together given the folder paths. The number of files in both folders should be the same. Pauses are added first and then the translated audio is added. Saves the final audio to the given path.
- **Parameters**
    - `pause_audio_folder`: **str**
        - The path to the folder containing the pause audio files.
    - `translated_audio_folder`: **str**
        - Path to the translated audio folder.
    - `output_file_path`: **str**:
        - Path where the final audio file will be saved.
#### Returns:
- ```None```
### Output:
- A single ```.wav``` audio file saved to the given path.

### get_audio_duration
- **Description**: Get the duration of the given audio file in seconds.
- **Parameters**
    - `audio_file`: **str**
        - The path to the audio file to get the duration of.

#### Returns:
- ```float```: The duration of the audio file in seconds.