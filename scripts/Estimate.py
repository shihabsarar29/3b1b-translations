""" UPDATE DOCUMENTATION """

import os
import json
import langdetect
import difflib
import warnings

class Estimate:
    '''
    A class to estimate the length of a translated text in a specific language.

    Attributes:
        language_averages_path (str): The path to the JSON file containing the average character count per second for each language
        language_averages (dict): A dictionary containing the average character count per second for each language. This attribute is automatically set using the language_averages_path attribute.
        language_conversion_path (str): = (None) The path to the JSON file containing the language conversion from language code to language name. Only necessary if language code -> language name conversion is not same as [standard](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes).
        
    Methods:
        _get_language: A method to detect the language from the given text.
        _get_conversions: A method to get the default language conversion dictionary if language_conversion_path is not provided.
        estimate_length: A method to estimate the length of a translated text. Can use a specific language or the language detected from the JSON object.
    '''
    def __init__(self, language_averages_path: str, language_conversion_path: str = None) -> None:
        self.language_averages_path = language_averages_path
        self.language_averages = None
        self.language_conversion_path = language_conversion_path

        with open(self.language_averages_path, 'r') as f:
            self.language_averages = json.load(f)
    
    def estimate_length(self, text: str, path: str = None, language: str = None) -> float:
        '''
        A method to estimate the length of a translated text. Can use a specific language or the language detected from the JSON object.

        Parameters:
            text (str) = (None): The text to estimate the length of
            path (str) = (None): The path to the JSON file containing the text. If provided, the function will first attempt to detect the language from the path of the file before using the text parameter.
            language (str) = (None): The language to use for the estimation. If not provided, the language will be detected from the text or path.

        Returns:
            (float): The estimated length of the translated text
        '''

        if not language:
            language = self._get_language(text, path)
        
        # Get the average character count per second for the language
        try:
            average = self.language_averages[language]
        except KeyError:
            # Suggest a language if the language is not found
            suggested_language = difflib.get_close_matches(language, self.language_averages.keys(), n=1)
            suggested_language = suggested_language[0] if suggested_language else "No suggestion available"

            raise KeyError(f'Language "{language}" is not supported. Did you mean "{suggested_language}"? Please provide a valid language code or language name. List of all supported languages: {list(self.language_averages.keys())}')

        # Estimate the length of the translated text
        return len(text) / average

    def estimate_length_list(self, text_list: list, path: str = None, language: str = None) -> list[float]:
        """
        A method to estimate the length of a list of translated texts. Can use a specific language or the language detected from the JSON object.

        Parameters:
            text_list (list[str]): The list of texts to estimate the length of
            path (str) = (None): The path to the JSON file containing the text. If provided, the function will first attempt to detect the language from the path of the file before using the text parameter.
            language (str) = (None): The language to use for the estimation. If not provided, the language will be detected from the text or path.
        
        Returns:
            (list[float]): The estimated length of the translated texts
        """

        if not language: # If language is not provided, detect the language from the text. Saves processing time to do it once here.
            try:
                language = self._get_language(" ".join(text_list), path)
            except ValueError:
                print(len(text_list))
                return [0 for _ in text_list]

        return [self.estimate_length(text, path, language) for text in text_list]
    
    def _get_language(self, text: str, path: str = None, in_keys: bool = True) -> str:
        '''
        A method to detect the language from the given text. Providing a path is more reliable and efficient than providing the text directly. Detecting a language directly from the text may be less accurate and not support all languages.

        Parameters:
            text (str) = (None): The text to detect the language from
            path (str) = (None): The path to the JSON file containing the text. If provided, the function will first attempt to detect the language from the path of the file before using the text parameter.

        Returns:
            (str): The detected language
        '''

        if path:
            # Get the parent directory of the file
            directory = os.path.dirname(path)

            # Get the language from the directory name
            language = os.path.basename(directory)

            if not in_keys and language:
                return language

            if language in list(self.language_averages.keys()):
                return language
            else:
                print("Path does not contain a valid language code. Attempting to detect language from text.")
        
        # If text attribute not available, attempt to load the text from the path
        if not text:
            # Load the JSON file
            with open(path, 'r', encoding="utf-8") as f:
                text = json.load(f)
            
            # Get the translated text from the JSON object
            text = ' '.join([item['translatedText'] for item in text])

        if text:
            # Use the text to detect the language
            try:
                language = langdetect.detect(text)
            except langdetect.lang_detect_exception.LangDetectException:
                raise ValueError(f'Unable to detect a valid language from the text. Please provide a valid language code or language name. Path provided: {path} List of all supported languages: {list(self.language_averages.keys())}')

            # Load the language conversion file if available
            if self.language_conversion_path:
                with open(self.language_conversion_path, 'r') as f:
                    language_conversion = json.load(f)
            else:
                language_conversion = self._get_conversions()

            # Map the language to the correct language name
            try:
                language = language_conversion[language]
            except KeyError:
                raise KeyError(f'Unable to decode a valid language from the text. Please provide a valid language code or language name. List of all supported languages: {list(self.language_averages.keys())}')

            # Give warning if confidence is not high
            if langdetect.detect_langs(text)[0].prob < 0.9:
                warnings.warn(f'Warning: Low confidence of {langdetect.detect_langs(text)[0].prob * 100}% detected for language {language}.')

            return language
        
        # Raise an error if neither text nor path is provided
        raise ValueError('Both text and path have failed to provide a valid language. Please provide a valid text or path.')
    
    def _get_conversions(self) -> dict:
        """
        A method to get the default language conversion dictionary if language_conversion_path is not provided.
        """
        return {
            "en": "english",
            "af": "afrikaans",
            "ar": "arabic",
            "bg": "bulgarian",
            "bn": "bengali",
            "ca": "catalan",
            "cs": "czech",
            "cy": "welsh",
            "da": "danish",
            "de": "german",
            "el": "greek",
            "es": "spanish",
            "et": "estonian",
            "fa": "persian",
            "fi": "finnish",
            "fr": "french",
            "gu": "gujarati",
            "he": "hebrew",
            "hi": "hindi",
            "hr": "croatian",
            "hu": "hungarian",
            "id": "indonesian",
            "it": "italian",
            "ja": "japanese",
            "kn": "kannada",
            "ko": "korean",
            "lt": "lithuanian",
            "lv": "latvian",
            "mk": "macedonian",
            "ml": "malayalam",
            "mr": "marathi",
            "ne": "nepali",
            "nl": "dutch",
            "no": "norwegian",
            "pa": "punjabi",
            "pl": "polish",
            "pt": "portuguese",
            "ro": "romanian",
            "ru": "russian",
            "sk": "slovak",
            "sl": "slovenian",
            "so": "somali",
            "sq": "albanian",
            "sv": "swedish",
            "sw": "swahili",
            "ta": "tamil",
            "te": "telugu",
            "th": "thai",
            "tl": "tagalog",
            "tr": "turkish",
            "uk": "ukrainian",
            "ur": "urdu",
            "vi": "vietnamese",
            "zh-cn": "chinese (simplified)",
            "zh-tw": "chinese (traditional)",
        }

# TESTING:
# estimate = Estimate(r'C:\Users\sapat\Downloads\3b1b\API\Experiments\average_count\3b1b_languages.json')
# print(estimate.estimate_length("Hola, ¿cómo estás?", language="spanish"))