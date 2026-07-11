# 🤖 AI Learning Buddy

An interactive, AI-powered learning assistant built with **Streamlit** and **Google Gemini**, focused entirely on **Artificial Intelligence and its related fields** — Machine Learning, Deep Learning, NLP, Computer Vision, Generative AI, Robotics, AI Ethics, and more.

Type in any AI topic, pick your experience level, choose an activity, and get instant, beginner-to-advanced-friendly responses — including a fully interactive quiz mode with live scoring and color-coded feedback.
---
## 🚀 Live Demo
🔗 **Live App:** https://ai-learning-buddy-ymnwvjbldvym2akdvt8pbg.streamlit.app/
---

## ✨ Features

- 🤖 **Ask AI** — free-form Q&A on any AI-related question
- 📖 **Explain Topic** — clear explanations tuned to your experience level
- 🌍 **Real-Life Examples** — relatable, concrete examples for abstract concepts
- 📝 **Quiz Generator** — instant MCQ / short-answer quizzes with an answer key
- 🎯 **Interactive Quiz** — a fully gamified quiz experience:
  - Single & multiple-correct MCQs, True/False, Fill-in-the-blank, Assertion-Reason, Coding Output, and Numerical questions
  - Answers are hidden until you click **Check Answer**
  - Green/red visual feedback with a beginner-friendly explanation every time
  - Live score tracking (question count, correct/wrong, percentage)
  - Final performance summary with a star rating and personalized suggestions
- 📚 **Study Tools** — Notes, Summaries, Practice Questions, Assignment Questions, Study Plans
- 💼 **Interview Prep** — technical AI/ML interview-style questions with ideal-answer pointers
- 💻 **Coding Problems** — AI/ML-related coding challenges with hints (no full solution given away)
- 🖼️ **Topic Images** — automatic Wikipedia thumbnail + summary for the topic you're learning
- ⬇️ **Download & Copy** — save any response as a `.txt` file or copy it with one click

---

## 🛠 Technologies Used

- **Python**
- **Streamlit** — the web interface
- **Google Gemini API** (`google-genai`) — response generation
- **Wikipedia REST API** — topic images and summaries
- **Streamlit Secrets** — secure API key management (no keys in code or in the repo)

---

## 📖 How to Use

1. **Select an AI Field** — e.g. Machine Learning, NLP, Computer Vision, Generative AI, LLMs, Robotics, AI Ethics & Safety, MLOps, Prompt Engineering, and more.
2. **Choose your Experience Level** — Beginner, Intermediate, or Advanced. Responses automatically adapt in depth and language.
3. **Enter a Topic** — type anything, or use the **📚 Quick Learning Guide** to instantly fill in a popular topic with one click.
4. **Choose an Activity** — Explain Topic, Real-Life Example, Notes, Summary, MCQs, Quiz, 🎯 Interactive Quiz, Practice Questions, Assignment Questions, Study Plan, Interview Questions, Coding Problem, or Ask Anything.
5. Click **✨ Generate** and watch the response stream in live.

---

## 📂 Project Structure

```
AI-Learning-Buddy/
├── app.py                      # Main Streamlit app (UI, Gemini calls, activity logic)
├── quiz_engine.py               # Interactive quiz engine (widgets, scoring, feedback)
├── requirements.txt             # Python dependencies
├── .gitignore                   # Excludes secrets.toml, venv, caches, etc.
├── .streamlit/
│   └── secrets.toml             # Your private Gemini API key (NOT committed to GitHub)
└── README.md                    # This file
```

---

## 🚀 Setup & Run Locally

### 1. Clone or download the project
```bash
git clone <your-repo-url>
cd AI-Learning-Buddy
```

### 2. Create a virtual environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key
Get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

Create `.streamlit/secrets.toml` in the project root:
```toml
GEMINI_API_KEY = "your-gemini-key-here"
```

> ⚠️ **Never commit `secrets.toml` to GitHub.** It's already listed in `.gitignore`.

### 5. Run the app
```bash
streamlit run app.py
```
The app opens automatically at `http://localhost:8501`.

---

## ☁️ Deploying (Streamlit Community Cloud)

1. Push `app.py`, `quiz_engine.py`, `requirements.txt`, `.gitignore`, and this `README.md` to a **public GitHub repo** — do **not** push `secrets.toml`.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub, and click **New app**.
3. Point it at your repo and `app.py`.
4. In your app's **Settings → Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-gemini-key-here"
   ```
5. Deploy — you'll get a public `https://yourapp.streamlit.app` link.

---

## 🔒 Security Notes

- The Gemini API key is never entered by the end user — it's configured once by the developer via Streamlit Secrets.
- `secrets.toml` is excluded from version control via `.gitignore`.
- If a key is ever accidentally exposed (e.g. pushed to a public repo), regenerate it immediately at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

---

## 🎓 About

Developed using Python, Streamlit, and the Google Gemini API. AI Learning Buddy provides an interactive AI-powered learning experience focused on Artificial Intelligence and its related fields — helping learners understand concepts, generate quizzes, view real-life examples, and receive study tips, all tailored to their experience level.
