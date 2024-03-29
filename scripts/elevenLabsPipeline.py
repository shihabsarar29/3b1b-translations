from ElevenLabsAPI.elevenLabsAPI import elevenLabsAPI
from Parser import Parser
from AudioManipulation import AudioManipulation
from dotenv import load_dotenv
import json
import fnmatch
import os
import random
import string
import pandas as pd
from AzureTTS import AzureTTS

class ElevenLabsPipeline:
    def __init__(self, path_to_transcripts: str, api_key: str = None, confirm_continuation: bool = True, plan: str = "creator"):
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
            audio_file_path, csv_file_path = self.generate_audio_to_file(path_to_transcript, output_folder)
        
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
    
    def generate_audio_to_file(self, transcript_file_path: str, output_folder: str, elevenLabs: bool = True, output_csv_file: str = "output.csv") -> list[str]:
        """creates the audio files from the fulfillment JSON"""
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

        # Get the output file path template for the eleven labs wrapper to use
        output_file_path = os.path.join(temp_audio_file_folder, "output")

        # Generate the audio files to the temp_audio_file_folder
        if elevenLabs:
            self.elevenLabsAPI.get_voice_id("Rachel", inPlace=True)
            self.elevenLabsAPI.get_audio_to_file(utterances_list, output_file_path)
        else:
            self.azureTTS.convert_text_to_speech_list(utterances_list, filename=output_file_path)

        # Generate the pause files into the temp_pause_file_folder
        self.audio_manipulation.batch_pause_audios(intervals, temp_pause_file_folder)

        # Get the final output file path name
        output_name = transcript_file_path.split("\\")[-2] + "." + transcript_file_path.split("\\")[-3] + ".mp3"

        # Create the final output path
        final_output_file_path = os.path.join(output_folder, output_name)

        # Get the CSV file path
        csv_file_path = os.path.join(output_folder, output_csv_file)

        # Sync the audio files to the fulfillment JSON
        self.sync_audio(transcript_file_path, temp_audio_file_folder, csv_file_path)

        # Merge the audio and pause audio files into the output_folder
        self.audio_manipulation.merge_audio_and_pause_audio_folders(temp_audio_file_folder, temp_pause_file_folder, final_output_file_path)

        # Sync the audio files to the fulfillment JSON
        #self.sync_audio(transcript_file_path, temp_audio_file_folder, csv_file_path)

        return final_output_file_path, csv_file_path
    
    def sync_audio(self, transcript_file_path: str, temp_audio_file_folder: str, save_csv_to: str) -> None:
        """syncs the audio files to the fulfillment JSON"""

        # Create parser object
        parser = Parser(transcript_file_path)
        
        # Get intervals for each utterance
        intervals = parser.get_interval_direct()

        # Dataframe to store information for each temp audio file
        df = pd.DataFrame(columns=["File_Name", "Duration", "Difference", "Flag", "Severe_Flag"])

        # Loop through each temp audio file
        for idx, file in enumerate(os.listdir(temp_audio_file_folder)):
            # Initialize the series to store the information for the current temp audio file
            series = pd.Series()

            # Get the full path to the temp audio file
            file_path = os.path.join(temp_audio_file_folder, file)
            
            # Create instance of AudioManipulation
            audio_manipulation = AudioManipulation()

            # Get target (original english) length
            original_length = intervals[idx]
        
            # Get basic information for the series
            series["File_Name"] = file
            series["Duration"] = audio_manipulation.get_audio_duration(file_path)
            series["Difference"] = abs(original_length - series["Duration"])
            series["Flag"] = False
            series["Severe_Flag"] = False

            # Get the duration of the audio file
            audio_duration = series["Duration"]
        
            # Get difference between the duration of the audio file and the duration of the utterance
            difference = series["Difference"]

            print("difference: ", difference)
            print("audio_duration: ", audio_duration)
            print("original_length: ", original_length)
            print("10%: ", 0.1 * audio_duration)
            print("20%: ", 0.2 * audio_duration)

            # If the audio segment is shorter, add silence to the end
            if difference < 0:
                self.audio_manipulation.add_silence_to_end(os.path.join(temp_audio_file_folder, file), abs(difference))

            # If this is less than 10% shorter than the duration of the utterance, speed it up to match the duration of the utterance
            elif difference < 0.1 * audio_duration and difference > 0:
                print("speeding up by: ", 1 + (original_length / audio_duration))
                self.elevenLabsAPI._speed_up(os.path.join(temp_audio_file_folder, file), 1 + (original_length / audio_duration))
        
            # If this is 10-20% shorter than the duration of the utterance, speed it up and flag it
            elif difference < 0.2 * audio_duration and difference > 0:
                print("speeding up by: ", 1 + (original_length / audio_duration))
                self.elevenLabsAPI._speed_up(os.path.join(temp_audio_file_folder, file), 1 + (original_length / audio_duration))
                series["Flag"] = True
        
            # If this is more than 20% shorter than the duration of the utterance, flag it and severely flag it
            elif difference > 0.2 * audio_duration and difference > 0:
                print("speeding up by: ", 1 + (original_length / audio_duration))
                self.elevenLabsAPI._speed_up(os.path.join(temp_audio_file_folder, file), 1 + (original_length / audio_duration))
                series["Flag"] = True
                series["Severe_Flag"] = True
        
            # Overwrite the temp audio file with the new audio segment
            #self.audio_manipulation.overwrite_audio_segment(os.path.join(temp_audio_file_folder, file), file_path)

            # Concatenate the series to the dataframe as a new row
            df = pd.concat([df, pd.DataFrame(series).transpose()], axis=0)
            df.reset_index()

        # Save the dataframe to a csv file
        df.to_csv(save_csv_to, index=False)

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

""" TESTING """
elevenLabsPipeline = ElevenLabsPipeline(r"C:\Users\sapat\Downloads\3b1b\API\Experiments\n_reviews_check\3b1bTranslationsP")

# Check if get_valid_file_paths works
# print(elevenLabsPipeline.get_valid_file_paths(r"C:\Users\sapat\Downloads\3b1b\API\is_fulfilled.json"))
elevenLabsPipeline.full_pipeline(r"C:\Users\sapat\Downloads\3b1b\API\is_fulfilled.json", r"C:\Users\sapat\Downloads\3b1b\API\output_debug_full_pipeline")