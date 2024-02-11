import sys
sys.path.insert(0, sys.path[0] + '/../../')

from scripts.Parser import Parser
from scripts.GoogleCloudTTS import GoogleCloudTTS
from scripts.AzureTTS import AzureTTS
from scripts.OpenAITTS import OpenAITTS
import time

main_dir = "Experiments/Bengali-TTS/"

# Parser
try:
  file_path = main_dir + 'sentence_translations.json'
  translator = Parser(file_path)
  text = translator.get_translated_texts()[:500]
  print(text, "\n\n")
except Exception as e:
    print(f"Failed to parse file: {e}")

# Google TTS
try:
  print("Google Cloud TTS")
  voice_name = "bn-IN-Wavenet-B"
  output_file = main_dir + "outputs/google-cloud.wav"
  start_time = time.time()
  google_cloud_tts = GoogleCloudTTS()
  google_cloud_tts.convert_text_to_speech(text, voice_name, output_file)
  print(f"Time taken by Google Cloud TTS: {time.time() - start_time} seconds.\n")
except Exception as e:
    print(f"Failed to convert text to speech using Google Cloud TTS: {e}")

# Azure TTS
try:
  print("Azure TTS")
  voice_name = "bn-BD-PradeepNeural"
  output_file = main_dir + "outputs/azure.wav"
  start_time = time.time()
  azure_tts = AzureTTS()
  azure_tts.convert_text_to_speech(text, voice_name, output_file)
  print(f"Time taken by Azure TTS: {time.time() - start_time} seconds.\n")
except Exception as e:
  print(f"Failed to convert text to speech using Azure TTS: {e}")

# OpenAI TTS
try:
  print("OpenAI TTS")
  voice_name = 'alloy'
  output_file = main_dir + "outputs/openai-tts.mp3"
  start_time = time.time()
  openai_tts = OpenAITTS()
  openai_tts.text_to_speech(text, voice_name, output_file)
  print(f"Time taken by OpenAI TTS: {time.time() - start_time} seconds.\n")
except Exception as e:
  print(f"Failed to convert text to speech using OpenAI TTS: {e}")