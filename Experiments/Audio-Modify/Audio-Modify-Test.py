import sys
sys.path.insert(0, sys.path[0] + '/../../')

from scripts.Parser import Parser
from scripts.AzureTTS import AzureTTS
from scripts.audio_helpers import AudioManipulation
import time
import os


main_dir = "Experiments/Audio-Modify/"

def get_filenames(folder_path):
    filenames = []
    
    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Get the full path of the file
        file_path = os.path.join(folder_path, filename)
        # Check if the path points to a file (not a folder)
        if os.path.isfile(file_path):
            # Add the filename to the list
            filenames.append(folder_path + '/'+ filename)
    
    return filenames


# Parser
try:
  file_path = main_dir + 'sentence_translations.json'
  translator = Parser(file_path)
  text_list = translator.get_translated_texts_list()
  start_timestamps = translator.get_start_timestamps()
  print(text_list, "\n\n")
except Exception as e:
    print(f"Failed to parse file: {e}")



# Azure TTS
try:
  print("Azure TTS")
  voice_name = "en-US-AndrewMultilingualNeural"
  start_time = time.time()
  azure_tts = AzureTTS()
  for i, text in enumerate(text_list):
    output_file = main_dir + f'temp_audios/azure_{i+1000}.wav'
    azure_tts.convert_text_to_speech(text, voice_name, output_file)
  print(f"Time taken by Azure TTS: {time.time() - start_time} seconds.\n")
except Exception as e:
  print(f"Failed to convert text to speech using Azure TTS: {e}")



# Create pause audio files
AudioManipulation.create_pause_audio(
    start_timestamps=start_timestamps,
    output_directory=main_dir + "temp_pauses",
    duration=0
)

print("Pause audio files created")

# Join pause and translated audio files
pause_audio_files = get_filenames(main_dir + "temp_pauses")
translated_audio_files = get_filenames(main_dir + "temp_audios")

AudioManipulation.join_audios(
    pause_audio_files=pause_audio_files,
    translated_audio_files=translated_audio_files,
    output_file_path=main_dir + "final_audio.wav"
)

print("Audio files joined")

