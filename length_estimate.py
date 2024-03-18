
class LengthEstimate:
    '''
    A class to estimate the length of a translated text in a specific language.
    It uses predefined average character counts per second for various languages to calculate estimates.
    
    Methods:
    estimate_length: Estimates the length of a translated text given the text itself, optionally a file path, and/or a specified language.
    '''
    
    language_averages = {
        "albanian": 16.18988391376451,
        "arabic": 11.140235910878113,
        "bengali": 16.13188367364978,
        "bulgarian": 14.547497288083061,
        "catalan": 16.559000861326442,
        "chinese": 5.550509637703098,
        "croatian": 14.401709401709402,
        "czech": 14.001308151418527,
        "danish": 16.473123955309227,
        "dutch": 16.56807270233196,
        "estonian": 16.764995083579155,
        "finnish": 14.299687010954617,
        "french": 21.795672076570952,
        "georgian": 18.316466371494833,
        "german": 17.68689298761472,
        "greek": 17.22652885443583,
        "gujarati": 11.106060606060606,
        "hebrew": 12.714206744057492,
        "hindi": 14.336328438892542,
        "hungarian": 14.151651651651651,
        "indonesian": 15.516253172848606,
        "italian": 18.016194331983804,
        "japanese": 6.64344685242518,
        "korean": 7.758916323731139,
        "lithuanian": 16.92236169223617,
        "malay": 15.41636319495023,
        "marathi": 14.64926464926465,
        "norwegian": 16.8747737965979,
        "persian": 13.159940906616903,
        "polish": 14.450753095181769,
        "portuguese": 16.675374433995124,
        "romanian": 16.23766623766624,
        "russian": 14.875315656565656,
        "serbian": 14.0914129785964,
        "slovak": 14.073297616274555,
        "slovenian": 15.09809239670916,
        "spanish": 18.300102967331274,
        "swedish": 17.050777590406597,
        "tagalog": 14.544025157232705,
        "tamil": 14.422100345317896,
        "telugu": 14.449427005480818,
        "thai": 14.207650273224044,
        "turkish": 15.403253721010731,
        "ukrainian": 15.879230836161142,
        "urdu": 19.284386617100374,
        "vietnamese": 17.01682466478777,
        "english": 19.780835684743522
    }

    def estimate_length(self, text: str, language: str) -> float:
        '''
        Estimates the length of a translated text based on the language's average character count per second.
        
        Parameters:
            text (str): The text to estimate the length of.
            language (str, optional): The language to use for the estimate. If not provided, the language will be detected.
        
        Returns:
            float: An estimated length of the translated text in seconds.
        '''
        try:
            average = self.language_averages[language]
        except KeyError:
            raise KeyError(f'Language "{language}" is not supported')

        return len(text) / average



# Example usage:
# length_estimate = LengthEstimate()
# print(length_estimate.estimate_length(text="Hola, ¿cómo estás?", language="spanish"))