"""
Experta-based inference engine for symptom-driven medical diagnosis.
"""

import collections
import collections.abc

if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, "MutableMapping"):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, "Sequence"):
    collections.Sequence = collections.abc.Sequence

from experta import Fact, KnowledgeEngine, MATCH, Rule

from preprocessor import normalize_symptom


class SymptomFact(Fact):
    pass


class DiagnosisFact(Fact):
    pass


class MedicalDiagnosisEngine(KnowledgeEngine):
    def __init__(self, disease_symptom_map: dict[str, list[str]]):
        super().__init__()
        self.disease_symptom_map = disease_symptom_map
        self.normalized_disease_map: dict[str, set[str]] = {}
        self.user_symptoms: list[str] = []
        self.matched_by_disease: dict[str, set[str]] = {}
        self.results: list[dict] = []

    def load_rules_from_knowledge_base(self):
        self.normalized_disease_map = {
            disease: {normalize_symptom(symptom) for symptom in symptoms if normalize_symptom(symptom)}
            for disease, symptoms in self.disease_symptom_map.items()
        }

    def reset(self):
        super().reset()
        self.user_symptoms = []
        self.matched_by_disease = {}
        self.results = []

    def assert_symptoms(self, symptoms: list[str]):
        for symptom in symptoms:
            clean_symptom = normalize_symptom(symptom)
            if clean_symptom:
                self.declare(SymptomFact(name=clean_symptom))

    @Rule(SymptomFact(name=MATCH.symptom))
    def collect_symptoms(self, symptom):
        clean_symptom = normalize_symptom(symptom)
        if clean_symptom not in self.user_symptoms:
            self.user_symptoms.append(clean_symptom)

        for disease, disease_symptoms in self.normalized_disease_map.items():
            if clean_symptom not in disease_symptoms:
                continue

            matched = self.matched_by_disease.setdefault(disease, set())
            if clean_symptom in matched:
                continue

            matched.add(clean_symptom)
            self.declare(
                DiagnosisFact(
                    disease=disease,
                    symptom=clean_symptom,
                    matched=len(matched),
                    total=len(disease_symptoms),
                )
            )

    def get_diagnosis_results(self) -> list[dict]:
        self.results = []

        for disease, matched_symptoms in self.matched_by_disease.items():
            disease_symptoms = self.normalized_disease_map.get(disease, set())
            if not matched_symptoms or not disease_symptoms:
                continue

            self.results.append(
                {
                    "disease": disease,
                    "matched": len(matched_symptoms),
                    "total": len(disease_symptoms),
                    "matched_symptoms": sorted(matched_symptoms),
                }
            )

        self.results.sort(
            key=lambda item: (item["matched"] / item["total"], item["matched"]),
            reverse=True,
        )
        return self.results
