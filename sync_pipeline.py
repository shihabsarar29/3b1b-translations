from translations_parser import TranslationsParser
from azure_tts import AzureTTS
from length_estimate import LengthEstimate
from edit_audio import EditAudio
import os
import traceback

class AudioSync:
    """
    A class to synchronize the audio with the translated text.
    """

    def __init__(self, json_path, output_file_path, language = "spanish", voice_name = "en-US-AndrewMultilingualNeural"):
        """
        The constructor for the AudioSync class.

        Inputs:
            json_path (str): The path to the JSON file containing the translated text.
            output_file_path (str): The path where the final audio file will be saved.
            language (str): The language of the translated text. Default is "spanish".
            voice_name (str): The name of the voice to use for the audio. Default is "en-US-AndrewMultilingualNeural".
        
        Outputs:
            None
        """
        self.json_path = json_path
        self.translations_folder_path = os.path.join("temp_audios")
        self.pause_audio_folder = os.path.join("temp_pauses")
        self.output_file_path = output_file_path
        self.language = language
        self.voice_name = voice_name
        self.lengthEstimate = LengthEstimate()
        self.azure_tts = AzureTTS()

    def convert_text_to_audio(self):
        """
        A method to convert the translated text to audio and synchronize it with the original audio.

        Inputs:
            None
        
        Outputs:
            None
        """
        # Make directories
        os.makedirs(self.translations_folder_path, exist_ok=True)
        os.makedirs(self.pause_audio_folder, exist_ok=True)

        # Parse translations
        try:
            translationsParser = TranslationsParser(self.json_path, json_encoding="utf-8")
            text_list = translationsParser.get_translated_texts(is_list=True)
            try:
                start_timestamps = translationsParser.get_start_timestamps()
                end_timestamps = translationsParser.get_end_timestamps()
            except KeyError:
                start_timestamps = translationsParser.get_start_timestamps_direct()
                end_timestamps = translationsParser.get_end_timestamps_direct()
            print(text_list, "\n\n")
        except Exception as e:
            print(f"Failed to parse file: {e}")
            return

        # Create pause audios and manipulate audio
        try:
            # Create the first pause audio
            EditAudio.create_single_pause_audio(duration=start_timestamps[0], output_file=os.path.join(self.pause_audio_folder, "pause_1000.wav"))

            accumulator = 0

            # Manipulate audio
            for i in range(len(start_timestamps)-1):
                segment_duration = end_timestamps[i] - start_timestamps[i]
                if segment_duration == 0:
                    continue

                # Estimated length of the translated text
                estimated_length = self.lengthEstimate.estimate_length(text_list[i], language=self.language)
                speed_rate = estimated_length / segment_duration
                if speed_rate > 1.05:
                    print(f'Warning: Speed rate is greater than 1.05: {speed_rate}')
                    speed_rate = 1.05

                elif speed_rate < 1:
                    speed_rate = 1

                # Convert text to speech with speed rate
                text = text_list[i]
                output_file = os.path.join(self.translations_folder_path, f'azure_{i+1000}.mp3')
                self.azure_tts.convert_text_to_speech(text=text, filename=output_file, speed_rate=speed_rate, voice_name=self.voice_name)
                translated_audio_length = EditAudio.get_audio_duration(output_file)


                # Create pause audio file
                pause_duration = start_timestamps[i+1] - end_timestamps[i]
                if segment_duration < translated_audio_length:
                    accumulator += translated_audio_length - segment_duration
                else:
                    pause_duration += segment_duration - translated_audio_length

                if pause_duration - accumulator > 0:
                    pause_duration -= accumulator
                    accumulator = 0
                else:
                    accumulator -= pause_duration
                    pause_duration = 0

                
                EditAudio.create_single_pause_audio(
                    duration= pause_duration,
                    output_file= os.path.join(self.pause_audio_folder, "pause_" + str(i+1001) + ".wav"))
                
            # Add the last audio
            segment_duration = end_timestamps[-1] - start_timestamps[-1]
            estimated_length = self.lengthEstimate.estimate_length(text_list[-1], language=self.language)
            speed_rate = estimated_length / segment_duration
            if speed_rate > 1.05:
                print(f'Warning: Speed rate is greater than 1.05: {speed_rate}')
                speed_rate = 1.05

            elif speed_rate < 1:
                speed_rate = 1

            # Convert text to speech with speed rate
            text = text_list[-1]
            output_file = os.path.join(self.translations_folder_path, f'azure_{len(start_timestamps)+1000}.mp3')
            self.azure_tts.convert_text_to_speech(text=text, filename=output_file, speed_rate=speed_rate, voice_name=self.voice_name)

        except Exception as e:
            print(traceback.format_exc())
            print(f"Failed to create pause audio files: {e}")
            return
        

        # Join audio
        try:
            EditAudio.join_audios(
                pause_audio_folder= self.pause_audio_folder,
                translated_audio_folder= self.translations_folder_path,
                output_file_path= self.output_file_path)
        except Exception as e:
            print(f"Failed to join audios: {e}")
            return

        # Deleting all files in the folders
        try:
            for file in os.listdir(self.pause_audio_folder):
                os.remove(os.path.join(self.pause_audio_folder, file))
            for file in os.listdir(self.translations_folder_path):
                os.remove(os.path.join(self.translations_folder_path, file))
        except Exception as e:
            print(f"Failed to delete files in the folders: {e}")
            return
        
        # Try to delete folders
        try:
            os.rmdir(os.path.join(self.translations_folder_path))
            os.rmdir(os.path.join(self.pause_audio_folder))
            return
        except Exception as e:
            print(f"Failed to delete folders: {e}")
            return
        


# # Example usage
# json_paths = [
#     "/Users/shihab/Documents/3b1b/captions/2024/shorts/mandelbrot/spanish/sentence_translations.json"
# ]

# for json_path in json_paths:
#     segments = os.path.normpath(json_path).split(os.sep)
#     year = segments[-4]
#     topic = segments[-3]
#     language = segments[-2]
#     output_path = f"{year}-{topic}-{language}.mp3"
#     voice_name = "en-US-AndrewNeural"
#     # voice_name = AzureTTS.get_voice_name(language)
#     print(language)

#     try:
#         # Create Azure Audio
#         audio_sync = AudioSync(
#             json_path=json_path,
#             output_file_path= output_path,
#             language=language,
#             voice_name=voice_name)
#         audio_sync.convert_text_to_audio()
#     except Exception as e:
#         print(f"Failed to convert text to audio: {e}")
#         continue