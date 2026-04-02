import re

STOPWORDS = {"is", "a", "the", "and", "in", "are", "for", "of", "to"}

def preprocess(text):
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)
    return [w for w in words if w not in STOPWORDS]