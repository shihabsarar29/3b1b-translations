""" UPDATE DOCUMENTATION """

import json
import os

class Parser:
    def __init__(self, file_path, json_encoding='utf-8'):
        '''
        The constructor for the Parser class.

        Inputs:
            file_path (str): The path to the JSON file to parse.
            json_encoding (str): The encoding to use when reading the JSON file. Default is 'utf-8'.

        Outputs:
            None
        '''
        if not os.path.isfile(file_path):
            raise ValueError(f'The file at path {file_path} does not exist. Please provide a valid file path.')
        try:
            with open(file_path, 'r', encoding=json_encoding) as file:
                self.json_list = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f'The file at path {file_path} is not a valid JSON file. {str(e)}')
        except Exception as e:
            raise Exception(f'An error occurred when attempting to read the file at path {file_path}: {str(e)}')
        
    def load_json(self):
        '''
        A method to load the JSON object from the file.

        Inputs:
            None

        Outputs:
            list: A list containing the JSON object.
        '''
        return self.json_list

    def get_translated_texts(self):
        '''
        A method to get the translated texts from the JSON object.

        Inputs:
            None

        Outputs:
            str: A string containing the translated texts.
        '''
        try:
            translated_texts = ' '.join([item['translatedText'] for item in self.json_list])
            print(translated_texts)
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "translatedText" attribute.')
        return translated_texts
    
    
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
    
    
    def get_original_texts_list(self):
        '''
        A method to get the translated texts in list from the JSON object.

        Inputs:
            None

        Outputs:
            str: A list containing the original (non-translated) texts.
        '''
        try:
            return [item['input'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "translatedText" attribute.')
    
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
        except IndexError:
            raise IndexError('The provided JSON object does not contain a valid "time_range" attribute; Unable to get the start timestamps.')
        
    def get_start_timestamps_direct(self):
        '''
        A method to get the start timestamps from the JSON object. Use this method if the JSON object does not contain a "time_range" attribute.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the start timestamps.
        '''
        try:
            return [item['start'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "start" attribute.')

    def get_end_timestamps(self):
        '''
        A method to get the en timestamps from the JSON object.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the start timestamps.
        '''
        try:
            return [item['time_range'][1] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "time_range" attribute.')
        except IndexError:
            raise IndexError('The provided JSON object does not contain a valid "time_range" attribute; Unable to get the end timestamps.')
    
    def get_end_timestamps_direct(self):
        '''
        A method to get the end timestamps from the JSON object. Use this method if the JSON object does not contain a "time_range" attribute.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the end timestamps.
        '''
        try:
            return [item['end'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "end" attribute.')
    
    def get_interval(self):
        '''
        A method to calculate the durations between start and end timestamps.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the durations (in seconds).
        '''
        start_times = self.get_start_timestamps()
        end_times = self.get_end_timestamps()

        # Ensure there is a one-to-one correspondence between start and end times
        if len(start_times) != len(end_times):
            raise ValueError("The number of start timestamps does not match the number of end timestamps.")

        durations = [end - start for start, end in zip(start_times, end_times)]
        return durations
    
    def get_interval_direct(self):
        '''
        A method to calculate the durations between start and end timestamps. Use this method if the JSON object does not contain a "time_range" attribute.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the durations (in seconds).
        '''
        start_times = self.get_start_timestamps_direct()
        end_times = self.get_end_timestamps_direct()

        # Ensure there is a one-to-one correspondence between start and end times
        if len(start_times) != len(end_times):
            raise ValueError("The number of start timestamps does not match the number of end timestamps.")

        durations = [end - start for start, end in zip(start_times, end_times)]
        return durations
    
    def get_reviews(self):
        '''
        A method to get a list of the number of reviews for each item in the JSON object.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the reviews.
        '''
        try:
            return [item['n_reviews'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "n_reviews" attribute.')

    
# Example usage
# file_path = 'Chinese/sentence_translations.json'
# translator = Parser(file_path)
# print(translator.get_original_texts())