# GoogleCloudTTS Class Documentation

## Overview
The `GoogleCloudTTS` class contains methods to generate audio data from text using [Google Cloud's Text-to-Speech API](https://cloud.google.com/text-to-speech?hl=en).

## Attributes
- `api_key`: **str**:
    - The API key for the Google Cloud Text-to-Speech API. This is retrieved from the dotenv variable `GOOGLE_CLOUD_API_KEY`.

## Methods
### convert_text_to_speech
- **Description**: Convert the translated text to audio. It uses Google Cloud's Text-to-Speech API to generate audio data.
- **Parameters**
    - `text`: **str**:
        - The text to convert to audio.
    - `voice_name`: **str** (default: **n-US-Standard-B**):
        - The name of the voice to use. The default is the US English Standard B voice.
    - `filename`: **str** (default: **output-google-cloud.mp3**):
        - The name of the file to save the audio to.
    - `audio_encoding`: **str** (default: **MP3**):
        - The encoding of the audio file. The default is MP3.
#### Returns
- ```None```
#### Outputs
- The audio is saved to `filename`.
#### Exceptions
- ```Exception```: Raised if the Text-to-Speech API request fails. The format is as follows: "Text to Speech API failed with status code: {response.status_code}, message: {response.text}".

### get_voice_names(self)
- **Description**: Get the names of the available voices for the Text-to-Speech API.
- **Parameters**
    - ```None```
- **Returns**
    - ```list```: A list of the available voice names.
- **Exceptions**
    - ```Exception```: Raised if the Text-to-Speech API request fails. The format is as follows: "Failed to get voices with status code: {response.status_code}, message: {response.text}".


## Example Usage:
##### Example 1: Basic Usage
```python
from OtherTTS.GoogleCloudTTS import GoogleCloudTTS

google_cloud_tts = GoogleCloudTTS()
print(google_cloud_tts.get_voice_names(), "\n")
google_cloud_tts.convert_text_to_speech("What is the temperature in Sydney?", "en-AU-Neural2-A")
```