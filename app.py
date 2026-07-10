"""
AI Learning Buddy — a Gemini-powered tutor for learners from Kindergarten to
Postgraduate level, across every stream and subject.

Run with:
    streamlit run app.py

Requires a GEMINI_API_KEY set in .streamlit/secrets.toml (see secrets.toml.example).
"""

import streamlit as st
from google import genai
import requests

from curriculum import (
    LEVELS, SCHOOL_LEVELS, KG_SUBJECTS, SCHOOL_SUBJECTS,
    INTER_STREAMS, INTER_SUBJECTS,
    UG_DEGREES, UG_BTECH_BRANCHES, UG_BTECH_SUBJECTS,
    UG_BSC_SPECIALIZATIONS, UG_BSC_SUBJECTS, UG_BCOM_SUBJECTS, UG_BBA_SUBJECTS,
    UG_BA_SPECIALIZATIONS, UG_BA_SUBJECTS,
    PG_DEGREES, PG_MTECH_SPECIALIZATIONS, PG_MTECH_SUBJECTS,
    PG_MBA_SPECIALIZATIONS, PG_MBA_SUBJECTS, PG_MCA_SUBJECTS,
    PG_MSC_SPECIALIZATIONS, PG_MSC_SUBJECTS,
    PG_MA_SPECIALIZATIONS, PG_MA_SUBJECTS, PG_MCOM_SUBJECTS,
    ACTIVITIES_BASE, ACTIVITIES_EXAM, ACTIVITIES_UG_PG_ONLY,
    CODING_ACTIVITY, PROGRAMMING_KEYWORDS,
)

MODEL_NAME = "gemini-3.1-flash-lite"  # current stable, fast, cost-efficient model (2.5-flash-lite retired for new API keys)

st.set_page_config(page_title="AI Learning Buddy", page_icon="🌱", layout="centered")


# =========================================================
# SESSION STATE INIT
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []   # list of dicts: context, subject, topic, activity, response
if "last_response" not in st.session_state:
    st.session_state.last_response = None
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""


# =========================================================
# HELPERS
# =========================================================
@st.cache_data(show_spinner=False, ttl=3600)
def fetch_topic_image(topic: str):
    """Fetch a Wikipedia thumbnail + short summary for the topic. Fails silently."""
    try:
        r = requests.get(
            "https://en.wikipedia.org/api/rest_v1/page/summary/" + requests.utils.quote(topic),
            timeout=6,
        )
        if r.status_code == 200:
            data = r.json()
            thumb = data.get("thumbnail", {}).get("source")
            extract = data.get("extract")
            return thumb, extract
    except Exception:
        pass
    return None, None


def is_programming_subject(subject: str) -> bool:
    if not subject:
        return False
    s = subject.lower()
    return any(kw in s for kw in PROGRAMMING_KEYWORDS)


def build_level_instruction(level: str) -> str:
    """Return tone/depth guidance for the model based on education level."""
    if level == "Kindergarten":
        return (
            "The learner is in Kindergarten. Use very simple words, short sentences, "
            "playful tone, relevant emojis, and fun, concrete examples (toys, animals, family). "
            "Never use technical or academic language."
        )
    if level in SCHOOL_LEVELS:
        grade_num = int(level.split()[-1])
        if grade_num <= 5:
            return (
                f"The learner is in {level} (primary school). Use simple words, short sentences, "
                "everyday examples, and a friendly, encouraging tone. Introduce only one new idea at a time."
            )
        return (
            f"The learner is in {level} (middle/high school). Use clear language appropriate for this "
            "grade, define any technical terms the first time they appear, and keep explanations exam-relevant."
        )
    if level == "Intermediate (11th & 12th)":
        return (
            "The learner is in Intermediate (11th/12th grade), preparing for board and entrance exams. "
            "Use standard subject terminology, defined on first use, and keep answers exam-oriented and precise."
        )
    if level == "Undergraduate (UG)":
        return (
            "The learner is an undergraduate student. Use proper academic/technical terminology, assume "
            "foundational knowledge of the subject, and explain the 'why' as well as the 'what'."
        )
    if level == "Postgraduate (PG)":
        return (
            "The learner is a postgraduate student. Use precise academic/technical language, assume strong "
            "foundational knowledge, and focus on depth, nuance, and current practice or research angles."
        )
    return "Explain clearly and appropriately for the learner's level."


