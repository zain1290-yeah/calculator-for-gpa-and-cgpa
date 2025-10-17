import streamlit as st

# Title of the app
st.title("📘 GPA & CGPA Calculator")
st.subheader("Enter your marks for 6 subjects (in percentage)")

# GPA conversion function
def percentage_to_gpa(percentage):
    if percentage >= 85:
        return 4.00
    elif percentage >= 75:
        return 3.66
    elif percentage >= 65:
        return 3.00
    elif percentage >= 60:
        return 2.50
    else:
        return 0.0

# Collect inputs
percentages = []
for i in range(1, 7):
    perc = st.number_input(f"Subject {i} (%)", min_value=0.0, max_value=100.0, step=0.1, key=f"subject_{i}")
    percentages.append(perc)

if st.button("Calculate GPA & CGPA"):
    gpas = [percentage_to_gpa(p) for p in percentages]
    cgpa = sum(gpas) / len(gpas)

    # Results
    st.markdown("### 📊 Results")
    for i, gpa in enumerate(gpas, 1):
        st.write(f"Subject {i} GPA: {gpa:.2f}")
    st.success(f"🎯 **Your CGPA is: {cgpa:.2f}**")

    if cgpa == 4.0:
        st.balloons()
        st.info("Excellent performance! Keep it up! 🎉")
    elif cgpa < 2.0:
        st.warning("You need to improve your grades. 🚨")

