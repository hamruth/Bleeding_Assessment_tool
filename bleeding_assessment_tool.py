import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Bleeding Assessment Tool · ISTH BAT",
    page_icon="🩸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Master CSS — Deep Navy / Teal Medical Dark Theme ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');

:root {
    --bg:       #0a0e1a;
    --surface:  #111827;
    --surface2: #1a2236;
    --border:   #1e2d45;
    --accent:   #00c2cb;
    --accent2:  #3b82f6;
    --red:      #f43f5e;
    --amber:    #f59e0b;
    --green:    #10b981;
    --purple:   #a855f7;
    --text:     #e2e8f0;
    --muted:    #64748b;
}

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > section,
[data-testid="block-container"],
.main, .block-container {
    background-color: var(--bg) !important;
    color: var(--text) !important;
}
[data-testid="stHeader"] { background-color: var(--bg) !important; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

*, p, span, div, label {
    font-family: 'Sora', sans-serif !important;
    color: var(--text);
}
h1, h2, h3 {
    font-family: 'Crimson Pro', serif !important;
    color: var(--text) !important;
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent2), var(--accent)) !important;
    border-radius: 99px;
    box-shadow: 0 0 12px rgba(0,194,203,0.4);
}
.stProgress > div > div {
    background: var(--surface2) !important;
    border-radius: 99px;
    height: 8px !important;
}

/* Buttons */
div.stButton > button {
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border-radius: 12px !important;
    padding: 0.65rem 1.5rem !important;
    border: 1px solid var(--border) !important;
    background: var(--surface2) !important;
    color: var(--text) !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}
div.stButton > button:hover {
    background: var(--surface) !important;
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    box-shadow: 0 0 16px rgba(0,194,203,0.2), 0 4px 16px rgba(0,0,0,0.4) !important;
    transform: translateY(-2px) !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0e7490, var(--accent)) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 0 24px rgba(0,194,203,0.3), 0 4px 16px rgba(0,0,0,0.4) !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, var(--accent), #0e7490) !important;
    color: #fff !important;
    transform: translateY(-3px) !important;
}

/* Cards */
.bat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.2rem 2rem;
    box-shadow: 0 0 40px rgba(0,194,203,0.06), 0 4px 32px rgba(0,0,0,0.5);
    margin-bottom: 1.4rem;
    position: relative;
    overflow: hidden;
}
.bat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
}

/* Hero */
.hero-wrap { text-align: center; padding: 2.5rem 1rem 1rem; }
.hero-icon {
    font-size: 3.8rem;
    filter: drop-shadow(0 0 20px rgba(244,63,94,0.6));
    margin-bottom: 0.4rem;
    animation: pulse-icon 2.5s ease-in-out infinite;
}
@keyframes pulse-icon {
    0%,100% { transform: scale(1); filter: drop-shadow(0 0 20px rgba(244,63,94,0.6)); }
    50%      { transform: scale(1.06); filter: drop-shadow(0 0 30px rgba(244,63,94,0.9)); }
}
.hero-title {
    font-family: 'Crimson Pro', serif !important;
    font-size: 2.6rem !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, #e2e8f0 30%, var(--accent));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0.2rem 0 !important;
    line-height: 1.2 !important;
}
.hero-sub {
    color: var(--muted) !important;
    font-size: 1rem;
    max-width: 500px;
    margin: 0.6rem auto 1.8rem;
    line-height: 1.6;
}

/* Pills */
.pill-row { display:flex; gap:0.6rem; justify-content:center; flex-wrap:wrap; margin-bottom:1.8rem; }
.pill {
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 99px;
    padding: 0.35rem 1rem;
    font-size: 0.82rem;
    color: var(--muted) !important;
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}
.pill span { color: var(--accent) !important; font-weight: 600; }

