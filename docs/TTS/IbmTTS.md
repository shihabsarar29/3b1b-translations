# IbmTTS Documentation

## Overview
The `IbmTTS` class is a client to interact with [IBM Watson Text to Speech service](https://www.ibm.com/products/speech-to-text), which is a cloud service that converts text to speech.

## Attributes
- `API_KEY`: **str**:
    - The API key for the IBM Watson Text to Speech service. This is retrieved from the dotenv variable `IBM_API_KEY`.
- `API_URL`: **str**:
    - The URL for the IBM Watson Text to Speech service. This is retrieved from the dotenv variable `IBM_SERVICE_URL`.

## Methods
### convert_text_to_speech
- **Description**: Convert the translated text to audio. It uses IBM Watson Text to Speech service to generate audio data.
- **Parameters**
    - `text`: **str**:
        - The text to convert to audio.
    - `voice`: **str** (default: **en-US_AllisonV3Voice**):
        - The name of the voice to use. The default is the US English Allison voice.
    - `filename`: **str** (default: **output-ibm.wav**):
        - The name of the file to save the audio to.
#### Returns:
- ```None```
#### Outputs:
- The audio is saved to `filename`.
#### Exceptions:
- ```ValueError```: Raised if the Text to Speech API request fails. Return's the response's JSON data. The format is as follows: "Error in API call: {response.json()}".

### get_voice_names
- **Description**: Get the names of the available voices for the Text to Speech API.
- **Parameters**
    - ```None```
- **Returns**
    - ```list```: A list of the available voice names.