import streamlit as st
import pandas as pd
import os

# File path to store grades
data_file = "grades_data.csv"

# Function to load student data
def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    return pd.DataFrame()

# Function to save student data
def save_data(df):
    df.to_csv(data_file, index=False)

# App Title
st.title("Grade Viewer")

# Select View Mode
mode = st.sidebar.radio("Select View", ["Teacher", "Student"])

if mode == "Teacher":
    st.subheader("Teacher View")
    passcode = st.text_input("Enter Passcode", type="password")
    
    if passcode == "dee-grade-viewer":
        uploaded_file = st.file_uploader("Upload an Excel file", type=["xls", "xlsx"])
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            st.write("Uploaded Data:")
            st.dataframe(df)
            
            if "Student Name" in df.columns and "Email" in df.columns:
                course_subject = st.text_input("Enter Course Subject")
                if course_subject:
                    df.insert(0, "Course Subject", course_subject)
                    save_data(df)
                    st.success("Data saved successfully!")
                    st.dataframe(df)
                else:
                    st.warning("Please enter a course subject.")
            else:
                st.error("Excel file must contain 'Student Name' and 'Email' columns.")
    else:
        st.warning("Incorrect passcode!")

elif mode == "Student":
    st.subheader("Student View")
    df = load_data()
    if df.empty:
        st.warning("No data available. Teachers need to upload grades first.")
    else:
        student_name = st.text_input("Enter Student Name").strip()
        email = st.text_input("Enter Email").strip()
        if student_name and email:
            student_data = df[(df["Student Name"].str.strip().str.lower() == student_name.lower()) &
                              (df["Email"].astype(str).str.strip() == email)]
            if not student_data.empty:
                st.success("Grades Found!")
                st.dataframe(student_data.drop(columns=["Course Subject", "Student Name", "Email"]))
            else:
                st.error("No matching student found.")
