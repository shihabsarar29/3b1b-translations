import os
from pydub import AudioSegment
from typing import Union

class AudioManipulation:
    """
    AudioManipulation class provides methods for manipulating audio files. Useful when trying to match translated audio with visuals.
    
    Methods:
        create_single_pause_audio
        join_audios
    """
    
    @staticmethod
    def create_single_pause_audio(duration: float, output_file: str) -> None:
        """
        Creates a single pause audio file based on the given duration.
        
        Args:
            duration (float): The duration of the pause.
            output_file (str): The path where the pause audio file will be saved.
            
        Returns:
            (None)
        """
        # Create the pause audio file
        pause_audio = AudioSegment.silent(duration=duration * 1000)  
        pause_audio.export(output_file, format="wav")
        print(f"Pause audio file created at {output_file} with duration: {duration} seconds\n")

    

    @staticmethod
    def join_audios(pause_audio_folder: str, translated_audio_folder: str, output_file_path: str) -> None:
        """
        Joins pause audio files and translated audio files together.
        
        Args:
            pause_audio_files (str): The folder to the pause audio files that will be joined with the translated audio files.
            translated_audio_files (str): The folder to the translated audio files that will be joined with the pause audio files.
            output_file_path (str): The path where the final audio file will be saved.
            
        Returns:
            (None)
        """
        pause_audio_files = [filename for filename in os.listdir(pause_audio_folder)]
        translated_audio_files = [filename for filename in os.listdir(translated_audio_folder)]

        # Sort the pause and translated audio files
        pause_audio_files.sort()
        translated_audio_files.sort()

        # Create an empty audio segment
        final_audio = AudioSegment.silent(duration=0)

        # Join the pause and translated audio files
        for pause_file, translate_file in zip(pause_audio_files, translated_audio_files):
            pause_audio = AudioSegment.from_file(os.path.join(pause_audio_folder, pause_file))
            translated_audio = AudioSegment.from_file(os.path.join(translated_audio_folder, translate_file))
            final_audio += pause_audio + translated_audio

        # Save the final audio file
        final_audio.export(output_file_path, format="wav")
        print(f"Final audio file created at {output_file_path}")


    @staticmethod
    def get_audio_duration(audio_file_path: str, format: str="mp3") -> float:
        """
        Gets the duration of an audio file.
        
        Args:
            audio_file (str): The audio file to get the duration of.
            
        Returns:
            (float): The duration of the audio file in seconds.
        """

        # Load the audio file
        audio = AudioSegment.from_file(audio_file_path, format=format)
        return audio.duration_seconds
    
    def batch_pause_audios(self, pause_durations: list[float], output_folder: str) -> None:
        """
        Creates multiple pause audio files based on the given durations.
        
        Args:
            pause_durations (list[float]): The durations of the pause audio files.
            output_folder (str): The folder where the pause audio files will be saved.
                
        Returns:
            (None)
        """
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Create the pause audio files
        for idx, duration in enumerate(pause_durations):
            output_file = os.path.join(output_folder, f"pause_{idx}.wav")
            self.create_single_pause_audio(duration, output_file)
    
    def merge_audio_and_pause_audio_folders(self, audio_folder: str, pause_audio_folder: str, output_file: str, format: str = "wav") -> None:
        """
        merge_audio_and_pause_audio_folders
        Merges audio and pause audio files to create full audio clip.

        Args:
            audio_folder (str): The folder to the audio files that will be merged with the pause audio files.
            pause_audio_folder (str): The folder to the pause audio files that will be merged with the audio files.
            output_file (str): The path where the final audio file will be saved.

        Returns:
            (None)
        """

        # Get the audio and pause audio files
        audio_files = [filename for filename in os.listdir(audio_folder)]
        pause_audio_files = [filename for filename in os.listdir(pause_audio_folder)]

        # Sort the audio and pause audio files
        audio_files.sort()
        pause_audio_files.sort()

        # Audio segment for the final audio
        final_audio = AudioSegment.silent(duration=0)

        # Create folder for temporary audio files
        temp_audio_file_folder = os.path.join(os.getcwd(), ".temp_audio_files")

        # Create the temporary audio file folder if it doesn't exist
        os.makedirs(temp_audio_file_folder, exist_ok=True)

        # Copy the audio files to the output folder
        for audio_file, pause_audio_file in zip(audio_files, pause_audio_files):
            audio_file_path = os.path.join(audio_folder, audio_file)
            pause_audio_file_path = os.path.join(pause_audio_folder, pause_audio_file)

            # Load the audio and pause audio files
            audio = AudioSegment.from_file(audio_file_path)
            pause_audio = AudioSegment.from_file(pause_audio_file_path)

            # Join the audio and pause audio files
            audio = pause_audio + audio

            # Save the audio file to the temporary folder
            audio.export(os.path.join(temp_audio_file_folder, audio_file), format="wav")
        
        # Loop through temporary audio files and join them
        for idx, file in enumerate(os.listdir(temp_audio_file_folder)):
            if idx == 0:
                final_audio = AudioSegment.from_file(os.path.join(temp_audio_file_folder, file), format=format)
            else:
                final_audio += AudioSegment.from_file(os.path.join(temp_audio_file_folder, file), format=format)
        
        # Save the final audio file
        final_audio.export(output_file, format="wav")
        
        # Delete every file within temp_audio_file_folder
        for file in os.listdir(temp_audio_file_folder):
            os.remove(os.path.join(temp_audio_file_folder, file))
        
        # Delete the temp_audio_file_folder
        os.rmdir(temp_audio_file_folder)

    def overwrite_audio_segment(self, audio_file_overwrite: str, audio_segment: Union[str, AudioSegment], format: str = "mp3") -> None:
        """
        Overwrites the audio segment of the audio file.
        
        Args:
            audio_file_overwrite (str): The audio file to overwrite.
            audio_segment (AudioSegment): The audio segment to overwrite the audio file with.
            format (str): The format of the audio file.
            
        Returns:
            (None)
        """
        if isinstance(audio_segment, str):
            audio_segment = AudioSegment.from_file(audio_segment, format=format)
        
        # Save the audio segment to the audio file
        audio_segment.export(audio_file_overwrite, format=format)
    
    def add_silence_to_end(self, path: str, seconds: float, format: str = "mp3"):
        """
        Adds silence to the end of the audio file.
        
        Args:
            path (str): The path to the audio file.
            seconds (float): The duration of the silence to add to the end of the audio file.
            
        Returns:
            (None)
        """
        # Load the audio file
        audio = AudioSegment.from_file(path, format=format)

        # Add silence to the end of the audio file
        silence = AudioSegment.silent(duration=seconds * 1000)
        audio += silence

        # Save the audio file
        audio.export(path, format=format)
    
    def speed_up_audio(self, file_path: str, rate: float, format: str = "mp3"):
        """
        Speeds up the audio file.
        
        Args:
            file_path (str): The path to the audio file.
            rate (float): The rate to speed up the audio file by.
            
        Returns:
            (None)
        """
        # Load the audio file
        audio = AudioSegment.from_file(file_path, format=format)

        # Speed up the audio file
        audio = audio.speedup(playback_speed=rate)

        # Save the audio file
        audio.export(file_path, format=format)