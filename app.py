"""
AI Learning Buddy — a Gemini-powered tutor focused entirely on Artificial
Intelligence and its related fields (Machine Learning, Deep Learning, NLP,
Computer Vision, Generative AI, Robotics, AI Ethics, and more).

Run with:
    streamlit run app.py

Requires a GEMINI_API_KEY set in .streamlit/secrets.toml (see secrets.toml.example).
"""

import time

import streamlit as st
from google import genai
import requests

import quiz_engine

MODEL_NAME = "gemini-3.1-flash-lite"  # current stable, fast, cost-efficient model

st.set_page_config(page_title="AI Learning Buddy", page_icon="🤖", layout="centered")


# =========================================================
# AI-FOCUSED TOPIC DATA (replaces the old education curriculum)
# =========================================================
AI_FIELDS = [
    "Artificial Intelligence (General)",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing (NLP)",
    "Computer Vision",
    "Generative AI",
    "Large Language Models (LLMs)",
    "Reinforcement Learning",
    "Robotics",
    "AI Ethics & Safety",
    "Data Science for AI",
    "MLOps & AI Deployment",
    "Prompt Engineering",
    "AI in Healthcare",
    "AI in Finance",
    "AI in Cybersecurity",
]

EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]

QUICK_TOPICS_ML = ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Classification", "Regression", "Overfitting"]
QUICK_TOPICS_DL = ["Neural Networks", "Transformers", "Large Language Models", "Prompt Engineering", "Generative Adversarial Networks", "Computer Vision Basics"]

ACTIVITIES_BASE = [
    "Explain Topic",
    "Real-Life Example",
    "Generate Notes",
    "Generate Summary",
    "Generate MCQs",
    "Generate Quiz",
    "🎯 Interactive Quiz",
    "Practice Questions",
    "Assignment Questions",
    "Study Plan",
    "Interview Questions",
    "Coding Problem",
    "Ask Anything",
]

ACTIVITY_PROMPTS = {
    "Explain Topic": "Explain the topic '{topic}' from the AI field '{field}'. End by asking if the learner wants a real-life example.",
    "Real-Life Example": "Give ONE clear, relatable real-life example that illustrates '{topic}' (AI field: '{field}').",
    "Generate Notes": "Write concise, well-organized study notes on '{topic}' (AI field: '{field}'), using headings and bullet points.",
    "Generate Summary": "Write a short summary (under 150 words) of '{topic}' (AI field: '{field}').",
    "Generate MCQs": "Write 5 multiple-choice questions on '{topic}' (AI field: '{field}'), each with 4 options. Provide the answer key separately at the end.",
    "Generate Quiz": "Write a 5-question quiz (mix of MCQ and short-answer) on '{topic}' (AI field: '{field}'). List questions first, then an answer key at the end.",
    "Practice Questions": "Write 5 practice questions (no answers) on '{topic}' (AI field: '{field}') for the learner to attempt on their own.",
    "Assignment Questions": "Write 3 assignment-style questions on '{topic}' (AI field: '{field}') suitable for homework submission.",
    "Study Plan": "Create a short, realistic study plan (spread over a few days) to master '{topic}' (AI field: '{field}').",
    "Interview Questions": "Write 5 interview-style questions on '{topic}' (AI field: '{field}') as might be asked in a technical AI/ML interview, with brief ideal-answer pointers.",
    "Coding Problem": "Give ONE coding problem related to '{topic}' (AI field: '{field}'), with a clear problem statement, one example input/output, and hints — but not the full solution unless asked.",
    "Ask Anything": "{topic}",  # the learner's own free-form question, passed straight through to Gemini
}

ACTIVITY_MAX_TOKENS = {
    "Explain Topic": 500,
    "Real-Life Example": 350,
    "Generate Notes": 1100,
    "Generate Summary": 300,
    "Generate MCQs": 700,
    "Generate Quiz": 700,
    "Practice Questions": 500,
    "Assignment Questions": 500,
    "Study Plan": 700,
    "Interview Questions": 800,
    "Coding Problem": 700,
    "Ask Anything": 600,
}


# =========================================================
# SESSION STATE INIT
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []
if "last_response" not in st.session_state:
    st.session_state.last_response = None
if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""
quiz_engine.init_quiz_state()


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


