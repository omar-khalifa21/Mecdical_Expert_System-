"""
Loads the CSV dataset and exposes disease, symptom, and precaution mappings.
"""

import csv
import math

from preprocessor import normalize_symptom


def _clean_cell(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_headers(fieldnames: list[str] | None) -> dict[str, str]:
    if not fieldnames:
        return {}
    return {header.strip().lower(): header for header in fieldnames if header}


def load_dataset(csv_path: str) -> list[dict]:
    dataset: list[dict] = []

    with open(csv_path, newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = _normalize_headers(reader.fieldnames)

        disease_key = headers.get("disease") or headers.get("prognosis")
        symptoms_key = headers.get("symptoms")
        precautions_key = headers.get("precautions")

        symptom_columns = [
            original
            for lowered, original in headers.items()
            if lowered.startswith("symptom")
        ]
        precaution_columns = [
            original
            for lowered, original in headers.items()
            if lowered.startswith("precaution")
        ]

        for row in reader:
            disease = _clean_cell(row.get(disease_key, ""))
            if not disease:
                continue

            if symptoms_key:
                raw_symptoms = _clean_cell(row.get(symptoms_key, ""))
                symptoms = [part.strip() for part in raw_symptoms.split(",") if part.strip()]
            else:
                symptoms = [
                    _clean_cell(row.get(column, ""))
                    for column in symptom_columns
                    if _clean_cell(row.get(column, ""))
                ]

            if precautions_key:
                raw_precautions = _clean_cell(row.get(precautions_key, ""))
                precautions = [part.strip() for part in raw_precautions.split(",") if part.strip()]
            else:
                precautions = [
                    _clean_cell(row.get(column, ""))
                    for column in precaution_columns
                    if _clean_cell(row.get(column, ""))
                ]

            dataset.append(
                {
                    "disease": disease,
                    "symptoms": symptoms,
                    "precautions": precautions,
                }
            )

    return dataset


def build_disease_symptom_map(dataset: list[dict]) -> dict[str, list[str]]:
    disease_symptom_map: dict[str, list[str]] = {}

    for row in dataset:
        disease = row["disease"].strip()
        normalized_symptoms = []
        for symptom in row.get("symptoms", []):
            cleaned = normalize_symptom(symptom)
            if cleaned and cleaned not in normalized_symptoms:
                normalized_symptoms.append(cleaned)

        if disease not in disease_symptom_map:
            disease_symptom_map[disease] = []

        for symptom in normalized_symptoms:
            if symptom not in disease_symptom_map[disease]:
                disease_symptom_map[disease].append(symptom)

    return disease_symptom_map


def build_disease_precaution_map(dataset: list[dict]) -> dict[str, list[str]]:
    disease_precaution_map: dict[str, list[str]] = {}

    for row in dataset:
        disease = row["disease"].strip()
        if disease in disease_precaution_map:
            continue

        precautions = []
        for precaution in row.get("precautions", []):
            cleaned = _clean_cell(precaution)
            if cleaned and cleaned not in precautions:
                precautions.append(cleaned)

        disease_precaution_map[disease] = precautions

    return disease_precaution_map


def build_symptom_weight_map(disease_symptom_map: dict[str, list[str]]) -> dict[str, dict[str, float]]:
    symptom_frequency: dict[str, int] = {}
    disease_count = len(disease_symptom_map)

    for symptoms in disease_symptom_map.values():
        for symptom in set(symptoms):
            symptom_frequency[symptom] = symptom_frequency.get(symptom, 0) + 1

    weight_map: dict[str, dict[str, float]] = {}
    for disease, symptoms in disease_symptom_map.items():
        weight_map[disease] = {}
        for symptom in symptoms:
            frequency = symptom_frequency.get(symptom, 1)
            weight_map[disease][symptom] = 1.0 + math.log((disease_count + 1) / (frequency + 1))

    return weight_map


def get_all_symptoms(disease_symptom_map: dict[str, list[str]]) -> list[str]:
    all_symptoms: set[str] = set()
    for symptoms in disease_symptom_map.values():
        all_symptoms.update(symptoms)
    return sorted(all_symptoms)


def get_symptoms_for_disease(disease: str, disease_symptom_map: dict[str, list[str]]) -> list[str]:
    return disease_symptom_map.get(disease, [])


def get_precautions_for_disease(disease: str, disease_precaution_map: dict[str, list[str]]) -> list[str]:
    return disease_precaution_map.get(disease, [])
