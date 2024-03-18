import os
from pydub import AudioSegment

class EditAudio:
    """
    A class to edit audio files.
    """
    
    @staticmethod
    def create_single_pause_audio(duration: float, output_file: str) -> None:
        """
        This method creates a single pause audio file based on the given duration.
        
        Args:
            duration: A float, the duration of the pause.
            output_file: A string, The path where the pause audio file will be saved.
            
        Returns:
        - This method does not return anything. It saves a pause audio file to the specified location.
        """
        # Create the pause audio file
        pause_audio = AudioSegment.silent(duration=duration * 1000)  
        pause_audio.export(output_file, format="wav")
        print(f"Pause audio file created at {output_file} with duration: {duration} seconds\n")

    

    @staticmethod
    def join_audios(pause_audio_folder: str, translated_audio_folder: str, output_file_path: str) -> None:
        """
        This method joins the pause audio files and translated audio files together.
        
        Args:
            pause_audio_folder: A string, the path to the directory containing the pause audio files.
            translated_audio_folder: A string, the directory containing the translated audio files.
            output_file_path: A string, the path where the final joined audio file will be saved.
            
        Returns:
        - This method does not return anything. It saves the joined audio file to the specified location.
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
        This method gets the duration of an audio file.
        
        Args:
            audio_file: A string, the path to the audio file.
            format: A string, the format of the audio file. Default is "mp3".
            
        Returns:
        - A float, the duration of the audio file in seconds.
        """

        # Load the audio file
        audio = AudioSegment.from_file(audio_file_path, format=format)
        return audio.duration_seconds
    
    @staticmethod
    def overlap_audio(audio_path: str, music_path: str, output_path: str, audio_volume_offset: int = 0, format: str = "mp3", crop: bool = False) -> None:
        """
        This method overlays the audio and music together.

        Args:
            audio_path: A string, the path to the audio file.
            music_path: A string, the path to the music file.
            output_path: A string, the path where the combined audio file will be saved.
            audio_volume_offset: An integer, the amount to increase the volume of the music. Default is -20.
            format: A string, the format of the audio file. Default is "mp3".
            crop: A boolean, whether to crop the music to the length of the audio. Default is False.

        Returns:
        - This method does not return anything. It saves the combined audio file to the specified location.
        """
        # Load the audio and music
        audio = AudioSegment.from_file(audio_path)
        music = AudioSegment.from_file(music_path)

        # If the music is shorter than the audio, append silence to the end of the music
        if len(music) < len(audio) and not crop:
            silence = AudioSegment.silent(duration=len(audio) - len(music))
            music = music + silence
        
        # Make music audio_volume_offset dB louder
        music = music.apply_gain(audio_volume_offset)

        # Overlay the audio and music
        combined = music.overlay(audio)

        # Export the combined audio
        combined.export(output_path, format=format)

        print(f"Combined audio file created at {output_path}")
    
    