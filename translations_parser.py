import json
import os

class TranslationsParser:
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
        

    def get_translated_texts(self, is_list=False):
        '''
        A method to get the translated texts from the JSON object.

        Inputs:
            None

        Outputs:
            str: A string containing the translated texts.
        '''
        try:
            if is_list:
                return [item['translatedText'] for item in self.json_list]
            else:
                translated_texts = ' '.join([item['translatedText'] for item in self.json_list])
                return translated_texts
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "translatedText" attribute.')
    
    
    
    def get_original_texts(self, is_list=False):
        '''
        A method to get the original texts from the JSON object.

        Inputs:
            None

        Outputs:
            str: A string containing the original texts.
        '''
        try:
            if is_list:
                return [item['input'] for item in self.json_list]
            else:
                original_texts = [item['input'] for item in self.json_list]
                return ' '.join(original_texts)
        except KeyError:
            raise KeyError('The provided JSON object does not contain an "input" attribute.')
    
    
    def get_start_timestamps(self):
        '''
        A method to get the start timestamps from the JSON object.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the start timestamps.
        '''
        try:
            return [item['start'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "time_range" attribute.')
        except IndexError:
            raise IndexError('The provided JSON object does not contain a valid "time_range" attribute; Unable to get the end timestamps.')


    def get_end_timestamps(self):
        '''
        A method to get the en timestamps from the JSON object.

        Inputs:
            None

        Outputs:
            list[int]: A list containing the start timestamps.
        '''
        try:
            return [item['end'] for item in self.json_list]
        except KeyError:
            raise KeyError('The provided JSON object does not contain a "time_range" attribute.')
        except IndexError:
            raise IndexError('The provided JSON object does not contain a valid "time_range" attribute; Unable to get the end timestamps.')
    
    
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
# file_path = '/Users/shihab/Documents/3b1b/captions/2017/neural-networks/italian/sentence_translations.json'
# translator = TranslationsParser(file_path)
# print(translator.get_original_texts())