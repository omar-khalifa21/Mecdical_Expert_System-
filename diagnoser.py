"""
diagnosis/diagnoser.py
Sits between the engine and the UI.
Handles confidence scoring, follow-up question generation,
and deciding when a diagnosis is conclusive enough to present.
"""


def compute_confidence_scores(
    user_symptoms: list[str],
    disease_symptom_map: dict[str, list[str]]
) -> list[dict]:
    # TODO: for each disease, compute:
    #         matched  = number of user symptoms found in disease's symptom list
    #         total    = total symptoms for that disease
    #         score    = matched / total  (or a weighted formula)
    #       return a list of dicts sorted descending by score, excluding 0-score diseases
    #       e.g. [{"disease": "Flu", "confidence": 0.70}, ...]
    pass


def normalize_confidence_scores(scored_diseases: list[dict]) -> list[dict]:
    # TODO: rescale scores so they sum to 100%
    #       e.g. if Flu=0.7, Cold=0.2, Allergy=0.1 → 70%, 20%, 10%
    pass


def is_diagnosis_confident(scored_diseases: list[dict], threshold: float = 0.5) -> bool:
    # TODO: return True if the top disease has a confidence score above the threshold
    #       used to decide whether to stop asking questions or keep probing
    pass


def get_followup_symptoms(
    user_symptoms: list[str],
    top_diseases: list[dict],
    disease_symptom_map: dict[str, list[str]],
    already_asked: list[str]
) -> list[str]:
    # TODO: from the top candidate diseases, find symptoms the user hasn't confirmed yet
    #       and hasn't been asked about yet — return them as follow-up questions
    #       prioritize symptoms shared across multiple top candidates (most discriminating)
    pass


def format_diagnosis_output(
    scored_diseases: list[dict],
    disease_precaution_map: dict[str, list[str]]
) -> str:
    # TODO: format the final output string shown to the user:
    #       - if single confident diagnosis: show disease + precautions
    #       - if multiple candidates: show ranked list with % confidence
    #       - always show precautions for the top disease
    pass


def select_top_disease(scored_diseases: list[dict]) -> str:
    # TODO: return the disease name with the highest confidence score
    pass
