"""
main.py
Entry point for the Medical Diagnosis Expert System.
Wires all modules together and starts the chatbot.
"""

import os

from knowledge_base.knowledge_base import (
    load_dataset,
    build_disease_symptom_map,
    build_disease_precaution_map,
    get_all_symptoms,
)
from nlp.preprocessor import extract_symptoms
from engine.expert_engine import MedicalDiagnosisEngine
from diagnosis.diagnoser import (
    compute_confidence_scores,
    normalize_confidence_scores,
    is_diagnosis_confident,
    get_followup_symptoms,
    format_diagnosis_output,
)
from ui.chatbot_ui import run_conversation_loop


DATASET_PATH = "dataset.csv"
CONFIDENCE_THRESHOLD = 0.5
MAX_FOLLOWUP_ROUNDS = 3


def initialize_system():
    # TODO: load dataset, build both maps, get all symptoms
    #       instantiate MedicalDiagnosisEngine and call load_rules_from_knowledge_base()
    #       return (engine, disease_symptom_map, disease_precaution_map, known_symptoms)
    pass


def run_engine(engine: MedicalDiagnosisEngine, symptoms: list[str]) -> list[dict]:
    # TODO: reset the engine, assert the symptom facts, run the engine,
    #       retrieve and return diagnosis results
    pass


def main():
    # TODO: call initialize_system() to get all components
    #       then call run_conversation_loop() passing all needed functions and data
    pass


if __name__ == "__main__":
    
    csv_path = os.path.join(os.path.dirname(__file__), "Medical Diagnosis Expert System.csv")

    dataset = load_dataset(csv_path)
    dsm = build_disease_symptom_map(dataset)
    dpm = build_disease_precaution_map(dataset)
    all_syms = get_all_symptoms(dsm)

    print(f"Rows loaded      : {len(dataset)}")
    print(f"Unique diseases  : {len(dsm)}")
    print(f"Unique symptoms  : {len(all_syms)}")

    first_disease = next(iter(dsm))
    print(f"\nDisease     : {first_disease}")
    print(f"Symptoms    : {get_symptoms_for_disease(first_disease, dsm)}")
    print(f"Precautions : {get_precautions_for_disease(first_disease, dpm)}")
    main()
