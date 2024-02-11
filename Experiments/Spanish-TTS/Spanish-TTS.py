import sys
sys.path.insert(0, sys.path[0] + '/../../')

from scripts.Parser import Parser
from scripts.GoogleCloudTTS import GoogleCloudTTS
from scripts.AmazonTTS import PollyClient
from scripts.ElevenLabsAPI.elevenLabsAPI import elevenLabsAPI
from scripts.IbmTTS import IbmTTS
from scripts.AzureTTS import AzureTTS
from scripts.OpenAITTS import OpenAITTS
import dotenv
import os
import time

main_dir = "Experiments/Spanish-TTS/"

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
  voice_name = "es-US-Studio-B"
  output_file = main_dir + "outputs/google-cloud.wav"
  start_time = time.time()
  google_cloud_tts = GoogleCloudTTS()
  google_cloud_tts.convert_text_to_speech(text, voice_name, output_file)
  print(f"Time taken by Google Cloud TTS: {time.time() - start_time} seconds.\n")
except Exception as e:
  print(f"Failed to convert text to speech using Google Cloud TTS: {e}")

# Amazon Polly
try:
  print("Amazon Polly")
  voice_name = "Miguel"
  output_file = main_dir + "outputs/amazon-polly.wav"
  start_time = time.time()
  polly_client = PollyClient()
  polly_client.convert_text_to_speech(text, voice_name, output_file)
  print(f"Time taken by Amazon Polly: {time.time() - start_time} seconds.\n")
except Exception as e:
  print(f"Failed to convert text to speech using Amazon TTS: {e}")

# IBM Watson
try:
  print("IBM Watson")
  voice_name = "es-ES_EnriqueV3Voice"
  output_file = main_dir + "outputs/ibm-watson.wav"
  start_time = time.time()
  ibm_tts = IbmTTS()
  ibm_tts.convert_text_to_speech(text, voice_name, output_file)
  print(f"Time taken by IBM Watson: {time.time() - start_time} seconds.\n")
except Exception as e:
  print(f"Failed to convert text to speech using IBM Watson TTS: {e}")

# Azure TTS
try:
  print("Azure TTS")
  voice_name = "es-US-AlonsoNeural"
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

# ElevenLabsAPI
try:
  print("ElevenLabs")
  voice_name = "Michael"
  output_file = "../../" + main_dir + "outputs/eleven-labs.wav"
  start_time = time.time()
  dotenv.load_dotenv()
  tts = elevenLabsAPI(os.getenv("ELEVEN_LABS_API_KEY"))
  tts.get_voice_id(voice_name, inPlace=True)
  tts.get_audio_to_file(text, output_file)
  print(f"Generated ElevenLabs speech saved to {output_file}")
  print(f"Time taken by ElevenLabs: {time.time() - start_time} seconds.\n")
except Exception as e:
  print(f"Failed to convert text to speech using ElevenLabs: {e}")

# ElevenLabsAPI Grant
try:
  print("ElevenLabs")
  voice_name = "3b1b"
  output_file = "../../" + main_dir + "outputs/eleven-labs-grant.wav"
  start_time = time.time()
  dotenv.load_dotenv()
  tts = elevenLabsAPI(os.getenv("ELEVEN_LABS_API_KEY"))
  tts.get_voice_id(voice_name, inPlace=True)
  tts.get_audio_to_file(text, output_file)
  print(f"Generated ElevenLabs speech saved to {output_file}")
  print(f"Time taken by ElevenLabs: {time.time() - start_time} seconds.\n")
except Exception as e:
  print(f"Failed to convert text to speech using ElevenLabs: {e}")
