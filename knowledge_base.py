"""
knowledge_base/knowledge_base.py
Loads the CSV dataset and provides a clean interface to query:
  - all known symptoms
  - symptoms per disease
  - precautions per disease
"""

import csv
from preprocessor import normalize_symptom


def load_dataset(csv_path: str) -> list[dict]:
    # TODO: read the CSV file (columns: Disease, Symptoms, Precautions)
    #       return a list of dicts, one per row
     dataset: list[dict] = []

     with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            cleaned_row = {key.strip(): value.strip() for key, value in row.items()}
            dataset.append(cleaned_row)

     return dataset


def build_disease_symptom_map(dataset: list[dict]) -> dict[str, list[str]]:
   # Map each disease to its deduplicated, normalized list of symptoms.
   disease_symptom_map: dict[str, list[str]] = {}

   for row in dataset:
        disease = row["disease"].strip()
        raw_symptoms = row["symptoms"].split(",")
        normalized_symptoms = [normalize_symptom(s) for s in raw_symptoms if s.strip()]

        if disease not in disease_symptom_map:
            disease_symptom_map[disease] = []

        existing = set(disease_symptom_map[disease])
        for symptom in normalized_symptoms:
            if symptom and symptom not in existing:
                disease_symptom_map[disease].append(symptom)
                existing.add(symptom)

   return disease_symptom_map


def build_disease_precaution_map(dataset: list[dict]) -> dict[str, list[str]]:
    #Map each disease to its list of precautions (first occurrence only).
    disease_precaution_map: dict[str, list[str]] = {}

    for row in dataset:
        disease = row["disease"].strip()

        if disease in disease_precaution_map:
            continue

        raw_precautions = row["precautions"].split(",")
        precautions = [p.strip() for p in raw_precautions if p.strip()]
        disease_precaution_map[disease] = precautions

    return disease_precaution_map


def get_all_symptoms(disease_symptom_map: dict[str, list[str]]) -> list[str]:
    # Return a deduplicated sorted list of every symptom across all diseases.
    all_symptoms: set[str] = set()

    for symptoms in disease_symptom_map.values():
        all_symptoms.update(symptoms)

    return sorted(all_symptoms)


def get_symptoms_for_disease(disease: str, disease_symptom_map: dict[str, list[str]]) -> list[str]:
    # TODO: return the symptom list for a specific disease, or [] if not found
    return disease_symptom_map.get(disease, [])


def get_precautions_for_disease(disease: str, disease_precaution_map: dict[str, list[str]]) -> list[str]:
    # TODO: return the precautions list for a specific disease, or [] if not found
    return disease_precaution_map.get(disease, [])




if __name__ == "__main__":
   
   
    csv_path = r"D:\3rd year\2nd term\Cognetive\Mecdical_Expert_System-\Medical Diagnosis Expert System.csv"

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