import time


def call_gemini_stream(client: "genai.Client", system_instruction: str, prompt: str, placeholder, max_tokens: int = 700, max_retries: int = 3) -> str:
    """
    Call Gemini with streaming so text appears progressively in `placeholder`
    instead of waiting for the full response. Retries on transient 503s
    before any tokens have been received.
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            full_text = ""
            stream = client.models.generate_content_stream(
                model=MODEL_NAME,
                contents=prompt,
                config={
                    "system_instruction": system_instruction,
                    "max_output_tokens": max_tokens,
                    "thinking_config": {"thinking_budget": 0},  # skip extended reasoning — not needed for tutoring Q&A
                },
            )
            for chunk in stream:
                if chunk.text:
                    full_text += chunk.text
                    placeholder.markdown(full_text + "▌")
            placeholder.markdown(full_text)
            return full_text
        except Exception as e:
            last_error = e
            if "503" in str(e) or "UNAVAILABLE" in str(e) or "overloaded" in str(e).lower():
                if attempt < max_retries - 1:
                    time.sleep(1.5 * (attempt + 1))
                    continue
            raise last_error
    raise last_error


ACTIVITY_PROMPTS = {
    "Explain Topic": "Explain the topic '{topic}' from the subject '{subject}'. End by asking if the learner wants a real-life example.",
    "Real-Life Example": "Give ONE clear, relatable real-life example that illustrates '{topic}' (subject: '{subject}').",
    "Generate Notes": "Write concise, well-organized study notes on '{topic}' (subject: '{subject}'), using headings and bullet points.",
    "Generate Summary": "Write a short summary (under 150 words) of '{topic}' (subject: '{subject}').",
    "Generate 10-Mark Answer": "Write a detailed, exam-style 10-mark answer on '{topic}' (subject: '{subject}'), with clear structure (introduction, main points, conclusion).",
    "Generate 5-Mark Answer": "Write a concise, exam-style 5-mark answer on '{topic}' (subject: '{subject}').",
    "Generate MCQs": "Write 5 multiple-choice questions on '{topic}' (subject: '{subject}'), each with 4 options. Provide the answer key separately at the end.",
    "Generate Quiz": "Write a 5-question quiz (mix of MCQ and short-answer) on '{topic}' (subject: '{subject}'). List questions first, then an answer key at the end.",
    "Practice Questions": "Write 5 practice questions (no answers) on '{topic}' (subject: '{subject}') for the learner to attempt on their own.",
    "Assignment Questions": "Write 3 assignment-style questions on '{topic}' (subject: '{subject}') suitable for homework submission.",
    "Previous Exam Tips": "Give practical exam-preparation tips for the topic '{topic}' (subject: '{subject}'), including commonly asked angles and common mistakes to avoid.",
    "Study Plan": "Create a short, realistic study plan (spread over a few days) to master '{topic}' (subject: '{subject}').",
    "Interview Questions (UG & PG)": "Write 5 interview-style questions on '{topic}' (subject: '{subject}') as might be asked in a technical or viva interview, with brief ideal-answer pointers.",
    CODING_ACTIVITY: "Give ONE coding problem related to '{topic}' (subject: '{subject}'), with a clear problem statement, one example input/output, and hints — but not the full solution unless asked.",
    "Ask Anything": "{topic}",  # the learner's own free-form question, passed straight through to Gemini
}


ACTIVITY_MAX_TOKENS = {
    "Explain Topic": 500,
    "Real-Life Example": 350,
    "Generate Notes": 1500,
    "Generate Summary": 300,
    "Generate 10-Mark Answer": 1500,
    "Generate 5-Mark Answer": 600,
    "Generate MCQs": 1500,
    "Generate Quiz": 1500,
    "Practice Questions": 500,
    "Assignment Questions": 1500,
    "Previous Exam Tips": 1000,
    "Study Plan": 700,
    "Interview Questions (UG & PG)": 800,
    CODING_ACTIVITY: 5000,
    "Ask Anything": 600,
}


# =========================================================
# API KEY (developer-set secret, never shown to the user)
# =========================================================
api_key = st.secrets.get("GEMINI_API_KEY") if hasattr(st, "secrets") else None

if not api_key:
    st.error(
        "This app isn't configured yet. The app owner needs to add a GEMINI_API_KEY "
        "in Streamlit secrets (`.streamlit/secrets.toml` locally, or App Settings → Secrets when deployed)."
    )
    st.stop()

client = genai.Client(api_key=api_key)


# =========================================================
# HEADER
# =========================================================
st.title("📘 AI Learning Buddy")
st.markdown("**Welcome to AI Learning Buddy!**")
st.caption(
    "This application uses Google Gemini AI to help students learn concepts in a simple "
    "and interactive way — for every learner, Kindergarten to Postgraduate."
)

feat_col1, feat_col2, feat_col3, feat_col4, feat_col5 = st.columns(5)
feat_col1.markdown("🤖 **Ask AI**")
feat_col2.markdown("📖 **Explain Topic**")
feat_col3.markdown("🌍 **Real-Life Examples**")
feat_col4.markdown("📝 **Quiz Generator**")
feat_col5.markdown("💡 **Study Tips**")

st.markdown("---")

with st.expander("✨ Features"):
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("#### 🤖 AI Tutor")
        st.write("Ask any question and receive simple, easy-to-understand explanations.")
    with c2:
        st.markdown("#### 📝 Quiz Generator")
        st.write("Generate multiple-choice quizzes instantly for practice.")
    with c3:
        st.markdown("#### 💡 Smart Study Tips")
        st.write("Receive study plans, resources, interview tips, and revision strategies.")

with st.expander("📖 How to Use this Application"):
    st.markdown(
        "1️⃣ Select your **Education Level** (Step 1).\n\n"
        "2️⃣ Choose your **Subject** (Step 2) — options adapt automatically to your level.\n\n"
        "3️⃣ Enter a **Topic**, or use the Quick Learning Guide below to pick one instantly (Step 3).\n\n"
        "4️⃣ Choose an activity — Explain Topic, Real-Life Example, Quiz, Study Plan, Ask Anything, "
        "and more — and click **Generate** (Step 4).\n\n"
        "The AI will generate beginner-friendly responses using Google Gemini, tailored to your level."
    )

with st.expander("📚 Quick Learning Guide"):
    st.markdown("**🤖 Machine Learning**")
    ml_topics = ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Classification", "Regression"]
    ml_cols = st.columns(len(ml_topics))
    for col, t in zip(ml_cols, ml_topics):
        if col.button(t, key=f"ml_{t}"):
            st.session_state.topic_input = t
            st.rerun()

    st.markdown("**💻 Computer Science Subjects**")
    cs_topics = ["Operating Systems", "Database Management System", "Computer Networks", "Python Programming", "Data Structures", "Artificial Intelligence"]
    cs_cols = st.columns(3)
    for i, t in enumerate(cs_topics):
        if cs_cols[i % 3].button(t, key=f"cs_{t}"):
            st.session_state.topic_input = t
            st.rerun()

st.markdown("---")

with st.sidebar:
    st.title("About")
    st.caption("Persona: **Gemini** 🌱 — a patient AI tutor for every education level.")

    st.markdown("#### ✨ Features")
    st.markdown(
        "- 🤖 Ask AI\n"
        "- 📖 Explain Topic\n"
        "- 🌍 Real-Life Examples\n"
        "- 📝 Quiz Generator\n"
        "- 💡 Study Tips"
    )

    st.markdown("#### 🛠 Technologies Used")
    st.markdown(
        "- Python\n"
        "- Streamlit\n"
        "- Google Gemini API"
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []
        st.session_state.last_response = None
        st.session_state.topic_input = ""
        st.rerun()


# =========================================================
# STEP 1 — EDUCATION LEVEL
# =========================================================
st.subheader("Step 1 · Select your Education Level")
level = st.selectbox("Select your Education Level", LEVELS, label_visibility="collapsed")

context_parts = [level]
subject = None
subject_options = []

# ---------------------------------------------------------
# STEP 2 — SUBJECT SELECTION (cascading by level)
# ---------------------------------------------------------
st.subheader("Step 2 · Select your Subject")

if level == "Kindergarten":
    subject_options = KG_SUBJECTS

elif level in SCHOOL_LEVELS:
    subject_options = SCHOOL_SUBJECTS

elif level == "Intermediate (11th & 12th)":
    stream = st.selectbox("Select your Stream", INTER_STREAMS)
    context_parts.append(stream)
    subject_options = INTER_SUBJECTS[stream]

elif level == "Undergraduate (UG)":
    degree = st.selectbox("Select your Degree", UG_DEGREES)
    context_parts.append(degree)

    if degree in ("B.Tech", "B.E."):
        branch = st.selectbox("Select your Branch", UG_BTECH_BRANCHES)
        context_parts.append(branch)
        subject_options = UG_BTECH_SUBJECTS.get(branch, [])

    elif degree == "B.Sc.":
        spec = st.selectbox("Select your Specialization", UG_BSC_SPECIALIZATIONS)
        context_parts.append(spec)
        subject_options = UG_BSC_SUBJECTS.get(spec, [])

    elif degree == "B.Com.":
        subject_options = UG_BCOM_SUBJECTS

    elif degree == "BBA":
        subject_options = UG_BBA_SUBJECTS

    elif degree == "BA":
        spec = st.selectbox("Select your Specialization", UG_BA_SPECIALIZATIONS)
        context_parts.append(spec)
        subject_options = UG_BA_SUBJECTS.get(spec, [])

elif level == "Postgraduate (PG)":
    degree = st.selectbox("Select your Degree", PG_DEGREES)
    context_parts.append(degree)

    if degree == "M.Tech":
        spec = st.selectbox("Select your Specialization", PG_MTECH_SPECIALIZATIONS)
        context_parts.append(spec)
        subject_options = PG_MTECH_SUBJECTS.get(spec, [])

    elif degree == "MBA":
        spec = st.selectbox("Select your Specialization", PG_MBA_SPECIALIZATIONS)
        context_parts.append(spec)
        subject_options = PG_MBA_SUBJECTS

    elif degree == "MCA":
        subject_options = PG_MCA_SUBJECTS

    elif degree == "M.Sc.":
        spec = st.selectbox("Select your Specialization", PG_MSC_SPECIALIZATIONS)
        context_parts.append(spec)
        subject_options = PG_MSC_SUBJECTS.get(spec, [])

    elif degree == "MA":
        spec = st.selectbox("Select your Specialization", PG_MA_SPECIALIZATIONS)
        context_parts.append(spec)
        subject_options = PG_MA_SUBJECTS.get(spec, [])

    elif degree == "M.Com.":
        subject_options = PG_MCOM_SUBJECTS

if subject_options:
    subject = st.selectbox("Select your Subject", subject_options)
    context_parts.append(subject)

level_context = " > ".join(context_parts)


# =========================================================
# STEP 3 — TOPIC
# =========================================================
st.subheader("Step 3 · What topic would you like to learn?")
topic = st.text_input(
    "Topic",
    placeholder="e.g. Binary Search, Photosynthesis, Electric Field, Profit and Loss — or type any question for 'Ask Anything'",
    label_visibility="collapsed",
    key="topic_input",
)

if topic and subject:
    thumb, extract = fetch_topic_image(topic)
    if thumb or extract:
        col1, col2 = st.columns([1, 2]) if thumb else (None, None)
        if thumb:
            with col1:
                st.image(thumb, caption=topic.title(), use_container_width=True)
            with col2:
                if extract:
                    st.markdown(f"*{extract}*")
        elif extract:
            st.markdown(f"*{extract}*")
    st.caption(f"📚 Context: {level_context} > {topic}")
    st.markdown("---")

    # =====================================================
    # STEP 4 — ACTIVITY SELECTION
    # =====================================================
    st.subheader("Step 4 · Choose an Activity")

    activities = list(ACTIVITIES_BASE)
    if level not in ("Kindergarten",) and level not in {f"Class {i}" for i in range(1, 6)}:
        activities += ACTIVITIES_EXAM
    if level in ("Undergraduate (UG)", "Postgraduate (PG)"):
        activities += ACTIVITIES_UG_PG_ONLY
    if is_programming_subject(subject):
        activities.append(CODING_ACTIVITY)

    activity = st.selectbox("Choose an Activity", activities, label_visibility="collapsed")

    if st.button("✨ Generate", type="primary"):
        system_instruction = (
            "Gemini, an encouraging AI learning buddy. "
            + build_level_instruction(level)
            + " Always stay on topic and keep your tone warm and supportive."
        )
        prompt = ACTIVITY_PROMPTS[activity].format(topic=topic, subject=subject)

        st.markdown("### 📖 Response")
        response_placeholder = st.empty()
        try:
            result = call_gemini_stream(
                client, system_instruction, prompt, response_placeholder,
                max_tokens=ACTIVITY_MAX_TOKENS.get(activity, 700),
            )
            st.session_state.last_response = result
            st.session_state.history.append({
                "context": level_context,
                "subject": subject,
                "topic": topic,
                "activity": activity,
                "response": result,
            })
            st.rerun()  # re-render once via the canonical display block below (avoids showing the answer twice)
        except Exception as e:
            if "503" in str(e) or "UNAVAILABLE" in str(e) or "overloaded" in str(e).lower():
                st.error("Gemini's servers are busy right now. This usually clears up in a few seconds — please click Generate again.")
            else:
                st.error(f"Something went wrong: {e}")

    # =====================================================
    # STEP 5 — DISPLAY RESPONSE
    # =====================================================
    if st.session_state.last_response:
        st.markdown("### 📖 Response")
        st.markdown(st.session_state.last_response)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "⬇️ Download Notes",
                data=st.session_state.last_response,
                file_name=f"{topic.replace(' ', '_')}_notes.txt",
                mime="text/plain",
            )
        with col2:
            with st.expander("📋 Copy Response"):
                st.code(st.session_state.last_response, language=None)
                st.caption("Click the copy icon in the top-right corner of the box above.")

    # =====================================================
    # SESSION HISTORY
    # =====================================================
    if len(st.session_state.history) > 1:
        with st.expander(f"🕘 Previous responses this session ({len(st.session_state.history) - 1})"):
            for item in reversed(st.session_state.history[:-1]):
                st.markdown(f"**{item['activity']}** — *{item['topic']}* ({item['context']})")
                st.markdown(item["response"])
                st.markdown("---")

else:
    st.info("👆 Select a subject and enter a topic above to get started.")


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🎓 <b>AI Learning Buddy</b><br>"
    "Developed using Python, Streamlit, and Google Gemini API.<br>"
    "This application provides an interactive AI-powered learning experience by helping students "
    "understand concepts, generate quizzes, view real-life examples, and receive study tips."
    "</div>",
    unsafe_allow_html=True,
)
