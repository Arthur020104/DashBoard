from langdetect import detect
from deep_translator import GoogleTranslator

def translateIfNeeded(text):
    try:
        language = detect(text)
        if language != 'en':
            translateText = GoogleTranslator(source=language, target='en').translate(text)
            return translateText.lower()
        
        return text.lower()
    except Exception as e:
        print(f"Translation error: {e}")
        return text.lower()