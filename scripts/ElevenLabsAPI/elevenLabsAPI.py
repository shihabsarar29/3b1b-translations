import requests


class elevenLabsAPI:
    def __init__(self, api_key, base_url="https://api.eleven-labs.io"):
        self.api_key = api_key
        self.base_url = base_url
        self.voice_id = None
        self.headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def get_voice_id(self, voice_name, inPlace=False):
        url = f"{self.base_url}/v1/voices"
        response = requests.get(url, headers=self.headers)
        voices  = response.json()["voices"]

        # Get element where name is voice_name 
        voice = next((voice for voice in voices if voice["name"] == voice_name), None)

        if voice and inPlace:
            return voice["voice_id"]
        elif voice:
            self.voice_id = voice["voice_id"]
    
    def __get_audio(self, text, CHUNK_SIZE, format, voice_id, stream = False): # Private method
        url = f"{self.base_url}/v1/text-to-speech/{voice_id}/"

        payload = {
            "text": text,
        }

        response = requests.request("POST", url, json=payload, headers=self.headers)

        return response

    def get_audio_to_file(self, text, CHUNK_SIZE = 1024, format="mp3", voice_id = None):
        if not voice_id: voice_id = self.voice_id

        url = f"{self.base_url}/v1/voices/{voice_id}/audio"
        data = {
            "text": text,
            "format": format
        }

        response =  self.__get_audio(response, CHUNK_SIZE, format, voice_id, stream = False)

        with open('output.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

eleven = elevenLabsAPI