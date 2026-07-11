# 🤖 AI Learning Buddy

An interactive, AI-powered learning assistant built with **Streamlit** and **Google Gemini**, focused entirely on **Artificial Intelligence and its related fields**—including Machine Learning, Deep Learning, NLP, Computer Vision, Generative AI, Robotics, AI Ethics, and more.
=======
Type in any AI topic, choose your experience level, select a learning activity, and receive personalized AI-generated explanations, quizzes, notes, interview questions, coding challenges, and more.

---

## 🚀 Live Demo

🌐 **Try the App:**  
https://ai-learning-buddy-ymnwvjbldvym2akdvt8pbg.streamlit.app/

📂 **GitHub Repository:**  
https://github.com/sbharathi09/AI-Learning-Buddy

---

## ✨ Features

- 🤖 **Ask AI** — Free-form Q&A on any AI-related topic
- 📖 **Explain Topic** — Clear explanations tailored to your experience level
- 🌍 **Real-Life Examples** — Understand concepts through practical examples
- 📝 **Quiz Generator** — Generate MCQs and short-answer quizzes with answer keys
- 🎯 **Interactive Quiz**
  - Single & multiple-correct MCQs
  - True/False questions
  - Fill-in-the-blank
  - Assertion & Reason questions
  - Coding Output questions
  - Numerical questions
  - Instant feedback with explanations
  - Live score tracking and performance summary
- 📚 **Study Tools**
  - Notes
  - Summaries
  - Practice Questions
  - Assignment Questions
  - Study Plans
- 💼 **Interview Preparation**
  - AI/ML interview questions
  - Ideal answer guidance
- 💻 **Coding Challenges**
  - AI & ML programming problems with hints
- 🖼️ **Wikipedia Integration**
  - Topic summaries and images
- ⬇️ **Download & Copy**
  - Save responses as `.txt`
  - One-click copy

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API (`google-genai`)
- Wikipedia REST API
- Streamlit Secrets

---

## 📖 How to Use

1. Select an AI field.
2. Choose your experience level.
3. Enter a topic.
4. Select a learning activity.
5. Click **✨ Generate** to receive AI-powered content.

---

## 📂 Project Structure

```text
AI-Learning-Buddy/
├── app.py
├── quiz_engine.py
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── secrets.toml
└── README.md
```

---

## 🚀 Run Locally

```bash
git clone https://github.com/sbharathi09/AI-Learning-Buddy.git

cd AI-Learning-Buddy

pip install -r requirements.txt

streamlit run app.py
```

Create `.streamlit/secrets.toml`:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

---

## 🔒 Security

- API keys are stored securely using **Streamlit Secrets**.
- `secrets.toml` is excluded using `.gitignore`.
- No API keys are stored in the source code.

---

## 📜 License

This project is developed for educational purposes.

---

## 👨‍💻 Developer

**Swamidas Bharathi**

GitHub: https://github.com/sbharathi09