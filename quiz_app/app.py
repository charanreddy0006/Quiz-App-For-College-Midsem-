import streamlit as st
import json
import random
from pathlib import Path

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ExamPrep Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
}
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none !important; }
.main .block-container { padding: 1.5rem 2rem 3rem; max-width: 960px; }

.stButton > button {
    background: #1f6feb !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 8px 20px !important;
    transition: all 0.2s !important;
    font-family: 'Inter', sans-serif !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #388bfd !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(56,139,253,0.4) !important;
}

div[data-testid="stRadio"] > div {
    display: flex !important;
    flex-direction: column !important;
    gap: 10px !important;
}
div[data-testid="stRadio"] label {
    background: #161b22 !important;
    border: 1.5px solid #30363d !important;
    border-radius: 10px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    color: #e6edf3 !important;
    margin: 0 !important;
}
div[data-testid="stRadio"] label:hover {
    border-color: #388bfd !important;
    background: rgba(56,139,253,0.08) !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #1f6feb, #56d364) !important;
    border-radius: 10px !important;
}
.stProgress > div > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    height: 8px !important;
}

[data-testid="stMetric"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
}
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    color: #79c0ff !important;
}
[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-size: 11px !important;
}

.hero-card {
    background: linear-gradient(135deg, #161b22, #1c2128);
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 1.5rem;
}
.hero-tag {
    display: inline-block;
    background: rgba(56,139,253,0.15);
    color: #79c0ff;
    border: 1px solid rgba(56,139,253,0.3);
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 14px;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(135deg, #79c0ff, #56d364, #d2a8ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 8px;
}
.hero-sub { color: #8b949e; font-size: 15px; margin: 0; }

.subj-card {
    background: #161b22;
    border: 1.5px solid #30363d;
    border-left: 4px solid var(--accent, #388bfd);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 10px;
}
.q-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 24px 26px;
    margin-bottom: 16px;
}
.section-row {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 8px;
}
.result-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 2.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
}

.sec-label {
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #8b949e;
    margin: 16px 0 10px;
}
.q-text { font-size: 17px; line-height: 1.65; color: #e6edf3; margin: 0; }
.q-num { font-size: 12px; color: #8b949e; font-family: 'JetBrains Mono', monospace; }

.badge { display: inline-block; padding: 3px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.badge-easy { background: rgba(86,211,100,0.12); color: #56d364; border: 1px solid rgba(86,211,100,0.3); }
.badge-medium { background: rgba(227,179,65,0.12); color: #e3b341; border: 1px solid rgba(227,179,65,0.3); }
.badge-hard { background: rgba(248,81,73,0.12); color: #f85149; border: 1px solid rgba(248,81,73,0.3); }
.badge-done { background: rgba(86,211,100,0.12); color: #56d364; border: 1px solid rgba(86,211,100,0.3); }
.badge-pending { background: rgba(56,139,253,0.1); color: #79c0ff; border: 1px solid rgba(56,139,253,0.2); }

.res-pct {
    font-size: 5rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    background: linear-gradient(135deg, #79c0ff, #56d364);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}
.pill { background: rgba(255,255,255,0.05); border: 1px solid #30363d; border-radius: 20px; padding: 3px 11px; font-size: 11px; color: #8b949e; font-family: 'JetBrains Mono', monospace; display: inline-block; margin-right: 4px; }
.dots-row { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 16px; }
.dot { width: 26px; height: 26px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 700; font-family: 'JetBrains Mono', monospace; border: 1px solid #30363d; color: #8b949e; background: #161b22; }
.dot-done { background: rgba(86,211,100,0.15); border-color: rgba(86,211,100,0.5); color: #56d364; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─── Data Loader ──────────────────────────────────────────────────────────────
@st.cache_data
def load_questions(filename: str) -> dict:
    path = Path(__file__).parent / filename
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ─── Subject Config ───────────────────────────────────────────────────────────
SUBJECTS = {
    "Java Programming": {
        "file": "questions_java.json",
        "icon": "☕",
        "color": "#e3b341",
        "desc": "OOP, JVM, Collections, Threads, Swing & Event Handling",
        "code": "JP",
    },
    "Computer Networks": {
        "file": "questions_cn.json",
        "icon": "🌐",
        "color": "#388bfd",
        "desc": "OSI, TCP/IP, HTTP, DNS, Routing & Data Link Layer",
        "code": "CN",
    },
    "OS & Virtualization": {
        "file": "questions_osv.json",
        "icon": "🖥️",
        "color": "#bc8cff",
        "desc": "Processes, Scheduling, Memory, File Systems & VM",
        "code": "OSV",
    },
    "Machine Learning": {
        "file": "questions_mle.json",
        "icon": "🤖",
        "color": "#56d364",
        "desc": "Linear Algebra, ML Types, Classification, Clustering & Python",
        "code": "MLE",
    },
}

DIFF_BADGE = {"Easy": "badge-easy", "Medium": "badge-medium", "Hard": "badge-hard"}


# ─── State ────────────────────────────────────────────────────────────────────
def init():
    defaults = {
        "screen": "home",
        "subject": None,
        "section": None,
        "questions": [],
        "q_idx": 0,
        "score": 0,
        "user_answers": {},
        "answered": False,
        "chosen": None,
        "section_scores": {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init()
S = st.session_state


def goto(screen, **kw):
    S.screen = screen
    for k, v in kw.items():
        setattr(S, k, v)
    st.rerun()


def pct(score, total):
    return round(score / total * 100) if total else 0


def grade(p):
    if p >= 90: return "🏆 Excellent!", "#56d364"
    if p >= 75: return "⭐ Great Job!", "#388bfd"
    if p >= 60: return "👍 Good Work", "#e3b341"
    if p >= 40: return "📚 Keep Studying", "#e09003"
    return "💪 Needs Practice", "#f85149"


def get_sec_info(subject, section):
    return S.section_scores.get(subject, {}).get(section)


# ══════════════════════════════════════════════════════════════════════════════
#  HOME
# ══════════════════════════════════════════════════════════════════════════════
if S.screen == "home":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-tag">Mid-Sem 2 · Exam Prep</div>
        <h1 class="hero-title">ExamPrep Pro</h1>
        <p class="hero-sub">Syllabus-aligned MCQ practice for B.Tech AI students &mdash; 690 questions across 23 sections</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Choose a Subject</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    for col, (name, meta) in zip([col1, col2, col1, col2], list(SUBJECTS.items())):
        data = load_questions(meta["file"])
        n_sec = len(data)
        n_q = sum(len(v) for v in data.values())
        done = len(S.section_scores.get(name, {}))
        done_pill = f'<span class="pill" style="color:#56d364;border-color:rgba(86,211,100,0.3)">{done}/{n_sec} done</span>' if done else ""

        with col:
            st.markdown(f"""
            <div class="subj-card" style="--accent:{meta['color']}">
                <div style="font-size:2rem;margin-bottom:8px">{meta['icon']}</div>
                <div style="font-size:16px;font-weight:700;margin-bottom:4px">{name}</div>
                <div style="font-size:12px;color:#8b949e;margin-bottom:12px">{meta['desc']}</div>
                <span class="pill">{n_sec} sections</span>
                <span class="pill">{n_q} questions</span>
                {done_pill}
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Open {meta['code']} →", key=f"h_{name}"):
                goto("subject", subject=name)

    st.markdown('<div class="sec-label" style="margin-top:20px">Your Progress</div>', unsafe_allow_html=True)
    done_secs = sum(len(v) for v in S.section_scores.values())
    total_secs = sum(len(load_questions(m["file"])) for m in SUBJECTS.values())
    total_correct = sum(v["score"] for s in S.section_scores.values() for v in s.values())
    total_att = sum(v["total"] for s in S.section_scores.values() for v in s.values())
    overall = f"{pct(total_correct, total_att)}%" if total_att else "—"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Sections Done", done_secs)
    c2.metric("Total Sections", total_secs)
    c3.metric("Qs Attempted", total_att)
    c4.metric("Overall %", overall)


# ══════════════════════════════════════════════════════════════════════════════
#  SUBJECT
# ══════════════════════════════════════════════════════════════════════════════
elif S.screen == "subject":
    meta = SUBJECTS[S.subject]
    data = load_questions(meta["file"])
    sections = list(data.items())

    if st.button("← Home", key="bk_home"):
        goto("home")

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;margin:16px 0 20px">
        <span style="font-size:2.2rem">{meta['icon']}</span>
        <div>
            <h2 style="margin:0;font-size:1.5rem;font-weight:700;color:#e6edf3">{S.subject}</h2>
            <p style="margin:0;color:#8b949e;font-size:13px">{meta['desc']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Completion dots
    dots = "".join(
        f'<div class="dot {"dot-done" if get_sec_info(S.subject, sec) else ""}" title="{sec}">{i+1}</div>'
        for i, (sec, _) in enumerate(sections)
    )
    st.markdown(f'<div class="dots-row">{dots}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-label">Sections</div>', unsafe_allow_html=True)

    for i, (sec, qs) in enumerate(sections):
        info = get_sec_info(S.subject, sec)
        if info:
            badge = f'<span class="badge badge-done">✓ {info["score"]}/{info["total"]} · {pct(info["score"], info["total"])}%</span>'
            btn_label = "Retake"
        else:
            badge = f'<span class="badge badge-pending">{len(qs)} Qs</span>'
            btn_label = "Start →"

        col_a, col_b = st.columns([6, 1])
        with col_a:
            st.markdown(f"""
            <div class="section-row">
                <div style="display:flex;justify-content:space-between;align-items:center">
                    <div>
                        <div style="font-weight:600;font-size:15px;margin-bottom:3px">{i+1}. {sec}</div>
                        <div style="font-size:12px;color:#8b949e">{len(qs)} questions · Easy / Medium / Hard mix</div>
                    </div>
                    <div>{badge}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_b:
            if st.button(btn_label, key=f"s_{i}"):
                qs_shuffled = qs.copy()
                random.shuffle(qs_shuffled)
                goto("quiz",
                     section=sec,
                     questions=qs_shuffled,
                     q_idx=0,
                     score=0,
                     user_answers={},
                     answered=False,
                     chosen=None)


# ══════════════════════════════════════════════════════════════════════════════
#  QUIZ
# ══════════════════════════════════════════════════════════════════════════════
elif S.screen == "quiz":
    total_q = len(S.questions)

    if S.q_idx >= total_q:
        goto("result")

    q = S.questions[S.q_idx]
    diff = q.get("difficulty", "Medium")
    meta = SUBJECTS[S.subject]

    # ── Header ────────────────────────────────────────────────────────────
    col_back, col_mid, col_sc = st.columns([1, 4, 2])
    with col_back:
        if st.button("← Exit", key="qz_exit"):
            goto("subject")
    with col_mid:
        st.markdown(f"<div style='padding-top:6px;font-weight:600;font-size:14px;color:#e6edf3'>{meta['icon']} {S.section}</div>",
                    unsafe_allow_html=True)
    with col_sc:
        st.markdown(
            f"<div style='text-align:right;padding-top:4px;font-family:monospace;font-size:16px;"
            f"font-weight:700;color:#56d364'>Score: {S.score}/{S.q_idx}</div>",
            unsafe_allow_html=True)

    # ── Progress bar ──────────────────────────────────────────────────────
    st.progress(S.q_idx / total_q)

    # ── Question card ─────────────────────────────────────────────────────
    badge_cls = DIFF_BADGE.get(diff, "badge-medium")
    st.markdown(f"""
    <div class="q-card">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
            <span class="q-num">Question {S.q_idx + 1} of {total_q}</span>
            <span class="badge {badge_cls}">{diff}</span>
        </div>
        <p class="q-text">{q['question']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Not yet answered ──────────────────────────────────────────────────
    if not S.answered:
        chosen = st.radio(
            "Pick your answer:",
            q["options"],
            key=f"q_{S.q_idx}",
            index=None,
            label_visibility="collapsed",
        )
        if chosen:
            S.chosen = chosen

        col_sub, _ = st.columns([2, 5])
        with col_sub:
            if st.button("✔ Submit Answer", key=f"sub_{S.q_idx}", disabled=(S.chosen is None)):
                S.answered = True
                if S.chosen == q["answer"]:
                    S.score += 1
                S.user_answers[S.q_idx] = S.chosen
                st.rerun()

    # ── Already answered: show feedback ───────────────────────────────────
    else:
        correct = q["answer"]
        is_correct = (S.chosen == correct)

        for opt in q["options"]:
            if opt == correct and is_correct:
                st.markdown(
                    f'<div style="background:rgba(86,211,100,0.1);border:1.5px solid '
                    f'rgba(86,211,100,0.5);border-radius:10px;padding:14px 18px;'
                    f'color:#56d364;font-weight:600;margin-bottom:8px">✅ {opt}</div>',
                    unsafe_allow_html=True)
            elif opt == correct:
                st.markdown(
                    f'<div style="background:rgba(86,211,100,0.08);border:1.5px solid '
                    f'rgba(86,211,100,0.4);border-radius:10px;padding:14px 18px;'
                    f'color:#56d364;margin-bottom:8px">✅ {opt}</div>',
                    unsafe_allow_html=True)
            elif opt == S.chosen and not is_correct:
                st.markdown(
                    f'<div style="background:rgba(248,81,73,0.1);border:1.5px solid '
                    f'rgba(248,81,73,0.5);border-radius:10px;padding:14px 18px;'
                    f'color:#f85149;margin-bottom:8px">❌ {opt}</div>',
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div style="background:#161b22;border:1px solid #21262d;'
                    f'border-radius:10px;padding:14px 18px;color:#6e7681;'
                    f'margin-bottom:8px">{opt}</div>',
                    unsafe_allow_html=True)

        # Feedback banner
        if is_correct:
            st.markdown(
                '<div style="background:rgba(86,211,100,0.1);border:1.5px solid '
                'rgba(86,211,100,0.4);border-radius:10px;padding:14px 18px;'
                'color:#56d364;font-weight:600;margin-top:4px">✓ Correct! Well done.</div>',
                unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div style="background:rgba(248,81,73,0.1);border:1.5px solid '
                f'rgba(248,81,73,0.4);border-radius:10px;padding:14px 18px;'
                f'color:#f85149;font-weight:600;margin-top:4px">✗ Incorrect!<br>'
                f'<span style="font-size:13px;color:#56d364;font-weight:500">'
                f'✅ Correct Answer: {correct}</span></div>',
                unsafe_allow_html=True)

        st.markdown("")
        is_last = (S.q_idx + 1 >= total_q)
        col_nxt, _ = st.columns([2, 5])
        with col_nxt:
            btn_lbl = "🏁 Finish Quiz" if is_last else "Next Question →"
            if st.button(btn_lbl, key=f"nx_{S.q_idx}"):
                S.q_idx += 1
                S.answered = False
                S.chosen = None
                if S.q_idx >= total_q:
                    goto("result")
                else:
                    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif S.screen == "result":
    total_q = len(S.questions)
    score = S.score
    p = pct(score, total_q)
    wrong = total_q - score
    grade_txt, grade_color = grade(p)
    meta = SUBJECTS[S.subject]

    # Persist score
    if S.subject not in S.section_scores:
        S.section_scores[S.subject] = {}
    S.section_scores[S.subject][S.section] = {"score": score, "total": total_q}

    st.markdown(f"""
    <div class="result-card">
        <p style="color:#8b949e;font-size:13px;margin-bottom:10px">{meta['icon']} {S.subject} &mdash; {S.section}</p>
        <div class="res-pct">{p}%</div>
        <p style="color:#8b949e;font-size:16px;margin:10px 0 4px">{score} out of {total_q} correct</p>
        <p style="font-size:1.3rem;font-weight:700;color:{grade_color};margin:0">{grade_txt}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("✅ Correct", score)
    c2.metric("❌ Wrong", wrong)
    c3.metric("📝 Total Qs", total_q)
    c4.metric("🎯 Score", f"{p}%")

    st.markdown("")
    st.markdown('<div class="sec-label">Difficulty Breakdown</div>', unsafe_allow_html=True)

    diff_data = {"Easy": [0, 0], "Medium": [0, 0], "Hard": [0, 0]}
    for i, q in enumerate(S.questions):
        d = q.get("difficulty", "Medium")
        diff_data[d][1] += 1
        if S.user_answers.get(i) == q["answer"]:
            diff_data[d][0] += 1

    dc1, dc2, dc3 = st.columns(3)
    for col, (diff, (c, t)) in zip([dc1, dc2, dc3], diff_data.items()):
        dp = pct(c, t)
        col.metric(diff, f"{c}/{t}", f"{dp}%")

    st.markdown("<br>", unsafe_allow_html=True)

    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🔄 Retake Quiz"):
            qs = S.questions.copy()
            random.shuffle(qs)
            goto("quiz", questions=qs, q_idx=0, score=0,
                 user_answers={}, answered=False, chosen=None)
    with b2:
        if st.button("📚 More Sections"):
            goto("subject")
    with b3:
        if st.button("🏠 Home"):
            goto("home")
