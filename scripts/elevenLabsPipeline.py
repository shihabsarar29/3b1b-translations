from ElevenLabsAPI.elevenLabsAPI import elevenLabsAPI
from Parser import Parser
from AudioManipulation import AudioManipulation
import dotenv
import json
import fnmatch
import os

class elevenLabsPipeline:
    def __init__(self, path_to_transcripts: str, api_key: str = None, eleven_labs_plan: str = "starter", confirm_continuation: bool = True):
        self.path_to_transcripts = path_to_transcripts
        self.eleven_labs_plan = eleven_labs_plan.lower()
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

        # Confirm continuation

        # List of files saves

        # Loop through each valid file path

            # Generate the audio to file
        
            # Add the file to the list of files saved
        

        pass

    def __confirm_continuation(self, price_estimate: float) -> bool:
        """confirm that user wants to continue with the process despite the price estimate"""
        # Calculate the price estimate

        # Tell the user the price estimate

        # Ask the user if they want to continue
        pass

    def get_price_estimate(self, full_data: list[str]) -> float:
        """estimate the price of generating audio files"""
        # Get the number of characters in the full_data

        # Get the price per character based on the plan

        # Return the price estimate
        pass
    
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
    
    def generate_audio_to_file(self, utterances_list: list[str], intervals: list[float], output_folder: str) -> str:
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

        return final_output_file_path
    
    def sync_audio(self, transcript_file_path: str, temp_audio_file_folder: str, save_csv_to: str) -> None:
        """syncs the audio files to the fulfillment JSON"""

        # Get intervals for each utterance

        # Dataframe to store information for each temp audio file

        # Loop through each temp audio file

            # Initialize the series to store the information for the current temp audio file
        
            # Get basic information for the series

            # Get the duration of the audio file
        
            # Get difference between the duration of the audio file and the duration of the utterance\
        
            # If this is less than 10% shorter than the duration of the utterance, speed it up
        
            # If this is 10-20% shorter than the duration of the utterance, speed it up and flag it
        
            # If this is more than 20% shorter than the duration of the utterance, flag it and severely flag it
        
            # If the audio segment is shorter, add silence to the end
        
            # Overwrite the temp audio file with the new audio segment

        # Save the dataframe to a csv file
        pass

    def garbage_disposal(self, *folders_to_dispose) -> None:
        """deletes the temporary audio files"""
        # Loop through each folder to dispose
            
                # Loop through each file in the folder
    
                    # Delete the file
    
                # Delete the folder

        pass

    def __price_per_character(self) -> float:
        """returns the price per character based on the plan"""
        pass