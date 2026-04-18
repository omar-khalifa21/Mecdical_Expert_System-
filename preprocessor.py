"""
nlp/preprocessor.py
Handles all NLP operations on raw user input:
tokenization, stopword removal, lemmatization, stemming,
and mapping free text to known symptom keywords.
"""

import re


def tokenize(text: str) -> list[str]:
    # TODO: lowercase the text, remove punctuation, split into word tokens
    pass


def remove_stopwords(tokens: list[str]) -> list[str]:
    # TODO: load a stopword list (e.g. NLTK's english stopwords)
    #       and filter them out from the token list
    pass


def lemmatize(tokens: list[str]) -> list[str]:
    # TODO: use NLTK WordNetLemmatizer (or spaCy) to reduce each token
    #       to its base form (e.g. "itching" → "itch", "rashes" → "rash")
    pass


def stem(tokens: list[str]) -> list[str]:
    # TODO: use NLTK PorterStemmer or SnowballStemmer as a fallback
    #       to further normalize tokens
    pass


def extract_symptoms(text: str, known_symptoms: list[str]) -> list[str]:
    # TODO: run the full pipeline: tokenize → remove_stopwords → lemmatize → stem
    #       then match resulting tokens (or n-grams) against the known_symptoms list
    #       return only symptoms that appear in the knowledge base
    pass


def normalize_symptom(symptom: str) -> str:
    # TODO: normalize a single symptom string (strip, lowercase, remove underscores/hyphens)
    #       used when loading the dataset so symptom strings are consistent
    pass
