from Parser import Parser
from AzureTTS import AzureTTS
from AudioManipulation import AudioManipulation
from Estimate import Estimate
import os
import traceback
from ElevenLabsAPI.elevenLabsAPI import elevenLabsAPI
import warnings
import json
import random
import json
from dotenv import load_dotenv
import string
import pandas as pd

class ElevenLabsPipeline:
    def __init__(self, path_to_transcripts: str, language_averages_path: str, api_key: str = None, confirm_continuation: bool = True, plan: str = "creator", voice_name: str = "Grant"):
        self.path_to_transcripts = path_to_transcripts
        self.confirm_continuation = confirm_continuation
        self.audio_manipulation = AudioManipulation()
        self.azureTTS = AzureTTS()
        self.plan = plan

        if api_key:
            self.elevenLabsAPI = elevenLabsAPI(api_key=api_key)
        else:
            load_dotenv()
            self.elevenLabsAPI = elevenLabsAPI(api_key=os.getenv("ELEVENLABS_API_KEY"))
        
        try:
            self.voice_name = self.elevenLabsAPI.get_voice_id(voice_name)
        except ValueError:
            warnings.warn(f"Voice name {voice_name} not found. Assuming it is a voice id.")
            self.voice_name = voice_name
        
        estimate = Estimate(language_averages_path)
        self.estimate = estimate

    def full_pipeline(self, fulfillment_json_path: str, output_folder: str) -> None:
        """the full pipeline to process the fulfillment JSON"""
        # Get the valid file paths from the fulfillment JSON
        valid_file_paths = self.get_valid_file_paths(fulfillment_json_path)

        # Confirm continuation
        if self.confirm_continuation:
            if not self.__confirm_continuation(valid_file_paths):
                return

        # Dictonary containing information on each file saved
        file_info = {}

        # Loop through each valid file path
        for path_to_transcript in valid_file_paths:
            # Generate the audio to file
            audio_file_path, csv_file_path = self.convert_text_to_audio(path_to_transcript, output_folder)
        
            # Add the file to the dictionary of information, alongside the path to the csv file
            file_info[audio_file_path] = {
                "csv_file_path": csv_file_path
            }
        
        # Return the dictionary of information
        return file_info

    def __confirm_continuation(self, valid_file_paths: list[str]) -> bool:
        """confirm that user wants to continue with the process despite the price estimate"""
        # Calculate the price estimate
        price_estimate = self.get_price_estimate(valid_file_paths)

        # Tell the user the price estimate
        print(f"The price estimate for generating the audio files is ${price_estimate} (assuming you have no leftover characters).")

        # Ask the user if they want to continue
        user_input = input("Do you want to continue? (y/n): ")

        # If the user wants to continue, return True
        if user_input.lower() == "y":
            return True
        else:
            return False

    def get_price_estimate(self, valid_file_paths: list[str]) -> float:
        """estimate the price of generating audio files"""
        # String to contain all the data
        all_string = ""

        # Create parser object
        for path_to_transcript in valid_file_paths:
            parser = Parser(path_to_transcript)

            # Get the full data
            full_data = parser.get_translated_texts_list()

            # Add the full data to the all_string
            all_string += ''.join(full_data)

        # Get the number of characters in the all_string variable
        full_data_characters = len(all_string)

        # Get the price per character based on the plan
        price_per_character = self.__price_per_character()

        # Return the price estimate
        return full_data_characters * price_per_character
    
    def get_valid_file_paths(self, fulfillment_json_path: str, json_target: str = "sentence_translations.json") -> list[str]:
        """gets the file paths to the valid audio files from the fulfillment JSON"""
        # Load the fulfillment JSON
        with open(fulfillment_json_path, 'r') as file:
            data = json.load(file)

        # Initialize an empty list to store the paths
        valid_paths = []

        # Iterate over each parent-child pair in the data
        for parent, children in data.items():
            for child, value in children.items():
                # If the value is True, append the parent-child pair to the list
                if value:
                    valid_paths.append(f"{parent}\\{child}\\{json_target}")

        # Initialize an empty list to store the matching paths
        matching_paths = []

        # Walk through the directory structure
        for root, dirs, files in os.walk(self.path_to_transcripts):
            for file in files:
                # Get the relative path of the file from the root of the directory structure
                rel_path = os.path.relpath(os.path.join(root, file), self.path_to_transcripts)

                # If any valid path is a substring of the relative path, append it to the matching_paths list
                if any(valid_path in rel_path for valid_path in valid_paths):
                    matching_paths.append(os.path.join(self.path_to_transcripts, rel_path))

        return matching_paths

    def convert_text_to_audio(self, transcript_file_path: str, output_folder: str, elevenLabs: bool = True, output_csv_file: str = "output.csv"):
        # Create Parser instance
        parser = Parser(transcript_file_path)

        # Extract basic information
        utterances_list = parser.get_translated_texts_list()
        intervals = parser.get_pause_direct()

        # Create the output folder
        os.makedirs(output_folder, exist_ok=True)

        # Get temp_audio_file_folder and temp_pause_file_folder
        temp_audio_file_folder = os.path.join(output_folder, "temp_audio_files")
        temp_pause_file_folder = os.path.join(output_folder, "temp_pause_files")

        # Create the temp_audio_file_folder and temp_pause_file_folder
        os.makedirs(temp_audio_file_folder, exist_ok=True)
        os.makedirs(temp_pause_file_folder, exist_ok=True)

        # Parse translations
        try:
            translator = Parser(transcript_file_path, json_encoding="utf-8")
            text_list = translator.get_translated_texts_list()
            original_text_list = translator.get_original_texts_list()
            try:
                start_timestamps = translator.get_start_timestamps()
                end_timestamps = translator.get_end_timestamps()
            except KeyError:
                start_timestamps = translator.get_start_timestamps_direct()
                end_timestamps = translator.get_end_timestamps_direct()
            print(text_list, "\n\n")
        except Exception as e:
            print(f"Failed to parse file: {e}")
            return

        # Create pause audios and manipulate audio
        try:
            AudioManipulation.create_single_pause_audio(duration=start_timestamps[0], output_file=os.path.join(temp_pause_file_folder, "pause_1000.wav"))

            accumulator = 0

            # Dataframe to store information for each temp audio file
            df = pd.DataFrame(columns=["File_Name", "Duration", "Difference", "Flag", "Severe_Flag", "Pause_Duration"])

            # Manipulate audio
            for i in range(len(start_timestamps)-1):
                # Initialize the series to store the information for the current iteration
                series = pd.Series()

                segment_duration = end_timestamps[i] - start_timestamps[i]

                # Estimated length of the translated text
                estimated_length = self.estimate.estimate_length(text_list[i], path=transcript_file_path)
                speed_rate = estimated_length / segment_duration
                if speed_rate > 1.05:
                    print(f'Warning: Speed rate is greater than 1.05: {speed_rate}')
                    speed_rate = 1.05

                elif speed_rate < 1:
                    speed_rate = 1

                # Convert text to speech with speed rate
                text = text_list[i]
                output_file = os.path.join(temp_audio_file_folder, f'azure_{i+1000}.mp3')
                print("passing in: ", output_file)
                if elevenLabs:
                    self.elevenLabsAPI.get_audio_to_file(text=text, output_file=output_file, speed_rate=speed_rate, voice_id=self.voice_name)
                else:
                    self.azureTTS.convert_text_to_speech(text=text, filename=output_file, speed_rate=speed_rate, voice_name=self.voice_name)
                translated_audio_length = AudioManipulation.get_audio_duration(output_file.replace(".mp3", ".wav"))


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
                    output_file=os.path.join(temp_pause_file_folder, "pause_" + str(i+1001) + ".wav"))
                
                # Get basic information for the series
                series["File_Name"] = output_file
                series["Duration"] = AudioManipulation.get_audio_duration(output_file.replace(".mp3", ".wav"))
                series["Difference"] = abs(segment_duration - series["Duration"])
                series["Flag"] = speed_rate > 1.1
                series["Severe_Flag"] = speed_rate > 1.2

                # Concatenate the series to the dataframe as a new row
                df = pd.concat([df, pd.DataFrame(series).transpose()], axis=0)
                df.reset_index()
                
            # Add the last audio
            # Initialize the series to store the information for the current iteration
            series = pd.Series()

            segment_duration = end_timestamps[-1] - start_timestamps[-1]
            estimated_length = self.estimate.estimate_length(text_list[-1], path=transcript_file_path)
            speed_rate = estimated_length / segment_duration
            if speed_rate > 1.05:
                print(f'Warning: Speed rate is greater than 1.05: {speed_rate}')
                speed_rate = 1.05
            elif speed_rate < 1:
                speed_rate = 1

            # Get basic information for the series
            series["File_Name"] = output_file
            series["Duration"] = AudioManipulation.get_audio_duration(output_file.replace(".mp3", ".wav"))
            series["Difference"] = abs(segment_duration - series["Duration"])
            series["Flag"] = speed_rate > 1.1
            series["Severe_Flag"] = speed_rate > 1.2

            # Convert text to speech with speed rate
            text = text_list[-1]
            output_file = os.path.join(temp_audio_file_folder, f'azure_{len(start_timestamps)+1000}.wav')
            self.elevenLabsAPI.get_audio_to_file(text=text, output_file=output_file, speed_rate=speed_rate, voice_id=self.voice_name)
            
            # Concatenate the series to the dataframe as a new row
            df = pd.concat([df, pd.DataFrame(series).transpose()], axis=0)
            df.reset_index()
        except Exception as e:
            print(traceback.format_exc())
            print(f"Failed to create pause audio files: {e}")
            return
        
        # Save the dataframe to a csv file
        #df.to_csv(save_csv_to, index=False)

        # Get the final output file path name
        output_name = transcript_file_path.split("\\")[-2] + "." + transcript_file_path.split("\\")[-3] + ".mp3"

        # Create the final output path
        final_output_file_path = os.path.join(output_folder, output_name)

        # Get the CSV file path
        csv_file_path = os.path.join(output_folder, output_csv_file)

        # Join audio
        try:
            AudioManipulation.join_audios(
                pause_audio_folder= temp_pause_file_folder,
                translated_audio_folder= temp_audio_file_folder,
                output_file_path=final_output_file_path)
        except Exception as e:
            print(f"Failed to join audios: {e}")
            return
        
        # Delete the temporary audio files
        self.garbage_disposal(temp_audio_file_folder, temp_pause_file_folder)

        # Save the dataframe to a csv file
        df.to_csv(csv_file_path, index=False)

        return final_output_file_path, csv_file_path

    def garbage_disposal(self, *folders_to_dispose) -> None:
        """deletes the temporary audio files"""
        # Loop through each folder to dispose
        for folder in folders_to_dispose:
            # Loop through each file in the folder
            for file in os.listdir(folder):
                # Delete the file
                os.remove(os.path.join(folder, file))

            # Delete the folder
            os.rmdir(folder)

    def __price_per_character(self) -> float:
        """returns the price per character based on the plan"""
        plan_prices = {
            "creator": 0.0003,
            "independent publisher": 0.00024,
            "growing business": 0.00018
        }

        return plan_prices[self.plan]

    def __generate_random_string(self, length: int) -> str:
        """generates a random string of the specified length"""
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

