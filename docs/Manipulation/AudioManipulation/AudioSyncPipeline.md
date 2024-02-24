# AudioSync Class Documentation

## Overview
The `AudioSync` class contains methods to synchronize the translated text with the original audio.

## Initialization Parameters
- `json_path`: **str**
    - The file path to the transcript data in JSON format.
- `main_dir`
    - The directory in which temporary files will go
- `output_file_path`: **str**
    - The file path where the synced audio will go
- `language_averages_path`: **str**
    - The path to the JSON file containing the average characters spoken per second for each language.

## Attributes
- `json_path`: **str**:
    - The file path to the transcript data in JSON format.
- `main_dir`: **str**:
    - The directory in which temporary files will go
- `translations_folder_path`
    - The directory in which the translated audios are located. This folder is deleted after the sync process. It is stored in `main_dir` as **"temp_audios"**
- `pause_audio_folder`
    - The directory in which the pause audios are located. This folder is deleted after the sync process. It is stored in `main_dir` as **temp_pauses**
- `output_file_path`: **str**:
    - The file path where the synced audio will go
- `estimate`
    - A reference to the [Estimate](../Calculation/Estimate.md) class, initialized with `language_averages_path`

## Methods
### convert_text_to_audio
- **Description**: Convert the translated text to synchronized audio. It uses Azure, from the [AzureTTS](../../TTS/AzureTTS.md) class, to generate audio data. It speeds up or slows down the individual translated audio segments to match the length of the original audio.
- **Returns**
    - ```None```
    - 
#### Warnings
- ```Speed Rate```: Raised if the speed rate of the translated audio is greater than 1.5x. The format is as follows "Warning: Speed rate is greater than 1.5: {speed_rate}".

#### Outputs
- The synced audio is saved to `output_file_path`.
- A CSV file is saved to the same path as `output_file_path` with the name `.speedup_rates.csv`. This CSV contains the following information:
    - `idx`: The index of the transcript utterance.
    - `speedup_rate`: How much the audio was sped up or slowed down, i.e. `1.25` means the audio was sped up by 25%.
    - `start_time`: The original start time of the utterance
    - `end_time`: The original end time of the utterance
    - `original_duration`: The original (English) duration of the utterance
    - `flag`: Whether or not the `speedup_rate` is greater than 1.25. If it is, the flag is set to `True`, otherwise it is `False`.
    - `character_count`: How many characters were in the translated text.
    - `original_character_count`: How many characters were in the original (English) text.
    - `translated_duration`: How many characters are in the translated text.
    - `estimated_duration`: How long the translated text was estimated to be, according to the character count.
    - `difference`: The difference between the estimated duration and the actual duration of the translated audio.