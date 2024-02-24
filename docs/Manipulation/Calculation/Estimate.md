# Estimate Class

## Overview
This class is used to estimate how long a translated text will take to speak using character counts.

## Attributes
- language_averages_path: **str**:
    - The path to the JSON file containing the average characters spoken per second for each language.
- language_averages: **dict**:
    - A dictionary containing the average characters spoken per second for each language. This attribute is automatically set when initializing the class using the language_averages_path attribute.
- language_conversion_path: **str** (default **None**)
    - The path to the JSON file containing the language conversion from language code to language name. Only necessary if not using path to detect language and if language name in **language_averages** dictionary is not same as [standard](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes).

## Methods
### _get_language
- **Description**: Detects the language of the given text. 
- **Parameters**:
    - `text`: **str**
        - The text to detect the language from. This function will try to determine the language of the text using the `langdetect` library. 55 languages are supported, they can be found [here](../../json/supported_languages.json).
    - `path`: **str** (default **None**)
        - The path to the JSON file where text is from. If provided, the function will first attempt to detect the language from the path of the file before using the text parameter. It will do this by checking the name of the file's parent directory.
#### **Returns**:
- ```str```: The detected language (full name).
#### **Exceptions**:
- ```KeyError```: If the language detected from **text** and/or **path** is not available in **language_averages**
#### **Warnings**:
- ```Low Confidence```: If it has a confidence of under 90% in the language detected from text.

### estimate_length
- **Description**: Estimate the speaking of a given translated text.
- **Parameters**
    - `text`: **str** (default **None**)
        - The text to estimate the length of.
    - `path`: **str** (default **None**)
        - The path to the file containing the text to estimate the length of. If provided, the function will first attempt to detect the language from the path of the file before using the text parameter.
    - `language`: **str** (default **None**)
        - The language of the text. If not provided, the function will attempt to detect the language from the text or path.
#### **Returns**:
- ```float```: The estimated length of the text in seconds.
#### **Exceptions**:
- ```KeyError```: If the language detected from **text** and/or **path** is not available in **language_averages**. It will try to provide a suggestion for the language to use if it is not found in **language_averages**.

### _get_conversions
- **Description**: Get the default language conversion dictionary if language_conversion_path is not provided.
#### **Returns**:
- ```dict```: The default language conversion dictionary. The keys are the language codes and the values are the languages' full names. Language codes are based on the ISO 639-1 standard.

## Example Usage:
##### Example 1: Basic Usage (Language Provided)
```python
from Estimate import Estimate

estimate = Estimate(r'path/to/3b1b_languages.json')
print(estimate.estimate_length("Hola, ¿cómo estás?", language="spanish"))
```

##### Example 2: Advanced Usage (Language Detected)
```python
from Estimate import Estimate

estimate = Estimate(r'path/to/3b1b_languages.json')
print(estimate.estimate_length("Hola, ¿cómo estás?", path=r'path/to/spanish/transcript.json'))
```