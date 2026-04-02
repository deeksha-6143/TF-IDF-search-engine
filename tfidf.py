import math
from collections import Counter

def compute_tf(doc):
    tf = {}
    counts = Counter(doc)
    
    for word, count in counts.items():
        # Logarithmic TF: 1 + log(count) - better for word frequency normalization
        tf[word] = 1 + math.log(count) if count > 0 else 0
    return tf


def compute_idf(docs):
    N = len(docs)
    idf = {}

    all_words = set(word for doc in docs for word in doc)

    for word in all_words:
        count = sum(1 for doc in docs if word in doc)
        # Standard IDF formula: log(N / count) - simpler and more effective
        idf[word] = math.log(N / count) if count > 0 else 0

    return idf


def compute_tfidf(tf, idf):
    return {word: tf[word] * idf.get(word, 0) for word in tf}