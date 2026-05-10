import re
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize


FALLBACK_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "for",
    "from", "had", "has", "have", "he", "her", "his", "i", "in", "is", "it",
    "me", "my", "of", "on", "or", "she", "that", "the", "their", "them",
    "they", "this", "to", "was", "we", "were", "with", "you", "your",
}

_lemmatizer = WordNetLemmatizer()
_stemmer = PorterStemmer()
_known_symptoms: list[str] = []
_symptom_index: dict[str, set[str]] = {}
_symptom_token_index: dict[str, set[str]] = defaultdict(set)


SYMPTOM_ALIASES = {
    "belly pain": "stomach pain",
    "blurry": "blurred distorted vision",
    "blurred": "blurred distorted vision",
    "breathless": "breathlessness",
    "cold": "chills",
    "dizzy": "dizziness",
    "exhausted": "fatigue",
    "fever": "high fever",
    "hot": "high fever",
    "hurt": "pain",
    "hurts": "pain",
    "jaundice": "yellowing of eyes",
    "lightheaded": "dizziness",
    "nauseous": "nausea",
    "painful": "pain",
    "queasy": "nausea",
    "shortness of breath": "breathlessness",
    "shiver": "shivering",
    "spinning": "dizziness",
    "stomachache": "stomach pain",
    "throwing up": "vomiting",
    "tired": "fatigue",
    "vomit": "vomiting",
    "weak": "fatigue",
    "yellow eyes": "yellowing of eyes",
}


def get_stopwords() -> set[str]:
    try:
        return set(stopwords.words("english"))
    except LookupError:
        return FALLBACK_STOPWORDS


def safe_word_tokenize(text: str) -> list[str]:
    try:
        return word_tokenize(text)
    except LookupError:
        return re.findall(r"[a-z0-9]+", text)


def safe_lemmatize(token: str) -> str:
    try:
        return _lemmatizer.lemmatize(token)
    except LookupError:
        return token


def normalize_symptom(symptom: str) -> str:
    return re.sub(r"\s+", " ", str(symptom).strip().lower().replace("_", " ").replace("-", " "))


def apply_aliases(text: str) -> str:
    normalized_text = text.lower()
    for phrase, target in SYMPTOM_ALIASES.items():
        pattern = r"\b" + re.escape(phrase) + r"\b"
        normalized_text = re.sub(pattern, target, normalized_text)
    return normalized_text


def tokenize(text: str) -> list[str]:
    text = normalize_symptom(text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return safe_word_tokenize(text)


def remove_stopwords(tokens: list[str]) -> list[str]:
    stopword_set = get_stopwords()
    return [token for token in tokens if token not in stopword_set and len(token) > 1]


def lemmatize(tokens: list[str]) -> list[str]:
    return [safe_lemmatize(token) for token in tokens]


def stem(tokens: list[str]) -> list[str]:
    return [_stemmer.stem(token) for token in tokens]


def preprocess_tokens(text: str) -> list[str]:
    tokens = tokenize(apply_aliases(text))
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    return stem(tokens)


def normalize_phrase(text: str) -> str:
    return " ".join(preprocess_tokens(text))


def configure_known_symptoms(known_symptoms: list[str]) -> None:
    global _known_symptoms, _symptom_index, _symptom_token_index

    _known_symptoms = sorted(set(known_symptoms))
    _symptom_index = {}
    _symptom_token_index = defaultdict(set)

    for symptom in _known_symptoms:
        normalized = normalize_phrase(symptom)
        if not normalized:
            continue

        _symptom_index[symptom] = set(normalized.split())
        for token in _symptom_index[symptom]:
            _symptom_token_index[token].add(symptom)


def candidate_phrases(tokens: list[str], max_size: int = 4) -> set[str]:
    phrases: set[str] = set()
    for size in range(1, min(max_size, len(tokens)) + 1):
        for start in range(0, len(tokens) - size + 1):
            phrases.add(" ".join(tokens[start:start + size]))
    return phrases


def extract_symptoms(text: str, known_symptoms: list[str] | None = None) -> list[str]:
    if known_symptoms is not None:
        configure_known_symptoms(known_symptoms)

    if not _known_symptoms:
        return []

    tokens = preprocess_tokens(text)
    if not tokens:
        return []

    token_set = set(tokens)
    phrase_set = candidate_phrases(tokens)
    matches: set[str] = set()
    candidate_symptoms: set[str] = set()

    for token in token_set:
        candidate_symptoms.update(_symptom_token_index.get(token, set()))

    for symptom in candidate_symptoms:
        symptom_tokens = _symptom_index.get(symptom, set())
        if not symptom_tokens:
            continue

        normalized_symptom = " ".join(sorted(symptom_tokens))
        overlap = len(symptom_tokens & token_set) / len(symptom_tokens)

        if overlap >= 1.0:
            matches.add(symptom)
            continue

        symptom_phrase = normalize_phrase(symptom)
        if symptom_phrase in phrase_set:
            matches.add(symptom)
            continue

        if len(symptom_tokens) == 1 and overlap >= 1.0:
            matches.add(symptom)
            continue

        if len(symptom_tokens) > 1 and overlap >= 0.75 and normalized_symptom:
            matches.add(symptom)

    return sorted(matches)
