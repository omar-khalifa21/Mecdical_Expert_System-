"""
Entry point for the Medical Diagnosis Expert System.
"""

import os

from chatbot_ui import run_conversation_loop
from diagnoser import (
    compute_confidence_scores,
    format_diagnosis_output,
    get_followup_symptoms,
    is_diagnosis_confident,
)
from expert_engine import MedicalDiagnosisEngine
from knowledge_base import (
    build_disease_precaution_map,
    build_disease_symptom_map,
    build_symptom_weight_map,
    get_all_symptoms,
    load_dataset,
)
from preprocessor import configure_known_symptoms, extract_symptoms


DATASET_PATH = "Medical Diagnosis Expert System (1).csv"
CONFIDENCE_THRESHOLD = 0.7
MAX_FOLLOWUP_ROUNDS = 3


def resolve_dataset_path(default_path: str) -> str:
    if os.path.exists(default_path):
        return default_path

    for root, _, files in os.walk("."):
        if "venv" in root.split(os.sep):
            continue
        for file_name in files:
            if file_name.lower().endswith(".csv"):
                return os.path.join(root, file_name)

    raise FileNotFoundError("No dataset CSV file was found in the project directory.")


def initialize_system():
    dataset_path = resolve_dataset_path(DATASET_PATH)
    dataset = load_dataset(dataset_path)
    disease_symptom_map = build_disease_symptom_map(dataset)
    disease_precaution_map = build_disease_precaution_map(dataset)
    known_symptoms = get_all_symptoms(disease_symptom_map)
    final_weights = build_symptom_weight_map(disease_symptom_map)

    configure_known_symptoms(known_symptoms)

    engine = MedicalDiagnosisEngine(disease_symptom_map)
    engine.load_rules_from_knowledge_base()

    return engine, disease_symptom_map, disease_precaution_map, known_symptoms, final_weights


def run_engine(engine: MedicalDiagnosisEngine, symptoms: list[str]) -> list[dict]:
    engine.reset()
    engine.assert_symptoms(symptoms)
    engine.run()
    return engine.get_diagnosis_results()


def main():
    engine, disease_symptom_map, disease_precaution_map, known_symptoms, final_weights = initialize_system()

    def extract_symptoms_fn(text: str) -> list[str]:
        return extract_symptoms(text, known_symptoms)

    def run_engine_fn(symptoms: list[str]) -> list[dict]:
        return run_engine(engine, symptoms)

    def compute_scores_fn(user_symptoms: list[str], symptom_map: dict[str, list[str]]) -> list[dict]:
        return compute_confidence_scores(user_symptoms, symptom_map, final_weights)

    def is_confident_fn(scored_diseases: list[dict]) -> bool:
        return is_diagnosis_confident(scored_diseases, threshold=CONFIDENCE_THRESHOLD)

    def get_followup_fn(
        user_symptoms: list[str],
        top_diseases: list[dict],
        symptom_map: dict[str, list[str]],
        already_asked: list[str],
    ) -> list[str]:
        return get_followup_symptoms(user_symptoms, top_diseases, symptom_map, already_asked, final_weights)

    run_conversation_loop(
        extract_symptoms_fn=extract_symptoms_fn,
        run_engine_fn=run_engine_fn,
        compute_scores_fn=compute_scores_fn,
        is_confident_fn=is_confident_fn,
        get_followup_fn=get_followup_fn,
        format_output_fn=format_diagnosis_output,
        known_symptoms=known_symptoms,
        disease_symptom_map=disease_symptom_map,
        disease_precaution_map=disease_precaution_map,
        max_followup_rounds=MAX_FOLLOWUP_ROUNDS,
    )


if __name__ == "__main__":
    main()
