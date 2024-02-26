import openai
from openai import OpenAI
from Parser import Parser
from Estimate import Estimate
import dotenv
from typing import Union

openai.api_key = dotenv.get_key(dotenv.find_dotenv(), "OPENAI_API_KEY")

client = OpenAI (
    
)

def adjust_sentences_based_on_characters_speed(file_path, language_averages_path, save=False, save_path=None) -> Union[dict, None]:
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

    # Iterate through the translated texts and durations
    for sentence, duration in zip(translated_texts_list, durations):
        # Estimate the length of the sentence using character averages
        length = estimate.estimate_length(sentence, path=file_path)

        # Calculate the adjustment factor and prompt percentage
        adjustment_factor = length / duration
        prompt_percentage = int(adjustment_factor * 100)

        try:
            # Generate the prompt and request sentence adjustment from the model
            prompt = f"Rewrite the following sentence to be {prompt_percentage}% or less of its original length, while mainting the same meaning of the sentence and prioritizing accuracy:\n\n{sentence}"
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",  # Using GPT-3.5 Turbo
                prompt=prompt,
                temperature=0.5,
                max_tokens=100
            )
            adjusted_sentence = response.choices[0].text.strip()
            print(f"Original: {sentence}\nAdjusted: {adjusted_sentence}\n")

            # Estimate the length of the adjusted sentence
            adjusted_length = estimate.estimate_length(adjusted_sentence, path=file_path)

            # Print the results (TEMPORARY - for testing purposes only)
            print(f"Original Length: {duration}")
            print(f"Adjusted Length: {adjusted_length}")
        except Exception as e:
            print(f"An error occurred while adjusting sentence: {e}")
        
        # TESTING ONLY (to save money and time):
        break

# Example usage
file_path = r'C:\Users\sapat\Downloads\3b1b\API\256-bit-security\bengali\sentence_translations.json' #File Path
language_averages_path = r"C:\Users\sapat\Downloads\3b1b\API\Experiments\average_count\3b1b_languages.json"
adjust_sentences_based_on_characters_speed(file_path, language_averages_path)