def build_experience_instruction(exp_level: str) -> str:
    """Return tone/depth guidance for the model based on the learner's self-reported AI experience."""
    if exp_level == "Beginner":
        return (
            "The learner is a complete beginner to AI. Use simple, everyday language, avoid heavy jargon, "
            "and define any technical term the moment you use it. Use relatable analogies."
        )
    if exp_level == "Intermediate":
        return (
            "The learner has some AI/ML background. You can use standard technical terminology, but briefly "
            "clarify more advanced or niche terms. Assume familiarity with basic concepts like models, training, and data."
        )
    return (  # Advanced
        "The learner is advanced in AI. Use precise technical/academic language, assume strong foundational "
        "knowledge, and focus on depth, nuance, trade-offs, and current practice or research angles."
    )


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
                    "thinking_config": {"thinking_budget": 0},
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
st.title("🤖 AI Learning Buddy")
st.markdown("**Welcome to AI Learning Buddy!**")
st.caption(
    "This application uses Google Gemini AI to help you learn Artificial Intelligence and its "
    "related fields — Machine Learning, Deep Learning, NLP, Computer Vision, Generative AI, and more."
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
        st.write("Ask any question about AI and its subfields, and get simple, easy-to-understand explanations.")
    with c2:
        st.markdown("#### 📝 Quiz Generator")
        st.write("Generate multiple-choice quizzes instantly for practice — including a fully interactive quiz mode.")
    with c3:
        st.markdown("#### 💡 Smart Study Tips")
        st.write("Receive study plans, interview prep, coding problems, and revision strategies.")

with st.expander("📖 How to Use this Application"):
    st.markdown(
        "1️⃣ Select an **AI Field** you want to learn about (e.g. Machine Learning, NLP, Computer Vision).\n\n"
        "2️⃣ Choose your **Experience Level** — Beginner, Intermediate, or Advanced.\n\n"
        "3️⃣ Enter a **Topic**, or use the Quick Learning Guide below to pick one instantly.\n\n"
        "4️⃣ Choose an activity — Explain Topic, Real-Life Example, Quiz, Interactive Quiz, Study Plan, "
        "Interview Questions, Coding Problem, Ask Anything, and more — and click **Generate**.\n\n"
        "The AI will generate responses tailored to your chosen experience level, using Google Gemini."
    )

with st.expander("📚 Quick Learning Guide"):
    st.markdown("**🧠 Machine Learning**")
    ml_cols = st.columns(len(QUICK_TOPICS_ML))
    for col, t in zip(ml_cols, QUICK_TOPICS_ML):
        if col.button(t, key=f"ml_{t}"):
            st.session_state.topic_input = t
            st.rerun()

    st.markdown("**🧬 Deep Learning & Advanced AI**")
    dl_cols = st.columns(3)
    for i, t in enumerate(QUICK_TOPICS_DL):
        if dl_cols[i % 3].button(t, key=f"dl_{t}"):
            st.session_state.topic_input = t
            st.rerun()

st.markdown("---")

with st.sidebar:
    st.title("About")
    st.caption("Persona: **Professor Sunny** 🤖 — a patient AI tutor focused entirely on AI and its subfields.")

    st.markdown("#### ✨ Features")
    st.markdown(
        "- 🤖 Ask AI\n"
        "- 📖 Explain Topic\n"
        "- 🌍 Real-Life Examples\n"
        "- 📝 Quiz Generator (+ Interactive Quiz)\n"
        "- 💡 Study Tips"
    )

    st.markdown("#### 🛠 Technologies Used")
    st.markdown(
        "- Python\n"
        "- Streamlit\n"
        "- Google Gemini API\n"
        "- Wikipedia API"
    )

    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []
        st.session_state.last_response = None
        st.session_state.topic_input = ""
        quiz_engine.clear_quiz()
        st.rerun()


# =========================================================
# STEP 1 — AI FIELD
# =========================================================
st.subheader("Step 1 · Select an AI Field")
field = st.selectbox("Select an AI Field", AI_FIELDS, label_visibility="collapsed")

# =========================================================
# STEP 2 — EXPERIENCE LEVEL
# =========================================================
st.subheader("Step 2 · Your Experience Level")
exp_level = st.radio("Your Experience Level", EXPERIENCE_LEVELS, horizontal=True, label_visibility="collapsed")

# =========================================================
# STEP 3 — TOPIC
# =========================================================
st.subheader("Step 3 · What topic would you like to learn?")
topic = st.text_input(
    "Topic",
    placeholder="e.g. Neural Networks, Transformers, Prompt Engineering — or type any question for 'Ask Anything'",
    label_visibility="collapsed",
    key="topic_input",
)

if topic:
    thumb, extract = fetch_topic_image(topic)
    if thumb or extract:
        if thumb:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(thumb, caption=topic.title(), use_container_width=True)
            with col2:
                if extract:
                    st.markdown(f"*{extract}*")
        elif extract:
            st.markdown(f"*{extract}*")
    st.caption(f"📚 Context: {field} > {exp_level} > {topic}")
    st.markdown("---")

    # =====================================================
    # STEP 4 — ACTIVITY SELECTION
    # =====================================================
    st.subheader("Step 4 · Choose an Activity")
    activity = st.selectbox("Choose an Activity", ACTIVITIES_BASE, label_visibility="collapsed")

    if st.button("✨ Generate", type="primary"):
        if activity == "🎯 Interactive Quiz":
            level_guidance = build_experience_instruction(exp_level)
            quiz_prompt = quiz_engine.build_quiz_prompt(topic, field, exp_level, level_guidance)
            with st.spinner("Professor Sunny is building your interactive quiz..."):
                try:
                    raw = client.models.generate_content(
                        model=MODEL_NAME,
                        contents=quiz_prompt,
                        config={
                            "system_instruction": "You are a precise quiz-writing assistant. Output ONLY valid JSON, nothing else.",
                            "max_output_tokens": 2200,
                            "thinking_config": {"thinking_budget": 0},
                        },
                    )
                    parsed = quiz_engine.parse_quiz_json(raw.text)
                    if parsed:
                        quiz_engine.start_new_quiz(parsed)
                        st.rerun()
                    else:
                        st.error("Couldn't build the quiz from the AI's response — please click Generate again.")
                except Exception as e:
                    if "503" in str(e) or "UNAVAILABLE" in str(e) or "overloaded" in str(e).lower():
                        st.error("Gemini's servers are busy right now. This usually clears up in a few seconds — please click Generate again.")
                    else:
                        st.error(f"Something went wrong: {e}")
        else:
            quiz_engine.clear_quiz()
            system_instruction = (
                "You are Professor Sunny, a patient and encouraging AI learning buddy specializing in AI and its subfields. "
                + build_experience_instruction(exp_level)
                + " Always stay on topic and keep your tone warm and supportive."
            )
            prompt = ACTIVITY_PROMPTS[activity].format(topic=topic, field=field)

            st.markdown("### 📖 Response")
            response_placeholder = st.empty()
            try:
                result = call_gemini_stream(
                    client, system_instruction, prompt, response_placeholder,
                    max_tokens=ACTIVITY_MAX_TOKENS.get(activity, 700),
                )
                st.session_state.last_response = result
                st.session_state.history.append({
                    "context": f"{field} > {exp_level}",
                    "topic": topic,
                    "activity": activity,
                    "response": result,
                })
                st.rerun()
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e) or "overloaded" in str(e).lower():
                    st.error("Gemini's servers are busy right now. This usually clears up in a few seconds — please click Generate again.")
                else:
                    st.error(f"Something went wrong: {e}")

    # =====================================================
    # INTERACTIVE QUIZ (persists across per-question reruns)
    # =====================================================
    if activity == "🎯 Interactive Quiz" and st.session_state.quiz:
        quiz_engine.render_quiz_ui()

    # =====================================================
    # STEP 5 — DISPLAY RESPONSE (skipped in Interactive Quiz mode)
    # =====================================================
    if activity != "🎯 Interactive Quiz" and st.session_state.last_response:
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
    # SESSION HISTORY (skipped in Interactive Quiz mode)
    # =====================================================
    if activity != "🎯 Interactive Quiz" and len(st.session_state.history) > 1:
        with st.expander(f"🕘 Previous responses this session ({len(st.session_state.history) - 1})"):
            for item in reversed(st.session_state.history[:-1]):
                st.markdown(f"**{item['activity']}** — *{item['topic']}* ({item['context']})")
                st.markdown(item["response"])
                st.markdown("---")

else:
    st.info("👆 Select an AI field, your experience level, and enter a topic above to get started.")


# =========================================================
# FOOTER
# =========================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🎓 <b>AI Learning Buddy</b><br>"
    "Developed using Python, Streamlit, and Google Gemini API.<br>"
    "This application provides an interactive AI-powered learning experience focused on Artificial "
    "Intelligence and its related fields — helping learners understand concepts, generate quizzes, "
    "view real-life examples, and receive study tips."
    "</div>",
    unsafe_allow_html=True,
)
