# 🤖 AI Learning Buddy

An AI-powered learning assistant built using **Python**, **Streamlit**, and **Google Gemini API** that helps learners understand **Artificial Intelligence** and its related domains through personalized explanations, quizzes, notes, coding challenges, and interactive learning.

---

## 🌐 Live Demo

**🔗 Live App:**  
https://ai-learning-buddy-ymnwvjbldvym2akdvt8pbg.streamlit.app/

**📂 GitHub Repository:**  
https://github.com/sbharathi09/AI-Learning-Buddy

---

## 📌 Overview

AI Learning Buddy is an intelligent tutor that adapts its responses based on the learner's experience level and learning activity. Users can also personalize their AI tutor by providing a custom **AI Persona Name**, making the learning experience more interactive and engaging.

---

## ✨ Features

### 👤 Personalized AI Persona
- Custom AI Buddy name
- Personalized introductions
- Consistent persona throughout the session

### 🎓 Adaptive Learning
- Beginner
- Intermediate
- Advanced

### 🧠 AI Learning Domains
- Artificial Intelligence
- Machine Learning
- Deep Learning
- Generative AI
- Large Language Models (LLMs)
- Natural Language Processing (NLP)
- Computer Vision
- Robotics
- Reinforcement Learning
- AI Ethics & Responsible AI
- Prompt Engineering
- MLOps

### 📚 Learning Activities
- Explain Topic
- Real-Life Example
- Generate Notes
- Generate Summary
- Practice Questions
- Assignment Questions
- Study Plan
- Previous Exam Tips

### 📝 Assessment
- MCQ Generator
- Interactive Quiz
- True/False Questions
- Fill in the Blanks
- Assertion & Reason
- Coding Output Questions
- Numerical Questions
- Instant Feedback
- Live Score Tracking

### 💼 Career Preparation
- Interview Questions
- Coding Problems
- Concept Revision
- AI Learning Guidance

### 🌍 Wikipedia Integration
- Topic Summary
- Topic Thumbnail/Image

### 📥 Utilities
- Download Response
- Copy Response
- Session History
- Clear Chat

### 🔒 Secure API Management
- Gemini API using Streamlit Secrets
- No API keys stored in source code

---

## 🛠️ Technologies Used

- Python
- Streamlit
- Google Gemini API
- Wikipedia REST API
- Streamlit Secrets
- Git & GitHub

---

## 📂 Project Structure

```text
AI-Learning-Buddy/
│
├── app.py
├── quiz_engine.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml
```

---

## 🚀 Run Locally

### Clone Repository

```bash
git clone https://github.com/sbharathi09/AI-Learning-Buddy.git
cd AI-Learning-Buddy
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Add Gemini API Key

Create:

```
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY="YOUR_API_KEY"
```

### Run

```bash
streamlit run app.py
```

---

## ☁️ Deployment

This project is deployed using **Streamlit Community Cloud**.

Simply connect the GitHub repository and add your **GEMINI_API_KEY** under **App Settings → Secrets**.

---

## 🔒 Security

- API keys are securely stored using Streamlit Secrets.
- `secrets.toml` is excluded using `.gitignore`.
- Sensitive credentials are never committed to GitHub.

---

## 🎯 Future Enhancements

- Voice-based AI Tutor
- PDF Notes Generator
- Multi-language Support
- Progress Dashboard
- Personalized Learning History
- Flashcards
- Learning Analytics

---

## 👨‍💻 Developer

**Swamidas Bharathi**

📧 GitHub: https://github.com/sbharathi09

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
