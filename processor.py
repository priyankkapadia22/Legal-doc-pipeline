from langdetect import detect
from deep_translator import GoogleTranslator
from datetime import datetime
from config import KEYWORDS

def translate_if_needed(text):
    lang = detect(text)
    if lang != 'en':
        return GoogleTranslator(source=lang, target='en').translate(text)
    return text

def extract_date(filename):
    import re
    match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
    return match.group(0) if match else datetime.now().strftime('%Y-%m-%d')

def extract_metadata(filename, text):
    translated = translate_if_needed(text)
    date = extract_date(filename)
    matched = [kw for kw in KEYWORDS if kw.lower() in translated.lower()]
    snippet = translated[:300] + '...' if len(translated) > 300 else translated
    return {
        'title': filename,
        'date': date,
        'keywords': ','.join(matched),
        'snippet': snippet,
        'text': translated
    }