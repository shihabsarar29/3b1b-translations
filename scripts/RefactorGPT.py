from openai import OpenAI
from Parser import Parser
from Estimate import Estimate
import dotenv
from typing import Union
import json
import os

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
        
    def adjust_sentences_based_on_characters_speed(self, file_path, language_averages_path, output_file="adjusted_sentences.json", percent_threshold: int = 80, all = False, save=False, inPlace=False) -> Union[None, list]:
        """
        Adjusts sentences based on the specified average speed count.

        Args:
            file_path (str): The file path to the transcript data in JSON format.
            language_averages_path (str): The file path to the language averages data in JSON format.
        """
        # Initialize the Parser with the json sentence data
        parser = Parser(file_path)

        # Retrieve list of sentence durations from the Parser
        durations = parser.get_interval()

        # Retrieve list of translated texts from the Parser
        translated_texts_list = parser.get_translated_texts_list()

        # Initialize Estimate class
        estimate = Estimate(language_averages_path=language_averages_path)

        # Initialize the adjusted_transcript list
        adjusted_transcript = []

        # Iterate through the translated texts and durations
        for sentence, duration in zip(translated_texts_list, durations):
            # Estimate the length of the sentence using character averages
            length = estimate.estimate_length(sentence, path=file_path)

            # Calculate the adjustment factor and prompt percentage
            adjustment_factor = length / duration
            prompt_percentage = int(adjustment_factor * 100)

            # Create adjusted_utterance dictionary for storing information
            adjusted_utterance = {

            }

            # If the adjustment factor is less than the threshold, adjust the sentence
            if (prompt_percentage > percent_threshold and not all) or (sentence == ""):
                # Set default values
                adjusted_utterance["is_adjusted"] = False
                adjusted_utterance["original"] = sentence
                adjusted_utterance["adjusted"] = None
                adjusted_utterance["original_translated_length"] = duration
                adjusted_utterance["adjusted_translated_length"] = None
                adjusted_utterance["target_length"] = length
                adjusted_utterance["same_language"] = True

                # Append the adjusted_utterance to the adjusted_transcript list
                adjusted_transcript.append(adjusted_utterance)

                continue
            else:
                print(f"PROMPT PERCENTAGE: {prompt_percentage}")
                print(f"PERCENT THRESHOLD: {percent_threshold}")
                print(f"ALL: {all}")

            try:
                # Get the language of the sentence
                language = estimate._get_language(sentence, path=file_path)

                # Adjusted Language (placeholder)
                adjusted_language = None

                # Set the context to None
                context = None

                # Generate the prompt and request sentence adjustment from the model
                prompt = f"Rewrite the following sentence to be around {prompt_percentage}% of its original length, while maintaining the same meaning of the sentence and prioritizing accuracy. The adjusted sentence should be in {language}."

                # Initialize sentence adjustment variable
                adjusted_sentence = ""
                context = None

                for i in range(3):
                    if sentence == "":
                        break

                    adjusted_sentence, is_same_language, is_less_length, context, prompt = self.adjust_GPT(prompt, sentence, context, estimate, language)       

                    if is_less_length and is_same_language:
                        break            


                print(f"Original: {sentence}\nAdjusted: {adjusted_sentence}\n")

                # Estimate the length of the adjusted sentence
                adjusted_length = estimate.estimate_length(adjusted_sentence, path=file_path)

                # Print the results (TEMPORARY - for testing purposes only)
                print(f"Original Length: {duration}")
                print(f"Adjusted Length: {adjusted_length}")

                # Add the original and adjusted sentences to the adjusted_transcript dictionary
                adjusted_utterance["is_adjusted"] = True
                adjusted_utterance["original"] = sentence
                adjusted_utterance["adjusted"] = adjusted_sentence
                adjusted_utterance["original_translated_length"] = duration
                adjusted_utterance["adjusted_translated_length"] = adjusted_length
                adjusted_utterance["target_length"] = length

                # Append the adjusted_utterance to the adjusted_transcript list
                adjusted_transcript.append(adjusted_utterance)
            except Exception as e:
                print(f"An error occurred while adjusting sentence: {e}")
            
            # TESTING ONLY (to save money and time):
            # break

        print(adjusted_transcript)
        print(prompt)

        # Write to json file (if save is True)
        if save:
            if inPlace:
                # Wtite to the same directory as the input file (inPlace)
                output_path = os.path.join(os.path.dirname(file_path), output_file)
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(adjusted_transcript, f, indent=4, ensure_ascii=False)
            else:
                # Write directly to the specified output file path (not inPlace)
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
        is_same_language = adjusted_language is language
        is_less_length = len(adjusted_sentence) > len(sentence)

        # Next prompt
        next_prompt = ""

        if not is_same_language:
            next_prompt += "Please ensure the adjusted sentence is in the same language as the original sentence. If the language is already the same, please disregard this message and continue."
        if is_less_length:
            next_prompt += "The adjusted sentence is longer than the original sentence. Please ensure the adjusted sentence is shorter than the original sentence while maintaining the same meaning."

        return adjusted_sentence, is_same_language, is_less_length, context, next_prompt      
     

# Example usage
file_path = r'C:\Users\sapat\Downloads\3b1b\API\256-bit-security\bengali\sentence_translations.json' #File Path
language_averages_path = r"C:\Users\sapat\Downloads\3b1b\API\Experiments\average_count\3b1b_languages.json"

refactor = RefactorGPT()

refactor.adjust_sentences_based_on_characters_speed(file_path, language_averages_path, save=True)