import requests
from typing import Union
import json
import os
from librosa.effects import time_stretch
from librosa import load
from soundfile import write
import dotenv
from pydub import AudioSegment
from audiostretchy.stretch import stretch_audio

class elevenLabsAPI:
    """
    Class/Wrapper for the ElevenLabs API

    Attributes:
        api_key str: The API key to use the ElevenLabs API
        base_url str: The base url of the API, default is "https://api.elevenlabs.io"
        voice_id str: The voice_id to use for the text-to-speech, can be used to use a specific voice for TTS; Set manually or using the **get_voice_id** method    
    
    Methods:
        get_voice_id(voice_name: str, inPlace: bool=False) -> str (Method)
        __get_audio(data: dict, voice_id: str) -> requests.Response (Private Method)
        get_audio_to_file(text: Union[str, list[str]], output_file: str, CHUNK_SIZE: int = 1024, voice_id: str = None) -> str (Method)
    """
    def __init__(self, api_key: str = None, base_url: str="https://api.elevenlabs.io", voice_id: str=None):
        if not api_key:
            dotenv.load_dotenv()
            self.api_key = os.getenv("ELEVENLABS_API_KEY")
        else:
            self.api_key = api_key


        self.base_url = base_url
        self.voice_id = voice_id
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/mpeg" # Required
        }
    
    def get_voice_id(self, voice_name: str, inPlace: bool=False) -> Union[str, None]:
        """
        Get the id of an ElevenLabs voice, given its name (i.e. "Rachel" or "John"). Voice can be custom trained. [Reference](https://elevenlabs.io/docs/api-reference/get-voices)

        Parameters:
            voice_name (str): The name of the voice to get the id
            inPlace (bool) = (False): If True, set the object's (voice_id) attribute to the voice_id found. If False, return the voice_id found

        Raises:
            (ValueError): If the voice with name voice_name is not found
        """

        url = f"{self.base_url}/v1/voices" # URL to send the request, formatted as f-string

        try:
            response = requests.get(url, headers=self.headers) # Send the request and retrieve the response
            response.raise_for_status() # Raise an error if the status code is not 200
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError("Error in making GET request for all voice_ids: ", err)
        except requests.exceptions.ConnectionError as err:
            raise requests.exceptions.ConnectionError("Error in connecting to the API, likely due to internet issues: ", err)
        except Exception as err:
            raise Exception("Unidentified error in getting audio: ", err)

        try:
            voices = response.json()["voices"]
        except json.decoder.JSONDecodeError as err:
            raise json.decoder.JSONDecodeError("An error occurred while parsing the response as JSONN: ", err)
        except KeyError as err:
            raise KeyError("The JSON response does not contain a key 'voices': ", err)
        except Exception as err:
            raise Exception("Unidentified error in getting voice ID from JSON data: ", err)

        # Get element where name is voice_name 
        voice = next((voice for voice in voices if voice["name"] == voice_name), None) # Find the voice with the name voice_name

        if voice and inPlace:
            self.voice_id = voice["voice_id"] # Set the voice_id attribute to the voice_id found if inPlace is True
        elif voice:
            return voice["voice_id"] # Return the voice_id if found and inPlace is True
        else:
            raise ValueError(f"Voice with name {voice_name} not found")
    
    def __get_audio(self, data: dict, voice_id: str) -> requests.Response: # Private method
        """
        Get the audio from the ElevenLabs API, given the data (payload) and voice_id. [Reference](https://elevenlabs.io/docs/api-reference/text-to-speech)

        Parameters:
            data (dict): The payload to send to the API. Contains the text to convert to speech, as well as custom voice_settings.
            voice_id (str): The voice_id to use for the text-to-speech. Use the **get_voice_id** method to obtain the voice_id or pass it in manually
        """

        url = f"{self.base_url}/v1/text-to-speech/{voice_id}" # URL to send the request, formatted as f-string
        payload = data # Payload to send to the API

        try:
            response = requests.post(url, json=payload, headers=self.headers) # Send the request and retrieve the response
            response.raise_for_status() # Raise an error if the status code is not 200
        except requests.exceptions.HTTPError as err:
            raise requests.exceptions.HTTPError("HTTPError in getting audio: ", err)
        except Exception as err:
            raise Exception("Unidentified error in getting audio: ", err)

        return response

    def get_audio_to_file(self, text: Union[str, list[str]], output_file: str, CHUNK_SIZE: int = 1024, voice_id: str = None, similarity_boost: float = 0.55, stability: float = 0.45, style: float = 0.4, percentage = False, segment_duration: float = None) -> Union[str, list[str]]:
        """
        Get the audio from the ElevenLabs API and save it to a file(s), given the text(s) and output_file. [Reference](https://elevenlabs.io/docs/api-reference/text-to-speech)

        Parameters:
            text (str) or (list[str]): The text to convert to speech. Can be a string or a list of strings. If a list, each element will be converted to a separate audio file
            output_file (str): The path to save the audio file(s). If text is a list, the output_file string will be used as a prefix for each file
            CHUNK_SIZE (int) = (1024): How many bytes to write to the file at a time. Default is 1024
            voice_id (str) = (None): The voice_id to use for the text-to-speech. Use the **get_voice_id** method to obtain the voice_id or pass it in manually
            similarity_boost (float) = (0.55), (0.0 - 1.0): Higher values boost the voice clarity but can introduce artifacts. Default is 0.55
            stability (float) = (0.45), (0.0 - 1.0): A higher stability is more predictable but can be monotone, while a lower stability is more expressive but unstable. Default is 0.45
            style (float) = (0.45), (0.0 - 1.0): Higher values are more "exaggerated" but also a lot more computationally expensive and take longer to generate. Default is 0.90
            percentage (bool) = (False): If True, print the percentage done for each file when text is a list
        
        Raises:
            (ValueError): If text is not a string or a list of strings
            (ValueError): If voice_id is not valid. Likely the user forgot to set it or pass it in manually
        """

        if not voice_id: # If voice_id is not passed, use the one in the object
            voice_id = self.voice_id 
            if not voice_id: # If voice_id is still not found, raise an error. Likely the user forgot to set it
                raise ValueError("Voice ID not found. Use the get_voice_id method to obtain the voice_id or pass it in manually.")
        
        data = { # Payload
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "similarity_boost": similarity_boost,
                "stability": stability,
                "style": style,
                "use_speaker_boost": True,
            },
        }

        original_output_file = output_file # Keep the original output_file

        # Prefix directory of current_file to output_file if output_file is not an absolute path
        if not os.path.isabs(output_file) or not os.path.exists(output_file):
            print("Output file is not an absolute path, establishing absolute path")
            current_file = os.path.abspath(__file__) # Get the absolute path of the current file
            current_directory = os.path.dirname(current_file) # Get the directory of the current file
            output_file = os.path.join(current_directory, output_file) # Join the directory of the current file with the output_file
            print("p1: ", current_file)

        # Check if the new output_file exists
        if not os.path.exists(output_file):
            current_cwd = os.getcwd() # Get the absolute path of the current working directory
            print("current cwd: ", current_cwd)
            output_file = os.path.join(current_cwd, original_output_file) # Join the directory of the current file with the output_file
                
        print("output_file: ", output_file)

        if type(text) == str: # If text is a string, can be converted to a single file
            response = self.__get_audio(data, voice_id) # Get the audio response from private method

            with open(output_file, 'wb') as f: # Write the response to a file by CHUNK_SIZE bytes at a time
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            
            # Load the audio file using pydub to get the duration
            if segment_duration:
                audio = AudioSegment.from_file(output_file)
                translated_length = len(audio)

                speed_rate = translated_length / segment_duration
                if speed_rate > 1.05:
                    print(f'Warning: Speed rate is greater than 1.05: {speed_rate}')
                    speed_rate = 1.05
                elif speed_rate < 1:
                    speed_rate = 1

                self._speed_up(output_file, speed_rate=speed_rate) # Speed up the audio file

            return output_file.replace(".mp3", ".wav"), speed_rate # Return the file path
        elif type(text) == list: # If text is a list, each element can be converted to a separate file

            for idx, t in enumerate(text): # Loop through each element in the list
                data["text"] = t # Change the text in the payload to the current element
                response = self.__get_audio(data, voice_id) # Get the audio response from private method

                if not os.path.exists(output_file):
                    open(output_file, 'a').close()

                with open(f"{output_file}_{idx}.mp3", 'wb') as f: # Write the response to a file by CHUNK_SIZE bytes at a time
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                
                # Print percentage done
                if percentage:
                    print(f"Percentage done: {round((idx+1)/len(text)*100, 2)}%")

            #self._speed_up(f"{output_file}_{idx}.mp3", speed_rate) # Speed up the audio file
            output_files = [f"{output_file}_{idx}.wav" for idx in range(len(text))] # Keep track of the file paths

            return output_files # Return the list of file paths written to
        else:
            raise ValueError("text must be a string or a list of strings")


    def _speed_up(self, audio_file: str, speed_rate: float = 1, delete_old: bool = True) -> str:
        """
        Speed up an audio file by a speed_rate using the librosa library

        Parameters:
            audio_file (str): The path to the audio file to speed up
            speed_rate (float) = (1): The speed rate to increase the audio by. Default is 1
        """

        # Get new output file path
        new_output_file = audio_file.replace(".mp3", ".wav")

        # Save the new audio file
        stretch_audio(audio_file, new_output_file, ratio=0.5)


        # Delete the old .mp3 file
        if delete_old:
            os.remove(audio_file)

