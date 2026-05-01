"""
diagnosis/diagnoser.py
Sits between the engine and the UI.
Handles confidence scoring, follow-up question generation,
and deciding when a diagnosis is conclusive enough to present.
"""


from collections import Counter


def compute_confidence_scores(user_symptoms: list[str],disease_symptom_map: dict[str, list[str]],final_weights: dict[str, dict[str, float]]) -> list[dict]:
    results = []

    for disease, symptoms in disease_symptom_map.items():
        weights = final_weights.get(disease, {})

        matched_weight = 0.0
        total_weight = 0.0

        for s in symptoms:
            weight = weights.get(s, 0.01)  # 0.01 fallback
            total_weight += weight

            if s in user_symptoms:
                matched_weight += weight

        if total_weight == 0:
            continue

        score = matched_weight / total_weight

        if score > 0:
            results.append({
                "disease": disease,
                "confidence": score
            })

    # sort descending
    results.sort(key=lambda x: x["confidence"], reverse=True)
    return results


def normalize_confidence_scores(scored_diseases: list[dict]) -> list[dict]:
    total = sum(d["confidence"] for d in scored_diseases)

    if total == 0:
        return scored_diseases

    for d in scored_diseases:
        d["confidence"] = round((d["confidence"] / total) * 100, 2)

    return scored_diseases

def is_diagnosis_confident(scored_diseases: list[dict], threshold: float = 0.7) -> bool:
    if not scored_diseases:
        return False

    return scored_diseases[0]["confidence"] >= threshold


def get_followup_symptoms(user_symptoms: list[str],top_diseases: list[dict],disease_symptom_map: dict[str, list[str]],already_asked: list[str]) -> list[str]:
    symptom_counter = Counter()

    for entry in top_diseases[:3]:
        disease = entry["disease"]
        symptoms = disease_symptom_map.get(disease, [])

        for s in symptoms:
            if s not in user_symptoms and s not in already_asked:
                symptom_counter[s] += 1

    return [s for s, _ in symptom_counter.most_common()]


def format_diagnosis_output(scored_diseases: list[dict],disease_precaution_map: dict[str, list[str]]) -> str:
    
    if not scored_diseases:
        return "Unable to determine diagnosis."

    output_lines = []

    top = scored_diseases[0]
    top_disease = top["disease"]
    top_conf = top["confidence"]

    # sure of diagnosis
    if top_conf >= 70:
        output_lines.append(f"Diagnosis: You most likely have {top_disease} ({top_conf}%)")
    else:
        output_lines.append("Possible conditions:")
        for d in scored_diseases[:3]:
            output_lines.append(f"- {d['disease']} ({d['confidence']}%)")

    # Always show precautions for top disease
    precautions = disease_precaution_map.get(top_disease, [])

    if precautions:
        output_lines.append("\nPrecautions:")
        for p in precautions:
            output_lines.append(f"- {p}")

    return "\n".join(output_lines)



def select_top_disease(scored_diseases: list[dict]) -> str:
    if not scored_diseases:
        return ""

    return scored_diseases[0]["disease"]