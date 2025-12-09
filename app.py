import streamlit as st
import pandas as pd
from pathlib import Path

# ---------- Data file ----------
DATA_FILE = Path("marks.xlsx")

def load_data():
    """Load marks or create empty file with correct columns."""
    if DATA_FILE.exists():
        return pd.read_excel(DATA_FILE)
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

# ---------- Page config & styles ----------
st.set_page_config(
    page_title="Student Weekly Report",
    layout="centered",
)

PRIMARY = "#00732F"   # UAE green
ACCENT = "#CE1126"    # UAE red
GOLD   = "#B88900"    # gold accent

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #F7F7F7;
        font-family: "Segoe UI", sans-serif;
    }}
    .main-title {{
        font-size: 32px;
        font-weight: 700;
        color: {PRIMARY};
        text-align: center;
        margin-bottom: 0.2rem;
    }}
    .sub-title {{
        text-align:center;
        color:#555;
        margin-bottom:1.2rem;
    }}
    .card {{
        background-color: white;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-top: 5px solid {GOLD};
    }}
    .subject-row {{
        margin-top:0.4rem;
        padding:0.5rem 0.7rem;
        border-radius:8px;
        background: #FAFAFA;
        border-left:4px solid {PRIMARY};
    }}
    .subject-name {{
        font-weight:600;
    }}
    .comment-label {{
        color:#666;
        font-size: 0.85rem;
        margin-top:0.2rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Student Weekly Report 🇦🇪</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">تقرير أسبوعي للطالب</div>', unsafe_allow_html=True)

mode = st.sidebar.radio("Who is using the app?", ["Parent", "Teacher"])

df = load_data()

# ---------- Parent view ----------
if mode == "Parent":
    st.sidebar.markdown("### 👨‍👩‍👧 Parent view")
    st.sidebar.write("Enter your child’s ID to view the report.")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    student_id = st.text_input("Enter Student ID / أدخل رقم الطالب", key="parent_id")

    if st.button("🔍 Search / بحث", type="primary"):
        sid = student_id.strip()
        if not sid:
            st.warning("Please enter a Student ID.")
        else:
            match = df[df["Student_ID"].astype(str) == sid]
            if match.empty:
                st.error("No report found for this Student ID.")
            else:
                row = match.iloc[0]

                # Basic info
                st.markdown(
                    f"""
                    **Student:** {row['Student_Name']}  
                    **ID:** {row['Student_ID']}  
                    **Class:** {row['Class']}  
                    **Term:** {row['Term']}
                    """
                )

                st.markdown("---")
                st.markdown("### Subjects & teacher comments")

                def subject_block(sub, mark_col, comm_col):
                    mark = row.get(mark_col, "")
                    comm = row.get(comm_col, "")
                    st.markdown(
                        f"""
                        <div class="subject-row">
                          <span class="subject-name">{sub}</span> — 
                          <b>{mark}</b>
                          <div class="comment-label">Teacher comment:</div>
                          <div>{comm if comm else "<i>No comment</i>"}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                subject_block("Arabic / العربية",       "Arabic",       "Arabic_Comment")
                subject_block("English / الإنجليزية",   "English",      "English_Comment")
                subject_block("Math / الرياضيات",       "Math",         "Math_Comment")
                subject_block("Science / العلوم",       "Science",      "Science_Comment")
                subject_block("Islamic / التربية الإسلامية", "Islamic", "Islamic_Comment")
                subject_block("Social Studies / الدراسات الاجتماعية",
                              "Social_Studies", "Social_Studies_Comment")

                st.markdown("---")
                st.markdown("### Overall teacher comment")
                st.write(row.get("Overall_Comment", ""))

                # Simple CSV download
                csv = match.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download this report (CSV)",
                    csv,
                    file_name=f"report_{row['Student_ID']}.csv",
                    mime="text/csv",
                )

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Teacher view ----------
else:
    st.sidebar.markdown("### 👩‍🏫 Teacher view")
    st.sidebar.write("Add or update a weekly report.")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Teacher entry form")

    with st.form("teacher_form", clear_on_submit=False):
        student_id = st.text_input("Student ID", key="t_id")
        student_name = st.text_input("Student name", key="t_name")
        student_class = st.text_input("Class", key="t_class")
        term = st.text_input("Term (e.g. T1 Week 3)", key="t_term")

        st.markdown("#### Marks")
        arabic      = st.text_input("Arabic", key="t_ar")
        english     = st.text_input("English", key="t_en")
        math        = st.text_input("Math", key="t_ma")
        science     = st.text_input("Science", key="t_sc")
        islamic     = st.text_input("Islamic", key="t_is")
        social      = st.text_input("Social Studies", key="t_ss")

        st.markdown("#### Comments")
        arabic_c    = st.text_area("Arabic comment", key="t_arc")
        english_c   = st.text_area("English comment", key="t_enc")
        math_c      = st.text_area("Math comment", key="t_mac")
        science_c   = st.text_area("Science comment", key="t_scc")
        islamic_c   = st.text_area("Islamic comment", key="t_isc")
        social_c    = st.text_area("Social Studies comment", key="t_ssc")
        overall_c   = st.text_area("Overall comment", key="t_oc")

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
                st.success("✅ Updated existing student report.")
            else:
                df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
                st.success("✅ Added new student report.")

            save_data(df)

    st.markdown('</div>', unsafe_allow_html=True)
