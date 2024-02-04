import os
import json
from pydub import AudioSegment
from pydub.playback import play

def adjust_speed_based_on_json(translated_file_path, json_file_path, output_file_path):
    # Get absolute paths for input files
    translated_file_path = os.path.abspath(translated_file_path)
    json_file_path = os.path.abspath(json_file_path)

    # Extract the file name of the translated audio
    translated_filename = os.path.basename(translated_file_path)

    # Read the JSON file
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Find the entry for the original audio file in the JSON data
    original_entry = next((entry for entry in data if entry.get("translatedText") == translated_filename), None)

    if original_entry:
        # Extract the time range from the original entry
        time_range = original_entry.get("time_range", [0, None])

        # Load the original English audio file based on the time range
        original_filename = original_entry.get("input", "")
        original_audio = AudioSegment.from_file(original_filename, format="mp3", codec="libmp3lame")[int(time_range[0] * 1000):]

        # Load the translated audio file
        translated_audio = AudioSegment.from_file(translated_file_path, format="mp3", codec="libmp3lame")

        # Calculate the length ratio
        length_ratio = len(translated_audio) / len(original_audio)

        # Set the speed factor to match the length ratio
        speed_factor = 1.0 / length_ratio

        # Apply speed change
        adjusted_audio = original_audio.speedup(playback_speed=speed_factor)

        # Construct the output file path
        output_file_path = os.path.join(output_file_path, "adjusted_translated_audio.mp3")

        # Export the result to the output file path
        adjusted_audio.export(output_file_path, format="mp3")  # Adjust format as needed
    else:
        print(f"Entry for '{translated_filename}' not found in the JSON file.")

# Example with absolute path:
translated_file_path = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese/Chinese.mp3" 
json_file_path = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese/sentence_translations.json"
output_directory = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese"

adjust_speed_based_on_json(translated_file_path, json_file_path, output_directory)
