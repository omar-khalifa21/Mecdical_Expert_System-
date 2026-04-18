"""
knowledge_base/knowledge_base.py
Loads the CSV dataset and provides a clean interface to query:
  - all known symptoms
  - symptoms per disease
  - precautions per disease
"""

import csv


def load_dataset(csv_path: str) -> list[dict]:
    # TODO: read the CSV file (columns: Disease, Symptoms, Precautions)
    #       return a list of dicts, one per row
    pass


def build_disease_symptom_map(dataset: list[dict]) -> dict[str, list[str]]:
    # TODO: build and return a dict mapping each disease name
    #       to its list of normalized symptom strings
    #       e.g. {"Fungal Infection": ["itching", "skin rash", ...], ...}
    pass


def build_disease_precaution_map(dataset: list[dict]) -> dict[str, list[str]]:
    # TODO: build and return a dict mapping each disease name
    #       to its list of precaution strings
    pass


def get_all_symptoms(disease_symptom_map: dict[str, list[str]]) -> list[str]:
    # TODO: return a deduplicated flat list of every symptom across all diseases
    #       used by the NLP layer to know what to match against
    pass


def get_symptoms_for_disease(disease: str, disease_symptom_map: dict[str, list[str]]) -> list[str]:
    # TODO: return the symptom list for a specific disease, or [] if not found
    pass


def get_precautions_for_disease(disease: str, disease_precaution_map: dict[str, list[str]]) -> list[str]:
    # TODO: return the precautions list for a specific disease, or [] if not found
    pass
