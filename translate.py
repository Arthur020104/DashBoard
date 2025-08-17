from langdetect import detect
from googletrans import Translator

async def translateIfNeeded(text):
    try:
        language = detect(text)
        if language != 'en':
            translator = Translator()
            translated = await translator.translate(text, src=language, dest='en')
            return translated.text.lower()
        
        return text.lower()
    except Exception as e:
        print(f"Translation error: {e}")
        return text.lower()