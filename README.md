# Student Performance Analytics

A Python command-line project that analyzes student marks and compares results
with attendance, study hours, department, and internet access.

## Problem

Reviewing student records one at a time makes it difficult to spot overall
performance patterns. This project calculates individual grades and summarizes
results across student groups.

## Questions answered

1. What are each student's total marks, average marks, and grade?
2. Which students have the highest averages or need academic support?
3. How do results compare by department, attendance, and internet access?
4. How are study hours related to marks, and what do Python-mark statistics show?

## Dataset

The included cleaned dataset is stored in `data/raw/`:

| File | Rows | Columns |
|---|---:|---|
| `02_student_performance_cleaned_550.csv` | 550 | Student details, attendance, study hours, internet access, and five subject marks |

The subject columns are `Python_Marks`, `Maths_Marks`, `DBMS_Marks`,
`Web_Tech_Marks`, and `Statistics_Marks`.

## Method

1. Read the selected CSV and analyze its first 550 rows.
2. Calculate each student's total marks, average marks, and grade.
3. Assign grades using strict cutoffs: A+ above 95, A above 90, B+ above 85,
   B above 80, C+ above 75, C above 70, D+ above 65, D above 60, and F otherwise.
4. Compare average marks by department, internet access, and attendance band:
   below 75%, 75% to below 90%, and 90% or higher.
5. Calculate the correlation between study hours and average marks.
6. Use NumPy to calculate Python-mark median, sample standard deviation,
   quartiles, and potential outliers using the 1.5 x IQR rule.

The input CSV is not changed. The processed student table is saved to
`data/processed/student_performance_processed.csv` when requested from the menu.

## Features

- Show the top 10 students by average marks
- List students with an average below 40%
- Compare grade distribution and group averages
- Show statistics and data-informed recommendations
- Save one processed CSV file

## Project structure

```text
student-performance-analytics/
|-- data/
|   |-- raw/          input CSV
|   `-- processed/    generated processed CSV
|-- project_code.py
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## How to run

Install the requirements and run the program:

```bash
python -m pip install -r requirements.txt
python project_code.py
```

Press Enter at the file prompt to use the included dataset. The menu is:

```text
1. Show top 10 students
2. Show students below 40% average
3. Compare grades, departments and student groups
4. Show statistics and recommendations
5. Save CSV reports
6. Exit
```

## Sample results

| Measure | Result |
|---|---:|
| Students analyzed | 550 |
| Students below 40% average | 17 |
| Python-mark median | 66 |
| Study-hours / average-marks correlation | 0.489 |
| Average marks, low attendance (<75%) | 58.41 |
| Average marks, medium attendance (75% to <90%) | 65.43 |
| Average marks, high attendance (90%+) | 69.62 |

## Key findings

- 212 of the 550 students received an F under the project's grade thresholds.
- The low-attendance group had a lower average than the medium- and
  high-attendance groups in this dataset.
- Students reporting internet access had a higher average (63.87) than those
  without access (58.90).
- Study hours and average marks had a positive correlation of 0.489. This does
  not show that study hours cause higher marks.
- Department averages ranged from 59.24 in Mechanical to 64.68 in CSE.

## Recommendations

- Prioritize individual academic support for the 17 students below a 40% average.
- Follow up with students in the low-attendance group.
- Review access to learning resources and subject-level support across departments.

## Limitations

The program analyzes the first 550 rows, which are not a random sample. Results
depend on the accuracy and preparation of the supplied records. Correlation
does not establish causation.

## Possible improvements

- Add charts to make group comparisons easier to interpret.
- Validate data ranges and missing values before analysis.
- Analyze a larger, representative dataset.

## Tools

Python 3, pandas, and NumPy.

## Author

Jai Sharma
