# ============================================================
#  STUDENT GRADE ANALYSER
#  Built with: Python + Pandas + Matplotlib
#  Beginner-friendly project for IBM Data Science course
# ============================================================

# STEP 1: Import libraries
# pandas  → for working with data (like Excel in Python)
# matplotlib → for drawing charts and graphs
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

print("=" * 50)
print("   STUDENT GRADE ANALYSER")
print("=" * 50)


# ============================================================
# STEP 2: Create the dataset
# In a real project you'd do: df = pd.read_csv("students.csv")
# Here we create sample data manually using a dictionary
# ============================================================

df = pd.read_csv("students.csv")

print("\n--- Raw Student Data ---")
print(df.to_string(index=False))  # .to_string() makes it print nicely


# ============================================================
# STEP 3: Calculate total marks and average per student
# axis=1 means "go across each row" (i.e. per student)
# axis=0 would mean "go down each column" (i.e. per subject)
# ============================================================

subjects = ["Math", "Science", "English", "History"]
max_marks_per_subject = 100
total_subjects = len(subjects)

df["Total"]   = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1).round(2)
df["Percentage"] = ((df["Total"] / (max_marks_per_subject * total_subjects)) * 100).round(2)
df["Rank"] = df["Average"].rank(ascending=False).astype(int)

# ============================================================
# STEP 4: Assign letter grades based on percentage
# We use a function and apply it to every row
# ============================================================

def assign_grade(percentage):
    """
    Takes a percentage and returns a letter grade.
    This is called a 'function' — reusable block of code.
    """
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 40:
        return "D"
    else:
        return "F"   # Below 40% = Fail

# .apply() runs our function on every value in the "Percentage" column
df["Grade"] = df["Percentage"].apply(assign_grade)

# Pass / Fail column: pass if average >= 40 in all subjects
df["Result"] = df[subjects].apply(
    lambda row: "PASS" if row.min() >= 40 else "FAIL", axis=1
)


# ============================================================
# STEP 5: Print the full result table
# ============================================================

print("\n--- Full Results ---")
print(df[["Rank", "Name", "Total", "Average", "Percentage", "Grade", "Result"]].sort_values("Rank").to_string(index=False))


# ============================================================
# STEP 6: Summary statistics
# ============================================================

print("\n--- Class Summary ---")

# Who scored highest?
topper = df.loc[df["Average"].idxmax()]
print(f"Class Topper  : {topper['Name']} ({topper['Average']}% avg)")

# Who scored lowest?
lowest = df.loc[df["Average"].idxmin()]
print(f"Lowest Score  : {lowest['Name']} ({lowest['Average']}% avg)")

# Class average
print(f"Class Average : {df['Average'].mean().round(2)}%")

# Count pass/fail
pass_count = (df["Result"] == "PASS").sum()
fail_count = (df["Result"] == "FAIL").sum()
print(f"Passed        : {pass_count} students")
print(f"Failed        : {fail_count} students")

# Subject averages
print("\n--- Subject-wise Class Average ---")
for subject in subjects:
    avg = df[subject].mean().round(2)
    print(f"  {subject:<10}: {avg}")


# ============================================================
# STEP 7: Top 3 and Bottom 3 students
# ============================================================

print("\n--- Top 3 Students ---")
top3 = df.nlargest(3, "Average")[["Name", "Average", "Grade"]]
print(top3.to_string(index=False))

print("\n--- Bottom 3 Students ---")
bottom3 = df.nsmallest(3, "Average")[["Name", "Average", "Grade"]]
print(bottom3.to_string(index=False))


# ============================================================
# STEP 8: Grade distribution
# ============================================================

print("\n--- Grade Distribution ---")
grade_counts = df["Grade"].value_counts().sort_index()
for grade, count in grade_counts.items():
    bar = "█" * count   # Simple text bar chart
    print(f"  {grade:<3}: {bar} ({count})")


# ============================================================
# STEP 9: Save results to a new CSV file
# ============================================================

output_file = "student_results.csv"
df.to_csv(output_file, index=False)
print(f"\nResults saved to '{output_file}'")


