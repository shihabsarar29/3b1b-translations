import sys
sys.path.insert(0, sys.path[0] + '/../../')
from scripts.AudioSyncPipeline import AudioSync


# Example usage
main_dir = "Experiments/Audio-Modify/"
json_path = main_dir + "sentence_translations.json"
output_file = main_dir + "output.mp3"
audio_sync = AudioSync(json_path, main_dir, output_file)
audio_sync.convert_text_to_audio()