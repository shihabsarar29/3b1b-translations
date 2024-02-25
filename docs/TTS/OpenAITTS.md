# OpenAITTS Class Documentation

## Overview
The `OpenAITTS` class contains methods to interact with the OpenAI TTS API, which is a cloud service that converts text to speech.

## Attributes
- `api_key`: **str**:
    - The API key for the OpenAI TTS API. This is retrieved from the dotenv variable `OPENAI_API_KEY`.

## Methods
### text_to_speech
- **Description**: Convert the translated text to audio. It uses OpenAI's TTS API to generate audio data.
- **Parameters**
    - `text`: **str**:
        - The text to convert to audio.
    - `voice`: **str** (default: **alloy**):
        - The voice to use. The default is the `alloy` voice.
    - `filename`: **str** (default: **output-openai.mp3**):
        - The path to the file to save the audio to.
#### **Returns**:
- ```None```
#### Outputs
- The audio is saved to `filename`.
#### Exceptions
- ```Exception```: Raised if the TTS API request fails. The format is as follows: "Text to Speech API failed with status code: {response.status_code}, message: {response.text}".