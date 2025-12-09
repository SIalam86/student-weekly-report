import streamlit as st
import pandas as pd
from pathlib import Path

DATA_FILE = Path("marks.xlsx")

# ---------- Data helpers ----------
def load_data():
    if DATA_FILE.exists():
        return pd.read_excel(DATA_FILE)
    else:
        cols = [
            "Student_ID", "Student_Name", "Class", "Term",
            "Arabic", "Arabic_Comment",
            "English", "English_Comment",
            "Math", "Math_Comment",
            "Science", "Science_Comment",
            "Islamic", "Islamic_Comment",
            "Social_Studies", "Social_Studies_Comment",
            "Overall_Comment",
        ]
        df = pd.DataFrame(columns=cols)
        df.to_excel(DATA_FILE, index=False)
        return df

def save_data(df: pd.DataFrame):
    df.to_excel(DATA_FILE, index=False)

# ---------- Streamlit basic setup ----------
st.set_page_config(page_title="Student Weekly Report", layout="centered")

st.title("Student Weekly Report 🇦🇪")
st.caption("تقرير أسبوعي للطالب")

mode = st.sidebar.radio("Who is using the app?", ["Parent", "Teacher"])

df = load_data()

# ---------- PARENT VIEW ----------
if mode == "Parent":
    st.subheader("👨‍👩‍👧 Parent view")
    st.write("Enter your child’s Student ID to view the report.")

    # >>> This is the IMPORTANT textbox <<<
    student_id = st.text_input("Enter Student ID / أدخل رقم الطالب")

    if st.button("🔍 Search / بحث"):
        sid = student_id.strip()
        if not sid:
            st.warning("Please enter a Student ID.")
        else:
            match = df[df["Student_ID"].astype(str) == sid]
            if match.empty:
                st.error("No report found for this Student ID.")
            else:
                row = match.iloc[0]

                st.markdown("### Student information")
                st.write(f"**Name:** {row['Student_Name']}")
                st.write(f"**ID:** {row['Student_ID']}")
                st.write(f"**Class:** {row['Class']}")
                st.write(f"**Term:** {row['Term']}")

                st.markdown("### Subjects & comments")

                def subject_block(sub, mcol, ccol):
                    st.write(f"**{sub}:** {row.get(mcol, '')}")
                    st.write(f"*Teacher comment:* {row.get(ccol, '')}")
                    st.divider()

                subject_block("Arabic", "Arabic", "Arabic_Comment")
                subject_block("English", "English", "English_Comment")
                subject_block("Math", "Math", "Math_Comment")
                subject_block("Science", "Science", "Science_Comment")
                subject_block("Islamic", "Islamic", "Islamic_Comment")
                subject_block("Social Studies", "Social_Studies", "Social_Studies_Comment")

                st.markdown("### Overall comment")
                st.write(row.get("Overall_Comment", ""))

# ---------- TEACHER VIEW ----------
else:
    st.subheader("👩‍🏫 Teacher view")
    st.write("Add or update a weekly report for a student.")

    with st.form("teacher_form", clear_on_submit=False):
        student_id = st.text_input("Student ID")
        student_name = st.text_input("Student name")
        student_class = st.text_input("Class")
        term = st.text_input("Term (e.g. T1 Week 3)")

        st.markdown("#### Marks")
        arabic  = st.text_input("Arabic")
        english = st.text_input("English")
        math    = st.text_input("Math")
        science = st.text_input("Science")
        islamic = st.text_input("Islamic")
        social  = st.text_input("Social Studies")

        st.markdown("#### Comments")
        arabic_c  = st.text_area("Arabic comment")
        english_c = st.text_area("English comment")
        math_c    = st.text_area("Math comment")
        science_c = st.text_area("Science comment")
        islamic_c = st.text_area("Islamic comment")
        social_c  = st.text_area("Social Studies comment")
        overall_c = st.text_area("Overall comment")

        submitted = st.form_submit_button("💾 Save / Update report")

    if submitted:
        sid = student_id.strip()
        if not sid:
            st.error("Student ID is required.")
        else:
            row_data = {
                "Student_ID": sid,
                "Student_Name": student_name,
                "Class": student_class,
                "Term": term,
                "Arabic": arabic,
                "Arabic_Comment": arabic_c,
                "English": english,
                "English_Comment": english_c,
                "Math": math,
                "Math_Comment": math_c,
                "Science": science,
                "Science_Comment": science_c,
                "Islamic": islamic,
                "Islamic_Comment": islamic_c,
                "Social_Studies": social,
                "Social_Studies_Comment": social_c,
                "Overall_Comment": overall_c,
            }

            mask = df["Student_ID"].astype(str) == sid
            if mask.any():
                df.loc[mask, list(row_data.keys())] = list(row_data.values())
                st.success("Updated existing student report.")
            else:
                df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
                st.success("Added new student report.")

            save_data(df)
