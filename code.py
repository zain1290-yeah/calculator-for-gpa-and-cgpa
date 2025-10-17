# comsats_gpa_cgpa_calculator.py
import streamlit as st
import pandas as pd

# ------------------------------
# COMSATS Grading Scale
# ------------------------------
def grade_to_points(marks):
    if marks >= 85:
        return 4.00, "A"
    elif marks >= 80:
        return 3.67, "A–"
    elif marks >= 75:
        return 3.33, "B+"
    elif marks >= 70:
        return 3.00, "B"
    elif marks >= 65:
        return 2.67, "B–"
    elif marks >= 60:
        return 2.33, "C+"
    elif marks >= 55:
        return 2.00, "C"
    elif marks >= 50:
        return 1.67, "C–"
    else:
        return 0.00, "F"

# ------------------------------
# GPA Calculation
# ------------------------------
def calculate_gpa(marks_list, credit_hours_list):
    total_points = 0
    total_credits = 0
    subject_data = []

    for marks, credit in zip(marks_list, credit_hours_list):
        grade_point, letter_grade = grade_to_points(marks)
        subject_gpa = round(grade_point, 2)
        total_points += grade_point * credit
        total_credits += credit
        subject_data.append({
            "Marks": marks,
            "Credit Hours": credit,
            "Grade": letter_grade,
            "Grade Points": grade_point
        })

    semester_gpa = round(total_points / total_credits, 2) if total_credits > 0 else 0.0
    return semester_gpa, subject_data

# ------------------------------
# Streamlit App Interface
# ------------------------------
st.set_page_config(page_title="COMSATS GPA & CGPA Calculator", layout="wide")
st.title("🎓 COMSATS GPA & CGPA Calculator")
st.markdown("Calculate **subject-wise GPA**, **semester GPA**, and **overall CGPA** according to COMSATS grading policy.")

# Step 1: Number of semesters
num_semesters = st.number_input("Enter number of semesters:", min_value=1, step=1)

semester_results = []  # to store semester GPAs and credits

# Step 2: Loop through semesters
for sem in range(1, num_semesters + 1):
    st.markdown(f"## 📘 Semester {sem}")
    num_subjects = st.number_input(f"Number of subjects in Semester {sem}:", min_value=1, step=1, key=f"subs_{sem}")

    marks_list, credit_list = [], []

    for subj in range(1, num_subjects + 1):
        cols = st.columns(2)
        with cols[0]:
            marks = st.number_input(f"Marks for Subject {subj}", 0, 100, key=f"m_{sem}_{subj}")
        with cols[1]:
            credit = st.number_input(f"Credit hours for Subject {subj}", 1.0, 5.0, 3.0, 0.5, key=f"c_{sem}_{subj}")
        marks_list.append(marks)
        credit_list.append(credit)

    if st.button(f"Calculate Semester {sem} GPA", key=f"calc_{sem}"):
        sem_gpa, subject_data = calculate_gpa(marks_list, credit_list)
        semester_results.append({"gpa": sem_gpa, "credits": sum(credit_list)})

        df = pd.DataFrame(subject_data)
        st.subheader(f"📄 Subject-wise Grades (Semester {sem})")
        st.dataframe(df, use_container_width=True)

        st.success(f"🎯 GPA for Semester {sem}: **{sem_gpa}**")

# Step 3: Calculate CGPA after all semesters
if len(semester_results) > 0:
    total_points = sum(s["gpa"] * s["credits"] for s in semester_results)
    total_credits = sum(s["credits"] for s in semester_results)
    overall_cgpa = round(total_points / total_credits, 2)

    st.markdown("---")
    st.header(f"🏅 Overall CGPA till Current Semester: **{overall_cgpa}**")

    if overall_cgpa >= 3.5:
        division = "Distinction"
    elif overall_cgpa >= 3.0:
        division = "First Division"
    elif overall_cgpa >= 2.5:
        division = "Second Division"
    elif overall_cgpa >= 2.0:
        division = "Third Division (Pass)"
    else:
        division = "Below Passing"

    st.info(f"🎓 Classification: **{division}**")
