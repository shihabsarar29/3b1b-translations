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

    # Extract the time range from the data dictionary
    if data:
        # Check if the list is not empty
        time_range = data[0].get("time_range", [0, None])
        start = time_range[0]
        end = time_range[1] if len(time_range) > 1 else None

    # Load the translated audio file and get duration
    translated_audio = AudioSegment.from_file(translated_file_path, format="mp3", codec="libmp3lame")
    translated_audio_length = translated_audio.duration_seconds
    print(translated_audio_length)
    
    # Calculate the length ratio
    length_ratio =  translated_audio_length/ (end - start)

    # Set speed factor according to the ratio of translation to original only if the translation was longer than the original in duration
    if length_ratio >= 1:
        speed_factor = 1.0 * length_ratio

    # Apply speed change
    adjusted_audio = translated_audio.speedup(playback_speed=speed_factor)

    # Construct the output file path
    output_file_path = os.path.join(output_file_path, "adjusted_translated_audio.mp3")

    # Export the result to the output file path
    adjusted_audio.export(output_file_path, format="mp3")  

# Example with absolute paths:
translated_file_path = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese/Chinese.mp3" 
json_file_path = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese/sentence_translations.json"
output_directory = "C:/Users/omwin/OneDrive/Documents/GitHub/3b1b-translations/Chinese"

# Call the function with the provided paths
adjust_speed_based_on_json(translated_file_path, json_file_path, output_directory)
