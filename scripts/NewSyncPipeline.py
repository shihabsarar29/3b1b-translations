from Parser import Parser
from AzureTTS import AzureTTS
from AudioManipulation import AudioManipulation
from Estimate import Estimate
import os
import traceback

class AudioSync:
    def __init__(self, json_path, main_dir, output_file_path, language_averages_path, voice_name = "en-US-AndrewMultilingualNeural"):
        self.json_path = json_path
        self.main_dir = main_dir
        self.translations_folder_path = self.main_dir + "/temp_audios"
        self.pause_audio_folder = self.main_dir + "/temp_pauses"
        self.output_file_path = output_file_path
        self.voice_name = voice_name
        
        estimate = Estimate(language_averages_path)
        self.estimate = estimate

    def convert_text_to_audio(self):
        # Make directories
        os.makedirs(self.translations_folder_path, exist_ok=True)
        os.makedirs(self.pause_audio_folder, exist_ok=True)

        # Parse translations
        try:
            translator = Parser(self.json_path, json_encoding="utf-8")
            text_list = translator.get_translated_texts_list()
            original_text_list = translator.get_original_texts_list()
            start_timestamps = translator.get_start_timestamps()
            end_timestamps = translator.get_end_timestamps()
            print(text_list, "\n\n")
        except Exception as e:
            print(f"Failed to parse file: {e}")
            return

  

        # Create pause audios and manipulate audio
        try:
            AudioManipulation.create_single_pause_audio(duration=start_timestamps[0], output_file=self.pause_audio_folder + "/pause_1000.wav")

            azure_tts = AzureTTS()
            accumulator = 0

            # Manipulate audio
            for i in range(len(start_timestamps)-1):
                segment_duration = end_timestamps[i] - start_timestamps[i]

                # Estimated length of the translated text
                estimated_length = self.estimate.estimate_length(text_list[i], path=self.json_path)
                speed_rate = estimated_length / segment_duration
                if speed_rate > 1.05:
                    print(f'Warning: Speed rate is greater than 1.05: {speed_rate}')
                    speed_rate = 1.05

                elif speed_rate < 1:
                    speed_rate = 1

                # Convert text to speech with speed rate
                text = text_list[i]
                output_file = self.translations_folder_path + f'/azure_{i+1000}.mp3'
                azure_tts.convert_text_to_speech(text=text, filename=output_file, speed_rate=speed_rate, voice_name=self.voice_name)
                translated_audio_length = AudioManipulation.get_audio_duration(output_file)


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

                
                AudioManipulation.create_single_pause_audio(
                    duration=pause_duration,
                    output_file=self.pause_audio_folder + "/pause_" + str(i+1001) + ".wav")
                
            # Add the last audio
            segment_duration = end_timestamps[-1] - start_timestamps[-1]
            estimated_length = self.estimate.estimate_length(text_list[-1], path=self.json_path)
            speed_rate = estimated_length / segment_duration
            if speed_rate > 1.05:
                print(f'Warning: Speed rate is greater than 1.05: {speed_rate}')
                speed_rate = 1.05

            elif speed_rate < 1:
                speed_rate = 1

            # Convert text to speech with speed rate
            text = text_list[-1]
            output_file = self.translations_folder_path + f'/azure_{len(start_timestamps)+1000}.mp3'
            azure_tts.convert_text_to_speech(text=text, filename=output_file, speed_rate=speed_rate)

        except Exception as e:
            print(traceback.format_exc())
            print(f"Failed to create pause audio files: {e}")
            return
        

        # Join audio
        try:
            AudioManipulation.join_audios(
                pause_audio_folder= self.pause_audio_folder,
                translated_audio_folder= self.translations_folder_path,
                output_file_path= self.output_file_path)
        except Exception as e:
            print(f"Failed to join audios: {e}")
            return
        
        # Try cleaning with command line
        try:
            os.system(f'rm -rf {self.pause_audio_folder}')
            os.system(f'rm -rf {self.translations_folder_path}')
            return
        except Exception:
            pass

        # Try deleting folders directly
        try:
            os.rmdir(self.pause_audio_folder)
            os.rmdir(self.translations_folder_path)
            return
        except Exception as e:
            pass

        # If not, likely there are files in the folders.
        # Deleting all files in the folders
        try:
            for file in os.listdir(self.pause_audio_folder):
                os.remove(self.pause_audio_folder + "/" + file)
            for file in os.listdir(self.translations_folder_path):
                os.remove(self.translations_folder_path + "/" + file)
        except Exception as e:
            print(f"Failed to delete files in the folders: {e}")
            return
        
        # Try to delete folders directly again
        try:
            os.rmdir(self.pause_audio_folder)
            os.rmdir(self.translations_folder_path)
            return
        except Exception as e:
            print(f"Failed to delete folders: {e}")
            return


# Example usage
json_path = r"/Users/shihab/Documents/3b1b/captions/2016/linear-transformations/spanish/sentence_translations.json"
main_dir = "captions"
output_path = "linear-transformations-spanish.mp3"
language_averages_path = "/Users/shihab/Documents/3b1b/3b1b-translations/Experiments/average_count/3b1b_languages.json"
# voice_name = AzureTTS.get_voice_name("french")
voice_name = "en-US-AndrewMultilingualNeural"
audio_sync = AudioSync(json_path, main_dir, output_path, language_averages_path, voice_name=voice_name)
audio_sync.convert_text_to_audio()