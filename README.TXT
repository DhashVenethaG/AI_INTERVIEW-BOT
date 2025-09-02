AI Interview Bot – Submission Package
-------------------------------------

1. Overview
This project implements a simple AI-powered Interview Bot for Level-1 assessment.
It simulates an HR-style screening round by asking structured questions, validating
responses, and scoring candidates based on predefined weights.

2. Files Included
- ai_interview_bot.py       → Main runnable bot code (Tkinter GUI)
- config.json               → Config file defining role, questions, validations,
                              deal-breakers, and scoring weights
- Sample_Outputs/           → Example transcripts and summaries
    ├── Alice_responses.xlsx
    ├── Alice_summary.json
    ├── Priya_responses.xlsx
    ├── Priya_summary.json

3. Dependencies
- Python 3.8+
- pandas
- openpyxl

To install dependencies:
    pip install pandas openpyxl

4. How to Run
    python ai_interview_bot.py

Steps:
- Enter candidate name
- Bot will explain the process and start asking questions
- Provide responses in the text box and click "Submit"
- At the end, responses and summary will be automatically saved as:
    <candidate_name>_responses.xlsx
    <candidate_name>_summary.json

5. Outputs
- Excel file → Stores candidate responses
- JSON file → Stores structured transcript, score, verdict, and timestamp

6. Originality & AI-Disclosure
- This project was built by the candidate with AI assistance (ChatGPT) for code
  scaffolding and structuring.
- All content has been reviewed and edited to ensure originality and alignment
  with assignment guidelines.
