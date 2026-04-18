"""
ui/chatbot_ui.py
CLI-based conversational interface.
Manages the conversation loop: greeting, symptom collection,
follow-up questioning, and displaying final results.
"""


def greet_user() -> None:
    # TODO: print a welcome message explaining what the system does
    #       and how to interact with it (type symptoms, type 'quit' to exit)
    pass


def get_user_input(prompt: str = "You: ") -> str:
    # TODO: display the prompt and read a line from stdin
    #       return the stripped input string
    pass


def display_system_message(message: str) -> None:
    # TODO: print the system's message with a "System: " prefix for clarity
    pass


def display_diagnosis_results(formatted_output: str) -> None:
    # TODO: print the final diagnosis results in a clearly formatted way
    #       (borders, spacing, emoji if desired — keep it readable in a terminal)
    pass


def ask_followup_question(symptom: str) -> bool:
    # TODO: ask the user whether they have a specific symptom
    #       e.g. "Do you also have 'fever'? (yes/no): "
    #       return True if yes, False if no
    pass


def ask_for_more_symptoms() -> str:
    # TODO: prompt the user to describe any additional symptoms they have
    #       return the raw input string for NLP processing
    pass


def display_no_diagnosis_message() -> None:
    # TODO: print a friendly message when no disease could be matched
    #       and suggest seeing a real doctor
    pass


def run_conversation_loop(
    extract_symptoms_fn,
    run_engine_fn,
    compute_scores_fn,
    is_confident_fn,
    get_followup_fn,
    format_output_fn,
    known_symptoms: list[str],
    disease_symptom_map: dict,
    disease_precaution_map: dict
) -> None:
    # TODO: orchestrate the full conversation:
    #   1. greet_user()
    #   2. get initial symptom input from user
    #   3. extract_symptoms from input
    #   4. run_engine to get candidate diseases
    #   5. compute_scores
    #   6. if not confident → ask followup questions, update confirmed symptoms, repeat
    #   7. if confident or max rounds reached → display_diagnosis_results
    #   8. loop: ask if user wants another diagnosis session or quit
    pass
