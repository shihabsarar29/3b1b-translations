import boto3
from contextlib import closing
from dotenv import load_dotenv
import os

class PollyClient:
    '''
    A client to interact with AWS Polly service.
    '''

    def __init__(self):
        '''
        Initializes the PollyClient class with AWS credentials and region.
        '''
        try:
            load_dotenv()
            access_key = os.getenv("AMAZON_ACCESS_KEY")
            secret_key = os.getenv("AMAZON_SECRET_KEY")
            region = os.getenv("AMAZON_REGION")
            self.polly_client = boto3.Session(
                aws_access_key_id=access_key,                     
                aws_secret_access_key=secret_key,
                region_name=region
            ).client('polly')
        except Exception as e:
            print(f'Error initializing PollyClient: {str(e)}')


    def convert_text_to_speech(self, text:str, voice_id: str='Joanna', filename: str="output-amazon.mp3", output_format: str='mp3'):
        '''
        A method to synthesize speech using AWS Polly and save it to a file.
        
        Inputs:
            voice_id (str): The voice to use. This is one of the voice names returned by the list_voice_ids() method.
            output_format (str): The format of the output audio. This can be 'mp3', 'ogg_vorbis', or 'pcm'.
            text (str): The text to convert to speech.
            filename (str): The name of the output file. Include the file extension, such as '.mp3'.
        
        Outputs:
            None. This method writes the audio stream to a file.
        '''
        try:
            response = self.synthesize_speech(text, voice_id, output_format)
            self.write_speech_to_file(response, filename)
            print(f'Generated Amazon Polly speech saved to "{filename}"')
        except Exception as e:
            print(f'Error synthesizing speech: {str(e)}')


    def synthesize_speech(self, text: str, voice_id: str, output_format: str) :
        '''
        A method to synthesize speech using AWS Polly.
        
        Inputs:
            voice_id (str): The voice to use. This is one of the voice names returned by the list_voice_ids() method.
            output_format (str): The format of the output audio. This can be 'mp3', 'ogg_vorbis', or 'pcm'.
            text (str): The text to convert to speech.

        Outputs:
            dict: A dictionary containing the audio stream of the synthesized speech.
        '''

        try:
            return self.polly_client.synthesize_speech(
                VoiceId=voice_id,
                OutputFormat=output_format, 
                Text=text
            )
        except Exception as e:
            print(f'Error synthesizing speech: {str(e)}')
    

    def write_speech_to_file(self, response: dict, filename: str):
        '''
        A method to write the audio stream to a file.
        
        Inputs:
            response (dict): The response from the synthesize_speech method.
            filename (str): The name of the output file. Include the file extension, such as '.mp3'.
            
        Outputs:
            None. This method writes the audio stream to a file.
        '''

        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                try:
                    with open(filename, "wb") as file:
                        file.write(stream.read())
                except IOError as ioe:
                    print(ioe)
                except Exception as e:
                    print(e)
                    
    

    def list_voice_ids(self):
        '''
        A method to get a list of available voice IDs in AWS Polly.

        Inputs:
            None
        
        Outputs:
            list: A list of strings where each string is the ID of a voice available in AWS Polly.
        '''

        try:
            voices = self.polly_client.describe_voices()
            return [voice['Id'] for voice in voices['Voices']]
        except Exception as e:
            print(f'Error listing voice IDs: {str(e)}')
    

# Example usage of the PollyClient class
# polly_client = PollyClient()
# print(polly_client.list_voice_ids())
# polly_client.convert_text_to_speech("Hello, my name is Polly.", "Joanna")