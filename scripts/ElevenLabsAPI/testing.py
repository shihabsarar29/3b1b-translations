from elevenLabsAPI import elevenLabsAPI
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv("ELEVEN_LABS_API_KEY")
tts = elevenLabsAPI(api_key)
tts.get_voice_id("3b1b", inPlace=True)

texts = []
import json

with open("C:\\Users\\sapat\\Downloads\\3b1b\\API\\scripts\\ElevenLabsAPI\\sentence_translations.json", "r") as file:
    data = json.load(file)
    for item in data:
        texts.append(item["translatedText"])

print(texts)

output_file = "outputs/output"
tts.get_audio_to_file(texts, output_file, percentage=True)
