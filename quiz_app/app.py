import streamlit as st
import json
import random
import time
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExamPrep Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --bg: #0a0e1a;
    --surface: #111827;
    --surface2: #1a2235;
    --border: #1e3a5f;
    --accent: #3b82f6;
    --accent2: #06b6d4;
    --accent3: #8b5cf6;
    --success: #10b981;
    --danger: #ef4444;
    --warning: #f59e0b;
    --text: #e2e8f0;
    --muted: #64748b;
    --card-glow: rgba(59, 130, 246, 0.08);
}

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main container */
.main .block-container {
    padding: 1.5rem 2rem;
    max-width: 1100px;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0f1f3d 0%, #1a2a4a 40%, #0d1b2e 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -20%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(59,130,246,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #60a5fa, #06b6d4, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.5px;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    margin: 0;
    font-weight: 400;
}
.hero-badge {
    display: inline-block;
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.3);
    color: #60a5fa;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* ── Subject Cards ── */
.subject-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.25s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.subject-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px;
    height: 100%;
    background: var(--accent-color, var(--accent));
    border-radius: 4px 0 0 4px;
}
.subject-card:hover {
    border-color: var(--accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(59,130,246,0.15);
}
.subject-card h3 {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0 0 0.3rem 0;
    color: var(--text);
}
.subject-card p {
    font-size: 0.82rem;
    color: var(--muted);
    margin: 0 0 1rem 0;
}
.subject-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
}
.stat-pills {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.stat-pill {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.72rem;
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
}

/* ── Section Grid ── */
.section-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.75rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s ease;
}
.section-card:hover {
    border-color: var(--accent);
    background: var(--surface2);
}
.section-left h4 { margin: 0 0 0.2rem 0; font-size: 0.95rem; font-weight: 600; }
.section-left p { margin: 0; font-size: 0.78rem; color: var(--muted); }
.section-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 700;
}
.badge-complete { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.badge-pending { background: rgba(59,130,246,0.1); color: #60a5fa; border: 1px solid rgba(59,130,246,0.2); }

/* ── Quiz Area ── */
.quiz-header {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.quiz-qnum {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    color: var(--muted);
}
.quiz-score-live {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--accent2);
}
.diff-badge {
    font-size: 0.7rem;
    padding: 2px 10px;
    border-radius: 20px;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
}
.diff-Easy { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.diff-Medium { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.diff-Hard { background: rgba(239,68,68,0.15); color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }

.question-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}
.question-text {
    font-size: 1.1rem;
    font-weight: 500;
    line-height: 1.6;
    margin: 0;
    color: var(--text);
}

/* ── Option Buttons ── */
.stRadio > div {
    gap: 0.6rem;
    flex-direction: column;
}
.stRadio label {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 0.85rem 1.2rem !important;
    font-size: 0.92rem !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    width: 100% !important;
    color: var(--text) !important;
}
.stRadio label:hover {
    border-color: var(--accent) !important;
    background: rgba(59,130,246,0.08) !important;
}

/* Correct/Wrong feedback */
.feedback-correct {
    background: rgba(16,185,129,0.1);
    border: 1px solid rgba(16,185,129,0.4);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #10b981;
    font-weight: 500;
    margin-top: 1rem;
}
.feedback-wrong {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.4);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    color: #ef4444;
    font-weight: 500;
    margin-top: 1rem;
}
.correct-answer-reveal {
    color: #10b981;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

/* ── Progress Bar ── */
.progress-container {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    height: 8px;
    margin-bottom: 1.5rem;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
    transition: width 0.4s ease;
}

/* ── Result Card ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 3rem;
    text-align: center;
    margin: 2rem 0;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: -100px; left: 50%;
    transform: translateX(-50%);
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(59,130,246,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.result-score-big {
    font-size: 5rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #60a5fa, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    line-height: 1;
}
.result-fraction { font-size: 1.2rem; color: var(--muted); margin-top: 0.3rem; }
.result-grade { font-size: 1.5rem; font-weight: 600; margin: 1rem 0; }
.result-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin: 1.5rem 0;
    flex-wrap: wrap;
}
.result-stat { text-align: center; }
.result-stat-val { font-size: 1.8rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.result-stat-label { font-size: 0.78rem; color: var(--muted); text-transform: uppercase; letter-spacing: 1px; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #3b82f6) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(59,130,246,0.3) !important;
}

/* Back button style */
.back-btn > button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
}

/* Section tracker pills */
.tracker-row {
    display: flex;
    gap: 0.4rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}
.tracker-dot {
    width: 28px; height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}
.dot-done { background: rgba(16,185,129,0.2); color: #10b981; border: 1px solid rgba(16,185,129,0.4); }
.dot-pending { background: rgba(255,255,255,0.05); color: var(--muted); border: 1px solid var(--border); }

/* Dividers */
.section-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: var(--muted);
    margin: 1.5rem 0 0.75rem;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Data Loader ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_questions(filename):
    path = Path(__file__).parent / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)

SUBJECTS = {
    "Java Programming": {
        "file": "questions_java.json",
        "icon": "☕",
        "color": "#f59e0b",
        "desc": "OOP, JVM, Collections, Threads, Swing & more",
        "code": "JP",
    },
    "Computer Networks": {
        "file": "questions_cn.json",
        "icon": "🌐",
        "color": "#3b82f6",
        "desc": "OSI, TCP/IP, Routing, HTTP, DNS & more",
        "code": "CN",
    },
    "Operating Systems & Virtualization": {
        "file": "questions_osv.json",
        "icon": "🖥️",
        "color": "#8b5cf6",
        "desc": "Processes, Memory, File Systems, VM & more",
        "code": "OSV",
    },
    "Machine Learning Essentials": {
        "file": "questions_mle.json",
        "icon": "🤖",
        "color": "#10b981",
        "desc": "Linear Algebra, ML Types, Classification, Clustering & more",
        "code": "MLE",
    },
}

# ── State Init ──────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "home",          # home | subject | quiz | result
        "subject": None,
        "section": None,
        "questions": [],
        "q_index": 0,
        "score": 0,
        "answers": {},             # {q_index: selected_option}
        "answered_current": False,
        "selected_option": None,
        "section_scores": {},      # {subject: {section: score}}
        "section_totals": {},      # {subject: {section: total}}
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()
s = st.session_state

# ── Helpers ─────────────────────────────────────────────────────────────────────
def go(screen, **kwargs):
    s.screen = screen
    for k, v in kwargs.items():
        setattr(s, k, v)

def get_section_status(subject_name, section_name):
    ss = s.section_scores.get(subject_name, {})
    st2 = s.section_totals.get(subject_name, {})
    if section_name in ss:
        score = ss[section_name]
        total = st2[section_name]
        pct = int(score / total * 100) if total else 0
        return "done", score, total, pct
    return "pending", 0, 0, 0

def grade_label(pct):
    if pct >= 90: return "🏆 Excellent!", "#10b981"
    if pct >= 75: return "⭐ Great Job!", "#3b82f6"
    if pct >= 60: return "👍 Good Work", "#f59e0b"
    if pct >= 40: return "📚 Keep Studying", "#f97316"
    return "💪 Needs Practice", "#ef4444"

def progress_bar_html(current, total):
    pct = int(current / total * 100) if total else 0
    return f"""
    <div class="progress-container">
        <div class="progress-fill" style="width:{pct}%"></div>
    </div>
    """

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: HOME
# ══════════════════════════════════════════════════════════════════════════════
if s.screen == "home":
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">Mid-Sem 2 Exam Prep</div>
        <h1 class="hero-title">ExamPrep Pro</h1>
        <p class="hero-sub">Master your B.Tech subjects with syllabus-aligned MCQs · Track progress · Ace your exams</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Choose a Subject to Practice</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, (subj_name, meta) in enumerate(SUBJECTS.items()):
        data = load_questions(meta["file"])
        total_q = sum(len(v) for v in data.values())
        n_sections = len(data)
        done_sections = len(s.section_scores.get(subj_name, {}))
        col = cols[i % 2]
        with col:
            with st.container():
                st.markdown(f"""
                <div class="subject-card" style="--accent-color:{meta['color']}">
                    <div class="subject-icon">{meta['icon']}</div>
                    <h3>{subj_name}</h3>
                    <p>{meta['desc']}</p>
                    <div class="stat-pills">
                        <span class="stat-pill">{n_sections} sections</span>
                        <span class="stat-pill">{total_q} questions</span>
                        <span class="stat-pill">{done_sections}/{n_sections} done</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Open {meta['code']} →", key=f"subj_{i}"):
                    go("subject", subject=subj_name)
                    st.rerun()

    # Overall progress
    st.markdown('<div class="section-title">Overall Progress</div>', unsafe_allow_html=True)
    all_done = sum(len(v) for v in s.section_scores.values())
    total_sections = sum(len(load_questions(m["file"])) for m in SUBJECTS.values())
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sections Completed", all_done)
    c2.metric("Total Sections", total_sections)
    total_correct = sum(sum(v.values()) for v in s.section_scores.values())
    total_attempted = sum(sum(v.values()) for v in s.section_totals.values())
    pct_overall = f"{int(total_correct/total_attempted*100)}%" if total_attempted else "—"
    c3.metric("Questions Attempted", total_attempted)
    c4.metric("Overall Score %", pct_overall)

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: SUBJECT (section list)
# ══════════════════════════════════════════════════════════════════════════════
elif s.screen == "subject":
    meta = SUBJECTS[s.subject]
    data = load_questions(meta["file"])

    col_back, col_title = st.columns([1, 6])
    with col_back:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Home"):
            go("home")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-bottom:1.5rem;">
        <span style="font-size:2.2rem">{meta['icon']}</span>
        <h2 style="margin:0;font-size:1.6rem;font-weight:700;color:var(--text)">{s.subject}</h2>
        <p style="color:var(--muted);font-size:0.85rem;margin:0">{meta['desc']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Section completion tracker dots
    dots_html = '<div class="tracker-row">'
    for idx, sec in enumerate(data.keys()):
        status, sc, tot, pct = get_section_status(s.subject, sec)
        cls = "dot-done" if status == "done" else "dot-pending"
        dots_html += f'<div class="tracker-dot {cls}" title="{sec}">{idx+1}</div>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Sections</div>', unsafe_allow_html=True)

    for idx, (sec_name, questions) in enumerate(data.items()):
        status, sc, tot, pct = get_section_status(s.subject, sec_name)
        col1, col2 = st.columns([5, 1])
        with col1:
            if status == "done":
                badge = f'<span class="section-badge badge-complete">✓ {sc}/{tot} · {pct}%</span>'
            else:
                badge = f'<span class="section-badge badge-pending">{len(questions)} Qs</span>'
            st.markdown(f"""
            <div class="section-card">
                <div class="section-left">
                    <h4>{idx+1}. {sec_name}</h4>
                    <p>{len(questions)} questions · Mix of Easy / Medium / Hard</p>
                </div>
                {badge}
            </div>
            """, unsafe_allow_html=True)
        with col2:
            btn_label = "Retake" if status == "done" else "Start"
            if st.button(btn_label, key=f"sec_{idx}"):
                # Prepare shuffled questions
                qs = questions.copy()
                random.shuffle(qs)
                go("quiz",
                   section=sec_name,
                   questions=qs,
                   q_index=0,
                   score=0,
                   answers={},
                   answered_current=False,
                   selected_option=None)
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: QUIZ
# ══════════════════════════════════════════════════════════════════════════════
elif s.screen == "quiz":
    total_q = len(s.questions)
    q_idx = s.q_index

    # If done
    if q_idx >= total_q:
        go("result")
        st.rerun()

    q = s.questions[q_idx]
    meta = SUBJECTS[s.subject]

    # Header row
    col_back, col_mid, col_score = st.columns([1, 5, 2])
    with col_back:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back"):
            go("subject")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_mid:
        st.markdown(f"""
        <div style="padding-top:0.4rem">
            <span style="font-size:1rem;font-weight:600;color:var(--text)">{meta['icon']} {s.section}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_score:
        st.markdown(f"""
        <div style="text-align:right;padding-top:0.4rem">
            <span class="quiz-score-live">Score: {s.score}/{q_idx}</span>
        </div>
        """, unsafe_allow_html=True)

    # Progress bar
    st.markdown(progress_bar_html(q_idx, total_q), unsafe_allow_html=True)

    # Question card
    diff = q.get("difficulty", "Medium")
    st.markdown(f"""
    <div class="question-box">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
            <span class="quiz-qnum">Question {q_idx+1} of {total_q}</span>
            <span class="diff-badge diff-{diff}">{diff}</span>
        </div>
        <p class="question-text">{q['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Options — shown as radio
    options = q["options"]

    if not s.answered_current:
        selected = st.radio(
            "Choose your answer:",
            options,
            key=f"radio_{q_idx}",
            index=None,
            label_visibility="collapsed",
        )
        if selected:
            s.selected_option = selected

        col_sub, col_skip = st.columns([2, 5])
        with col_sub:
            if st.button("Submit Answer", disabled=(s.selected_option is None)):
                s.answered_current = True
                if s.selected_option == q["answer"]:
                    s.score += 1
                st.rerun()
    else:
        # Show options with feedback
        correct = q["answer"]
        chosen = s.selected_option
        is_correct = chosen == correct

        for opt in options:
            if opt == correct:
                st.markdown(f"✅ **{opt}**")
            elif opt == chosen and not is_correct:
                st.markdown(f"❌ ~~{opt}~~")
            else:
                st.markdown(f"◦ {opt}")

        if is_correct:
            st.markdown(f'<div class="feedback-correct">✓ Correct! Well done.</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="feedback-wrong">✗ Incorrect.<br><span class="correct-answer-reveal">Correct answer: {correct}</span></div>', unsafe_allow_html=True)

        col_next, _ = st.columns([2, 5])
        with col_next:
            btn_label = "Finish Quiz →" if q_idx + 1 >= total_q else "Next Question →"
            if st.button(btn_label, type="primary"):
                s.answers[q_idx] = chosen
                s.q_index += 1
                s.answered_current = False
                s.selected_option = None
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  SCREEN: RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif s.screen == "result":
    total_q = len(s.questions)
    score = s.score
    pct = int(score / total_q * 100) if total_q else 0
    wrong = total_q - score
    grade, grade_color = grade_label(pct)

    # Save result
    if s.subject not in s.section_scores:
        s.section_scores[s.subject] = {}
        s.section_totals[s.subject] = {}
    s.section_scores[s.subject][s.section] = score
    s.section_totals[s.subject][s.section] = total_q

    meta = SUBJECTS[s.subject]

    st.markdown(f"""
    <div class="result-card">
        <p style="color:var(--muted);font-size:0.85rem;margin-bottom:0.5rem">{meta['icon']} {s.subject} · {s.section}</p>
        <p class="result-score-big">{pct}%</p>
        <p class="result-fraction">{score} out of {total_q} correct</p>
        <p class="result-grade" style="color:{grade_color}">{grade}</p>
        <div class="result-stats">
            <div class="result-stat">
                <div class="result-stat-val" style="color:#10b981">{score}</div>
                <div class="result-stat-label">Correct</div>
            </div>
            <div class="result-stat">
                <div class="result-stat-val" style="color:#ef4444">{wrong}</div>
                <div class="result-stat-label">Wrong</div>
            </div>
            <div class="result-stat">
                <div class="result-stat-val" style="color:#3b82f6">{total_q}</div>
                <div class="result-stat-label">Total</div>
            </div>
            <div class="result-stat">
                <div class="result-stat-val" style="color:#8b5cf6">{pct}%</div>
                <div class="result-stat-label">Score</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Difficulty breakdown
    diff_stats = {"Easy": [0,0], "Medium": [0,0], "Hard": [0,0]}
    for i, q in enumerate(s.questions):
        diff = q.get("difficulty", "Medium")
        diff_stats[diff][1] += 1
        if s.answers.get(i) == q["answer"]:
            diff_stats[diff][0] += 1

    st.markdown('<div class="section-title">Difficulty Breakdown</div>', unsafe_allow_html=True)
    dc1, dc2, dc3 = st.columns(3)
    for col, (diff, (correct, total)) in zip([dc1, dc2, dc3], diff_stats.items()):
        pct_d = int(correct/total*100) if total else 0
        col.metric(f"{diff}", f"{correct}/{total}", f"{pct_d}%")

    st.markdown("")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Retake Quiz"):
            qs = s.questions.copy()
            random.shuffle(qs)
            go("quiz", questions=qs, q_index=0, score=0, answers={},
               answered_current=False, selected_option=None)
            st.rerun()
    with col2:
        if st.button(f"📚 More Sections"):
            go("subject")
            st.rerun()
    with col3:
        if st.button("🏠 Home"):
            go("home")
            st.rerun()
