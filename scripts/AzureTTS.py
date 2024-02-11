import os
import requests
import xml.sax.saxutils as saxutils
from dotenv import load_dotenv

class AzureTTS:
    def __init__(self):
        """
        The constructor for the AzureTTS class.
        """
        try:
            load_dotenv()
            self.speech_key = os.getenv("AZURE_SPEECH_KEY")
            self.speech_region = os.getenv("AZURE_SPEECH_REGION")
            if not self.speech_key or not self.speech_region:
                raise ValueError("SPEECH_KEY or SPEECH_REGION not found in environment variables.")
        except Exception as e:
            print(f"Failed to get Azure Cognitive Service Data. Error: {e}")

    def convert_text_to_speech(self, text: str, voice_name: str="en-US-BrianNeural", filename: str="output-azure.mp3"):
        """
        A method to convert text to speech using Azure Cognitive Services Speech Service.

        Inputs:
            text (str): The text to convert to speech.

        Outputs:
            This method does not return anything. It saves an audio file to the current directory.
        """
        try:
            url = f"https://{self.speech_region}.tts.speech.microsoft.com/cognitiveservices/v1"
            headers = {
                'Ocp-Apim-Subscription-Key': self.speech_key,
                'Content-Type': 'application/ssml+xml',
                'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3',
                'User-Agent': 'azure-tts-client',
            }
            lang=voice_name.split("-")[0]+"-"+voice_name.split("-")[1]
            escaped_text = saxutils.escape(text)
            data = f'''
            <speak version='1.0' xml:lang='{lang}'>
                <voice xml:lang='{lang}' xml:gender='Male' name='{voice_name}'>
                    {escaped_text}
                </voice>
            </speak>
            '''
            response = requests.post(url, headers=headers, data=data.encode("utf-8"))
            response.raise_for_status()

            with open(filename, 'wb') as audio:
                audio.write(response.content)
                print(f'Audio content written to file "{filename}"')
        except Exception as e:
            print(f"Exception occurred when converting text to speech. Error: {e}")


# Example usage:
# azure_tts = AzureTTS()
# azure_tts.convert_text_to_speech("Hello World!")