from openai import OpenAI
from Parser import Parser
from Estimate import Estimate
import dotenv
from typing import Union
import json
import os
import json

class RefactorGPT:
    def __init__(self, api_key: str = None):
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

        client = OpenAI (
            api_key=self.api_key
        )

        self.client = client
        
    def adjust_sentences_based_on_characters_speed(self, file_path, language_averages_path, output_file="adjusted_sentences.json", percent_threshold: int = 95, all = False, save=False, inPlace=False, sentence_translations_output: bool = False) -> Union[None, list]:
        """
        Adjusts sentences based on the specified average speed count.

        Args:
            file_path (str): The file path to the transcript data in JSON format.
            language_averages_path (str): The file path to the language averages data in JSON format.
        """
        # Initialize the Parser with the json sentence data
        parser = Parser(file_path)

        # Retrieve list of sentence durations from the Parser
        try:
            durations = parser.get_interval()
        except KeyError:
            durations = parser.get_interval_direct()

        # Retrieve list of translated texts from the Parser
        translated_texts_list = parser.get_translated_texts_list()

        # Initialize Estimate class
        estimate = Estimate(language_averages_path=language_averages_path)

        # Initialize the adjusted_transcript list
        adjusted_transcript = []

        # Iterate through the translated texts and durations
        for sentence, original_duration in zip(translated_texts_list, durations):
            # Estimate the length of the sentence using character averages
            original_translated_length = estimate.estimate_length(sentence, path=file_path)

            # Calculate the adjustment factor and prompt percentage
            try:
                adjustment_factor = original_translated_length / original_duration
                prompt_percentage = int(adjustment_factor * 100)
            except ZeroDivisionError:
                adjustment_factor = 1
                prompt_percentage = 100

            # Create adjusted_utterance dictionary for storing information
            adjusted_utterance = {

            }

            # If the adjustment factor is less than the threshold, adjust the sentence
            if (original_translated_length < original_duration and not all) or (sentence == ""):
                # Set default values
                adjusted_utterance["is_adjusted"] = False
                adjusted_utterance["original"] = sentence
                adjusted_utterance["adjusted"] = None
                adjusted_utterance["translated_length"] = original_translated_length
                adjusted_utterance["adjusted_translated_length"] = None
                adjusted_utterance["original_length"] = original_duration
                adjusted_utterance["same_language"] = True
                adjusted_utterance["flag"] = "Not Adjusted"

                # Append the adjusted_utterance to the adjusted_transcript list
                adjusted_transcript.append(adjusted_utterance)

                continue
            else:
                print(f"PROMPT PERCENTAGE: {prompt_percentage}")
                print(f"PERCENT THRESHOLD: {percent_threshold}")
                print(f"ALL: {all}")

            #try:
            # Get the language of the sentence
            language = estimate._get_language(sentence, path=file_path)

            # Adjusted Language (placeholder)
            adjusted_language = None

            # Set the context to None
            context = None

            # Generate the prompt and request sentence adjustment from the model
            prompt = f"Rewrite the following sentence to be at most {prompt_percentage}% of its original length, while maintaining the same meaning of the sentence and prioritizing accuracy. The adjusted sentence should be in {language}."

            # Initialize sentence adjustment variable
            adjusted_sentence = ""
            context = None

            # Keep track of the responses so the best one can be chosen
            responses = []

            for i in range(3):
                if sentence == "":
                    break

                adjusted_sentence, is_same_language, is_greater_length, is_same_length, within_threshold, context, new_prompt = self.adjust_GPT(prompt, sentence, context, estimate, language)    
                ' '.join([new_prompt, prompt])
                prompt = new_prompt 

                if is_greater_length and is_same_language and not is_same_length and within_threshold:
                    break           
                else:
                    responses.append({
                        "adjusted_sentence": adjusted_sentence,
                        "is_same_language": is_same_language,
                        "is_greater_length": is_greater_length,
                        "is_same_length": is_same_length,
                        "within_threshold": within_threshold,
                        "character_difference": abs(len(adjusted_sentence) - len(sentence))
                    })
            
            best_response = { # Placeholder
                "adjusted_sentence": "",
                "is_same_language": False,
                "is_greater_length": False,
                "is_same_length": False,
                "within_threshold": False,
                "character_difference": 1000000
            }

            print(responses)

            # Choose the best response
            for response in responses:
                if response["is_same_language"] and response["character_difference"] < best_response["character_difference"]:
                    best_response = response
                else:
                    print(response)
            
            # Set empty flag
            adjusted_utterance["flag"] = ""
            
            # Set the adjusted sentence
            adjusted_sentence = best_response["adjusted_sentence"]
            
            # CHeck if the adjusted sentence is the placeholder
            if adjusted_sentence == "":
                adjusted_sentence = sentence
                adjusted_utterance["flag"] += ".no_adjustment_made"
            elif len(adjusted_sentence) > len(sentence):
                adjusted_sentence = sentence
                adjusted_utterance["flag"] += ".no_adjustment_made"
            
            # Set flag. Should be empty if nothing wrong
            if not best_response["is_same_language"]:
                adjusted_utterance["flag"] += ".language_mismatch"
            if best_response["is_greater_length"]:
                adjusted_utterance["flag"] += ".greater_length"
            if best_response["is_same_length"]:
                adjusted_utterance["flag"] += ".same_length"
            if not best_response["within_threshold"]:
                adjusted_utterance["flag"] += ".not_within_threshold"

            print(f"Original: {sentence}\nAdjusted: {adjusted_sentence}\n")

            # Estimate the length of the adjusted sentence
            adjusted_length = estimate.estimate_length(adjusted_sentence, path=file_path)

            # Print the results (TEMPORARY - for testing purposes only)
            print(f"Original Translated Length: {original_translated_length}")
            print(f"Adjusted Length: {adjusted_length}")

            # Add the original and adjusted sentences to the adjusted_transcript dictionary
            adjusted_utterance["is_adjusted"] = True
            adjusted_utterance["original"] = sentence
            adjusted_utterance["adjusted"] = adjusted_sentence
            adjusted_utterance["translated_length"] = original_translated_length
            adjusted_utterance["adjusted_translated_length"] = adjusted_length
            adjusted_utterance["original_length"] = original_duration
            adjusted_utterance["same_language"] = True

            # Append the adjusted_utterance to the adjusted_transcript list
            adjusted_transcript.append(adjusted_utterance)
            #except Exception as e:
            #    print(f"An error occurred while adjusting sentence: {e}")
            
            # TESTING ONLY (to save money and time):
            # break

        # Write to json file (if save is True)
        if save:
            if sentence_translations_output:
                # Load json file from file_path
                with open(file_path, "r", encoding="utf-8") as f:
                    sentence_translations = json.load(f)
                
                output_sentence_translations = []

                for utterance, adjusted_utterance_ in zip(sentence_translations, adjusted_transcript):
                    new_utterance = {}

                    try:
                        new_utterance["input"] = utterance["input"]
                    except KeyError:
                        new_utterance["input"] = None
                    
                    try:
                        new_utterance["translatedText"] = utterance["translatedText"]
                    except KeyError:
                        new_utterance["translatedText"] = None

                    try:
                        new_utterance["model"] = utterance["model"]
                    except KeyError:
                        new_utterance["model"] = None

                    try:
                        new_utterance["time_range"] = utterance["time_range"]
                    except KeyError:
                        try:
                            new_utterance["start"] = utterance["start"]
                            new_utterance["end"] = utterance["end"]
                        except:
                            new_utterance["time_range"] = None
                    
                    try:
                        new_utterance["adjusted"] = adjusted_utterance_["adjusted"]
                    except KeyError:
                        new_utterance["adjusted"] = None
                    
                    try:
                        new_utterance["adjusted_flag"] = adjusted_utterance_["flag"]
                    except KeyError:
                        new_utterance["adjusted_flag"] = None

                    try:
                        new_utterance["adjusted_estimated_time"] = adjusted_utterance_["adjusted_translated_length"]
                    except KeyError:
                        new_utterance["adjusted_estimated_time"] = None

                    output_sentence_translations.append(new_utterance)
                
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(output_sentence_translations, f, indent=4, ensure_ascii=False)
                
                print("output_sentence_translations: ", output_sentence_translations)

                return

            if inPlace:
                # Wtite to the same directory as the input file (inPlace)
                output_path = os.path.join(os.path.dirname(file_path), output_file)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(adjusted_transcript, f, indent=4, ensure_ascii=False)
            else:
                # Write directly to the specified output file path (not inPlace)
                print("dumping directly!")
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(adjusted_transcript, f, indent=4, ensure_ascii=False)
        else:
            # Return the adjusted_transcript list
            return adjusted_transcript

    def adjust_GPT(self, prompt: str, sentence: str, context: str, estimate: Estimate, language: str) -> tuple[str, bool, bool, list[dict], str]:
        """
        Adjusts the GPT-3.5 output based on the specified average speed count.

        Args:
            text (str): The text to adjust.
            language (str): The language of the text.
            percent_threshold (int): The percentage threshold to adjust the text.
            all (bool): If True, adjust all sentences regardless of the threshold.

        Returns:
            str: The adjusted text.
        """

        if not context:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",  # Using GPT-3.5 Turbo
                messages=[{"role": "system", "content": prompt}, {"role": "user", "content": sentence}],
            )
        else:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",  # Using GPT-3.5 Turbo
                messages=context + [{"role": "system", "content": prompt}, {"role": "user", "content": sentence}],
            )

        adjusted_sentence = response.choices[0].message.content

        # Get the output language of the adjusted sentence
        adjusted_language = estimate._get_language(adjusted_sentence, path=file_path)

        # Get context
        context = [{"role": "system", "content": prompt}, {"role": "user", "content": sentence}]

        # Return variable
        is_same_language = adjusted_language == language
        is_greater_length = len(adjusted_sentence) > len(sentence)
        is_same_length = len(adjusted_sentence) == len(sentence)

        # If the adjusted sentence is within 10% of the original sentence or there is less than a 7 character difference, then the adjusted sentence is within the threshold
        within_threshold = len(adjusted_sentence) <= len(sentence) * 1.1 or len(adjusted_sentence) - len(sentence) < 7

        # Next prompt
        next_prompt = ""

        if not is_same_language:
            ' '.join([next_prompt, "Please ensure the adjusted sentence is in the same language as the original sentence. If the language is already the same, please disregard this message and continue."])
        if is_greater_length:
            ' '.join([next_prompt, "The adjusted sentence is longer than the original sentence. Please ensure the adjusted sentence is shorter than the original sentence while maintaining the same meaning."])
        if is_same_length:
            ' '.join([next_prompt, "The adjusted sentence is the same length as the original sentence. Please ensure the adjusted sentence is shorter than the original sentence while maintaining the same meaning."])
        if not within_threshold and not is_same_length and not is_greater_length:
            ' '.join([next_prompt, "The adjusted sentence is not short enough. Please ensure the adjusted sentence is shorter than the original sentence while maintaining the same meaning. If the adjusted sentence is already shorter than the original sentence, please disregard this message and continue."])

        return adjusted_sentence, is_same_language, is_greater_length, is_same_length, within_threshold, context, next_prompt
     

# Example usage
file_path = r'C:\Users\sapat\Downloads\3b1b\API\Experiments\n_reviews_check\3b1bTranslationsP\2019\clacks\chinese\sentence_translations.json' #File Path
language_averages_path = r"C:\Users\sapat\Downloads\3b1b\API\Experiments\average_count\3b1b_languages.json"

refactor = RefactorGPT()

refactor.adjust_sentences_based_on_characters_speed(file_path, language_averages_path, save=True, sentence_translations_output=True)