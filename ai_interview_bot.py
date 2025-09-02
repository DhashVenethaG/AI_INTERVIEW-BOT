import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import pandas as pd
import os
from datetime import datetime

# Load config
with open("config.json", "r") as f:
    config = json.load(f)

role_name = config["role_name"]
questions = config["questions"]
deal_breakers = config["deal_breakers"]
scoring_weights = config["scoring_weights"]
required_intents = config["required_intents"]
validations = config["validations"]

responses = []
current_q_index = 0
candidate_name = ""


def start_interview():
    global candidate_name, current_q_index
    candidate_name = entry_name.get().strip()
    if not candidate_name:
        messagebox.showerror("Error", "Please enter your name to continue.")
        return

    entry_name.config(state="disabled")
    btn_start.config(state="disabled")

    chat_box.insert(tk.END, f"Hello {candidate_name}, welcome to the {role_name} interview!\n")
    chat_box.insert(tk.END, "I'll ask you a few screening questions. Please answer below.\n\n")

    ask_question()


def ask_question():
    global current_q_index
    if current_q_index < len(questions):
        question = questions[current_q_index]
        chat_box.insert(tk.END, f"Q{current_q_index+1}: {question}\n")
        chat_box.see(tk.END)
    else:
        finish_interview()


def validate_answer(question, answer):
    for rule in validations:
        if rule["question"].lower() in question.lower():
            if rule["type"] == "min_words":
                if len(answer.split()) < rule["value"]:
                    return False, f"Answer must have at least {rule['value']} words."
    return True, ""


def submit_answer():
    global current_q_index
    answer = entry_answer.get().strip()
    if not answer:
        return

    valid, msg = validate_answer(questions[current_q_index], answer)
    if not valid:
        messagebox.showwarning("Validation Failed", msg)
        return

    chat_box.insert(tk.END, f"{candidate_name}: {answer}\n\n")
    responses.append({"Question": questions[current_q_index], "Answer": answer})

    entry_answer.delete(0, tk.END)
    current_q_index += 1
    ask_question()


def evaluate_response(answer):
    score = 0
    if any(db in answer.lower() for db in deal_breakers):
        return 0

    # Communication
    if len(answer.split()) > 5:
        score += scoring_weights["communication"] * 10
    else:
        score += scoring_weights["communication"] * 5

    # Role understanding
    if any(intent in answer.lower() for intent in required_intents):
        score += scoring_weights["role_understanding"] * 10

    # Technical
    if "python" in answer.lower() or "project" in answer.lower() or "model" in answer.lower():
        score += scoring_weights["technical_fit"] * 10

    return round(score, 2)


def finish_interview():
    avg_score = round(sum(evaluate_response(r["Answer"]) for r in responses) / len(responses), 2)
    verdict = "Pass" if avg_score >= 6 else "Review Needed"

    chat_box.insert(tk.END, f"\nInterview Finished!\nAverage Score: {avg_score}\nVerdict: {verdict}\n")

    df = pd.DataFrame(responses)
    filename = f"{candidate_name}_responses.xlsx"
    df.to_excel(filename, index=False)

    # Save transcript JSON
    transcript = {
        "candidate_name": candidate_name,
        "role": role_name,
        "score": avg_score,
        "verdict": verdict,
        "responses": responses,
        "timestamp": datetime.now().isoformat()
    }
    json_filename = f"{candidate_name}_summary.json"
    with open(json_filename, "w") as f:
        json.dump(transcript, f, indent=4)

    messagebox.showinfo("Interview Complete", f"Responses saved to {filename} and {json_filename}")


# ===== Tkinter UI =====
root = tk.Tk()
root.title("AI Interview Bot")
root.geometry("600x500")

frame_top = tk.Frame(root)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Enter your name: ").pack(side=tk.LEFT)
entry_name = tk.Entry(frame_top, width=30)
entry_name.pack(side=tk.LEFT, padx=5)
btn_start = tk.Button(frame_top, text="Start Interview", command=start_interview)
btn_start.pack(side=tk.LEFT)

chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, state="normal")
chat_box.pack(padx=10, pady=10)

frame_bottom = tk.Frame(root)
frame_bottom.pack(pady=5)

entry_answer = tk.Entry(frame_bottom, width=50)
entry_answer.pack(side=tk.LEFT, padx=5)
btn_submit = tk.Button(frame_bottom, text="Submit Answer", command=submit_answer)
btn_submit.pack(side=tk.LEFT)

root.mainloop()
