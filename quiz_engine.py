"""
quiz_engine.py
Interactive quiz system: asks Gemini for structured quiz JSON, then renders
each question as a real Streamlit widget, holds back the correct answer
until the learner clicks "Check Answer", and shows color-coded feedback,
explanations, live scoring, and a final performance summary.
"""

import json
import re
import time

import streamlit as st

QUIZ_QUESTION_COUNT = 5

QUIZ_CSS = """
<style>
.quiz-card {
    border: 1px solid #e0e0e0;
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 16px;
    background: #fafafa;
    transition: box-shadow 0.2s ease, transform 0.15s ease;
}
.quiz-card:hover {
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    transform: translateY(-1px);
}
.feedback-box {
    border-radius: 12px;
    padding: 14px 16px;
    margin-top: 10px;
    border: 2px solid;
}
.feedback-correct {
    border-color: #2e7d32;
    background: #e8f5e9;
    color: #1b5e20;
}
.feedback-wrong {
    border-color: #c62828;
    background: #fdecea;
    color: #7f1d1d;
}
.score-pill {
    display: inline-block;
    padding: 4px 14px;
    border-radius: 999px;
    background: #eef2ff;
    color: #3730a3;
    font-weight: 600;
    margin-right: 8px;
    font-size: 0.9rem;
}
</style>
"""

QUIZ_TYPE_INSTRUCTIONS = """
Generate exactly {n} interactive quiz questions on the topic '{topic}' (subject: '{subject}'), for a {level} learner.
{level_guidance}

Use a MIX of these question types (choose types that make sense for this subject — e.g. only include
"coding_output" if the subject is programming-related, only include "numerical" if the subject is
Math/Physics/Chemistry-like, only include "assertion_reason" for higher-grade/exam-style learners):

- "single_mcq": one correct answer, exactly 4 options.
- "multi_mcq": TWO OR MORE correct answers, 4 to 6 options.
- "true_false": exactly 2 options, "True" and "False".
- "fill_blank": no options; a short exact-answer text question (e.g. one word or short phrase).
- "assertion_reason": question text contains an Assertion (A) and a Reason (R) statement; exactly 4 options
  being the 4 standard assertion-reason choices (e.g. "Both A and R are true, and R is the correct explanation of A", etc.).
- "coding_output": question shows a short code snippet and asks what it outputs; exactly 4 options.
- "numerical": no options; a short numeric-answer question.

Respond with ONLY a valid JSON array (no markdown fences, no commentary, no extra text) in exactly this shape:

[
  {{
    "type": "single_mcq",
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "the exact matching option text",
    "explanation": "a short, beginner-friendly explanation of why this is correct"
  }},
  {{
    "type": "multi_mcq",
    "question": "...",
    "options": ["...", "...", "...", "..."],
    "correct_answer": ["exact option text 1", "exact option text 2"],
    "explanation": "..."
  }},
  {{
    "type": "fill_blank",
    "question": "...",
    "options": [],
    "correct_answer": "short exact answer",
    "explanation": "..."
  }}
]

Every question object MUST have "type", "question", "options" (empty list if not applicable), "correct_answer",
and "explanation". Return ONLY the JSON array.
"""


def build_quiz_prompt(topic: str, subject: str, level: str, level_guidance: str, n: int = QUIZ_QUESTION_COUNT) -> str:
    return QUIZ_TYPE_INSTRUCTIONS.format(n=n, topic=topic, subject=subject, level=level, level_guidance=level_guidance)


def parse_quiz_json(raw_text: str):
    """Strip markdown code fences if present, then parse the JSON array. Returns None on failure."""
    text = raw_text.strip()
    text = re.sub(r"^```(json)?", "", text.strip(), flags=re.IGNORECASE).strip()
    text = re.sub(r"```$", "", text.strip()).strip()
    try:
        data = json.loads(text)
        if isinstance(data, list) and len(data) > 0:
            return data
    except (json.JSONDecodeError, TypeError):
        pass
    return None


def init_quiz_state():
    if "quiz" not in st.session_state:
        st.session_state.quiz = None            # list of question dicts
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}       # idx -> {"checked": bool, "selected": ..., "correct": bool}
    if "quiz_started_at" not in st.session_state:
        st.session_state.quiz_started_at = None


def start_new_quiz(questions):
    st.session_state.quiz = questions
    st.session_state.quiz_answers = {}
    st.session_state.quiz_started_at = time.time()


def clear_quiz():
    st.session_state.quiz = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_started_at = None


def _grade(q_type: str, selected, correct) -> bool:
    if q_type == "multi_mcq":
        sel = set(x.strip().lower() for x in (selected or []))
        cor = set(x.strip().lower() for x in (correct or []))
        return sel == cor and len(sel) > 0
    if q_type in ("numerical",):
        try:
            return abs(float(str(selected).strip()) - float(str(correct).strip())) < 1e-6
        except (ValueError, TypeError):
            return str(selected).strip().lower() == str(correct).strip().lower()
    # single_mcq, true_false, fill_blank, assertion_reason, coding_output
    return str(selected).strip().lower() == str(correct).strip().lower()


