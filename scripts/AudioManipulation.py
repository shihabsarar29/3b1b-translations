import os
from pydub import AudioSegment

class AudioManipulation:
    """
    ## AudioManipulation
    AudioManipulation class provides methods for manipulating audio files. Useful when trying to match translated audio with visuals.
    
    ### Methods:
    - create_single_pause_audio
    - join_audios
    """
    
    @staticmethod
    def create_single_pause_audio(duration: float, output_file: str) -> None:
        """
        ### create_single_pause_audio
        Creates a single pause audio file based on the given duration.
        
        #### Args:
            duration ```float```: 
                The duration of the pause.
            output_file ```str```: 
                The path where the pause audio file will be saved.
            
        #### Returns:
        - ```None```
        """
        # Create the pause audio file
        pause_audio = AudioSegment.silent(duration=duration * 1000)  
        pause_audio.export(output_file, format="wav")
        print(f"Pause audio file created at {output_file} with duration: {duration} seconds\n")

    

    @staticmethod
    def join_audios(pause_audio_folder: str, translated_audio_folder: str, output_file_path: str) -> None:
        """
        ### join_audios
        Joins pause audio files and translated audio files together.
        
        #### Args:
            pause_audio_files ```str```: 
                The folder to the pause audio files that will be joined with the translated audio files.
            translated_audio_files ```str```: 
                The folder to the translated audio files that will be joined with the pause audio files.
            output_file_path ```str```: 
                The path where the final audio file will be saved.
            
        #### Returns:
        - ```None```
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


    # @staticmethod
    def get_audio_duration(audio_file: str, format: str="mp3") -> float:
        """
        ### get_audio_duration
        Gets the duration of an audio file.
        
        #### Args:
            audio_file ```str```: 
                The audio file to get the duration of.
            
        #### Returns:
        - ```float```: The duration of the audio file in seconds.
        """

        # Load the audio file
        audio = AudioSegment.from_file(audio_file, format=format)
        return audio.duration_seconds
    
