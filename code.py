# gpa_cgpa_comsats.py
import streamlit as st

# ------------------------------
# COMSATS Grading Scale Function
# ------------------------------
def grade_to_points(marks):
    if marks >= 85:
        return 4.00
    elif marks >= 80:
        return 3.67
    elif marks >= 75:
        return 3.33
    elif marks >= 70:
        return 3.00
    elif marks >= 65:
        return 2.67
    elif marks >= 60:
        return 2.33
    elif marks >= 55:
        return 2.00
    elif marks >= 50:
        return 1.67
    else:
        return 0.00

# ------------------------------
# GPA Calculation
# ------------------------------
def calculate_gpa(marks_list, credit_hours_list):
    total_points = 0
    total_credits = 0
    for marks, credit in zip(marks_list, credit_hours_list):
        grade_point = grade_to_points(marks)
        total_points += grade_point * credit
        total_credits += credit
    if total_credits == 0:
        return 0.0
    return round(total_points / total_credits, 2)

# ------------------------------
# Streamlit App UI
# ------------------------------
st.title("🎓 COMSATS GPA & CGPA Calculator")
st.write("Calculate your semester-wise GPA and overall CGPA according to COMSATS University rules.")

# Step 1: Number of semesters
num_semesters = st.number_input("Enter number of semesters:", min_value=1, step=1)

semester_gpas = []
semester_credits = []

# Step 2: Loop through semesters
for sem in range(1, num_semesters + 1):
    st.header(f"📘 Semester {sem}")
    num_subjects = st.number_input(f"Enter number of subjects for Semester {sem}:", min_value=1, step=1, key=f"subcount_{sem}")

    marks_list = []
    credit_hours_list = []

    # Step 3: Loop through subjects
    for subj in range(1, num_subjects + 1):
        st.subheader(f"Subject {subj}")
        marks = st.number_input(f"Enter marks for Subject {subj}:", min_value=0, max_value=100, key=f"marks_{sem}_{subj}")
        credit = st.number_input(f"Enter credit hours for Subject {subj}:", min_value=1.0, max_value=5.0, step=0.5, key=f"credit_{sem}_{subj}")
        marks_list.append(marks)
        credit_hours_list.append(credit)

    # Step 4: GPA for this semester
    if st.button(f"Calculate GPA for Semester {sem}", key=f"calc_{sem}"):
        gpa = calculate_gpa(marks_list, credit_hours_list)
        semester_gpas.append(gpa)
        semester_credits.append(sum(credit_hours_list))
        st.success(f"🎯 GPA for Semester {sem}: **{gpa}**")

# Step 5: CGPA calculation (if all semesters completed)
if len(semester_gpas) > 0:
    total_points = sum(g * c for g, c in zip(semester_gpas, semester_credits))
    total_credits = sum(semester_credits)
    cgpa = round(total_points / total_credits, 2)
    st.markdown("---")
    st.subheader(f"🏅 Overall CGPA till current semester: **{cgpa}**")

    # Degree classification
    if cgpa >= 3.5:
        division = "Distinction"
    elif cgpa >= 3.0:
        division = "First Division"
    elif cgpa >= 2.5:
        division = "Second Division"
    elif cgpa >= 2.0:
        division = "Third Division (Pass)"
    else:
        division = "Below Passing"

    st.info(f"🎓 Classification: **{division}**")