# ============================================================
# STEP 10: Draw charts using Matplotlib
# We create a figure with 4 different charts (subplots)
# fig, axes = plt.subplots(rows, cols) creates a grid of charts
# ============================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Student Grade Analyser — Visual Report", fontsize=16, fontweight="bold")

# ── Chart 1 (top-left): Average score per student (horizontal bar) ──
ax1 = axes[0, 0]
colors = ["#e74c3c" if g == "F" else "#2ecc71" if a >= 80 else "#3498db"
          for g, a in zip(df["Grade"], df["Average"])]
bars = ax1.barh(df["Name"], df["Average"], color=colors)
ax1.set_xlabel("Average Score (%)")
ax1.set_title("Average Score per Student")
ax1.axvline(x=40, color="red", linestyle="--", linewidth=1, label="Pass mark (40%)")
ax1.legend(fontsize=8)
ax1.set_xlim(0, 100)
# Add value labels on bars
for bar, val in zip(bars, df["Average"]):
    ax1.text(val + 0.5, bar.get_y() + bar.get_height() / 2,
             f"{val}%", va="center", fontsize=8)

# ── Chart 2 (top-right): Grade distribution (pie chart) ──
ax2 = axes[0, 1]
grade_colors = {"A+": "#2ecc71", "A": "#27ae60", "B": "#3498db",
                "C": "#f39c12", "D": "#e67e22", "F": "#e74c3c"}
pie_colors = [grade_colors.get(g, "#95a5a6") for g in grade_counts.index]
wedges, texts, autotexts = ax2.pie(
    grade_counts.values,
    labels=grade_counts.index,
    autopct="%1.0f%%",
    colors=pie_colors,
    startangle=90
)
ax2.set_title("Grade Distribution")

# ── Chart 3 (bottom-left): Subject-wise average (bar chart) ──
ax3 = axes[1, 0]
subject_avgs = df[subjects].mean().round(2)
subject_colors = ["#9b59b6", "#1abc9c", "#e67e22", "#e74c3c"]
bars3 = ax3.bar(subjects, subject_avgs, color=subject_colors, width=0.5)
ax3.set_ylabel("Class Average (%)")
ax3.set_title("Subject-wise Class Average")
ax3.set_ylim(0, 100)
ax3.axhline(y=40, color="red", linestyle="--", linewidth=1)
for bar, val in zip(bars3, subject_avgs):
    ax3.text(bar.get_x() + bar.get_width() / 2, val + 1,
             f"{val}%", ha="center", fontsize=9, fontweight="bold")

# ── Chart 4 (bottom-right): Pass vs Fail (donut chart) ──
ax4 = axes[1, 1]
pf_counts = df["Result"].value_counts()
pf_colors = ["#2ecc71", "#e74c3c"]
wedges4, texts4, auto4 = ax4.pie(
    pf_counts.values,
    labels=pf_counts.index,
    autopct="%1.0f%%",
    colors=pf_colors,
    startangle=90,
    wedgeprops={"width": 0.6}   # Makes it a donut by leaving a hole
)
ax4.set_title("Pass vs Fail")
# Add total in center of donut
ax4.text(0, 0, f"{len(df)}\nStudents", ha="center", va="center",
         fontsize=12, fontweight="bold")

plt.tight_layout()
plt.savefig("student_report.png", dpi=150, bbox_inches="tight")
print("Charts saved to 'student_report.png'")
plt.show()

print("\nProject complete! Check student_results.csv and student_report.png")
print("=" * 50)

# ============================================================
# BONUS: Subject-wise Topper (Aesthetic Display)
# ============================================================

subject_emojis = {
    "Math": "📐",
    "Science": "🔬",
    "English": "📖",
    "History": "🏛️"
}

print("\n")
print("╔══════════════════════════════════════════════╗")
print("║         🏆  SUBJECT-WISE TOPPERS  🏆          ║")
print("╚══════════════════════════════════════════════╝")

