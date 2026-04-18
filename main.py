"""
main.py
Entry point for the Medical Diagnosis Expert System.
Wires all modules together and starts the chatbot.
"""

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
    main()
