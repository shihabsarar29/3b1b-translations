from scripts.Parser import Parser
from scripts.AzureTTS import AzureTTS
from scripts.AudioManipulation import AudioManipulation
import os

class AudioSync:
    def __init__(self, json_path, main_dir, output_file_path):
        self.json_path = json_path
        self.main_dir = main_dir
        self.translations_folder_path = self.main_dir + "temp_audios"
        self.pause_audio_folder = self.main_dir + "temp_pauses"
        self.output_file_path = output_file_path

    def convert_text_to_audio(self):
        # Make directories
        os.makedirs(self.translations_folder_path, exist_ok=True)
        os.makedirs(self.pause_audio_folder, exist_ok=True)

        # Parse translations
        try:
            translator = Parser(self.json_path)
            text_list = translator.get_translated_texts_list()
            start_timestamps = translator.get_start_timestamps()
            print(text_list, "\n\n")
        except Exception as e:
            print(f"Failed to parse file: {e}")
            return

        # Convert text to speech
        print("Azure TTS")
        azure_tts = AzureTTS()
        try:
            for i, text in enumerate(text_list):
                output_file = self.translations_folder_path + f'/azure_{i+1000}.mp3'
                azure_tts.convert_text_to_speech(text=text, filename=output_file)
        except Exception as e:
            print(f"Failed to convert text to speech using Azure TTS: {e}")
            return

        # Create pause audios and manipulate audio
        try:
            AudioManipulation.create_single_pause_audio(duration=start_timestamps[0], output_file=self.pause_audio_folder + "/pause_1000.wav")
            # Manipulate audio
            for i in range(len(start_timestamps)-1):
                segment_duration = start_timestamps[i+1] - start_timestamps[i]
                translated_audio_length = AudioManipulation.get_audio_duration(audio_file=self.translations_folder_path + "/azure_" + str(i+1000) + ".mp3")

                # Create pause audio file
                if segment_duration > translated_audio_length:
                    AudioManipulation.create_single_pause_audio(
                        duration=segment_duration - translated_audio_length,
                        output_file=self.pause_audio_folder + "/pause_" + str(i+1001) + ".wav")
                else:
                    speed_rate = translated_audio_length / segment_duration
                    if speed_rate > 1.5:
                        print(f'Warning: Speed rate is greater than 1.5: {speed_rate}')

                    # Convert text to speech with speed rate
                    text = text_list[i]
                    output_file = self.translations_folder_path + f'/azure_{i+1000}.mp3'
                    azure_tts.convert_text_to_speech(text=text, filename=output_file, speed_rate=speed_rate)

                    # Create pause audio file
                    AudioManipulation.create_single_pause_audio(
                        duration=0,
                        output_file=self.pause_audio_folder + "/pause_" + str(i+1001) + ".wav")
        except Exception as e:
            print(f"Failed to create pause audio files: {e}")
            return

        # Join audio
        try:
            AudioManipulation.join_audios(
                pause_audio_folder= self.pause_audio_folder,
                translated_audio_folder= self.translations_folder_path,
                output_file_path= self.output_file_path)
        except Exception as e:
            print(f"Failed to join audios: {e}")
            return
    
        # Cleaning
        os.system(f'rm -rf {self.pause_audio_folder}')
        os.system(f'rm -rf {self.translations_folder_path}')


# Example usage
# json_path = "path/to/json"
# main_dir = "path/to/main_dir"
# audio_sync = AudioSync(json_path, main_dir)
# audio_sync.convert_text_to_audio()