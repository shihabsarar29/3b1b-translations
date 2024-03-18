import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pathlib import Path
from edit_audio import EditAudio
from sync_pipeline import AudioSync
from rvc.rvc import infer

if __name__ == "__main__":
    
    translations_path = Path("/Users/shihab/Documents/3b1b/captions/2024/shorts/mandelbrot/spanish/sentence_translations.json")
    music_path = Path("/Users/shihab/Downloads/only_music.mp3")

    files_to_delete = []

    segments = translations_path.parts
    year, topic, language = segments[-4], segments[-3], segments[-2]
    azure_output_path = Path.cwd() / f"{year}-{topic}-{language}-azure.mp3"
    final_output_path = Path.cwd() / f"{year}-{topic}-{language}.mp3"
    voice_name = "en-US-AndrewNeural"

    try:
        audio_sync = AudioSync(
            json_path=str(translations_path),
            output_file_path=str(azure_output_path),
            language=language,
            voice_name=voice_name)
        audio_sync.convert_text_to_audio()

        files_to_delete.append(azure_output_path)

        rvc_output_filename = f"{topic}-{language}-rvc.mp3"

        infer(
            "init-experiment-2.pth",
            str(azure_output_path),
            str(rvc_output_filename),
            "logs/init-experiment-2/added_IVF4048_Flat_nprobe_1_init-experiment-2_v2.index", 0, -2, "rmvpe", 160, 3, 0, 1, 0.95, 0.33)

        rvc_output_path = Path.cwd() / Path("rvc/audio-outputs") / rvc_output_filename
        files_to_delete.append(rvc_output_path)

        EditAudio.overlap_audio(
            audio_path=str(rvc_output_path),
            music_path=str(music_path),
            output_path=str(final_output_path)
        )

    except Exception as e:
        print(f"Failed to process: {e}")

    for file_path in files_to_delete:
        try:
            file_path.unlink()
            print(f"Deleted: {file_path}")
        except OSError as e:
            print(f"Error deleting file {file_path}: {e}")
