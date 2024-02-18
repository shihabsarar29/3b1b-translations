# import os
# from scripts.Parser import Parser
# from scripts.AzureTTS import AzureTTS
# from scripts.audio_helpers import AudioManipulation
# import time
# from pydub import AudioSegment



# def parse_json_files(root_directory, target_directory):
#     # Walk through root_directory
#     for dir_path, dir_names, filenames in os.walk(root_directory):
#         # Check if target_directory is a subdirectory of dir_path
#         if target_directory in dir_path.split(os.sep):
#             # Iterate over every file in the current directory
#             for filename in filenames:
#                 # Check if the file is a JSON file
#                 if filename.endswith('sentence_translations.json'):

#                     start_timestamps = []
#                     text_list = []

#                     # Folder Check
#                     main_dir = dir_path + '/'
#                     os.makedirs(main_dir + "temp_pauses", exist_ok=True)
#                     os.makedirs(main_dir + "temp_audios", exist_ok=True)



#                     # Parser
#                     try:
#                         file_path = main_dir + 'sentence_translations.json'
#                         translator = Parser(file_path)
#                         text_list = translator.get_translated_texts_list()
#                         start_timestamps = translator.get_start_timestamps()
#                         print(text_list, "\n\n")
#                     except Exception as e:
#                         print(f"Failed to parse file: {e}")



#                     # Azure TTS
#                     print("Azure TTS")
#                     try:
#                         azure_tts = AzureTTS()
#                         for i, text in enumerate(text_list):
#                             output_file = main_dir + f'temp_audios/azure_{i+1000}.mp3'
#                             azure_tts.convert_text_to_speech(text=text, filename=output_file)
#                             time.sleep(2)
#                     except Exception as e:
#                         print(f"Failed to convert text to speech using Azure TTS: {e}")





#                     # First pause audio file
#                     try:
#                         AudioManipulation.create_single_pause_audio(
#                             duration=start_timestamps[0], 
#                             output_file=main_dir + "temp_pauses/pause_1000.wav")
#                     except Exception as e:
#                         print(f"Failed to create pause audio files: {e}")




#                     translations_folder_path = main_dir + "temp_audios"
#                     filenames = [filename for filename in os.listdir(translations_folder_path) if filename.endswith('.mp3')]

#                     for i in range(len(start_timestamps)-1):
#                         segment_duration = start_timestamps[i+1] - start_timestamps[i]

#                         # Load the audio file
#                         audio = AudioSegment.from_file(translations_folder_path + '/' + "azure_" + str(i+1000) + ".mp3", format="mp3")  
#                         translated_audio_length = audio.duration_seconds

#                         if segment_duration > translated_audio_length:
#                             AudioManipulation.create_single_pause_audio(
#                                 duration=segment_duration - translated_audio_length, 
#                                 output_file=main_dir + "temp_pauses/pause_" + str(i+1001) + ".wav")

#                         else:
#                             speed_rate = translated_audio_length / segment_duration
#                             if speed_rate > 1.5:
#                                 print(f'Warning: Speed rate is greater than 1.5: {speed_rate}')

#                             # Create pause audio file
#                             AudioManipulation.create_single_pause_audio(
#                                 duration=0, 
#                                 output_file=main_dir + "temp_pauses/pause_" + str(i+1001) + ".wav")
                            
#                             text = text_list[i]
#                             output_file = main_dir + f'temp_audios/azure_{i+1000}.mp3'
#                             azure_tts.convert_text_to_speech(text=text, filename=output_file, speed_rate=speed_rate)
#                             time.sleep(2)



#                     # Join pause and translated audio files
#                     AudioManipulation.join_audios(
#                         pause_audio_folder= main_dir + "temp_pauses",
#                         translated_audio_folder= main_dir + "temp_audios",
#                         output_file_path= main_dir + "azure-sync.mp3")
                    
#                     # Delete temp files
#                     os.system(f"rm -r {main_dir}temp_pauses")
#                     os.system(f"rm -r {main_dir}temp_audios")


# # Test the function
# parse_json_files('../', '256-bit-security')



from scripts.FileUtils import FileUtils
from scripts.AudioSyncPipeline import AudioSync

# Variables
root_directory= '../'
video_folder = 'cross-products'
json_filename= 'sentence_translations.json'

# Get JSON files
fileUtils = FileUtils(root_directory, video_folder, json_filename)
json_files = fileUtils.get_json_files()

# Convert text to audio
for filename in json_files:
    try:
        audio_sync = AudioSync(
            json_path=filename, 
            main_dir=filename.replace(json_filename, ''),
            output_file_path=filename.replace(json_filename, '') + "azure-sync.mp3")
        audio_sync.convert_text_to_audio()
    except Exception as e:
        print(f"Failed to convert text to audio: {e}")
