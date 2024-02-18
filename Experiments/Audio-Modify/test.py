import os
import json
from pydub import AudioSegment

def adjust_speed_based_on_json(translations_folder_path, json_file_path, output_folder_path):
        # Get absolute paths for input files
        translations_folder_path = os.path.abspath(translations_folder_path)
        json_file_path = os.path.abspath(json_file_path)
        output_folder_path = os.path.abspath(output_folder_path)

        print(translations_folder_path)
        print(json_file_path)
        print(output_folder_path)

        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Get list of files in the translations folder
        filenames = [filename for filename in os.listdir(translations_folder_path) if filename.endswith('.mp3')]

        # Iterate through JSON entries and files simultaneously
        for i, entry in enumerate(data):
            # Check if there are still files in the translations folder
            if i >= len(filenames):
                break
            
            time_range = entry.get("time_range", [0, None])
            start, end = time_range

            filename = filenames[i]
            # Load the translated audio file and get duration
            translated_file_path = os.path.join(translations_folder_path, filename)
            translated_audio = AudioSegment.from_file(translated_file_path, format="mp3")
            translated_audio_length = translated_audio.duration_seconds
            
            # Calculate the length ratio
            length_ratio = translated_audio_length / (end - start) if start is not None and end is not None else 1.0

            # Set speed factor according to the ratio of translation to original only if the translation was longer than the original in duration
            if length_ratio >= 1:
                speed_factor = 1.0 * length_ratio
            else:
                speed_factor = 1.0

            print(translated_audio_length)
            print(end - start)
            print(f"Speed factor: {speed_factor}")

            # Apply speed change
            if speed_factor >= 1: # Use built-in speedup function if speeding up
                # adjusted_audio = translated_audio.speedup(playback_speed=speed_factor)
                adjusted_audio = translated_audio.speedup(playback_speed=speed_factor,)
            # else: # Lower frame rate if slowing down
            #     adjusted_audio = translated_audio._spawn(translated_audio.raw_data, overrides={
            #         "frame_rate": int(translated_audio.frame_rate * 1)
            #     }).set_frame_rate(translated_audio.frame_rate)

            # Construct the output file path
            output_file_path = os.path.join(output_folder_path, f"adjusted_{filename}")

            # Export the adjusted audio to the output file path
            adjusted_audio.export(output_file_path, format="mp3")

# Adjust speed based on JSON
print("Adjusting speed based on JSON")
translations_folder_path =  r"temp_audios"
json_file_path = r"sentence_translations.json"
output_folder_path = r"temp_audios2"

adjust_speed_based_on_json(translations_folder_path, json_file_path, output_folder_path)