def render_question(idx: int, q: dict):
    """Render one quiz question with the appropriate widget, a Check Answer button, and feedback."""
    q_type = q.get("type", "single_mcq")
    question_text = q.get("question", "")
    options = q.get("options") or []
    correct = q.get("correct_answer")
    explanation = q.get("explanation", "")

    state = st.session_state.quiz_answers.get(idx, {"checked": False, "selected": None, "correct": False})

    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
    st.markdown(f"**Q{idx + 1}. {question_text}**")

    widget_key = f"quiz_widget_{idx}"

    if state["checked"]:
        # Answer already locked in — just show what was selected, disabled-style, plus feedback.
        selected = state["selected"]
    else:
        if q_type == "multi_mcq":
            selected = st.multiselect("Select all that apply:", options, key=widget_key)
        elif q_type == "fill_blank" or q_type == "numerical":
            selected = st.text_input("Your answer:", key=widget_key)
        else:  # single_mcq, true_false, assertion_reason, coding_output
            selected = st.radio("Choose one:", options, key=widget_key, index=None)

        if st.button("✔ Check Answer", key=f"check_{idx}"):
            is_correct = _grade(q_type, selected, correct)
            st.session_state.quiz_answers[idx] = {"checked": True, "selected": selected, "correct": is_correct}
            st.rerun()

    if state["checked"]:
        selected_display = ", ".join(state["selected"]) if isinstance(state["selected"], list) else str(state["selected"])
        correct_display = ", ".join(correct) if isinstance(correct, list) else str(correct)

        if state["correct"]:
            st.markdown(
                f'<div class="feedback-box feedback-correct">'
                f'✅ <b>Correct!</b> Excellent work!<br><br>{explanation}'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="feedback-box feedback-wrong">'
                f'❌ <b>Incorrect</b><br><br>'
                f'<b>You selected:</b> {selected_display or "(no answer given)"}<br>'
                f'<b>Correct Answer:</b> {correct_display}<br><br>'
                f'<b>Explanation:</b> {explanation}'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)


def compute_performance(correct: int, total: int):
    """Return (stars, label, suggestion) for the final summary."""
    pct = (correct / total * 100) if total else 0
    if pct >= 90:
        return "⭐⭐⭐⭐⭐", "Excellent", "You've clearly mastered this topic — try a harder topic next!"
    if pct >= 75:
        return "⭐⭐⭐⭐", "Good", "Solid understanding — a quick review of the missed questions will make it perfect."
    if pct >= 50:
        return "⭐⭐⭐", "Average", "You're getting there — revisit the explanations above and try a fresh quiz."
    if pct >= 30:
        return "⭐⭐", "Needs Improvement", "This topic needs more practice — try 'Explain Topic' again before retaking the quiz."
    return "⭐", "Needs Improvement", "Don't worry — go through 'Explain Topic' and 'Generate Notes' first, then retry."


def render_quiz_ui():
    """Render the full quiz: all questions, live score bar, and final summary once complete."""
    st.markdown(QUIZ_CSS, unsafe_allow_html=True)
    questions = st.session_state.quiz
    total = len(questions)
    answered = st.session_state.quiz_answers
    checked_count = sum(1 for a in answered.values() if a["checked"])
    correct_count = sum(1 for a in answered.values() if a["checked"] and a["correct"])
    wrong_count = checked_count - correct_count
    pct = (correct_count / checked_count * 100) if checked_count else 0

    st.markdown(
        f'<span class="score-pill">📊 Question {min(checked_count + 1, total)}/{total}</span>'
        f'<span class="score-pill">✅ Correct: {correct_count}</span>'
        f'<span class="score-pill">❌ Wrong: {wrong_count}</span>'
        f'<span class="score-pill">📈 {pct:.0f}%</span>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    for idx, q in enumerate(questions):
        render_question(idx, q)

    if checked_count == total and total > 0:
        stars, label, suggestion = compute_performance(correct_count, total)
        elapsed = time.time() - st.session_state.quiz_started_at if st.session_state.quiz_started_at else None
        st.markdown("---")
        st.markdown("## 🏁 Quiz Complete!")
        st.markdown(f"### {stars}  {label}")
        c1, c2, c3 = st.columns(3)
        c1.metric("Final Score", f"{correct_count}/{total}")
        c2.metric("Percentage", f"{pct:.0f}%")
        if elapsed:
            c3.metric("Time Taken", f"{int(elapsed // 60)}m {int(elapsed % 60)}s")
        st.info(f"💡 **Suggestion:** {suggestion}")
        if st.button("🔄 Try a New Quiz"):
            clear_quiz()
            st.rerun()
