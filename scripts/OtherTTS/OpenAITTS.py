import os
import requests
from dotenv import load_dotenv

class OpenAITTS:
    def __init__(self):
        """
        The constructor for the OpenAITTS class.
        """
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables.")

    def text_to_speech(self, text: str, voice: str='alloy', filename: str="output-openai.mp3"):
        """
        A method to convert text to speech using OpenAI TTS.

        Inputs:
            text (str): The text to convert to speech.
            model (str): The model to use for conversion.
            voice (str): The voice to use for the conversion.
            filename (str): The filename to save the generated speech.

        Outputs:
            This method does not return anything. It saves an mp3 file to the current directory.
        """
        url = "https://api.openai.com/v1/audio/speech"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": 'tts-1-hd',
            "input": text,
            "voice": voice
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            with open(filename, 'wb') as out:
                out.write(response.content)
                print(f'Audio content written to file "{filename}"')
        else:
            raise Exception(f"Text to Speech API failed with status code: {response.status_code}, message: {response.text}")


# Example usage:
# openai_tts = OpenAITTS()
# openai_tts.text_to_speech("Today is a wonderful day to build something people love!")