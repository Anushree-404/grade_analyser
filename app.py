import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Grade Analyser", layout="wide", page_icon="🎓")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
    background-attachment: fixed !important;
    min-height: 100vh;
}

.block-container {
    padding: 1.5rem 2rem 3rem !important;
    max-width: 1300px !important;
}

/* Glass card base */
.glass {
    background: rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 16px !important;
}

/* Metric cards */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 16px !important;
    padding: 1.25rem 1.5rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.3) !important;
}

div[data-testid="metric-container"] label {
    font-family: 'Outfit', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: rgba(255,255,255,0.5) !important;
}

div[data-testid="metric-container"] div[data-testid="metric-value"] {
    font-family: 'Outfit', sans-serif !important;
    font-size: 34px !important;
    font-weight: 800 !important;
    color: #ffffff !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 0.55rem 1.5rem !important;
    letter-spacing: 0.03em !important;
    transition: all 0.2s !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.6) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    backdrop-filter: blur(10px) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15,12,41,0.85) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255,255,255,0.1) !important;
}

section[data-testid="stSidebar"] .block-container {
    padding: 1.5rem 1rem !important;
}

/* Slider */
.stSlider > div > div > div {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
}

/* Multiselect */
.stMultiSelect > div > div {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
}

/* Dataframe */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.1) !important;
    margin: 1rem 0 !important;
}

h1, h2, h3 {
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
}

/* Section labels */
.section-lbl {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.4);
    margin-bottom: 0.6rem;
}

