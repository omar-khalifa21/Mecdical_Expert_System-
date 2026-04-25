import re
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from rapidfuzz import process, fuzz
from sentence_transformers import SentenceTransformer, util
from nltk.stem import PorterStemmer

_stopwords  = set(stopwords.words("english"))
_lemmatizer = WordNetLemmatizer()
# _stemmer = PorterStemmer()
# model       = SentenceTransformer('all-MiniLM-L6-v2')


#maping because fuzz if threshold is high the symptoms don't find it's match and if low then more false postive
SYMPTOM_ALIASES = {
    "dizzy": "dizziness",
    "lightheaded": "dizziness",
    "spinning":"dizziness",
    "tired": "fatigue",
    "exhausted": "fatigue",
    "weak": "fatigue",
    "nauseous": "nausea",
    "queasy": "nausea",
    "vomit": "vomiting",
    "throwing up": "vomiting",
    "fever": "high_fever",
    "hot": "high_fever",
    "hurt": "pain",
    "hurts": "pain",
    "painful": "pain",
    "stomachache": "stomach_pain",
    "belly pain": "stomach_pain",
    "breathless": "breathlessness",
    "shortness of breath": "breathlessness",
    "blurry": "blurred_and_distorted_vision",
    "blurred": "blurred_and_distorted_vision",
    "shiver": "shivering",
    "shivering": "shivering",
    "cold": "chills",
    "jaundice": "yellowing_of_eyes",
    "yellow eyes": "yellowing_of_eyes",
}

def tokenize(text: str) -> list[str]:
    text = str(text).lower()
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    return word_tokenize(text)

def remove_stopwords(tokens: list[str]) -> list[str]:
    return [t for t in tokens if t not in _stopwords and len(t) > 2]

def lemmatize(tokens: list[str]) -> list[str]:
    return [_lemmatizer.lemmatize(t) for t in tokens]

# def stem(tokens: list[str]) -> list[str]:
#     return [_stemmer.stem(token) for token in tokens]

def normalize_symptom(symptom: str) -> str:
    return symptom.strip().lower().replace("_", " ").replace("-", " ")

# instead of a word it search for a phrase so it lower the fuzz errors
def apply_aliases(text: str) -> str:
    text = text.lower()
    for phrase, target in SYMPTOM_ALIASES.items():
        pattern = r"\b" + re.escape(phrase) + r"\b"
        text = re.sub(pattern, target.replace("_", " "), text)

    return text

df = pd.read_csv(r"C:\Users\ranee\Downloads\cog\Mecdical_Expert_System-\Medical Diagnosis Expert System.csv")

known_symptoms = sorted(set(
    s.strip()
    for row in df['symptoms'].dropna()
    for s in row.split(',')
))
#mapping the symptoms to be intend instead of _ then make it a list to compare to later
symptom_map        = {normalize_symptom(s): s for s in known_symptoms}
symptom_display    = list(symptom_map.keys())


# symptom_embeddings = model.encode(symptom_display, convert_to_tensor=True)  



def extract_symptoms(text: str) -> list[str]:

    text=apply_aliases(text)

    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    # tokens = stem(tokens)

    matched = set()

    for token in tokens:
        if token in SYMPTOM_ALIASES:
            matched.add(SYMPTOM_ALIASES[token])
            continue

        result = process.extractOne(
            token,
            symptom_display,
            scorer=fuzz.token_sort_ratio
        )
        if result and result[1] >= 70:
            matched.add(symptom_map[result[0]])

### if we use a model in finding the similarty between the symptoms instead of mapping by comparing a vector of values for each word
        # token_embedding = model.encode(token, convert_to_tensor=True)
        # scores          = util.cos_sim(token_embedding, symptom_embeddings)[0]
        # best_idx        = scores.argmax().item()
        # best_score      = scores[best_idx].item()

        # if best_score >= 0.6:
        #     matched.add(symptom_map[symptom_display[best_idx]])

    return sorted(matched)


while True:
        user_input = input("Enter symptoms: ")
        result     = extract_symptoms(user_input)
        print("Detected:", result)