# src/prompts.py

def explain_topic(topic: str) -> str:
    return f"""
    You are a friendly, patient tutor helping a student understand '{topic}'.
    Explain it in simple, conversational English — like you're talking to a friend.
    Keep it under 150 words.
    Include one real-life example.
    Do NOT use markdown, headings, or diagrams — just plain text.
    """

def summarize_notes(notes: str) -> str:
    return f"""
    Summarize the following notes into 3 to 5 short bullet points.
    Use only bullet points starting with '- ' .
    Do not add any introduction, conclusion, or extra text.
    Focus on key facts, definitions, and concepts.

    Notes:  {notes}
    """

def generate_quiz(content: str, num_questions: int = 3) -> str:
    return f"""
    Generate exactly {num_questions} multiple-choice questions (MCQs) based ONLY on the content below.
    Follow these rules STRICTLY:

    - Number of questions: EXACTLY {num_questions}
    - Format for each question:
        [Number]. [Question text]
        A) [Option A]
        B) [Option B]
        C) [Option C]
        D) [Option D]

    - After all questions, add a section:
        Answers:
        1. [Letter]
        2. [Letter]
        ...
        {num_questions}. [Letter]

    - Do NOT add explanations, introductions, or extra text.
    - Each option must be on a new line.
    - Use only facts from the provided content.

    Content: {content}
    """