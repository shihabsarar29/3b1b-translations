from elevenLabsAPI import elevenLabsAPI

api_key = "API_KEY_HERE" # Replace
tts = elevenLabsAPI(api_key)
tts.get_voice_id("3b1b", inPlace=True)

text = "Hi, my name is Grant. I like dogs, cats, and Bayes Theorem."
output_file = "outputs/output.mp3"
tts.get_audio_to_file(text, output_file)
