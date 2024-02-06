from elevenLabsAPI import elevenLabsAPI
import dotenv
import os

dotenv.load_dotenv()
api_key = os.getenv("ELEVEN_LABS_API_KEY")
tts = elevenLabsAPI(api_key)
tts.get_voice_id("3b1b", inPlace=True)

text = "Hi, my name is Grant. I like dogs, cats, and Bayes Theorem."
output_file = "outputs/output.mp3"
tts.get_audio_to_file(text, output_file)
