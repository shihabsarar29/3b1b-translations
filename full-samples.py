from scripts.Parser import Parser
from scripts.AzureTTS import AzureTTS
from scripts.FileUtils import FileUtils

# Variables
root_directory= '../'
video_folder = 'cross-products'
json_filename= 'sentence_translations.json'

# Get JSON files
fileUtils = FileUtils(root_directory, video_folder, json_filename)
json_files = fileUtils.get_json_files()

# Parse JSON files
for filename in json_files:
    try:
        translator = Parser(filename)
        text = translator.get_translated_texts()
    except Exception as e:
        print(f"Failed to parse file: {e}")

    # Azure TTS
    try:
        azure_tts = AzureTTS()
        output_file = filename.replace(json_filename, '') + "azure.wav"
        azure_tts.convert_text_to_speech(text=text, filename=output_file)
    except Exception as e:
        print(f"Failed to convert text to speech using Azure TTS: {e}")
