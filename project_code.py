from pathlib import Path

import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATA_PATH = BASE_DIR / "data" / "raw" / "02_student_performance_cleaned_550.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

SUBJECTS = [
    "Python_Marks",
    "Maths_Marks",
    "DBMS_Marks",
    "Web_Tech_Marks",
    "Statistics_Marks"]
REQUIRED_COLUMNS = [
    "Student_ID",
    "Student_Name",
    "Department",
    "Attendance_Pct",
    "Study_Hours_Per_Week",
    "Internet_Access",
    *SUBJECTS,
]


def load_data(file_path):
    """Read the CSV and keep the first 550 records."""
    data = pd.read_csv(file_path)
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in data.columns]
    if missing_columns:
        raise ValueError(f"CSV is missing required columns: {', '.join(missing_columns)}")
    data = data.head(550).copy()
    return data


def assign_grade(average):
    """Assign grades using the agreed strict 'above' thresholds."""
    if average > 95:
        return "A+"
    elif average > 90:
        return "A"
    elif average > 85:
        return "B+"
    elif average > 80:
        return "B"
    elif average > 75:
        return "C+"
    elif average > 70:
        return "C"
    elif average > 65:
        return "D+"
    elif average > 60:
        return "D"
    else:
        return "F"


def add_student_results(data):
    """Calculate each student's total, average and grade."""
    result = data.copy()
    result["Total_Marks"] = result[SUBJECTS].sum(axis=1)
    result["Average_Marks"] = result[SUBJECTS].mean(axis=1)
    result["Grade"] = result["Average_Marks"].apply(assign_grade)
    return result


def attendance_analysis(data):
    """Compare average marks in the attendance bands chosen by the student."""
    result = data.copy()
    result["Attendance_Band"] = pd.cut(
        result["Attendance_Pct"],
        bins=[-np.inf, 75, 90, np.inf],
        labels=["Low (<75%)", "Medium (75% to <90%)", "High (90%+)"] ,
        right=False,
    )
    return result.groupby("Attendance_Band", observed=False).agg(
        Student_Count=("Student_ID", "count"),
        Average_Marks=("Average_Marks", "mean"),
        Average_Attendance=("Attendance_Pct", "mean"),
    ).round(2)


def study_hours_analysis(data):
    """Measure the relationship and summarize study hours without arbitrary bands."""
    correlation = data["Study_Hours_Per_Week"].corr(data["Average_Marks"])
    print("\nSTUDY HOURS ANALYSIS")
    print("Correlation between study hours and average marks:", round(correlation, 3))
    print("A positive value means the two tend to increase together; correlation does not prove causation.")

    summary = data["Study_Hours_Per_Week"].describe().round(2).to_frame("Study_Hours_Per_Week")
    print("\nStudy-hours summary:")
    print(summary)
    return summary


def python_mark_statistics(data):
    """Calculate Python mark statistics using NumPy."""
    marks = data["Python_Marks"].dropna().to_numpy()
    q1, median, q3 = np.percentile(marks, [25, 50, 75])
    print("\nPYTHON MARK STATISTICS (NumPy)")
    print("Median:", round(float(median), 2))
    print("Standard deviation (sample, ddof=1):", round(float(np.std(marks, ddof=1)), 2))
    print("Q1:", round(float(q1), 2))
    print("Q2 (median):", round(float(median), 2))
    print("Q3:", round(float(q3), 2))

    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outliers = data[(data["Python_Marks"] < lower_fence) |
                    (data["Python_Marks"] > upper_fence)]
    print("IQR lower fence:", round(float(lower_fence), 2))
    print("IQR upper fence:", round(float(upper_fence), 2))
    print("Potential Python-mark outliers:")
    if outliers.empty:
        print("None")
    else:
        print(outliers[["Student_ID", "Student_Name", "Python_Marks"]].to_string(index=False))


def make_recommendations(data, department_summary, internet_summary):
    """Print five recommendations tied to the calculated results."""
    low_attendance = data[data["Attendance_Pct"] < 75]
    low_average = data[data["Average_Marks"] < 40]
    study_correlation = data["Study_Hours_Per_Week"].corr(data["Average_Marks"])

    print("\nRECOMMENDATIONS")
    print("1. Arrange individual academic support for the", len(low_average),
          "students with an average below 40%.")
    print("2. Contact students in the low-attendance band (below 75%);",
          len(low_attendance), "students are currently in this band, including missing attendance recorded as 0%.")
    if study_correlation > 0:
        print("3. Encourage structured weekly study plans; study hours and marks show a positive correlation.")
    elif study_correlation < 0:
        print("3. Review study methods and workload; more reported study hours are not associated with higher marks in this data.")
    else:
        print("3. Review study habits with students; this dataset shows little linear relationship between study hours and marks.")

    if len(internet_summary) == 2 and internet_summary["Average_Marks"].nunique() > 1:
        higher_access = internet_summary["Average_Marks"].idxmax()
        print("4. Compare learning support for students with and without internet access; the higher average is in the",
              str(higher_access), "group. Consider access support if needed.")
    else:
        print("4. Review internet access needs and ensure students can use equivalent learning resources.")

    lowest_department = department_summary["Average_Marks"].idxmin()
    print("5. Review subject-level support in", lowest_department,
          "which has the lowest department average in this sample.")


