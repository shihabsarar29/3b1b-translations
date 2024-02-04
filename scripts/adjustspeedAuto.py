import os
import json
from pydub import AudioSegment

def adjust_speed_based_on_json(translated_file_path, json_file_path, output_file_path):
    # Get absolute paths for input files
    translated_file_path = os.path.abspath(translated_file_path)
    json_file_path = os.path.abspath(json_file_path)

    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    # Assuming data is a list and you want to work with the first entry
    if data and isinstance(data[0], dict):
        # Extract the time range from the first entry
        time_range = data[0].get("time_range", [0, None])

        # Load the translated audio file
        translated_audio = AudioSegment.from_file(translated_file_path, format="mp3", codec="libmp3lame")

        # Calculate the length ratio
        length_ratio = len(translated_audio) / (time_range[1] - time_range[0])

        # Set speed factor according to the ratio of translation to original only if the translation was longer than the original in duration
        if length_ratio >= 1:
            speed_factor = 1.0 * length_ratio

        # Apply speed change
        adjusted_audio = translated_audio.speedup(playback_speed=speed_factor)

        # Construct the output file path
        output_file_path = os.path.join(output_file_path, "adjusted_translated_audio.mp3")

        # Export the result to the output file path
        adjusted_audio.export(output_file_path, format="mp3")
    else:
        print("Invalid or empty JSON data.")

# Example with absolute paths:
translated_file_path = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese/Chinese.mp3" 
json_file_path = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese/sentence_translations.json"
output_directory = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese"

# Call the function with the provided paths
adjust_speed_based_on_json(translated_file_path, json_file_path, output_directory)
