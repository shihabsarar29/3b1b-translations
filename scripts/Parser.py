import json
import os

class Parser:
    def __init__(self, file_path):
        '''
        The constructor for the Parser class.

        Inputs:
            file_path (str): The path to the JSON file to parse.

        Outputs:
            None
        '''
        if not os.path.isfile(file_path):
            raise ValueError(f'The file at path {file_path} does not exist. Please provide a valid file path.')
        try:
            with open(file_path, 'r') as file:
                self.json_list = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f'The file at path {file_path} is not a valid JSON file.')
        except Exception as e:
            raise Exception(f'An error occurred when attempting to read the file at path {file_path}: {str(e)}')
        

    def get_translated_texts(self):
        '''
        A method to get the translated texts from the JSON object.

        Inputs:
            None

        Outputs:
            str: A string containing the translated texts.
        '''
        try:
            translated_texts = [item['translatedText'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "translatedText" attribute.')
        return ' '.join(translated_texts)
    

    def get_translated_texts_list(self):
        '''
        A method to get the translated texts in list from the JSON object.

        Inputs:
            None

        Outputs:
            str: A list containing the translated texts.
        '''
        try:
            return [item['translatedText'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "translatedText" attribute.')
    
    
    def get_original_texts(self):
        '''
        A method to get the original texts from the JSON object.

        Inputs:
            None

        Outputs:
            str: A string containing the original texts.
        '''
        try:
            original_texts = [item['input'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain an "input" attribute.')
        return ' '.join(original_texts)
    
    def get_start_timestamps(self):
        '''
        A method to get the start timestamps from the JSON object.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the start timestamps.
        '''
        try:
            return [item['time_range'][0] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "start" attribute.')
    
# Example usage
# file_path = 'Chinese/sentence_translations.json'
# translator = Parser(file_path)
# print(translator.get_original_texts())