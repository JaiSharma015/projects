# Student Performance Analytics

A Python command-line tool for reviewing student marks, grades, attendance,
study hours, department, and internet access.

## Dataset

The included file `data/raw/02_student_performance_cleaned_550.csv` contains
550 student records. The program can also read another CSV with the same
required columns.

## Analysis

- Calculate each student's total marks, average, and grade.
- Compare grades and average marks by department, attendance band, and internet access.
- List the ten highest averages and students with averages below 40%.
- Summarize study hours and Python marks, including quartiles and possible IQR outliers.

Grades use strict cutoffs: A+ above 95, A above 90, B+ above 85, B above 80,
C+ above 75, C above 70, D+ above 65, D above 60, and F otherwise.
Attendance groups are below 75%, 75% to below 90%, and 90% or higher.

## Run

Install dependencies and start the program:

```bash
python -m pip install -r requirements.txt
python project_code.py
```

Press Enter at the file prompt to use the included dataset. The menu provides:

1. Top ten students
2. Students below 40% average
3. Grade, department, attendance, and internet-access comparisons
4. Statistics and recommendations
5. Save CSV reports
6. Exit

## Reports

Choose **Save CSV reports** to create files in `data/processed/`:

- `cleaned_student_performance_550.csv`
- `grade_distribution.csv`
- `department_summary.csv`
- `at_risk_students.csv`
- `attendance_summary.csv`
- `study_hours_summary.csv`

## Limitations

The program analyzes the first 550 rows. The results describe this dataset;
correlation does not establish that study hours cause changes in marks.

## Tools

Python 3, pandas, and NumPy.

## Author

Jai Sharma
