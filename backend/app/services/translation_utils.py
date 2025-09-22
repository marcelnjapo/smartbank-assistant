
from deep_translator import GoogleTranslator

def translate_to_english(text: str) -> str:
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}"
