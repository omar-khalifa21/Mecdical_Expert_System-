"""
Scoring and follow-up helpers for the medical diagnosis workflow.
"""

from collections import Counter


def compute_confidence_scores(
    user_symptoms: list[str],
    disease_symptom_map: dict[str, list[str]],
    final_weights: dict[str, dict[str, float]] | None = None,
) -> list[dict]:
    normalized_user_symptoms = set(user_symptoms)
    results = []

    for disease, symptoms in disease_symptom_map.items():
        if not symptoms:
            continue

        weights = final_weights.get(disease, {}) if final_weights else {}
        matched_weight = 0.0
        total_weight = 0.0
        matched_symptoms = []

        for symptom in symptoms:
            weight = weights.get(symptom, 1.0)
            total_weight += weight

            if symptom in normalized_user_symptoms:
                matched_weight += weight
                matched_symptoms.append(symptom)

        if total_weight == 0 or matched_weight == 0:
            continue

        results.append(
            {
                "disease": disease,
                "confidence": matched_weight / total_weight,
                "matched_symptoms": matched_symptoms,
                "matched": len(matched_symptoms),
                "total": len(symptoms),
            }
        )

    results.sort(key=lambda item: (item["confidence"], item["matched"]), reverse=True)
    return results


def normalize_confidence_scores(scored_diseases: list[dict]) -> list[dict]:
    normalized_results = []
    for disease_result in scored_diseases:
        normalized_copy = dict(disease_result)
        normalized_copy["confidence"] = round(normalized_copy["confidence"] * 100, 2)
        normalized_results.append(normalized_copy)
    return normalized_results


def is_diagnosis_confident(scored_diseases: list[dict], threshold: float = 0.7) -> bool:
    if not scored_diseases:
        return False
    return scored_diseases[0]["confidence"] >= threshold


def get_followup_symptoms(
    user_symptoms: list[str],
    top_diseases: list[dict],
    disease_symptom_map: dict[str, list[str]],
    already_asked: list[str],
    final_weights: dict[str, dict[str, float]] | None = None,
) -> list[str]:
    known_symptoms = set(user_symptoms)
    asked_symptoms = set(already_asked)
    symptom_scores: Counter = Counter()

    for entry in top_diseases[:3]:
        disease = entry["disease"]
        disease_probability = entry["confidence"]
        for symptom in disease_symptom_map.get(disease, []):
            if symptom in known_symptoms or symptom in asked_symptoms:
                continue

            symptom_weight = 1.0
            if final_weights:
                symptom_weight = final_weights.get(disease, {}).get(symptom, 1.0)

            symptom_scores[symptom] += disease_probability * symptom_weight

    return [symptom for symptom, _ in symptom_scores.most_common()]


def format_diagnosis_output(scored_diseases: list[dict], disease_precaution_map: dict[str, list[str]]) -> str:
    if not scored_diseases:
        return "Unable to determine diagnosis."

    output_lines = []
    top = scored_diseases[0]
    top_disease = top["disease"]
    top_confidence = round(top["confidence"] * 100, 2)

    if top["confidence"] >= 0.70:
        output_lines.append(f"Diagnosis: You most likely have {top_disease} ({top_confidence}%).")
    else:
        output_lines.append("Possible conditions:")
        for disease in scored_diseases[:3]:
            percentage = round(disease["confidence"] * 100, 2)
            output_lines.append(f"- {disease['disease']} ({percentage}%)")

    precautions = disease_precaution_map.get(top_disease, [])
    if precautions:
        output_lines.append("")
        output_lines.append("Precautions:")
        for precaution in precautions:
            output_lines.append(f"- {precaution}")

    return "\n".join(output_lines)


def select_top_disease(scored_diseases: list[dict]) -> str:
    if not scored_diseases:
        return ""
    return scored_diseases[0]["disease"]
