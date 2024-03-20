import os
import requests
import xml.sax.saxutils as saxutils
import time
from dotenv import load_dotenv
from pydub import AudioSegment


class AzureTTS:
    """
    A class to convert text to speech using Azure Cognitive Services Speech Service.
    """
    
    language_to_voice_map = {
        "albanian": "sq-AL-IlirNeural2",
        "arabic": "ar-EG-ShakirNeural",
        "bengali": "bn-IN-BashkarNeural2",
        "bulgarian": "bg-BG-BorislavNeural",
        "catalan": "ca-ES-EnricNeural",
        "chinese": "zh-CN-YunfengNeural",
        "croatian": "hr-HR-SreckoNeural",
        "czech": "cs-CZ-AntoninNeural",
        "danish": "da-DK-JeppeNeural",
        "dutch": "nl-BE-ArnaudNeural",
        "estonian": "et-EE-KertNeural2",
        "finnish": "fi-FI-HarriNeural",
        "french": "fr-FR-HenriNeural",
        "georgian": "ka-GE-GiorgiNeural2",
        "german": "de-DE-ConradNeural1",
        "greek": "el-GR-NestorasNeural",
        "gujarati": "gu-IN-NiranjanNeural",
        "hebrew": "he-IL-AvriNeural",
        "hindi": "hi-IN-MadhurNeural",
        "hungarian": "hu-HU-TamasNeural",
        "indonesian": "id-ID-ArdiNeural",
        "italian": "it-IT-LisandroNeural",
        "japanese": "ja-JP-NaokiNeural",
        "korean": "ko-KR-BongJinNeural",
        "lithuanian": "lt-LT-LeonasNeural2",
        "malay": "ms-MY-OsmanNeural",
        "marathi": "mr-IN-ManoharNeural",
        "norwegian": "nb-NO-FinnNeural",
        "persian": "fa-IR-FaridNeural2",
        "polish": "pl-PL-MarekNeural",
        "portuguese": "pt-BR-NicolauNeural",
        "romanian": "ro-RO-EmilNeural",
        "russian": "ru-RU-DmitryNeural",
        "serbian": "sr-Latn-RS-NicholasNeural2",
        "slovak": "sk-SK-LukasNeural",
        "slovenian": "sl-SI-RokNeural",
        "spanish": "es-MX-GerardoNeural",
        "swedish": "sv-SE-MattiasNeural",
        "tagalog": "fil-PH-AngeloNeural2",
        "tamil": "ta-LK-KumarNeural",
        "telugu": "te-IN-MohanNeural",
        "thai": "th-TH-NiwatNeural",
        "turkish": "tr-TR-AhmetNeural",
        "ukrainian": "uk-UA-OstapNeural",
        "urdu": "ur-IN-SalmanNeural",
        "vietnamese": "vi-VN-NamMinhNeural",
        "english": "en-US-TonyNeural"
    }
     
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
            raise Exception(f"Failed to initialize AzureTTS. Error: {e}")

    def convert_text_to_speech(self, text, voice_name: str="en-US-AndrewMultilingualNeural", filename: str="output-azure.mp3", speed_rate: float=1.0, is_list=False):
        """
        A method to convert text to speech using Azure Cognitive Services Speech Service.

        Inputs:
            text (str/list of String): The text to convert to speech.

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

            if is_list:
                input_data = text
            else:
                input_data = [text]

            for idx, text in enumerate(input_data):
                escaped_text = saxutils.escape(text)
                data = f'''
                <speak version='1.0' xml:lang='{lang}'>
                    <voice xml:lang='{lang}' xml:gender='Male' name='{voice_name}'>
                        <prosody rate='{speed_rate}'>
                            {escaped_text}
                        </prosody>
                    </voice>
                </speak>
                '''
                response = requests.post(url, headers=headers, data=data.encode("utf-8"))
                response.raise_for_status()

                if response.content == b'':
                    raise Exception("Response content is empty.")
                    
                output_filename = f"{filename}_{idx}.mp3" if is_list else filename
                    
                with open(output_filename, 'wb') as audio:
                    audio.write(response.content)
                    print(f'Audio content written to file "{output_filename}"')

                time.sleep(2)
            
        except Exception as e:
            raise Exception(f"Exception occurred when converting text to speech. Error: {e}")



    @staticmethod
    def get_audio_duration(filename: str):
        """
        A method to get the duration of an audio file.

        Inputs:
            filename (str): The name of the audio file.

        Outputs:
            duration (float): The duration of the audio file in seconds.
        """
        try:
            audio = AudioSegment.from_file(filename)
            duration = len(audio) / 1000
            return duration
        except Exception as e:
            raise Exception(f"Exception occurred when getting audio duration. Error: {e}")
        
    @staticmethod
    def get_voice_name(language: str) -> str:
        """
        A static method to output the voice name taking language as input.

        Inputs:
            language (str): The language in English (e.g., "english", "french").

        Outputs:
            voice_name (str): The voice name corresponding to the input language.
        """
        voice_name = AzureTTS.language_to_voice_map.get(language.lower())
        if not voice_name:
            raise ValueError(f"Voice name for language '{language}' not found.")
        return voice_name




# Example usage:
# azure_tts = AzureTTS()
# azure_tts.convert_text_to_speech("Hello World!")
