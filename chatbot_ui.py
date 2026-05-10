"""
Tkinter GUI conversation flow for the medical diagnosis expert system.
"""

import tkinter as tk
from tkinter import scrolledtext


def greet_user() -> str:
    return (
        "Welcome to the Medical Diagnosis Expert System.\n"
        "Describe your symptoms in natural language, then press Send."
    )


def get_user_input(prompt: str = "You: ") -> str:
    return prompt


def display_system_message(message: str) -> str:
    return f"System: {message}"


def display_diagnosis_results(formatted_output: str) -> str:
    border = "=" * 60
    return f"{border}\n{formatted_output}\n{border}"


def ask_followup_question(symptom: str) -> str:
    return f"System: Do you also have '{symptom}'?"


def ask_for_more_symptoms() -> str:
    return "System: Tell me any additional symptoms you have."


def display_no_diagnosis_message() -> str:
    return "System: I could not match your symptoms confidently. Please consult a doctor for proper advice."


def run_conversation_loop(
    extract_symptoms_fn,
    run_engine_fn,
    compute_scores_fn,
    is_confident_fn,
    get_followup_fn,
    format_output_fn,
    known_symptoms: list[str],
    disease_symptom_map: dict,
    disease_precaution_map: dict,
    max_followup_rounds: int = 3,
) -> None:
    root = tk.Tk()
    root.title("Medical Diagnosis Expert System")
    root.geometry("900x700")
    root.minsize(760, 600)
    root.configure(bg="#f4efe6")

    state = {
        "confirmed_symptoms": [],
        "already_asked": [],
        "scored_diseases": [],
        "followup_rounds": 0,
        "pending_symptom": None,
        "awaiting_more_text": False,
        "conversation_finished": False,
    }

    title_label = tk.Label(
        root,
        text="Medical Diagnosis Expert System",
        font=("Georgia", 20, "bold"),
        bg="#f4efe6",
        fg="#1f3a5f",
        pady=12,
    )
    title_label.pack()

    subtitle_label = tk.Label(
        root,
        text="Symptom-based diagnosis using rule-based reasoning and NLP preprocessing",
        font=("Segoe UI", 10),
        bg="#f4efe6",
        fg="#5a6775",
    )
    subtitle_label.pack()

    transcript = scrolledtext.ScrolledText(
        root,
        wrap=tk.WORD,
        font=("Consolas", 11),
        bg="#fffdf8",
        fg="#1d2430",
        relief=tk.FLAT,
        padx=14,
        pady=14,
        height=24,
    )
    transcript.pack(fill=tk.BOTH, expand=True, padx=18, pady=(16, 10))
    transcript.configure(state=tk.DISABLED)

    input_frame = tk.Frame(root, bg="#f4efe6")
    input_frame.pack(fill=tk.X, padx=18, pady=(0, 8))

    symptom_entry = tk.Entry(
        input_frame,
        font=("Segoe UI", 11),
        bg="#ffffff",
        fg="#1d2430",
        relief=tk.FLAT,
    )
    symptom_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

    button_frame = tk.Frame(root, bg="#f4efe6")
    button_frame.pack(fill=tk.X, padx=18, pady=(0, 16))

    def append_message(message: str) -> None:
        transcript.configure(state=tk.NORMAL)
        transcript.insert(tk.END, message + "\n\n")
        transcript.configure(state=tk.DISABLED)
        transcript.see(tk.END)

    def set_followup_mode(active: bool) -> None:
        if active:
            send_button.configure(state=tk.DISABLED)
            yes_button.configure(state=tk.NORMAL)
            no_button.configure(state=tk.NORMAL)
            symptom_entry.configure(state=tk.DISABLED)
        else:
            send_button.configure(state=tk.NORMAL)
            yes_button.configure(state=tk.DISABLED)
            no_button.configure(state=tk.DISABLED)
            symptom_entry.configure(state=tk.NORMAL)
            symptom_entry.focus_set()

    def reset_session() -> None:
        state["confirmed_symptoms"] = []
        state["already_asked"] = []
        state["scored_diseases"] = []
        state["followup_rounds"] = 0
        state["pending_symptom"] = None
        state["awaiting_more_text"] = False
        state["conversation_finished"] = False
        symptom_entry.delete(0, tk.END)
        set_followup_mode(False)
        append_message(display_system_message("Session reset. Describe your symptoms to begin again."))

    def finish_with_results() -> None:
        if not state["scored_diseases"]:
            append_message(display_no_diagnosis_message())
        else:
            formatted = format_output_fn(state["scored_diseases"], disease_precaution_map)
            append_message(display_diagnosis_results(formatted))

        state["conversation_finished"] = True
        state["pending_symptom"] = None
        set_followup_mode(False)

    def advance_diagnosis() -> None:
        while state["followup_rounds"] <= max_followup_rounds:
            engine_results = run_engine_fn(state["confirmed_symptoms"])
            if not engine_results:
                state["scored_diseases"] = []
                finish_with_results()
                return

            state["scored_diseases"] = compute_scores_fn(
                state["confirmed_symptoms"],
                disease_symptom_map,
            )
            if not state["scored_diseases"]:
                finish_with_results()
                return

            if is_confident_fn(state["scored_diseases"]):
                finish_with_results()
                return

            if state["followup_rounds"] >= max_followup_rounds:
                finish_with_results()
                return

            followup_candidates = get_followup_fn(
                state["confirmed_symptoms"],
                state["scored_diseases"],
                disease_symptom_map,
                state["already_asked"],
            )
            if not followup_candidates:
                finish_with_results()
                return

            next_symptom = followup_candidates[0]
            state["pending_symptom"] = next_symptom
            state["already_asked"].append(next_symptom)
            state["followup_rounds"] += 1
            append_message(ask_followup_question(next_symptom))
            set_followup_mode(True)
            return

        finish_with_results()

    def process_text_submission() -> None:
        user_input = symptom_entry.get().strip()
        if not user_input:
            return

        symptom_entry.delete(0, tk.END)
        append_message(f"You: {user_input}")

        extracted = extract_symptoms_fn(user_input)
        if not extracted:
            if state["awaiting_more_text"]:
                append_message(display_no_diagnosis_message())
                state["awaiting_more_text"] = False
                state["conversation_finished"] = True
            else:
                state["awaiting_more_text"] = True
                append_message(display_system_message("I could not detect known symptoms from that description."))
                append_message(ask_for_more_symptoms())
            return

        state["awaiting_more_text"] = False
        state["conversation_finished"] = False

        for symptom in extracted:
            if symptom not in state["confirmed_symptoms"]:
                state["confirmed_symptoms"].append(symptom)

        append_message(
            display_system_message(
                "Detected symptoms: " + ", ".join(state["confirmed_symptoms"])
            )
        )
        advance_diagnosis()

    def handle_followup_response(has_symptom: bool) -> None:
        pending_symptom = state["pending_symptom"]
        if not pending_symptom:
            return

        append_message(f"You: {'yes' if has_symptom else 'no'}")
        if has_symptom and pending_symptom not in state["confirmed_symptoms"]:
            state["confirmed_symptoms"].append(pending_symptom)
            append_message(
                display_system_message(
                    "Updated symptoms: " + ", ".join(state["confirmed_symptoms"])
                )
            )

        state["pending_symptom"] = None
        set_followup_mode(False)
        advance_diagnosis()

    send_button = tk.Button(
        button_frame,
        text="Send",
        command=process_text_submission,
        font=("Segoe UI", 10, "bold"),
        bg="#1f6f5f",
        fg="white",
        activebackground="#185548",
        activeforeground="white",
        relief=tk.FLAT,
        padx=18,
        pady=8,
    )
    send_button.pack(side=tk.LEFT, padx=(0, 8))

    yes_button = tk.Button(
        button_frame,
        text="Yes",
        command=lambda: handle_followup_response(True),
        font=("Segoe UI", 10, "bold"),
        bg="#cc8b3b",
        fg="white",
        activebackground="#a86d27",
        activeforeground="white",
        relief=tk.FLAT,
        padx=18,
        pady=8,
        state=tk.DISABLED,
    )
    yes_button.pack(side=tk.LEFT, padx=(0, 8))

    no_button = tk.Button(
        button_frame,
        text="No",
        command=lambda: handle_followup_response(False),
        font=("Segoe UI", 10, "bold"),
        bg="#8c4b3f",
        fg="white",
        activebackground="#6d382f",
        activeforeground="white",
        relief=tk.FLAT,
        padx=18,
        pady=8,
        state=tk.DISABLED,
    )
    no_button.pack(side=tk.LEFT, padx=(0, 8))

    reset_button = tk.Button(
        button_frame,
        text="New Session",
        command=reset_session,
        font=("Segoe UI", 10, "bold"),
        bg="#325d88",
        fg="white",
        activebackground="#254565",
        activeforeground="white",
        relief=tk.FLAT,
        padx=18,
        pady=8,
    )
    reset_button.pack(side=tk.RIGHT)

    symptom_entry.bind("<Return>", lambda event: process_text_submission())

    append_message(display_system_message(greet_user()))
    set_followup_mode(False)
    root.mainloop()
