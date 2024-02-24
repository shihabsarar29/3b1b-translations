import sys
sys.path.insert(0, sys.path[0] + '/../../')

import json
import os
from scripts.AzureTTS import AzureTTS

main_dir = "Experiments/average_count/"

# text_to_translate = "This is a test. This is only a test."
text_to_translate = ("This is a 3. It's sloppily written and rendered at an extremely low resolution of 28x28 pixels, "
                        "but your brain has no trouble recognizing it as a 3. And I want you to take a moment to "
                        "appreciate how crazy it is that brains can do this so effortlessly. I mean, this, this and this "
                        "are also recognizable as 3s, even though the specific values of each pixel is very different from "
                        "one image to the next. The particular light-sensitive cells in your eye that are firing when you "
                        "see this 3 are very different from the ones firing when you see this 3. But something in that "
                        "crazy-smart visual cortex of yours resolves these as representing the same idea, while at the same "
                        "time recognizing other images as their own distinct ideas.")


try:
    azure_tts = AzureTTS()
    supported_languages = azure_tts.get_supported_languages()
    print(f"Supported languages: {supported_languages}")

    all_languages_average_character_count = {}

    for lang in supported_languages:
        lang_code = lang
        lang = supported_languages[lang_code]
        print(f"Translating to {lang} ({lang_code})...")

        # Translate the text
        translated_text = azure_tts.translate_text(text_to_translate, lang_code)

        # Convert the translated text to speech
        filename = main_dir + f"{lang}.mp3"
        try:
            azure_tts.convert_text_to_speech(text=translated_text, filename= filename)

            # Calculate the audio duration
            audio_duration = azure_tts.get_audio_duration(filename)
            print(f"In {supported_languages[lang_code]} ({lang_code}), the audio duration is {audio_duration} seconds")

            # Calculate average character count
            average_character_count = len(translated_text) / audio_duration
            all_languages_average_character_count[lang] = average_character_count

            print(average_character_count)

        except Exception as e:
            print(f"Error occurred while converting translated text to speech. Error: {e}")

        # Delete the audio file
        try:
            os.remove(filename)
        except Exception as e:
            print(f"Error occurred while deleting audio file. Error: {e}")

    # Write to JSON
    with open(main_dir + f"all_lang_avg_char.json", 'w') as f:
        json.dump(all_languages_average_character_count, f, indent=4)
        print(f"Data written to all_lang_avg_char.json")
        

except Exception as e:
    print(f"Error occurred while translating text to all languages. Error: {e}")