import requests
from dotenv import load_dotenv
import json
import os

class IbmTTS:
    '''
    A class to convert text to speech using IBM Watson TTS.
    '''
    def __init__(self):
        '''
        The constructor for the IbmTTS class.
        '''
        try:
            load_dotenv()
            self.API_KEY = os.getenv("IBM_API_KEY")
            self.API_URL = os.getenv("IBM_SERVICE_URL")
            if not self.API_KEY or not self.API_URL:
                raise ValueError('Check your .env file, API details are missing')

        except Exception as e:
            print(f"Error in initialization: {str(e)}")

    def convert_text_to_speech(self, text: str, voice: str='en-US_AllisonV3Voice', filename: str='output-ibm.wav'):
        '''
        A method to convert text to speech and save it as a wav file using IBM Watson TTS.
        
        Inputs:
            text (str): The text to convert to speech.
            voice (str): The name of the voice to use. This is one of the voice names returned by the get_voice_names() method.
            filename (str): The name of the output wav file. Include ".wav" in the name.
            
        Outputs:
            This method does not return anything. It saves a wav file to the current directory.
        '''
        try:
            response = requests.post(f"{self.API_URL}/v1/synthesize?voice={voice}", 
                                    auth=("apikey", self.API_KEY), 
                                    headers={"Content-Type": "application/json", "Accept": "audio/wav"},
                                    data=json.dumps({"text": text}))

            if response.status_code != 200:
                raise ValueError(f"Error in API call: {response.json()}")

            with open(filename, 'wb') as audio_file:
                audio_file.write(response.content)

            print(f'Generated IBM Watson speech saved to "{filename}"')
            
        except Exception as e:
            print(f"Error in convert_text_to_speech: {str(e)}")

    def get_voice_names(self):
        '''
        A method to get a list of available voice names in IBM Watson TTS.
        
        Inputs:
            None
        
        Outputs:
            list: A list of strings where each string is the name of a voice available in IBM Watson TTS.  
        '''
        try:
            response = requests.get(f"{self.API_URL}/v1/voices", auth=("apikey", self.API_KEY))
            if response.status_code != 200:
                raise ValueError(f"Error in API call: {response.json()}")

            voice_list = response.json().get('voices', [])
            voice_names = [voice.get('name', '') for voice in voice_list]
            return voice_names

        except Exception as e:
            print(f"Error in get_voice_names: {str(e)}")
    
# Example usage:
# ibm_tts = IbmTTS()
# print(ibm_tts.get_voice_names())
# ibm_tts.convert_text_to_speech('Hello Hello', 'en-US_AllisonV3Voice')