def save_reports(results, grade_distribution, department_summary, at_risk,
                 attendance_summary, study_summary):
    """Write generated reports under the project directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    grade_distribution.to_csv(OUTPUT_DIR / "grade_distribution.csv", index=False)
    department_summary.to_csv(OUTPUT_DIR / "department_summary.csv")
    at_risk.to_csv(OUTPUT_DIR / "at_risk_students.csv", index=False)
    attendance_summary.to_csv(OUTPUT_DIR / "attendance_summary.csv")
    study_summary.to_csv(OUTPUT_DIR / "study_hours_summary.csv")
    results.to_csv(OUTPUT_DIR / "cleaned_student_performance_550.csv", index=False)


def show_top_students(top_ten):
    """Print the students with the highest average marks."""
    print("\nTOP 10 STUDENTS BY AVERAGE MARKS")
    print(top_ten[
        ["Student_ID", "Student_Name", "Department", "Average_Marks", "Grade"]
    ].to_string(index=False))


def show_at_risk_students(at_risk):
    """Print students whose average marks are below 40%."""
    print("\nSTUDENTS BELOW 40% AVERAGE (AT RISK)")
    if at_risk.empty:
        print("No students are below the 40% threshold.")
        return
    print(at_risk[
        ["Student_ID", "Student_Name", "Department", "Average_Marks", "Grade"]
    ].to_string(index=False))


def show_group_comparisons(grade_distribution, department_summary,
                           attendance_summary, internet_summary):
    """Print grade counts and group performance comparisons."""
    print("\nGRADE DISTRIBUTION")
    print(grade_distribution.to_string(index=False))
    print("\nAVERAGE MARKS BY DEPARTMENT")
    print(department_summary)
    print("\nAVERAGE MARKS BY ATTENDANCE BAND")
    print(attendance_summary)
    print("\nAVERAGE MARKS BY INTERNET ACCESS")
    print(internet_summary)


def main():
    file_path = input(
        "Enter cleaned CSV path (default: data/raw/02_student_performance_cleaned_550.csv): "
    ).strip()
    selected_file = Path(file_path).expanduser() if file_path else DEFAULT_DATA_PATH

    original = load_data(selected_file)
    results = add_student_results(original)

    grade_distribution = results["Grade"].value_counts().reindex(
        ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"], fill_value=0
    ).rename_axis("Grade").reset_index(name="Student_Count")
    department_summary = results.groupby("Department").agg(
        Student_Count=("Student_ID", "count"),
        Average_Marks=("Average_Marks", "mean"),
    ).sort_values("Average_Marks", ascending=False).round(2)
    top_ten = results.nlargest(10, "Average_Marks")
    at_risk = results[results["Average_Marks"] < 40].sort_values("Average_Marks")
    attendance_summary = attendance_analysis(results)
    internet_summary = results.groupby("Internet_Access").agg(
        Student_Count=("Student_ID", "count"),
        Average_Marks=("Average_Marks", "mean"),
    ).round(2)

    print(f"\nLoaded {len(results)} student records.")
    while True:
        print("\n===== Student Performance Analytics =====")
        print("1. Show top 10 students")
        print("2. Show students below 40% average")
        print("3. Compare grades, departments and student groups")
        print("4. Show statistics and recommendations")
        print("5. Save CSV reports")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            show_top_students(top_ten)
        elif choice == "2":
            show_at_risk_students(at_risk)
        elif choice == "3":
            show_group_comparisons(
                grade_distribution,
                department_summary,
                attendance_summary,
                internet_summary,
            )
        elif choice == "4":
            study_hours_analysis(results)
            python_mark_statistics(results)
            make_recommendations(results, department_summary, internet_summary)
        elif choice == "5":
            study_summary = results["Study_Hours_Per_Week"].describe().round(2).to_frame(
                "Study_Hours_Per_Week"
            )
            save_reports(
                results,
                grade_distribution,
                department_summary,
                at_risk,
                attendance_summary,
                study_summary,
            )
            print(f"Saved CSV reports in {OUTPUT_DIR.relative_to(BASE_DIR)}.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
