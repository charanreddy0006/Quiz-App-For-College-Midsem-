# ExamPrep Pro — B.Tech Mid-Sem Quiz App

A Streamlit-based MCQ quiz app for B.Tech (AI) students preparing for mid-semester exams.

## Subjects Covered
- ☕ Java Programming — 180 questions · 6 sections
- 🌐 Computer Networks — 150 questions · 5 sections
- 🖥️ OS & Virtualization — 150 questions · 5 sections
- 🤖 Machine Learning — 210 questions · 7 sections

**Total: 690 questions across 23 sections**

## Run Locally

```bash
pip install streamlit
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this folder to a GitHub repository
2. Go to https://share.streamlit.io
3. Connect your GitHub repo
4. Set `app.py` as the main file
5. Click Deploy!

## Project Structure

```
quiz_app/
├── app.py                  # Main Streamlit application
├── questions_java.json     # Java Programming MCQs
├── questions_cn.json       # Computer Networks MCQs
├── questions_osv.json      # OS & Virtualization MCQs
├── questions_mle.json      # Machine Learning MCQs
├── requirements.txt        # Python dependencies
└── README.md
```