/* Question */
.q-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent) !important;
    margin-bottom: 0.5rem;
}
.q-text {
    font-family: 'Crimson Pro', serif !important;
    font-size: 1.55rem !important;
    line-height: 1.45;
    color: var(--text) !important;
    margin-bottom: 0.6rem !important;
}
.q-hint {
    font-size: 0.84rem;
    color: var(--muted) !important;
    background: var(--surface2);
    border-left: 3px solid var(--accent2);
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 0.9rem;
}

/* Step */
.step-row { display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; }
.step-label { color: var(--muted) !important; font-size: 0.82rem; }
.step-num   { color: var(--accent) !important; font-size: 0.82rem; font-weight: 600; }

/* Divider */
.glow-divider {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 1rem 0;
}

/* Stats bar */
.stat-bar {
    display: flex;
    justify-content: space-around;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem;
    margin-bottom: 1.2rem;
}
.stat-item { text-align: center; }
.stat-val {
    font-size: 1.6rem;
    font-weight: 700;
    font-family: 'Crimson Pro', serif !important;
    line-height: 1;
}
.stat-lbl { font-size: 0.75rem; color: var(--muted) !important; margin-top: 0.2rem; }

/* Result rows */
.result-row {
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid var(--border);
    font-size: 0.9rem;
}
.result-row:last-child { border-bottom: none; }
.r-qnum { min-width:2rem; font-size:0.75rem; color:var(--muted) !important; padding-top:0.1rem; font-weight:600; }
.r-text { flex:1; color:#cbd5e1 !important; line-height:1.4; }
.r-ans  { min-width:3rem; text-align:right; font-weight:700; font-size:0.88rem; }

/* Category tags */
.cat-tag {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    border-radius: 8px;
    padding: 0.3rem 0.75rem;
    margin: 0.2rem;
    font-size: 0.82rem;
    font-weight: 500;
}

/* Disclaimer */
.disclaimer {
    background: linear-gradient(135deg, #1c1a05, #292400);
    border: 1px solid #ca8a04;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.83rem;
    color: #fbbf24 !important;
    margin-top: 1.5rem;
    line-height: 1.5;
}

/* Score ring */
.score-ring {
    width: 130px; height: 130px;
    border-radius: 50%;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    margin: 0 auto 1rem;
}
.score-big {
    font-family: 'Crimson Pro', serif !important;
    font-size: 2.8rem !important;
    font-weight: 700 !important;
    line-height: 1 !important;
}
.score-of { font-size:0.85rem; color:var(--muted) !important; }

.risk-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    border-radius: 99px;
    padding: 0.5rem 1.4rem;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 0.8rem;
}
.advice-text {
    font-size: 0.93rem;
    color: #94a3b8 !important;
    line-height: 1.6;
    text-align: center;
    max-width: 480px;
    margin: 0 auto;
}

#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Questions ─────────────────────────────────────────────────────────────────
QUESTIONS = [
    {"id":1,  "text":"Do you bruise easily without a clear cause, forming bruises larger than a 50-paise coin?",
     "hint":"Spontaneous bruising not related to trauma", "category":"Bruising", "weight":1},
    {"id":2,  "text":"Have you ever had nosebleeds (epistaxis) lasting more than 10 minutes or requiring medical attention?",
     "hint":"Includes spontaneous and recurrent nosebleeds", "category":"Epistaxis", "weight":1},
    {"id":3,  "text":"Do your gums bleed spontaneously or during routine toothbrushing?",
     "hint":"Oral cavity / gum bleeding", "category":"Oral Cavity", "weight":1},
    {"id":4,  "text":"Have you ever bled excessively after a tooth extraction or dental procedure?",
     "hint":"Bleeding requiring additional intervention after dental work", "category":"Post-Dental Bleeding", "weight":1},
    {"id":5,  "text":"Have you ever had prolonged or heavy bleeding after a surgical procedure?",
     "hint":"Bleeding beyond what was expected post-operatively", "category":"Post-Surgical Bleeding", "weight":1},
    {"id":6,  "text":"Have you ever required a blood transfusion due to a bleeding episode?",
     "hint":"Any transfusion related to bleeding, not surgery itself", "category":"Transfusion Requirement", "weight":2},
    {"id":7,  "text":"Do you experience heavy menstrual bleeding (periods lasting >7 days or soaking a pad/tampon every hour)?",
     "hint":"For female patients; skip if not applicable", "category":"Menorrhagia", "weight":1},
    {"id":8,  "text":"Have you ever been hospitalised or had an emergency visit specifically because of bleeding?",
     "hint":"Excludes planned surgical admissions", "category":"Emergency / Hospitalisation", "weight":2},
    {"id":9,  "text":"Have you ever had bleeding into a joint (haemarthrosis), causing pain and swelling?",
     "hint":"Typically knees, elbows, or ankles", "category":"Haemarthrosis", "weight":2},
    {"id":10, "text":"Have you ever had a muscle haematoma (deep bruise / bleed inside a muscle)?",
     "hint":"Often without significant trauma", "category":"Muscle Haematoma", "weight":2},
    {"id":11, "text":"Have you ever noticed blood in your urine (haematuria) without a urinary infection?",
     "hint":"Frank or microscopic haematuria not explained by infection", "category":"Haematuria", "weight":1},
    {"id":12, "text":"Have you ever had blood in your stools or a confirmed gastrointestinal bleed?",
     "hint":"Melaena, haematochezia, or confirmed GI bleeding", "category":"GI Bleeding", "weight":1},
    {"id":13, "text":"Has a close family member been diagnosed with a bleeding disorder?",
     "hint":"E.g. haemophilia, von Willebrand disease, platelet disorder", "category":"Family History", "weight":1},
    {"id":14, "text":"Have you ever had excessive bleeding after childbirth (postpartum haemorrhage >= 500 mL)?",
     "hint":"For female patients who have delivered; skip if not applicable", "category":"Postpartum Haemorrhage", "weight":1},
    {"id":15, "text":"Do minor cuts or wounds take unusually long to stop bleeding (>15 minutes of direct pressure)?",
     "hint":"Bleeding from minor wounds", "category":"Wound Bleeding", "weight":1},
    {"id":16, "text":"Have you ever had a spontaneous intracranial bleed or bleeding in or around the brain?",
     "hint":"ICH, subdural or subarachnoid haemorrhage not related to trauma", "category":"Intracranial Bleeding", "weight":3},
    {"id":17, "text":"Have you been treated with iron supplements or diagnosed with iron-deficiency anaemia due to bleeding?",
     "hint":"Anaemia attributed to chronic blood loss", "category":"Anaemia / Iron Deficiency", "weight":1},
    {"id":18, "text":"Do you develop small red/purple pin-point spots on the skin (petechiae) without injury?",
     "hint":"Petechiae especially on lower limbs or mucous membranes", "category":"Petechiae", "weight":1},
    {"id":19, "text":"Do you bleed excessively when taking aspirin, NSAIDs, or blood-thinning medications?",
     "hint":"Disproportionate bleeding on antiplatelet / anticoagulant drugs", "category":"Drug-Enhanced Bleeding", "weight":1},
    {"id":20, "text":"Have you ever had a miscarriage or pregnancy loss associated with heavy bleeding?",
     "hint":"For female patients; skip if not applicable", "category":"Pregnancy-Related Bleeding", "weight":1},
]

# ── Classification ────────────────────────────────────────────────────────────
def classify(ws):
    if ws == 0:
        return {"label":"Low Risk","color":"#10b981",
                "bg":"linear-gradient(135deg,#022c22,#064e3b)","ring":"rgba(16,185,129,0.25)","icon":"✅",
                "advice":"Your responses suggest a low likelihood of a significant bleeding disorder. Routine follow-up with your physician is recommended."}
    elif ws <= 3:
        return {"label":"Borderline / Mild","color":"#f59e0b",
                "bg":"linear-gradient(135deg,#1c1005,#292100)","ring":"rgba(245,158,11,0.25)","icon":"⚠️",
                "advice":"Some bleeding symptoms are present. A clinical evaluation and basic haematology workup (CBC, PT, aPTT) is advisable. Consider discussing with a haematologist."}
    elif ws <= 6:
        return {"label":"Moderate Risk","color":"#f43f5e",
                "bg":"linear-gradient(135deg,#1f0a10,#4c0519)","ring":"rgba(244,63,94,0.25)","icon":"🔴",
                "advice":"Multiple bleeding symptoms are present. Referral to a haematologist is recommended for further evaluation including von Willebrand factor assays and platelet function tests."}
    else:
        return {"label":"High Risk — Urgent","color":"#a855f7",
                "bg":"linear-gradient(135deg,#1a0a2e,#3b0764)","ring":"rgba(168,85,247,0.25)","icon":"🚨",
                "advice":"Significant bleeding symptoms across multiple domains. Urgent haematology referral is strongly advised. Comprehensive workup including factor assays, platelet aggregation studies, and fibrinogen levels should be performed."}

# ── Session state ─────────────────────────────────────────────────────────────
if "page"    not in st.session_state: st.session_state.page    = 0
if "answers" not in st.session_state: st.session_state.answers = {}

def go_to(p): st.session_state.page = p

# ══════════════════════════════════════════════════════════════════════════════
# INTRO PAGE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == 0:
    st.markdown("""
    <div class='hero-wrap'>
        <div class='hero-icon'>🩸</div>
        <h1 class='hero-title'>Bleeding Assessment Tool</h1>
        <p class='hero-sub'>
            A structured 20-question clinical screening instrument based on the
            <strong style='color:#00c2cb;'>ISTH BAT framework</strong> to evaluate
            the likelihood of an underlying bleeding disorder.
        </p>
        <div class='pill-row'>
            <div class='pill'>🗒️ <span>20</span> Questions</div>
            <div class='pill'>⏱️ <span>3-5</span> Minutes</div>
            <div class='pill'>📊 Instant Results</div>
            <div class='pill'>🏥 ISTH BAT Based</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown("""
        <div class='bat-card'>
            <div style='display:grid; grid-template-columns:1fr 1fr; gap:1rem;'>
                <div style='background:#1a2236; border-radius:12px; padding:1rem; border:1px solid #1e2d45;'>
                    <div style='color:#00c2cb; font-size:1.3rem; margin-bottom:0.4rem;'>🎯</div>
                    <div style='font-weight:600; font-size:0.9rem; margin-bottom:0.3rem;'>Purpose</div>
                    <div style='color:#64748b; font-size:0.82rem; line-height:1.5;'>Screen for hemostatic defects and determine pre-test probability</div>
                </div>
                <div style='background:#1a2236; border-radius:12px; padding:1rem; border:1px solid #1e2d45;'>
                    <div style='color:#3b82f6; font-size:1.3rem; margin-bottom:0.4rem;'>📋</div>
                    <div style='font-weight:600; font-size:0.9rem; margin-bottom:0.3rem;'>Instructions</div>
                    <div style='color:#64748b; font-size:0.82rem; line-height:1.5;'>Answer Yes or No based on your personal bleeding history</div>
                </div>
                <div style='background:#1a2236; border-radius:12px; padding:1rem; border:1px solid #1e2d45;'>
                    <div style='color:#f59e0b; font-size:1.3rem; margin-bottom:0.4rem;'>⚖️</div>
                    <div style='font-weight:600; font-size:0.9rem; margin-bottom:0.3rem;'>Scoring</div>
                    <div style='color:#64748b; font-size:0.82rem; line-height:1.5;'>Weighted scoring — severe symptoms carry higher points</div>
                </div>
                <div style='background:#1a2236; border-radius:12px; padding:1rem; border:1px solid #1e2d45;'>
                    <div style='color:#10b981; font-size:1.3rem; margin-bottom:0.4rem;'>🏥</div>
                    <div style='font-weight:600; font-size:0.9rem; margin-bottom:0.3rem;'>Outcome</div>
                    <div style='color:#64748b; font-size:0.82rem; line-height:1.5;'>Risk classification with clinical guidance for next steps</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🩸  Begin Assessment", use_container_width=True, type="primary"):
            st.session_state.answers = {}
            go_to(1)
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# QUESTION PAGES  (1-20)
# ══════════════════════════════════════════════════════════════════════════════
elif 1 <= st.session_state.page <= 20:
    q_idx = st.session_state.page - 1
    q     = QUESTIONS[q_idx]
    total = len(QUESTIONS)

    st.markdown(f"""
    <div class='step-row'>
        <span class='step-label'>ISTH Bleeding Assessment</span>
        <span class='step-num'>Q {q_idx+1} / {total}</span>
    </div>
    """, unsafe_allow_html=True)
    st.progress(q_idx / total)
    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        st.markdown(f"""
        <div class='bat-card'>
            <div class='q-label'>Question {q['id']} &nbsp;·&nbsp; {q['category']}</div>
            <div class='q-text'>{q['text']}</div>
            <hr class='glow-divider'>
            <div class='q-hint'>ℹ️&nbsp;&nbsp;{q['hint']}</div>
        </div>
        """, unsafe_allow_html=True)

        prev = st.session_state.answers.get(q["id"], None)
        c1, c2 = st.columns(2)
        with c1:
            label = "✅  Yes  ✓" if prev == "Yes" else "✅  Yes"
            if st.button(label, use_container_width=True,
                         type="primary" if prev == "Yes" else "secondary",
                         key=f"yes_{q['id']}"):
                st.session_state.answers[q["id"]] = "Yes"
                go_to(st.session_state.page + 1)
                st.rerun()
        with c2:
            label = "❌  No  ✓" if prev == "No" else "❌  No"
            if st.button(label, use_container_width=True,
                         type="primary" if prev == "No" else "secondary",
                         key=f"no_{q['id']}"):
                st.session_state.answers[q["id"]] = "No"
                go_to(st.session_state.page + 1)
                st.rerun()

        st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([2, 3, 2])
        with nav1:
            if st.session_state.page > 1:
                if st.button("← Back", use_container_width=True):
                    go_to(st.session_state.page - 1)
                    st.rerun()
        with nav3:
            if q["id"] in st.session_state.answers:
                if st.button("Skip →", use_container_width=True):
                    go_to(st.session_state.page + 1)
                    st.rerun()

        # Progress dots
        dot_html = "<div style='display:flex;gap:4px;justify-content:center;margin-top:1.2rem;flex-wrap:wrap;'>"
        for i, qq in enumerate(QUESTIONS):
            ans = st.session_state.answers.get(qq["id"])
            if i == q_idx:          col = "#00c2cb"
            elif ans == "Yes":      col = "#f43f5e"
            elif ans == "No":       col = "#10b981"
            else:                   col = "#1e2d45"
            dot_html += f"<div style='width:10px;height:10px;border-radius:50%;background:{col};'></div>"
        dot_html += "</div>"
        st.markdown(dot_html, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RESULTS PAGE  (page == 21)
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == 21:
    answers   = st.session_state.answers
    yes_count = sum(1 for v in answers.values() if v == "Yes")
    no_count  = sum(1 for v in answers.values() if v == "No")
    total_ans = len(answers)
    weighted  = sum(q["weight"] for q in QUESTIONS if answers.get(q["id"]) == "Yes")
    result    = classify(weighted)
    c         = result["color"]

    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 0.5rem;'>
        <div style='font-size:2.2rem;'>📊</div>
        <h1 style='margin:0.2rem 0;'>Assessment Results</h1>
        <p style='color:#64748b; font-size:0.9rem;'>ISTH Bleeding Assessment Tool · Clinical Screening</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:

        # Stats bar
        st.markdown(f"""
        <div class='stat-bar'>
            <div class='stat-item'>
                <div class='stat-val' style='color:{c};'>{yes_count}</div>
                <div class='stat-lbl'>Positive</div>
            </div>
            <div class='stat-item'>
                <div class='stat-val' style='color:#10b981;'>{no_count}</div>
                <div class='stat-lbl'>Negative</div>
            </div>
            <div class='stat-item'>
                <div class='stat-val' style='color:#3b82f6;'>{total_ans}</div>
                <div class='stat-lbl'>Answered</div>
            </div>
            <div class='stat-item'>
                <div class='stat-val' style='color:{c};'>{weighted}</div>
                <div class='stat-lbl'>Weighted Score</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk card
        st.markdown(f"""
        <div class='bat-card' style='text-align:center; background:{result["bg"]};
             border-color:{c}44;'>
            <div class='score-ring' style='background:radial-gradient(circle,{result["ring"]} 0%,transparent 70%);
                 border:3px solid {c};'>
                <div class='score-big' style='color:{c};'>{yes_count}</div>
                <div class='score-of'>/ {total_ans}</div>
            </div>
            <div class='risk-badge' style='background:{c}22; color:{c}; border:1px solid {c}55;'>
                {result["icon"]} &nbsp; {result["label"]}
            </div>
            <p class='advice-text'>{result["advice"]}</p>
        </div>
        """, unsafe_allow_html=True)

        # Positive categories
        pos_cats = [q["category"] for q in QUESTIONS if answers.get(q["id"]) == "Yes"]
        if pos_cats:
            st.markdown("#### 🔴 Positive Symptom Domains")
            tag_colors = ["#f43f5e","#f59e0b","#a855f7","#3b82f6","#10b981","#ec4899"]
            tags = "".join(
                f"<span class='cat-tag' style='background:{tag_colors[i%len(tag_colors)]}18;"
                f"border:1px solid {tag_colors[i%len(tag_colors)]}44;"
                f"color:{tag_colors[i%len(tag_colors)]};'>● {cat}</span>"
                for i, cat in enumerate(pos_cats)
            )
            st.markdown(f"<div style='margin-bottom:1rem;display:flex;flex-wrap:wrap;gap:0.4rem;'>{tags}</div>",
                        unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:#022c22;border:1px solid #10b981;border-radius:12px;
                 padding:0.9rem 1.2rem;color:#10b981;font-size:0.9rem;margin-bottom:1rem;'>
                ✅ No positive bleeding symptoms reported across all domains.
            </div>""", unsafe_allow_html=True)

        # Answer summary
        st.markdown("#### 📝 Complete Answer Summary")
        rows = ""
        for q in QUESTIONS:
            ans = answers.get(q["id"], "—")
            ac  = "#f43f5e" if ans=="Yes" else ("#10b981" if ans=="No" else "#64748b")
            ab  = "#f43f5e11" if ans=="Yes" else ("#10b98111" if ans=="No" else "transparent")
            rows += (f"<div class='result-row'>"
                     f"<span class='r-qnum'>Q{q['id']}</span>"
                     f"<span class='r-text'>{q['text']}</span>"
                     f"<span class='r-ans' style='color:{ac};background:{ab};"
                     f"border-radius:6px;padding:0.15rem 0.5rem;'>{ans}</span>"
                     f"</div>")
        st.markdown(f"<div class='bat-card' style='padding:1.2rem 1.5rem;'>{rows}</div>",
                    unsafe_allow_html=True)

        # Disclaimer
        st.markdown("""
        <div class='disclaimer'>
            ⚠️ <strong>Medical Disclaimer:</strong> This tool is for educational and screening
            purposes only. It does not constitute a medical diagnosis. Please consult a qualified
            haematologist or physician for clinical evaluation and appropriate testing based on
            ISTH BAT guidelines.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)
        b1, b2 = st.columns(2)
        with b1:
            if st.button("🔄  Retake Assessment", use_container_width=True, type="primary"):
                st.session_state.answers = {}
                go_to(0)
                st.rerun()
        with b2:
            if st.button("← Review Questions", use_container_width=True):
                go_to(1)
                st.rerun()
