import os
import requests
import base64
from dotenv import load_dotenv


class GoogleCloudTTS:
    def __init__(self):
        """
        The constructor for the GoogleCloudTTS class.
        """
        try:
            load_dotenv()
            self.api_key = os.getenv("GOOGLE_CLOUD_API_KEY")
            if not self.api_key:
                raise ValueError("GOOGLE_CLOUD_API_KEY not found in environment variables.")
        except Exception as e:
            print(f"Failed to get Google Cloud API Key. Error: {e}")

    def convert_text_to_speech(self, text: str, voice_name: str='en-US-Standard-B', filename: str="output-google-cloud.mp3", audio_encoding: str='MP3'):
        """
        A method to convert text to speech using Google Cloud TTS.
        
        Inputs:
            text (str): The text to convert to speech.
            voice_name (str): The name of the voice to use. This is one of the voice names returned by the get_voice_names() method.
            audio_encoding (str): The format of the output audio. This can be 'LINEAR16' or 'MP3'.

        Outputs:
            This method does not return anything. It saves an mp3 file to the current directory.
        """
        try:
            url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={self.api_key}"
            headers = {"Content-Type": "application/json"}
            data = {
                'input': {
                    'text': text,
                },
                'voice': {
                    'languageCode': voice_name.split("-")[0] + "-" + voice_name.split("-")[1],
                    'name': voice_name,
                },
                'audioConfig': {
                    'audioEncoding': audio_encoding,
                }
            }

            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 200:
                audio_content = base64.b64decode(response.json()['audioContent'])
                with open(filename, 'wb') as out:
                    out.write(audio_content)
                    print(f'Audio content written to file "{filename}"')
            else:
                raise Exception(f"Text to Speech API failed with status code: {response.status_code}, message: {response.text}")
        except Exception as e:
            print(f"Exception occurred when converting text to speech. Error: {e}")


    def get_voice_names(self):
        """
        A method to get a list of available voice names in Google Cloud TTS.

        Inputs:
            None

        Outputs:
            list: A list of strings where each string is the name of a voice available in Google Cloud TTS.
        """
        try:
            url = f"https://texttospeech.googleapis.com/v1/voices?key={self.api_key}"
            response = requests.get(url)
            
            if response.status_code == 200:
                voices = response.json().get('voices', [])
                voice_names = [voice.get('name', '') for voice in voices]
                return voice_names
            else:
                raise Exception(f"Failed to get voices with status code: {response.status_code}, message: {response.text}")
        except Exception as e:
            print(f"Exception occurred when fetching voice names. Error: {e}")
            return []
        
        
# Example usage:
# google_cloud_tts = GoogleCloudTTS()
# print(google_cloud_tts.get_voice_names(), "\n")
# google_cloud_tts.convert_text_to_speech("What is the temperature in Sydney?", "en-AU-Neural2-A")