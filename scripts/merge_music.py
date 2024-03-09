from typing import Union
from pydub import AudioSegment
import os

class MergeMusic:
    """ Contains utilites for merging music and audio """
    def __init__(self):
        pass

    def merge(self, audio_path: str, music_path: str, output_path: str, audio_volume_offset: int, format: str, crop: bool = False) -> None:
        """ Merges the audio and music together. """
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

    def merge_batch(self, audio_paths: Union[list[str], str], music_paths: Union[list[str], str], output_paths: Union[list[str], str], audio_volume_offset: int, format: str = "mp3", output_file_names: str = "output", crop: bool = False) -> None:
        """ Merges the audio and music together in batch. If the paths are strings, then the function will assume that the paths are directories and will merge all the files in the directories together. If the paths are lists, then the function will assume that the paths are files and will merge the files together."""
        
        if isinstance(audio_paths, list) and isinstance(music_paths, list) and isinstance(output_paths, list):
            self.__merge_batch_files(audio_paths, music_paths, output_paths, audio_volume_offset, format, crop=crop)
        elif isinstance(audio_paths, str) and isinstance(music_paths, str) and isinstance(output_paths, str):
            self.__merge_batch_dirs(audio_paths, music_paths, output_paths, output_file_names, audio_volume_offset, format, crop=crop)
        else:
            raise ValueError("The audio, music, and output paths must be either all strings or all lists")

    def __merge_batch_dirs(self, audio_dir: str, music_dir: str, output_dir: str, output_file_names: str, audio_volume_offset: int, format: str, crop: bool = False) -> None:
        """ Merges the audio and music together in batch """
        for idx, (audio, music) in enumerate(zip(os.listdir(audio_dir), os.listdir(music_dir))):
            # Merge the audio and music together
            self.merge(os.path.join(audio_dir, audio), os.path.join(music_dir, music), os.path.join(output_dir, f"{output_file_names}_{idx}.mp3"), audio_volume_offset, format, crop=crop)

    def __merge_batch_files(self, audio_file: list[str], music_file: list[str], output_files: list[str],  audio_volume_offset: int, format: str, crop: bool = False) -> None:
        """ Merges the audio and music together in batch """

        # Loop through the audio and music files
        for audio, music, output in zip(audio_file, music_file, output_files):
            # Merge the audio and music together
            self.merge(audio, music, output, audio_volume_offset, format, crop=crop)

# Example usage
# Merge the audio and music together
merge_music = MergeMusic()
merge_music.merge(r"C:\Users\sapat\Downloads\3b1b\API\scripts\background.mp3", r"C:\Users\sapat\Downloads\3b1b\API\scripts\foreground.mp3", "output.mp3", -20, "mp3")