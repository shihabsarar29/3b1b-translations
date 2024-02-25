# AmazonTTS (Polly) Class Documentation

## Overview
The `PollyClient` is a class to interact with [AWS Polly service](https://aws.amazon.com/polly/), which is a cloud service that converts text to speech.

## Attributes
- `polly_client` = **boto3.client**
    - The boto3 client for the Polly service.

## Environment Variables
- `AMAZON_ACCESS_KEY`: **str**
    - The access key for the AWS account.
- `AMAZON_SECRET_KEY`: **str**
    - The secret key for the AWS account.
- `AMAZON_REGION`: **str**
    - The region name for the AWS account, i.e. `eastus`.

## Methods 
### convert_text_to_speech
- **Description**: A method to convert text to speech using AWS Polly and save it to a file.
- **Parameters**:
    - `text`: **str**
        - The text to convert to speech. 
    - `voice_id`: **str** (default: **Joanna**):
        - The ID of the voice to use for the text-to-speech.
    - `output_format`: **str** (default: **mp3**)
        - The format of the audio file. The default is mp3.
    - `output_file`: **str** (default: **output.mp3**)
        - The name of the file to save the audio to.
#### **Returns**:
- ```None```
#### Outputs
- The audio is saved to `output_file`.

### synthesize_speech
- **Description**: A method to synthesize speech using AWS Polly.
- **Parameters**: 
    - `text`: **str**
        - The text to synthesize.
    - `voice_id`: **str** (default: **Joanna**)
        - The ID of the voice to use for the text-to-speech.
    - `output_format`: **str** (default: **mp3**)
        - The format of the audio file. The default is mp3.
#### **Returns**:
- ```dict```: A dictionary containing the output of [polly_client.synthesize_speech](https://docs.aws.amazon.com/polly/latest/dg/SynthesizeSpeechSamplePython.html) method.

### write_speech_to_file
- **Description**: A method to write the synthesized speech to a file.
- **Parameters**:
    - `response`: **dict**
        - The output of the [polly_client.synthesize_speech](https://docs.aws.amazon.com/polly/latest/dg/SynthesizeSpeechSamplePython.html) method.
    - `filename`: **str** (default: **output.mp3**)
        - The name of the file to save the audio to.
#### **Returns**:
- ```None```

### list_voice_ids
- **Description**: A method to list the available voice IDs for AWS Polly.
- **Parameters**:
    - ```None```
#### **Returns**:
- ```list```: A list of the available voice IDs.