#'''
# Example usage
#json_path = r"C:\Users\sapat\Downloads\3b1b\API\Experiments\n_reviews_check\3b1bTranslationsP\2016\linear-transformations\spanish\sentence_translations.json"
#main_dir = r"C:\Users\sapat\Downloads\3b1b\API\temp" # where temp files will go
#output_path = "linear-transformations-spanish.mp3"
#language_averages_path = r"C:\Users\sapat\Downloads\3b1b\API\Experiments\n_reviews_check\3b1b_languages.json"
# voice_name = AzureTTS.get_voice_name("french")
#voice_name = "Grant"
#audio_sync = AudioSync(json_path, main_dir, output_path, language_averages_path, voice_name=voice_name)
#audio_sync.convert_text_to_audio()
#'''

# Example usage
elevenLabsPipeline = ElevenLabsPipeline(r"C:\Users\sapat\Downloads\3b1b\API\Experiments\n_reviews_check\3b1bTranslationsP", r"C:\Users\sapat\Downloads\3b1b\API\Experiments\average_count\3b1b_languages.json")
elevenLabsPipeline.full_pipeline(r"C:\Users\sapat\Downloads\3b1b\API\is_fulfilled.json", r"C:\Users\sapat\Downloads\3b1b\API\output_debug_full_pipeline")