import streamlit as st
import sqlite3
import pandas as pd

# -------------------------
# Database Connection
# -------------------------

conn = sqlite3.connect("students.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    gender TEXT,
    course TEXT,
    marks REAL
)
""")

conn.commit()


# -------------------------
# Functions
# -------------------------

def add_student(name, age, gender, course, marks):
    cursor.execute(
        "INSERT INTO students(name,age,gender,course,marks) VALUES(?,?,?,?,?)",
        (name, age, gender, course, marks)
    )
    conn.commit()


def view_students():
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    return data


def update_student(student_id, name, age, gender, course, marks):
    cursor.execute("""
        UPDATE students
        SET name=?, age=?, gender=?, course=?, marks=?
        WHERE id=?
    """, (name, age, gender, course, marks, student_id))
    conn.commit()


def delete_student(student_id):
    cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
    conn.commit()


# -------------------------
# Streamlit UI
# -------------------------

st.set_page_config(
    page_title="Student Record Management System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Student Record Management System")

menu = [
    "Home",
    "Add Student",
    "View Students",
    "Update Student",
    "Delete Student"
]

choice = st.sidebar.selectbox("Menu", menu)

# -------------------------
# Home
# -------------------------

if choice == "Home":

    st.subheader("Dashboard")

    data = view_students()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Name",
            "Age",
            "Gender",
            "Course",
            "Marks"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Students", len(df))

    with col2:
        if len(df) > 0:
            st.metric(
                "Average Marks",
                round(df["Marks"].mean(), 2)
            )
        else:
            st.metric("Average Marks", 0)

    st.write(df)

# -------------------------
# Add Student
# -------------------------

elif choice == "Add Student":

    st.subheader("Add Student")

    name = st.text_input("Student Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=100,
        value=18
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    course = st.text_input("Course")

    marks = st.number_input(
        "Marks",
        min_value=0.0,
        max_value=100.0
    )

    if st.button("Add Student"):

        if name != "" and course != "":

            add_student(
                name,
                age,
                gender,
                course,
                marks
            )

            st.success("Student Added Successfully!")

        else:
            st.error("Please fill all fields.")

# -------------------------
# View Students
# -------------------------

elif choice == "View Students":

    st.subheader("Student Records")

    data = view_students()

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Name",
            "Age",
            "Gender",
            "Course",
            "Marks"
        ]
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        csv,
        "students.csv",
        "text/csv"
    )

# -------------------------
# Update Student
# -------------------------

elif choice == "Update Student":

    st.subheader("Update Student")

    data = view_students()

    if len(data) == 0:

        st.warning("No students available.")

    else:

        ids = [i[0] for i in data]

        selected_id = st.selectbox(
            "Select Student ID",
            ids
        )

        selected = None

        for row in data:
            if row[0] == selected_id:
                selected = row
                break

        name = st.text_input(
            "Name",
            value=selected[1]
        )

        age = st.number_input(
            "Age",
            value=selected[2]
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(selected[3])
        )

        course = st.text_input(
            "Course",
            value=selected[4]
        )

        marks = st.number_input(
            "Marks",
            value=float(selected[5])
        )

        if st.button("Update"):

            update_student(
                selected_id,
                name,
                age,
                gender,
                course,
                marks
            )

            st.success("Student Updated Successfully!")

# -------------------------
# Delete Student
# -------------------------

elif choice == "Delete Student":

    st.subheader("Delete Student")

    data = view_students()

    if len(data) == 0:

        st.warning("No records found.")

    else:

        ids = [i[0] for i in data]

        selected = st.selectbox(
            "Select Student ID",
            ids
        )

        if st.button("Delete Student"):

            delete_student(selected)

            st.success("Student Deleted Successfully!")
