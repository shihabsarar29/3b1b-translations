""" 
Calculate the average number of characters per line and per second in the translated text for each language.
Calculates the average number of characters per second in the translated (azure) audio and the synced translated (azure) audio.

Outputs two different JSON files for each language:
- character_counts.json: Contains the average number of characters per line and per second in the translated text, as well as the average number of characters per second in the translated (azure) audio and the synced translated (azure) audio.

- character_count_detailed.json: Contains the character count for every item in the JSON list, including the start and end time.
"""

import os
import json
import pydub
import gc

ROOT_DIR = r"" # REPLACE WITH THE FOLDER YOU WANT TO GET CHARACTER AVERAGES FOR

# List of folders in the root directory
folders = [f for f in os.listdir(ROOT_DIR) if os.path.isdir(os.path.join(ROOT_DIR, f))]
print(folders)

all_languages_count = {}

# Loop through each folder
for idx in range(len(folders)):
    folder_name = folders[idx]
    full_path = os.path.join(ROOT_DIR, folder_name)

    character_count_detailed = [] # Has character count for every item in JSON list, incuding the start and end time
    character_counts = {
        "total": 0, # Total number of translated characters in the video
        "avg_per_line": 0, # Average number of translated characters per line
        "avg_translated": None, # Average number of translated characters per second in translated (azure) audio
        "avg_translated_sync": None, # Average number of translated characters per second in synced translated (azure) audio
    }

    # Check if sentence_translations.json exists within the folder
    if os.path.exists(os.path.join(full_path, "sentence_translations.json")):
        print("Available for: ", folder_name)
        with open(os.path.join(full_path, "sentence_translations.json"), "r", encoding="utf-8") as f:
            data = json.load(f)

            # Loop through each item in the JSON list
            for item in data:
                # Count the number of characters in the sentence
                character_count = len(item["translatedText"])
                character_counts["total"] += character_count

                # Add to character_count_detailed
                current_item = {
                    "start": item["start"],
                    "end": item["end"],
                    "character_count": character_count
                }

                character_count_detailed.append(current_item)
    else:
        continue # If not available, move onto next folder (language)
    # Calculate average per line
    character_counts["avg_per_line"] = character_counts["total"] / len(data)

    # Attempt to open azure.wav
    try:
        audio = pydub.AudioSegment.from_file(os.path.join(full_path, "azure.wav"))
        
        # Get length of audio in seconds
        audio_length = len(audio) / 1000

        # Calculate average number of translated characters per second
        character_counts["avg_translated"] = character_counts["total"] / audio_length
        # character_counts["avg_translated"] = 500 / audio_length
        all_languages_count[folder_name] = character_counts["avg_translated"]

        # Delete audio variable
        del audio

        # Collect garbage
        gc.collect()
    except FileNotFoundError:
        pass # If not available, don't do anything

    # Attempt to open azure-sync.mp3
    try:
        audio = pydub.AudioSegment.from_file(os.path.join(full_path, "azure-sync.mp3"))
        
        # Get length of audio in seconds
        audio_length = len(audio) / 1000

        # Calculate average number of translated characters per second
        character_counts["avg_translated_sync"] = character_counts["total"] / audio_length

        # Delete audio variable
        del audio

        # Collect garbage
        gc.collect()
    except FileNotFoundError:
        pass # If not available, don't do anything

    # Save to json
    with open(os.path.join(full_path, "character_counts.json"), "w", encoding="utf-8") as f:
        json.dump(character_counts, f, ensure_ascii=False, indent=4)

    with open(os.path.join(full_path, "character_count_detailed.json"), "w", encoding="utf-8") as f:
        json.dump(character_count_detailed, f, ensure_ascii=False, indent=4)

    with open(os.path.join(ROOT_DIR, "avg_chars_per_sec.json"), "w", encoding="utf-8") as f:    
        json.dump(all_languages_count, f, ensure_ascii=False, indent=4)
