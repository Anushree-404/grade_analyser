import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load data
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

def assign_result(row):
    return "PASS" if min(row[s] for s in subjects) >= 40 else "FAIL"

df["Grade"]  = df["Percentage"].apply(assign_grade)
df["Result"] = df.apply(assign_result, axis=1)

bar_colors = ["#2ecc71" if a >= 80 else "#e74c3c" if a < 40 else "#3498db"
              for a in df["Average"]]

grade_counts = df["Grade"].value_counts().sort_index()
grade_color_map = {"A+": "#2ecc71", "A": "#27ae60", "B": "#3498db",
                   "C": "#f39c12", "D": "#e67e22", "F": "#e74c3c"}

subject_avgs = df[subjects].mean().round(2)
pf_counts    = df["Result"].value_counts()

# ── Build dashboard with 4 charts ──
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=(
        "Average Score per Student",
        "Grade Distribution",
        "Subject-wise Class Average",
        "Pass vs Fail"
    ),
    specs=[
        [{"type": "bar"},  {"type": "pie"}],
        [{"type": "bar"},  {"type": "pie"}]
    ]
)

# Chart 1 — Horizontal bar: average per student
df_sorted = df.sort_values("Average", ascending=True)
fig.add_trace(go.Bar(
    x=df_sorted["Average"],
    y=df_sorted["Name"],
    orientation="h",
    marker_color=[
        "#2ecc71" if a >= 80 else "#e74c3c" if a < 40 else "#3498db"
        for a in df_sorted["Average"]
    ],
    text=[f"{a}%" for a in df_sorted["Average"]],
    textposition="outside",
    hovertemplate="<b>%{y}</b><br>Average: %{x}%<extra></extra>",
    name="Average"
), row=1, col=1)

# Chart 2 — Pie: grade distribution
fig.add_trace(go.Pie(
    labels=grade_counts.index,
    values=grade_counts.values,
    marker_colors=[grade_color_map.get(g, "#95a5a6") for g in grade_counts.index],
    hovertemplate="<b>Grade %{label}</b><br>Students: %{value}<br>%{percent}<extra></extra>",
    textinfo="label+percent",
    hole=0.3,
    name="Grades"
), row=1, col=2)

# Chart 3 — Bar: subject averages
fig.add_trace(go.Bar(
    x=subjects,
    y=subject_avgs,
    marker_color=["#9b59b6", "#1abc9c", "#e67e22", "#e74c3c"],
    text=[f"{a}%" for a in subject_avgs],
    textposition="outside",
    hovertemplate="<b>%{x}</b><br>Class Average: %{y}%<extra></extra>",
    name="Subject Avg"
), row=2, col=1)

# Chart 4 — Donut: pass vs fail
fig.add_trace(go.Pie(
    labels=pf_counts.index,
    values=pf_counts.values,
    marker_colors=["#2ecc71", "#e74c3c"],
    hovertemplate="<b>%{label}</b><br>Students: %{value}<br>%{percent}<extra></extra>",
    textinfo="label+value",
    hole=0.6,
    name="Result"
), row=2, col=2)

# ── Layout ──
fig.update_layout(
    title=dict(
        text="📊 Student Grade Analyser — Interactive Dashboard",
        font=dict(size=20),
        x=0.5
    ),
    height=750,
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Segoe UI", size=13),
    hoverlabel=dict(bgcolor="white", font_size=13)
)

fig.update_xaxes(range=[0, 110], row=1, col=1)
fig.update_yaxes(row=2, col=1, range=[0, 110])

fig.write_html("dashboard.html")
print("Dashboard saved as 'dashboard.html' — open it in your browser!")
fig.show()