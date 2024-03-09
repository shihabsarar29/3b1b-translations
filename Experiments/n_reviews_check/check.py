""" UPDATE DOCUMENTATION """
import json
import os
import sys
from typing import Union

# Add parent directory to start of module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import from scripts
from scripts.FileUtils import FileUtils
from scripts.Estimate import Estimate
from scripts.Parser import Parser

class Validate:
    """
    ### Validate
    Class to validate the fulfillment of the conditions for JSON files in a directory.

    #### Initialization Parameters:
    root_directory: ```str```
        The root directory to search for JSON files
    language_averages_path: ```str```
        The path to the JSON file containing the average character count per second for each language
    json_filename: ```str``` = "sentence_translations.json"
        The name of the JSON file to search for.
    target_directory: ```str``` = ```None```
        The target directory to search for JSON files. If not provided, all JSON files in the root_directory will be considered

    #### Attributes:
    fileUtils: ```FileUtils```
        An instance of the FileUtils class to use for file operations. Initialized with the root_directory, target_directory, and json_filename.
    estimate: ```Estimate```
        An instance of the Estimate class to use for estimating the length of translated texts. Initialized with the language_averages_path.
    """

    def __init__(self, language_averages_path: str, json_filename='sentence_translations.json', target_directory: str = None):
        self.target_directory = target_directory
        self.json_filename = json_filename

        # Create Estimate object
        self.estimate = Estimate(language_averages_path)
    
    def check_fullfilment_full(self, root_directory: str, output_file: str) -> None:
        """
        """
        json_files_list = []

        json_files_list = self.get_all_fulfillment_jsons(root_directory)
        print(json_files_list)

        json_files_dict = {}

        for json_file in json_files_list:
            video_name = json_file.split("\\")[-3]
            language_name = json_file.split("\\")[-2]
            if video_name not in json_files_dict:
                json_files_dict[video_name] = {}

            json_files_dict[video_name][language_name] = json.load(open(json_file, "r"))["fulfilled"]
        
        # Save to output_file 
        with open(output_file, "w") as f:
            json.dump(json_files_dict, f, indent=4)

    def check_fulfillment(self, root_directory: str, output_file: str, inPlace: bool = False) -> None:
        """
        ### check_fulfillment
        Check if all JSON files in the root_directory are fulfill all conditions to be considered as fulfilled.

        #### Fulfilled conditions:
        - The JSON file has atleast 80% n_reviews > 0
        - Atleast 80% of translated sentences are estimated to have a translated duration that is similar to the original duration

        #### Parameters:
        output_file: ```str```
            The relative path to the (JSON) output file to write the results to
        inPlace: ```bool``` = ```False```
            If True, the results will be written to a JSON file at `output_file` relative to the directory of `json_filename` passed in at initialization. If false, the results will be written to a single JSON file at `output_file`.

        #### Returns:
        ```None```

        #### Note:
        This function assumes that the parent directory of the JSON files is the language name. It uses this as the key when writing the results to the output file. If the parent directory is not a language name, the function will try to detect the language from the text itself. This may be less accurate. Refer to the [language detection documentation](https://github.com/shihabsarar29/3b1b-translations/blob/main/docs/Manipulation/Calculation/Estimate.md) for more information.
        """

        # test
        fileUtils = FileUtils(root_directory, self.target_directory, self.json_filename)

        # Get all JSON files in the root_directory
        if fileUtils.target_directory is not None:
            json_files = fileUtils.get_json_files()
        else:
            json_files = fileUtils.get_json_files_root()
        
        # Counters for the total number of JSON files and the number of JSON files that fulfill the conditions
        n_total = len(json_files)
        n_fulfilled = 0

        # Dicitionary to store the results
        fulfillment_dict = {}

        for json_file in json_files:
            # Counters for the current file
            n_reviews = 0
            n_similar_durations = 0

            # Output file for the current file
            output_file_path = os.path.join(os.path.dirname(json_file), output_file)

            # Check if the JSON file fulfills the conditions
            results = self.check_fulfillment_single_file(json_file, output_file=output_file_path, inPlace=inPlace)

            # If InPlace, continue to the next file
            if inPlace:
                if results: n_fulfilled += 1
                continue

            # Attempt to get the language name from the parent directory
            try:
                language_name = self.estimate._get_language(None, json_file)

                # Write the results to the dictionary
                fulfillment_dict[language_name] = {
                    "n_reviews_fulfilled": results[0],
                    "n_reviews_fulfilled_bool": results[1],
                    "similar_durations_fulfilled": results[2],
                    "similar_durations_fulfilled_bool": results[3],
                    "fulfilled": results[3] and results[1],
                    "n_total_utterances": results[4]
                }
            except ValueError:
                # If the language name is not found, write the results to the dictionary with the parent directory as the key
                fulfillment_dict[self.estimate._get_language(None, json_file, in_keys=False)] = {
                    "n_reviews_fulfilled": None,
                    "n_reviews_fulfilled_bool": None,
                    "similar_durations_fulfilled": None,
                    "similar_durations_fulfilled_bool": None,
                    "fulfilled": None,
                    "n_total_utterances": None
                }

            # Increment the counter if the conditions are fulfilled
            if results[3] and results[1]: n_fulfilled += 1


        print(f"{n_fulfilled} out of {n_total} JSON files fulfill the conditions. ({n_fulfilled/n_total*100:.2f}%)")

        # Write the results to the output file if not InPlace
        if not inPlace:
            with open(output_file, 'w') as f:
                json.dump(fulfillment_dict, f)

        return
    
    def check_fulfillment_single_file(self, input_file: str, output_file: str = None, inPlace: bool = False) -> Union[tuple[int, bool, int, bool, bool, int], bool]:
        """
        ### check_fulfillment_single_file
        Check if a JSON file fulfills all conditions to be considered as fulfilled.

        #### Fulfilled conditions:
        - The JSON file has atleast 80% n_reviews > 0
        - Atleast 80% of translated sentences are estimated to have a translated duration that is similar to the original duration

        #### Parameters:
        input_file: ```str```
            The path to the JSON file to check
        output_file: ```str``` = ```None```
            The relative path to the (JSON) output file to write the results to. If InPlace is False, this parameter will be ignored.
        inPlace: ```bool``` = ```False```
            If True, the results will be written to a JSON file at `output_file` relative to the directory of `json_filename` passed in at initialization. If false, the results will be returned as a tuple.

        #### Returns:
        ```tuple[int, bool, int, bool, bool, int]```
            The number of reviews that are fulfilled
            A boolean indicating if the n_reviews condition is fulfilled
            The number of similar durations that are fulfilled
            A boolean indicating if the similar durations condition is fulfilled
            Whether or not the conditions are fulfilled
            The number of utterances in the JSON file
        ```bool```
            If InPlace is True, the function will return whether or not the conditions are fulfilled.
        """

        # Get JSON object from the file
        try:
            parser = Parser(input_file)
        except ValueError:
            print("Invalid file: ", input_file)

            if inPlace:
                with open(output_file, 'w') as f:
                    json.dump({
                        "n_reviews_fulfilled": None,
                        "n_reviews_fulfilled_bool": None,
                        "similar_durations_fulfilled": None,
                        "similar_durations_fulfilled_bool": None,
                        "fulfilled": None,
                        "n_total_utterances": None
                    }, f)

                return False
            else:
                return 0, False, 0, False, False, 0

        # Get all translated texts as a list
        translated = parser.get_translated_texts_list()

        # Get all the intervals
        try:
            intervals = parser.get_interval()
        except KeyError:
            intervals = parser.get_interval_direct()

        # Get the number of reviews
        n_reviews = parser.get_reviews()

        # Estimate the length of the translated texts
        estimated_lengths = self.estimate.estimate_length_list(translated, input_file)

        # Check if atleast 80% of n_reviews > 0
        try:
            n_reviews_fulfilled = sum([1 for review in n_reviews if review > 0])
            n_reviews_fulfilled_bool = n_reviews_fulfilled/len(n_reviews) >= 0.8

            # Check if atleast 80% of translated sentences are estimated to have a translated duration that is similar to the original duration (within 1 second)
            similar_durations_fulfilled = sum([1 for original, translated in zip(intervals, estimated_lengths) if abs(original - translated) <= 1])
            similar_durations_fulfilled_bool = similar_durations_fulfilled/len(intervals) >= 0.5
        except ZeroDivisionError:
            n_reviews_fulfilled = 0
            n_reviews_fulfilled_bool = False
            similar_durations_fulfilled = 0
            similar_durations_fulfilled_bool = False

        # If InPlace, write the results to the output file
        if inPlace:
            with open(output_file, 'w') as f:
                json.dump({
                    "n_reviews_fulfilled": n_reviews_fulfilled,
                    "n_reviews_fulfilled_bool": n_reviews_fulfilled_bool,
                    "similar_durations_fulfilled": similar_durations_fulfilled,
                    "similar_durations_fulfilled_bool": similar_durations_fulfilled_bool,
                    "fulfilled": n_reviews_fulfilled_bool and similar_durations_fulfilled_bool,
                    "n_total_utterances": len(intervals)
                }, f)

            return n_reviews_fulfilled_bool and similar_durations_fulfilled_bool
        
        # Return the results if not InPlace
        return n_reviews_fulfilled, n_reviews_fulfilled_bool, similar_durations_fulfilled, similar_durations_fulfilled_bool, len(intervals)
    
    def check_fulfillment_full_dir(self, current_path: str, target_path: str = "chinese") -> None:
        """Output"""
        # For each subfolder, go down one level
        if (not (target_path in os.listdir(current_path))):
            for subfolder in os.listdir(current_path):
                subfolder_path = os.path.join(current_path, subfolder)
                if os.path.isdir(subfolder_path):
                    self.check_fulfillment_full_dir(subfolder_path, target_path=target_path)
        else:
            self.check_fulfillment(current_path, output_file="fulfillment.json", inPlace=True)
    
    def get_all_fulfillment_jsons(self, current_path: str, target_path: str = "chinese") -> list[str]:
        """Output"""
        lists = []

        # For each subfolder, go down one level
        if (not (target_path in os.listdir(current_path))):
            for subfolder in os.listdir(current_path):
                subfolder_path = os.path.join(current_path, subfolder)
                if os.path.isdir(subfolder_path):
                    lists += self.get_all_fulfillment_jsons(subfolder_path, target_path=target_path)
        else:
            # Loop through all directories and get the fulfillment.json file
            for subfolder in os.listdir(current_path):
                subfolder_path = os.path.join(current_path, subfolder)
                if os.path.isdir(subfolder_path):
                    json_file = os.path.join(subfolder_path, "fulfillment.json")
                    if os.path.exists(json_file):
                        lists.append(json_file)
        
        return lists

# Usage:
root_directory = r'C:\Users\sapat\Downloads\3b1b\API\Experiments\n_reviews_check\3b1bTranslationsP'
language_averages_path = r'C:\Users\sapat\Downloads\3b1b\API\Experiments\average_count\3b1b_languages.json'
validator = Validate(language_averages_path)
validator.check_fulfillment(root_directory, 'fulfillment.json', inPlace=True)
validator.check_fullfilment_full(root_directory, "fulfillment.json")