import os
import json
from pydub import AudioSegment

class AudioManipulation:
    """
    ## AudioManipulation
    AudioManipulation class provides methods for manipulating audio files. Useful when trying to match translated audio with visuals.
    
    ### Methods:
        - adjust_speed_based_on_json(translated_file_path: str, json_file_path: str, output_file_path: str) -> None
        - create_pause_audio(start_timestamps: List[int], output_directory: str, duration: int) -> None
        - join_audios(pause_audio_files: List[str], translated_audio_files: List[str], output_file_path: str) -> None
    """
    
    @staticmethod
    def adjust_speed_based_on_json(translated_file_path: str, json_file_path: str, output_file_path: str):
        """
        ### adjust_speed_based_on_json
        Adjusts the speed of an audio file based on the data from a JSON file.
        
        #### Args:
        translated_file_path ```str```: 
            The path to the translated audio file.
         json_file_path ```str```: 
            The path to the JSON file containing the data for speed adjustment.
        output_file_path ```str```: 
            The path where the adjusted audio file will be saved.
            
        #### Returns:
        - ```None```
        """
        
        # Convert relative paths to absolute paths
        translated_file_path = os.path.abspath(translated_file_path)
        json_file_path = os.path.abspath(json_file_path)

        # Load data from the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Extract time range from the data
        if data:
            time_range = data[4].get("time_range", [0, None])
            start = time_range[0]
            end = time_range[1] if len(time_range) > 1 else None

        # Load the translated audio file
        translated_audio = AudioSegment.from_file(translated_file_path, format="mp3")
        translated_audio_length = translated_audio.duration_seconds

        # Calculate the length ratio
        length_ratio =  translated_audio_length / (end - start)

        # Determine the speed factor
        if length_ratio >= 1:
            speed_factor = 1.0 * length_ratio
        else:
            speed_factor = 1.0

        # Adjust the speed of the audio
        if speed_factor >= 1:
            adjusted_audio = translated_audio.speedup(playback_speed=speed_factor)
        else:
            adjusted_audio = translated_audio._spawn(translated_audio.raw_data, overrides={
                "frame_rate": int(translated_audio.frame_rate * 1)
            }).set_frame_rate(translated_audio.frame_rate)

        # Save the adjusted audio file
        output_file_path = os.path.join(output_file_path, "adjusted_translated_audio.mp3")
        adjusted_audio.export(output_file_path, format="mp3")  

    @staticmethod
    def create_pause_audio(start_timestamps: list[int], output_directory: str, duration: float):
        """
        ### create_pause_audio
        Creates pause audio files based on the given start timestamps and duration.
        
        #### Args:
            start_timestamps ```list[int]```: 
                The start timestamps for the pauses.
            output_directory ```str```: 
                The directory where the pause audio files will be saved.
            duration ```float```: 
                The duration of the pauses.
            
        #### Returns:
        - ```None```
        """
        # Create the output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        start_timestamps.sort()

        # Create pause audio files
        for i in range(1, len(start_timestamps)):
            segment_duration = start_timestamps[i] - start_timestamps[i - 1] - duration
            pause_audio = AudioSegment.silent(duration=segment_duration * 1000)  
            output_file_path = os.path.join(output_directory, f"pause_{i}.wav")
            pause_audio.export(output_file_path, format="mp3", codec="libmp3lame")

    @staticmethod
    def join_audios(pause_audio_files: list[str], translated_audio_files: list[str], output_file_path: str):
        """
        ### join_audios
        Joins pause audio files and translated audio files together.
        
        #### Args:
            pause_audio_files ```list[str]```: 
                The pause audio files to be joined.
            translated_audio_files ```list[str]```: 
                The translated audio files to be joined.
            output_file_path ```str```: 
                The path where the final audio file will be saved.
            
        #### Returns:
        - ```None```
        """
        # Create an empty audio segment
        final_audio = AudioSegment.silent(duration=0)

        # Join the pause and translated audio files
        for pause_file, translate_file in zip(pause_audio_files, translated_audio_files):
            pause_audio = AudioSegment.from_file(pause_file)
            translated_audio = AudioSegment.from_file(translate_file)
            final_audio += pause_audio + translated_audio

        # Save the final audio file
        final_audio.export(output_file_path, format="mp3")