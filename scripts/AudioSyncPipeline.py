from Parser import Parser
from AzureTTS import AzureTTS
from AudioManipulation import AudioManipulation
from Estimate import Estimate
import os
import pandas as pd
import time
import traceback

class AudioSync:
    def __init__(self, json_path, main_dir, output_file_path, language_averages_path):
        self.json_path = json_path
        self.main_dir = main_dir
        self.translations_folder_path = self.main_dir + "temp_audios"
        self.pause_audio_folder = self.main_dir + "temp_pauses"
        self.output_file_path = output_file_path
        
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
            print(text_list, "\n\n")
        except Exception as e:
            print(f"Failed to parse file: {e}")
            return

        # Get starting time
        start_time = time.time()

        # Convert text to speech
        azure_tts = AzureTTS()
        try:
            for i, text in enumerate(text_list):
                output_file = self.translations_folder_path + f'/azure_{i+1000}.mp3'
                azure_tts.convert_text_to_speech(text=text, filename=output_file)
        except Exception as e:
            print(f"Failed to convert text to speech using Azure TTS: {e}")
            return
        
        # Get ending time
        end_time = time.time()

        # Print time elapsed
        print(f"Time elapsed for Azure: {end_time - start_time} seconds")

        # Create pause audios and manipulate audio
        try:
            AudioManipulation.create_single_pause_audio(duration=start_timestamps[0], output_file=self.pause_audio_folder + "/pause_1000.wav")

            # Dataframe to store the speedup rates
            speedup_rates = pd.DataFrame(columns=[
                "idx", 
                "speedup_rate", 
                "start_time", 
                "end_time", 
                "original_duration", 
                "flag", 
                "character_count", 
                "original_character_count", 
                "translated_duration", 
                "estimated_duration", 
                "difference"
            ])

            # Manipulate audio
            for i in range(len(start_timestamps)-1):
                segment_duration = start_timestamps[i+1] - start_timestamps[i]
                translated_audio_length = AudioManipulation.get_audio_duration(audio_file=self.translations_folder_path + "/azure_" + str(i+1000) + ".mp3")

                # Estimated length of the translated text
                estimated_length = self.estimate.estimate_length(text_list[i], path=self.json_path)

                # Create pause audio file
                if segment_duration > translated_audio_length:
                    AudioManipulation.create_single_pause_audio(
                        duration=segment_duration - translated_audio_length,
                        output_file=self.pause_audio_folder + "/pause_" + str(i+1001) + ".wav")
                else:
                    speed_rate = translated_audio_length / segment_duration
                    if speed_rate > 1.5:
                        print(f'Warning: Speed rate is greater than 1.5: {speed_rate}')

                    # Convert text to speech with speed rate
                    text = text_list[i]
                    output_file = self.translations_folder_path + f'/azure_{i+1000}.mp3'
                    azure_tts.convert_text_to_speech(text=text, filename=output_file, speed_rate=speed_rate)


                    # Add information to speedup_rates dataframe via concatenation
                    speedup_rates = pd.concat([speedup_rates, pd.DataFrame({
                        "idx": i, # Index
                        "speedup_rate": [speed_rate], # Speedup rate
                        "start_time": [start_timestamps[i]], # Start time
                        "end_time": [start_timestamps[i+1]], # End time
                        "original_duration": [translated_audio_length], # How long the original audio was
                        "flag": [speed_rate >= 1.25], # Flag if speed rate is greater than 1.25
                        "character_count": [len(text)], # Number of characters in the text
                        "original_character_count": [len(original_text_list[i])], # Number of characters in the original text
                        "translated_duration": [translated_audio_length], # Duration of the translated audio
                        "estimated_duration": [estimated_length], # Estimated duration of the translated text
                        "difference": [abs(translated_audio_length - estimated_length)] # Difference between the estimated duration and the actual translated duration
                    })])

                    # Reset index
                    speedup_rates = speedup_rates.reset_index(drop=True)

                    # Create pause audio file
                    AudioManipulation.create_single_pause_audio(
                        duration=0,
                        output_file=self.pause_audio_folder + "/pause_" + str(i+1001) + ".wav")
        except Exception as e:
            print(traceback.format_exc())
            print(f"Failed to create pause audio files: {e}")
            return
        
        # Save speedup rates to a csv file. 
        try:
            # Get file extension of output file
            file_extension = self.output_file_path.split('.')[-1]
            try:
                # Save speedup rates to a csv file, replacing the file extension with _speedup_rates.csv
                speedup_rates.to_csv(self.output_file_path.replace(file_extension, "speedup_rates.csv"), index=False)

                # Print success message
                print(f"Speedup rates saved to {self.output_file_path.replace(file_extension, 'speedup_rates.csv')}")
            except IndexError:
                # No file extension
                speedup_rates.to_csv(self.output_file_path + "speedup_rates.csv", index=False)

                # Print success message
                print(f"Speedup rates saved to {self.output_file_path + 'speedup_rates.csv'}")
        except Exception as e:
            print("Failed to save speedup rates to a csv file: {e}")
            print(traceback.format_exc())
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
# json_path = r"path/to/json"
# main_dir = "path/to/main_dir"
# output_path = "path/to/output.wav"
# audio_sync = AudioSync(json_path, main_dir, output_path)
# audio_sync.convert_text_to_audio()