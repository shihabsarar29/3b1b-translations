# elevenLabsAPI Class Documentation

## Overview
The `elevenLabsAPI` class serves as a wrapper for interacting with the ElevenLabs API, particularly for text-to-speech functionalities. This class provides methods to facilitate the conversion of text to audio files using the ElevenLabs API.

## Attributes

- `api_key`: **str**
    - The API key used to access the ElevenLabs API.
- `base_url`: **str**
    - The base URL of the ElevenLabs API. Default is "https://api.elevenlabs.io".
- `voice_id`: **str**
    - The voice ID used for text-to-speech. Can be set manually or retrieved using the `get_voice_id` method.

## Methods
##### get_voice_id
- **Description**: Retrieves the ID of an ElevenLabs voice given its name.
- **Parameters**:
    - `voice_name`: **str**
        - The name of the voice to get the ID.
    - `inPlace`: **bool** (default: False)
        - If True, sets the object's `voice_id` attribute to the retrieved voice ID. If False, returns the voice ID.
###### **Returns**: 
- ```str```: The voice ID of the given voice name.
- ```None```: If `inPlace` is True, the method returns None.

###### **Exceptions**:
  - `ValueError`: 
    - If the voice with the given name is not found.
  - `requests.exceptions.HTTPError`: 
    - If an HTTP-related error occurs.
  - `requests.exceptions.ConnectionError`: 
    - If a connection-related error occurs.
  - `json.decoder.JSONDecodeError`: 
    - If there is an error decoding JSON data.
  - `Exception`: 
    - A catch-all exception for unidentified errors.

##### get_audio_to_file
- **Description**: Converts text to audio and saves the audio to a file or files.
- **Parameters**:
    - `text`: (**str** / **list[str]**)
        - The text to convert to speech. Can be a string or a list of strings. If a list, each element will be converted to a separate audio file.
    - `output_file`: **str**
        - The path to save the audio file(s). If text is a list, the output_file string will be used as a prefix for each file.
    - `CHUNK_SIZE`: **int** (default 1024)
        - How many bytes to write to the file at a time. Default is 1024.
    - `voice_id`: **str** (default None)
        - The voice ID to use for the text-to-speech. Use the `get_voice_id` method to obtain the voice ID or pass it in manually.
    - `similarity_boost`: **float** (default 0.55) (0.0 - 1.0)
        - Higher values boost the voice clarity but can introduce artifacts. Default is 0.55.
    - `stability`: **float** (default 0.45) (0.0 - 1.0)
        - A higher stability is more predictable but can be monotone, while a lower stability is more expressive but unstable. Default is 0.45.
    - `style`: **float** (default 0.9) (0.0 - 1.0)
        - Higher values are more "exaggerated" but also a lot more computationally expensive and take longer to generate. Default is 0.90.
###### **Returns**: 
- ```str```: The path to the saved audio file.
- ```list[str]```: If text argument is a list of prompts, the method returns a list of paths to the saved audio files.
###### **Exceptions**:
  - `ValueError`:
    - If text is not a string or a list of strings, or if voice_id is not valid.
  - `requests.exceptions.HTTPError`: 
    - If an HTTP-related error occurs.
  - `requests.exceptions.ConnectionError`: 
    - If a connection-related error occurs.
  - `Exception`: 
    - A catch-all exception for unidentified errors.

## Example Usage:
##### Example 1: Basic, Single Prompt Usage
```python
from scripts.ElevenLabsAPI.elevenLabsAPI.py import elevenLabsAPI
import dotenv

# Load API_KEY from environment file
dotenv.load_dotenv()
API_KEY = os.getenv('ELEVEN_LABS_API_KEY')

# Initialize API Wrapper
elevenLabs = elevenLabsAPI(API_KEY)

# Get the voice_id for the custom model
elevenLabs.get_voice_id('3b1b', inPlace=True)

# Get the text to be converted
text = "Hello, World!"

# Convert the text to speech
elevenLabs.TTS_to_file("TTS_OUTPUT.mp3", text) #  Output will be saved as TTS_OUTPUT.mp3
```

##### Example 2: Advanced, Multi-Prompt Usage
```python
from scripts.ElevenLabsAPI.elevenLabsAPI.py import elevenLabsAPI
import dotenv

# Load API_KEY from environment file
dotenv.load_dotenv()

# Initialize API Wrapper
elevenLabs = elevenLabsAPI(os.getenv('ELEVEN_LABS_API_KEY'))

# Get the voice_id for the custom model
elevenLabs.get_voice_id('3b1b', inPlace=True)

# Get the list of texts to be converted
texts = ["Hello, World!", "This is a test.", "I am a robot."]

# Convert the list of texts to speech
elevenLabs.TTS_to_file("TTS_OUTPUT", texts) #  Output will be saved as TTS_OUTPUT_0.mp3, TTS_OUTPUT_1.mp3, and TTS_OUTPUT_2.mp3
```