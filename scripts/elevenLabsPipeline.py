from ElevenLabsAPI.elevenLabsAPI import elevenLabsAPI
from Parser import Parser
from AudioManipulation import AudioManipulation
import dotenv
import json
import fnmatch
import os
import random
import string
import pandas as pd
class elevenLabsPipeline:
    def __init__(self, path_to_transcripts: str, api_key: str = None, confirm_continuation: bool = True):
        self.path_to_transcripts = path_to_transcripts
        self.confirm_continuation = confirm_continuation
        self.audio_manipulation = AudioManipulation()

        if api_key:
            self.elevenLabsAPI = elevenLabsAPI(api_key=api_key)
        else:
            dotenv.load_dotenv()
            self.elevenLabsAPI = elevenLabsAPI(api_key=dotenv.get('ELEVEN_LABS_API_KEY'))
    
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
        
        # Sync the audio to the fulfillment JSON
        self.sync_audio(fulfillment_json_path, file_info)
        
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
    
    def get_valid_file_paths(self, fulfillment_json_path: str) -> list[str]:
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
                    valid_paths.append(f"{parent}/{child}")

        # Initialize an empty list to store the matching paths
        matching_paths = []

        # Walk through the directory structure
        for root, dirs, files in os.walk(self.path_to_transcripts):
            for file in files:
                # Get the relative path of the file from the root of the directory structure
                rel_path = os.path.relpath(os.path.join(root, file), self.path_to_transcripts)

                # If any valid path is a substring of the relative path, append it to the matching_paths list
                if any(valid_path in rel_path for valid_path in valid_paths):
                    matching_paths.append(rel_path)

        return matching_paths
    
    def generate_audio_to_file(self, utterances_list: list[str], intervals: list[float], output_folder: str, transcript_file_path: str) -> list[str]:
        """creates the audio files from the fulfillment JSON"""
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
        self.elevenLabsAPI.get_audio_to_file(utterances_list, output_file_path)

        # Generate the pause files into the temp_pause_file_folder
        self.audio_manipulation.batch_pause_audios(intervals, temp_pause_file_folder)

        # Create the final output path
        final_output_file_path = os.path.join(output_folder, "final_output.mp3")

        # Merge the audio and pause audio files into the output_folder
        self.audio_manipulation.merge_audio_and_pause_audio_folders(temp_audio_file_folder, temp_pause_file_folder, final_output_file_path)

        # Get the CSV file path
        csv_file_path = os.path.join(output_folder, "audio_sync " + self.__generate_random_string(20) + ".csv")

        # Sync the audio files to the fulfillment JSON
        self.sync_audio(transcript_file_path, temp_audio_file_folder, csv_file_path)

        return final_output_file_path, csv_file_path
    
    def sync_audio(self, transcript_file_path: str, temp_audio_file_folder: str, save_csv_to: str) -> None:
        """syncs the audio files to the fulfillment JSON"""

        # Create parser object
        parser = Parser(transcript_file_path)
        
        # Get intervals for each utterance
        intervals = Parser(transcript_file_path)

        # Dataframe to store information for each temp audio file
        df = pd.DataFrame(columns=["File Name", "Duration", "Difference", "Flag", "Severe Flag"])

        # Loop through each temp audio file
        for file in os.listdir(temp_audio_file_folder):
            # Initialize the series to store the information for the current temp audio file
            series = pd.Series()
        
            # Get basic information for the series
            series["File Name"] = file
            series["Duration"] = self.audio_manipulation.get_audio_duration(os.path.join(temp_audio_file_folder, file))
            series["Difference"] = -1 * (intervals[file] - series["Duration"])
            series["Flag"] = False
            series["Severe Flag"] = False

            # Get the duration of the audio file
            audio_duration = series["Duration"]
        
            # Get difference between the duration of the audio file and the duration of the utterance
            difference = series["Difference"]

             # If the audio segment is shorter, add silence to the end
            if difference < 0:
                self.audio_manipulation.add_silence_to_end(os.path.join(temp_audio_file_folder, file), audio_duration)

            # If this is less than 10% shorter than the duration of the utterance, speed it up to match the duration of the utterance
            elif difference < 0.1 * audio_duration and difference > 0:
                self.audio_manipulation.speed_up_audio(os.path.join(temp_audio_file_folder, file), audio_duration)
        
            # If this is 10-20% shorter than the duration of the utterance, speed it up and flag it
            elif difference < 0.2 * audio_duration and difference > 0:
                self.audio_manipulation.speed_up_audio(os.path.join(temp_audio_file_folder, file), audio_duration)
                series["Flag"] = True
        
            # If this is more than 20% shorter than the duration of the utterance, flag it and severely flag it
            elif difference > 0.2 * audio_duration and difference > 0:
                series["Flag"] = True
                series["Severe Flag"] = True
        
            # Overwrite the temp audio file with the new audio segment
            self.audio_manipulation.overwrite_audio_segment(os.path.join(temp_audio_file_folder, file), audio_duration)

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
        return 0.30

    def __generate_random_string(self, length: int) -> str:
        """generates a random string of the specified length"""
        return ''.join(random.choice(string.ascii_lowercase) for i in range(length))