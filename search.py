import math

def cosine_similarity(vec1, vec2):
    common = set(vec1.keys()) & set(vec2.keys())

    dot = sum(vec1[w] * vec2[w] for w in common)

    mag1 = math.sqrt(sum(v*v for v in vec1.values()))
    mag2 = math.sqrt(sum(v*v for v in vec2.values()))

    if mag1 == 0 or mag2 == 0:
        return 0

    return dot / (mag1 * mag2)