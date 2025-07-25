from deep_translator import GoogleTranslator

def translate_text(text, target_language='en'):
    translator = GoogleTranslator(source='auto', target=target_language)
    translation = translator.translate(text)
    return translation

# Exemple d'utilisation
#translated_text = translate_text("Bonjour, comment ça va ?", 'en')
#print(translated_text)