p, div, span, label {
    color: rgba(255,255,255,0.85) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Data ──
df = pd.read_csv("students.csv")
subjects = ["Math", "Science", "English", "History"]

df["Total"]      = df[subjects].sum(axis=1)
df["Average"]    = df[subjects].mean(axis=1).round(2)
df["Percentage"] = ((df["Total"] / 400) * 100).round(2)
df["Rank"]       = df["Average"].rank(ascending=False).astype(int)

def assign_grade(p):
    if p >= 90: return "A+"
    elif p >= 80: return "A"
    elif p >= 70: return "B"
    elif p >= 60: return "C"
    elif p >= 40: return "D"
    else: return "F"

df["Grade"]  = df["Percentage"].apply(assign_grade)
df["Result"] = df.apply(
    lambda row: "PASS" if min(row[s] for s in subjects) >= 40 else "FAIL", axis=1
)

PLOT_BG    = "rgba(0,0,0,0)"
GRID_COLOR = "rgba(255,255,255,0.08)"
FONT_COLOR = "#ffffff"
COLORS     = ["#6366f1","#8b5cf6","#ec4899","#14b8a6","#f59e0b","#10b981"]

grade_color_map = {
    "A+": "#10b981", "A": "#10b981", "B": "#6366f1",
    "C":  "#f59e0b", "D": "#f97316", "F": "#ef4444"
}


# ════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:0.5rem 0 1.5rem;">
        <div style="font-size:36px;">🎓</div>
        <div style="font-size:18px;font-weight:800;color:#fff;letter-spacing:-0.01em;">Grade Analyser</div>
        <div style="font-size:10px;color:rgba(255,255,255,0.4);letter-spacing:0.15em;margin-top:2px;">BATCH 2024–25</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-lbl">Filter by Grade</div>', unsafe_allow_html=True)
    all_grades   = sorted(df["Grade"].unique().tolist())
    grade_filter = st.multiselect("Grades", all_grades, default=all_grades, label_visibility="collapsed")

    st.markdown('<div class="section-lbl" style="margin-top:1rem;">Filter by Result</div>', unsafe_allow_html=True)
    result_filter = st.multiselect("Result", ["PASS","FAIL"], default=["PASS","FAIL"], label_visibility="collapsed")

    st.markdown('<div class="section-lbl" style="margin-top:1rem;">Minimum Average</div>', unsafe_allow_html=True)
    min_avg = st.slider("Min Average", 0, 100, 0, label_visibility="collapsed")

    st.markdown('<div class="section-lbl" style="margin-top:1rem;">Subject Focus</div>', unsafe_allow_html=True)
    subject_focus = st.selectbox("Subject", ["All"] + subjects, label_visibility="collapsed")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:11px;color:rgba(255,255,255,0.35);text-align:center;line-height:2;">
        <div>Total Students: {len(df)}</div>
        <div>Subjects: {len(subjects)}</div>
        <div>Max Marks: 400</div>
    </div>
    """, unsafe_allow_html=True)

# Apply filters
filtered_df = df[
    (df["Grade"].isin(grade_filter)) &
    (df["Result"].isin(result_filter)) &
    (df["Average"] >= min_avg)
]

if subject_focus != "All":
    filtered_df = filtered_df.sort_values(subject_focus, ascending=False)


# ════════════════════════════════════════
# HEADER
# ════════════════════════════════════════
st.markdown("""
<div style="padding:1rem 0 0.5rem;">
    <div style="font-size:11px;font-weight:600;letter-spacing:0.2em;
        text-transform:uppercase;color:rgba(255,255,255,0.4);margin-bottom:6px;">
        Academic Performance System
    </div>
    <div style="font-size:42px;font-weight:800;color:#ffffff;
        line-height:1;letter-spacing:-0.02em;margin-bottom:4px;">
        Student Grade
        <span style="background:linear-gradient(135deg,#6366f1,#a78bfa);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;">
        Analyser</span>
    </div>
    <div style="font-size:13px;color:rgba(255,255,255,0.4);margin-top:4px;">
        Showing {shown} of {total} students
    </div>
</div>
""".format(shown=len(filtered_df), total=len(df)), unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ════════════════════════════════════════
# METRIC CARDS
# ════════════════════════════════════════
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Students",      len(filtered_df))
m2.metric("Class Average", f"{filtered_df['Average'].mean().round(2)}%" if len(filtered_df) else "—")
m3.metric("Highest",       f"{filtered_df['Average'].max()}%" if len(filtered_df) else "—")
m4.metric("Passed",        len(filtered_df[filtered_df['Result'] == 'PASS']))
m5.metric("Failed",        len(filtered_df[filtered_df['Result'] == 'FAIL']))

st.markdown("<hr>", unsafe_allow_html=True)


# ════════════════════════════════════════
# STUDENT NAVIGATOR
# ════════════════════════════════════════
st.markdown('<div class="section-lbl">🔍 Student Navigator</div>', unsafe_allow_html=True)

if "student_index" not in st.session_state:
    st.session_state.student_index = 0

if st.session_state.student_index >= len(filtered_df):
    st.session_state.student_index = 0

nav1, nav2, nav3, nav4 = st.columns([1, 1, 3, 1])

with nav1:
    if st.button("◀  Prev"):
        st.session_state.student_index = (st.session_state.student_index - 1) % len(filtered_df)

with nav2:
    if st.button("Next  ▶"):
        st.session_state.student_index = (st.session_state.student_index + 1) % len(filtered_df)

with nav3:
    names = filtered_df["Name"].tolist()
    if names:
        selected_name = st.selectbox(
            "Student",
            names,
            index=st.session_state.student_index,
            label_visibility="collapsed"
        )
        st.session_state.student_index = names.index(selected_name)

with nav4:
    st.markdown(f"""
    <div style="font-size:12px;color:rgba(255,255,255,0.4);
        text-align:right;padding-top:10px;letter-spacing:0.05em;">
        {str(st.session_state.student_index+1).zfill(2)} / {str(len(filtered_df)).zfill(2)}
    </div>
    """, unsafe_allow_html=True)

if not names:
    st.warning("No students match the current filters.")
    st.stop()

row = filtered_df.iloc[st.session_state.student_index]
g_color     = grade_color_map.get(row["Grade"], "#fff")
res_color   = "#10b981" if row["Result"] == "PASS" else "#ef4444"
initials    = row["Name"][0].upper()

# Student banner card
st.markdown(f"""
<div style="background:rgba(255,255,255,0.07);
    backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);
    border:1px solid rgba(255,255,255,0.15);border-radius:16px;
    padding:1.5rem 2rem;margin:0.75rem 0 1rem;
    display:flex;align-items:center;justify-content:space-between;
    box-shadow:0 8px 32px rgba(99,102,241,0.2);">
    <div style="display:flex;align-items:center;gap:1.25rem;">
        <div style="width:56px;height:56px;border-radius:50%;
            background:linear-gradient(135deg,#6366f1,#a78bfa);
            display:flex;align-items:center;justify-content:center;
            font-size:24px;font-weight:800;color:#fff;
            box-shadow:0 4px 15px rgba(99,102,241,0.5);">
            {initials}
        </div>
        <div>
            <div style="font-size:26px;font-weight:800;color:#fff;line-height:1;">
                {row['Name']}
            </div>
            <div style="font-size:11px;color:rgba(255,255,255,0.4);
                letter-spacing:0.1em;margin-top:3px;">
                RANK #{row['Rank']} &nbsp;·&nbsp; TOTAL {row['Total']} / 400
            </div>
        </div>
    </div>
    <div style="display:flex;align-items:center;gap:2rem;">
        <div style="text-align:center;">
            <div style="font-size:36px;font-weight:800;color:{g_color};
                text-shadow:0 0 20px {g_color}88;">{row['Grade']}</div>
            <div style="font-size:9px;color:rgba(255,255,255,0.4);
                letter-spacing:0.12em;">GRADE</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:36px;font-weight:800;color:#fff;">{row['Average']}%</div>
            <div style="font-size:9px;color:rgba(255,255,255,0.4);
                letter-spacing:0.12em;">AVERAGE</div>
        </div>
        <div style="text-align:center;">
            <div style="font-size:26px;font-weight:800;color:{res_color};
                text-shadow:0 0 20px {res_color}88;">{row['Result']}</div>
            <div style="font-size:9px;color:rgba(255,255,255,0.4);
                letter-spacing:0.12em;">RESULT</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Student vs Class Average chart
class_avgs     = df[subjects].mean().round(2).tolist()
student_scores = [int(row[s]) for s in subjects]

fig = go.Figure()
fig.add_trace(go.Bar(
    x=subjects, y=student_scores,
    name=row["Name"],
    marker=dict(
        color=["#6366f1","#8b5cf6","#a78bfa","#c4b5fd"],
        opacity=0.9,
        line=dict(color="rgba(255,255,255,0.1)", width=1)
    ),
    text=student_scores, textposition="outside",
    textfont=dict(color="#fff", size=13, family="Outfit"),
    hovertemplate="<b>%{x}</b><br>Score: %{y}<extra></extra>"
))
fig.add_trace(go.Scatter(
    x=subjects, y=class_avgs,
    name="Class Average",
    mode="lines+markers+text",
    line=dict(color="#f59e0b", width=2.5, dash="dot"),
    marker=dict(color="#f59e0b", size=8,
                line=dict(color="#fff", width=1.5)),
    text=[f"{a}" for a in class_avgs],
    textposition="top center",
    textfont=dict(color="#f59e0b", size=11, family="Outfit"),
    hovertemplate="<b>%{x}</b><br>Class Avg: %{y}<extra></extra>"
))
fig.update_layout(
    barmode="group",
    height=320,
    plot_bgcolor=PLOT_BG,
    paper_bgcolor=PLOT_BG,
    font=dict(family="Outfit", color=FONT_COLOR, size=12),
    yaxis=dict(range=[0, 120], gridcolor=GRID_COLOR,
               zerolinecolor=GRID_COLOR, tickfont=dict(color="rgba(255,255,255,0.4)")),
    xaxis=dict(gridcolor=GRID_COLOR,
               tickfont=dict(color="rgba(255,255,255,0.7)", size=13)),
    legend=dict(orientation="h", y=1.12,
                bgcolor="rgba(0,0,0,0)",
                font=dict(color="rgba(255,255,255,0.7)")),
    margin=dict(l=10, r=10, t=40, b=10),
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ════════════════════════════════════════
# BOTTOM SECTION
# ════════════════════════════════════════
left, right = st.columns([1.2, 1], gap="large")

with left:
    st.markdown('<div class="section-lbl">📋 Class Roster</div>', unsafe_allow_html=True)
    st.dataframe(
        filtered_df[["Rank","Name","Math","Science","English",
                     "History","Total","Average","Grade","Result"]]
        .sort_values("Rank")
        .reset_index(drop=True),
        use_container_width=True,
        height=380
    )

with right:
    # Grade distribution
    st.markdown('<div class="section-lbl">🎓 Grade Distribution</div>', unsafe_allow_html=True)
    grade_counts = filtered_df["Grade"].value_counts().sort_index()
    fig2 = go.Figure(go.Bar(
        x=grade_counts.index,
        y=grade_counts.values,
        marker=dict(
            color=[grade_color_map.get(g,"#6366f1") for g in grade_counts.index],
            opacity=0.85,
            line=dict(color="rgba(255,255,255,0.1)", width=1)
        ),
        text=grade_counts.values,
        textposition="outside",
        textfont=dict(color="#fff", size=12, family="Outfit"),
        hovertemplate="<b>Grade %{x}</b><br>Students: %{y}<extra></extra>"
    ))
    fig2.update_layout(
        height=190,
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=dict(family="Outfit", color=FONT_COLOR, size=12),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
                   tickfont=dict(color="rgba(255,255,255,0.4)")),
        xaxis=dict(tickfont=dict(color="rgba(255,255,255,0.7)", size=13)),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Subject averages
    st.markdown('<div class="section-lbl">📚 Subject Averages</div>', unsafe_allow_html=True)
    subject_avgs = filtered_df[subjects].mean().round(2)
    fig3 = go.Figure()
    for i, (subj, val) in enumerate(zip(subjects, subject_avgs)):
        fig3.add_trace(go.Bar(
            x=[subj], y=[val],
            marker=dict(color=COLORS[i], opacity=0.85,
                        line=dict(color="rgba(255,255,255,0.1)", width=1)),
            text=[f"{val}%"], textposition="outside",
            textfont=dict(color="#fff", size=12, family="Outfit"),
            hovertemplate=f"<b>{subj}</b><br>Avg: {val}%<extra></extra>",
            name=subj
        ))
    fig3.update_layout(
        height=190,
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=dict(family="Outfit", color=FONT_COLOR, size=12),
        yaxis=dict(range=[0,110], gridcolor=GRID_COLOR,
                   zerolinecolor=GRID_COLOR,
                   tickfont=dict(color="rgba(255,255,255,0.4)")),
        xaxis=dict(tickfont=dict(color="rgba(255,255,255,0.7)", size=13)),
        margin=dict(l=10, r=10, t=10, b=10),
        showlegend=False, barmode="group"
    )
    st.plotly_chart(fig3, use_container_width=True)


# ── Footer ──
st.markdown("""
<div style="text-align:center;padding:2rem 0 0.5rem;">
    <div style="display:inline-block;
        background:rgba(255,255,255,0.05);
        border:1px solid rgba(255,255,255,0.1);
        border-radius:100px;padding:8px 24px;
        font-size:10px;color:rgba(255,255,255,0.3);
        letter-spacing:0.15em;">
        GRADE ANALYSER · PYTHON · PANDAS · STREAMLIT · PLOTLY
    </div>
</div>
""", unsafe_allow_html=True)
