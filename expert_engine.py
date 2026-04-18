"""
engine/expert_engine.py
Defines the Experta-based knowledge engine.
Facts represent observed symptoms; Rules fire when symptom
combinations match known disease patterns.

Lab 3 reference: Experta KnowledgeEngine with Fact + @Rule decorators.
"""

from experta import KnowledgeEngine, Fact, Rule, AND, OR, NOT, L, W, MATCH


class SymptomFact(Fact):
    """
    Represents a single confirmed symptom observed in the user's input.
    e.g. SymptomFact(name="itching")
    """
    # TODO: define the 'name' field (string) using experta's Field if needed
    pass


class DiagnosisFact(Fact):
    """
    Represents a candidate disease conclusion produced by a rule.
    e.g. DiagnosisFact(disease="Fungal Infection", matched=2, total=4)
    """
    # TODO: define fields: disease (str), matched (int), total (int)
    pass


class MedicalDiagnosisEngine(KnowledgeEngine):
    """
    Main Experta engine.
    Rules are generated dynamically from the disease-symptom knowledge base
    OR defined manually for high-priority diseases.
    """

    def __init__(self, disease_symptom_map: dict):
        # TODO: call super().__init__(), store the disease_symptom_map,
        #       initialize a list to collect diagnosis results
        pass

    def load_rules_from_knowledge_base(self):
        # TODO: dynamically generate and register @Rule methods for each disease
        #       each rule fires when SymptomFacts matching that disease's symptoms exist
        #       this replaces writing hundreds of rules by hand
        pass

    def get_diagnosis_results(self) -> list[dict]:
        # TODO: return the collected DiagnosisFacts as a list of dicts
        #       e.g. [{"disease": "Flu", "matched": 3, "total": 5}, ...]
        pass

    def assert_symptoms(self, symptoms: list[str]):
        # TODO: for each symptom in the list, call self.declare(SymptomFact(name=symptom))
        pass

    # --- Example of a manually written rule (for reference) ---
    # @Rule(AND(SymptomFact(name="itching"), SymptomFact(name="skin rash")))
    # def rule_fungal_infection(self):
    #     self.declare(DiagnosisFact(disease="Fungal Infection"))