for subject in subjects:
    topper_idx = df[subject].idxmax()
    topper_name = df.loc[topper_idx, "Name"]
    topper_score = df.loc[topper_idx, subject]
    emoji = subject_emojis[subject]

    filled = int(topper_score / 5)
    bar = "█" * filled + "░" * (20 - filled)

    print(f"║                                              ║")
    print(f"║  {emoji}  {subject:<10}                            ║")
    print(f"║     🥇 {topper_name:<10} scored {topper_score}/100            ║")
    print(f"║     [{bar}] {topper_score}%  ║")

print(f"║                                              ║")
print("╚══════════════════════════════════════════════╝")
print()

# ============================================================
# BONUS: Student name search
# ============================================================
while True:
    print("\nEnter a student name to see their report (or type 'exit' to quit):")
    name = input("Name: ").strip().capitalize()

    if name == "Exit":
        print("Goodbye!")
        break

    match = df[df["Name"].str.capitalize() == name]

    if match.empty:
        print(f"No student found with the name '{name}'. Try again.")
    else:
        row = match.iloc[0]
        print("\n" + "=" * 40)
        print(f"  Report for {row['Name']}")
        print("=" * 40)
        print(f"  Math       : {row['Math']}")
        print(f"  Science    : {row['Science']}")
        print(f"  English    : {row['English']}")
        print(f"  History    : {row['History']}")
        print(f"  Total      : {row['Total']}")
        print(f"  Average    : {row['Average']}%")
        print(f"  Grade      : {row['Grade']}")
        print(f"  Result     : {row['Result']}")
        print(f"  Class Rank : {row['Rank']}")
        print("=" * 40)

# ============================================================
# BONUS: Student name search
# ============================================================

while True:
    print("\nEnter a student name to see their report (or type 'exit' to quit):")
    name = input("Name: ").strip().capitalize()

    if name == "Exit":
        print("Goodbye!")
        break

    # Search for the student in the dataframe
    match = df[df["Name"].str.capitalize() == name]

    if match.empty:
        print(f"No student found with the name '{name}'. Try again.")
    else:
        row = match.iloc[0]
        print("\n" + "=" * 40)
        print(f"  Report for {row['Name']}")
        print("=" * 40)
        print(f"  Math       : {row['Math']}")
        print(f"  Science    : {row['Science']}")
        print(f"  English    : {row['English']}")
        print(f"  History    : {row['History']}")
        print(f"  Total      : {row['Total']}")
        print(f"  Average    : {row['Average']}%")
        print(f"  Grade      : {row['Grade']}")
        print(f"  Result     : {row['Result']}")
        print(f"  Class Rank : {row['Rank']}")
        print("=" * 40)
        print("DEBUG: starting chart...")

        # ── Student vs Class Average Chart ──
        class_avgs = df[subjects].mean().round(2)
        student_scores = [row[subject] for subject in subjects]

        x = range(len(subjects))
        width = 0.35

        fig2, ax = plt.subplots(figsize=(8, 5))
        bars1 = ax.bar([i - width/2 for i in x], student_scores, width, label=row['Name'], color="#3498db", zorder=3)
        bars2 = ax.bar([i + width/2 for i in x], class_avgs, width, label="Class Average", color="#e67e22", zorder=3)

        # Add value labels on top of each bar
        for bar in bars1:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f"{bar.get_height():.0f}", ha="center", fontsize=9, color="#3498db", fontweight="bold")
        for bar in bars2:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f"{bar.get_height():.0f}", ha="center", fontsize=9, color="#e67e22", fontweight="bold")

        ax.set_xticks(list(x))
        ax.set_xticklabels(subjects)
        ax.set_ylabel("Marks")
        ax.set_ylim(0, 110)
        ax.set_title(f"{row['Name']} vs Class Average — Subject Breakdown", fontweight="bold")
        ax.legend()
        ax.grid(axis="y", linestyle="--", alpha=0.5, zorder=0)
        ax.axhline(y=40, color="red", linestyle="--", linewidth=1, label="Pass mark")
        plt.tight_layout()
        filename = f"E:/grade-analyser/{row['Name']}_vs_class.png"
        print(f"Saving chart to: {filename}")
        plt.savefig(filename, dpi=150, bbox_inches="tight")
        print(f"\nChart saved as '{row['Name']}_vs_class.png'")
        plt.show()
        
        