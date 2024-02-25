# AzureTTS Class Documentation

## Overview
The `AzureTTS` class contains methods to interact with the Azure TTS API, which is a cloud service that converts text to speech.

## Attributes
- `speech_key`
    - The API key for the Azure TTS API. This is retrieved from the dotenv variable `AZURE_SPEECH_KEY`.
- `speech_region`
    - The region for the Azure TTS API. This is retrieved from the dotenv variable `AZURE_SPEECH_REGION`.
- `translator_text_key`
    - The API key for the Azure Translator Text API. This is retrieved from the dotenv variable `AZURE_TRANSLATOR_KEY`.

## Methods
### convert_text_to_speech
- **Description**: Convert the translated text to audio using Azure Cognitive Services Speech Service. The program sleeps for 2 seconds after every call to avoid the API rate limit.
- **Parameters**:
    - `text`: **str**
        - The text to convert to audio.
    - `voice_name`: **str** (default: **en-US-AndrewMultilingualNeural**):
        - The name of the voice to use. The default is the US English Andrew Multilingual Neural voice.
    - `filename`: **str** (default: **output-azure.mp3**):
        - The name of the file to save the audio to.
    - `speed_rate`: **float** (default: **1.0**):
        - The prosoody speed rate of the speech. The default is 1.0.
#### **Returns**:
- ```None```
#### Outputs:
- The audio is saved to `filename`.

### translate_text
- **Description**: Translate text using Azure Cognitive Services Translator Text Service.
- **Parameters**:
    - `text`: **str**
        - The text to translate.
    - `to_lang`: **str** (default: **es**)
        - The language to translate the text to. The default is Spanish.
#### **Returns**:
- ```str```: The translated text.

### get_audio_duration
- **Description**: Get the duration of the audio file.
- **Parameters**:
    - `filename`: **str**
        - The name of the audio file.
#### **Returns**:
- ```float```: The duration of the audio file in seconds.

### get_supported_languages
- **Description**: Fetch the supported languages by Azure translation service.
- **Parameters**:
    - ```None```
#### **Returns**:
- ```list```: A list of the supported languages.