import pandas as pd
import plotly.graph_objects as go

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

class_avgs = df[subjects].mean().round(2).tolist()

# Build one trace per student (only first visible)
fig = go.Figure()

for i, row in df.iterrows():
    student_scores = [row[s] for s in subjects]
    visible = (i == 0)

    # Student bars
    fig.add_trace(go.Bar(
        x=subjects,
        y=student_scores,
        name=row["Name"],
        marker_color="#3498db",
        text=[f"{s}" for s in student_scores],
        textposition="outside",
        visible=visible,
        hovertemplate="<b>%{x}</b><br>Score: %{y}<extra></extra>",
    ))

    # Class average bars
    fig.add_trace(go.Bar(
        x=subjects,
        y=class_avgs,
        name="Class Avg",
        marker_color="#e67e22",
        text=[f"{a}" for a in class_avgs],
        textposition="outside",
        visible=visible,
        hovertemplate="<b>%{x}</b><br>Class Avg: %{y}<extra></extra>",
    ))

n = len(df)

# Build steps for slider
steps = []
for i, row in df.iterrows():
    visible_array = [False] * (n * 2)
    visible_array[i * 2]     = True
    visible_array[i * 2 + 1] = True
    step = dict(
        method="update",
        args=[
            {"visible": visible_array},
            {"title": f"📊 {row['Name']} — Rank #{row['Rank']} | Grade: {row['Grade']} | Result: {row['Result']} | Average: {row['Average']}%"}
        ],
        label=row["Name"]
    )
    steps.append(step)

# Forward / Backward buttons
buttons = []
for i, row in df.iterrows():
    visible_array = [False] * (n * 2)
    visible_array[i * 2]     = True
    visible_array[i * 2 + 1] = True
    buttons.append(dict(
        method="update",
        args=[
            {"visible": visible_array},
            {"title": f"📊 {row['Name']} — Rank #{row['Rank']} | Grade: {row['Grade']} | Result: {row['Result']} | Average: {row['Average']}%"}
        ],
        label=row["Name"]
    ))

first = df.iloc[0]
fig.update_layout(
    title=f"📊 {first['Name']} — Rank #{first['Rank']} | Grade: {first['Grade']} | Result: {first['Result']} | Average: {first['Average']}%",
    barmode="group",
    height=600,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Segoe UI", size=13),
    yaxis=dict(range=[0, 120]),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    sliders=[dict(
        active=0,
        steps=steps,
        x=0.05,
        xanchor="left",
        y=-0.12,
        yanchor="top",
        len=0.9,
        currentvalue=dict(
            prefix="Student: ",
            visible=True,
            xanchor="center",
            font=dict(size=14, color="#3498db")
        ),
        transition=dict(duration=300)
    )],
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            x=0.5,
            xanchor="center",
            y=-0.3,
            yanchor="top",
            buttons=[
                dict(
                    label="◀ Previous",
                    method="animate",
                    args=[None, {"frame": {"duration": 0}, "mode": "immediate"}]
                ),
                dict(
                    label="▶ Next",
                    method="animate",
                    args=[None, {"frame": {"duration": 0}, "mode": "immediate"}]
                ),
            ],
            direction="left",
            pad={"r": 10, "t": 10},
            bgcolor="white",
            bordercolor="#3498db",
            borderwidth=1,
            font=dict(color="#3498db", size=13)
        ),
        dict(
            type="buttons",
            showactive=False,
            x=1.0,
            xanchor="right",
            y=1.15,
            yanchor="top",
            buttons=buttons,
            direction="down",
            pad={"r": 10, "t": 10},
            bgcolor="white",
            bordercolor="#3498db",
            borderwidth=1,
            font=dict(color="#3498db", size=12)
        )
    ]
)

fig.write_html("student_navigator.html")
print("Saved as 'student_navigator.html' — open in your browser!")
fig.show()