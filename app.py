# app.py
import streamlit as st
import pandas as pd
from pathlib import Path

# =========================================================
#                   BASIC SETTINGS
# =========================================================
st.set_page_config(
    page_title="Student Weekly Report",
    page_icon="📄",
    layout="wide",
)

DATA_FILE = Path("student_weekly_reports.csv")

# ---------------------------------------------------------
#               DATA LOAD / SAVE HELPERS
# ---------------------------------------------------------
COLUMNS = [
    "Student_ID",
    "Student_Name",
    "Class",
    "Term",
    "Arabic",
    "Arabic_Comment",
    "English",
    "English_Comment",
    "Math",
    "Math_Comment",
    "Science",
    "Science_Comment",
    "Islamic",
    "Islamic_Comment",
    "Social_Studies",
    "Social_Studies_Comment",
    "Overall_Comment",
]


def load_data() -> pd.DataFrame:
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE, dtype=str)
    else:
        df = pd.DataFrame(columns=COLUMNS)
    # ensure all columns exist
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = ""
    return df


def save_data(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)


df = load_data()

# =========================================================
#                       GLOBAL CSS
# =========================================================
st.markdown(
    """
<style>

/* ---------- Top spacing for main content ---------- */
section.main > div:first-child {
    padding-top: 3.5rem !important;
}

/* ---------- Big emoji header ---------- */
.big-header-emoji {
    text-align: center;
    font-size: 64px;
    margin-top: 0.5rem;
    margin-bottom: 0.2rem;
}

/* ---------- Headings ---------- */
h1 {
    color: #00692F !important;   /* UAE green */
    font-weight: 800 !important;
}
h2, h3, h4, h5, h6 {
    color: #222222 !important;
}

/* ---------- Sidebar text on dark background ---------- */
[data-testid="stSidebar"] * {
    color: #F5F5F5 !important;
    font-size: 16px;
}
[data-testid="stSidebar"] label {
    font-weight: 600 !important;
}

/* ---------- Input / textarea styling ---------- */
.stTextInput > div > div > input,
.stNumberInput > div > div > input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 10px !important;
    border: 1px solid #CCCCCC !important;
    padding: 10px !important;
    font-size: 16px !important;
}

.stTextArea textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 10px !important;
    border: 1px solid #CCCCCC !important;
    padding: 12px !important;
    font-size: 16px !important;
}

/* ---------- Input labels ---------- */
.stTextInput label,
.stTextArea label,
.stNumberInput label {
    color: #222222 !important;
    font-size: 17px !important;
    font-weight: 600 !important;
}

/* ---------- Buttons (Search, Save) ---------- */
.stButton > button {
    background-color: #FF5C5C !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 999px !important;
    padding: 0.6rem 2.3rem !important;
    font-size: 17px !important;
    font-weight: 600 !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    background-color: #E14A4A !important;
    color: #FFFFFF !important;
}

.stButton > button:active {
    background-color: #C63F3F !important;
    color: #FFFFFF !important;
    transform: translateY(1px);
}

.stButton > button:focus:not(:active) {
    box-shadow: 0 0 0 0.12rem rgba(255, 92, 92, 0.35) !important;
    outline: none !important;
}

</style>
""",
    unsafe_allow_html=True,
)

# =========================================================
#                     HEADER COMPONENT
# =========================================================
def render_header():
    # Big emoji line
    st.markdown('<div class="big-header-emoji">📄 💯 📄</div>', unsafe_allow_html=True)

    # Main title + Arabic subtitle
    st.markdown(
        """
    <h1 style="text-align:center;">Student Weekly Report</h1>
    <h2 style="text-align:center; color:#C8102E; margin-top:0.4rem;">
        تقرير أسبوعي ملون للطالب
    </h2>
    """,
        unsafe_allow_html=True,
    )


# =========================================================
#                     PARENT VIEW
# =========================================================
def parent_view(df: pd.DataFrame):
    render_header()

    # Instructions
    st.markdown(
        """
    <div style="text-align:center; font-size:20px; margin-top:1rem;">
        <p style="margin:4px 0;">
            Enter your child's student ID below to search for their report
        </p>
        <p style="margin:4px 0; direction:rtl;">
            أدخل رقم الطالب الخاص بطفلك أدناه للبحث عن تقريره
        </p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Search input + button
    st.write("")  # small spacer
    student_id = st.text_input("Enter Student ID / أدخل رقم الطالب", key="parent_search_id")
    col_center = st.columns([1, 1, 1])[1]
    with col_center:
        search_clicked = st.button("🔍 Search / بحث")

    st.write("")

    if search_clicked:
        sid = student_id.strip()
        if not sid:
            st.warning("Please enter a Student ID.")
            return

        mask = df["Student_ID"].astype(str) == sid
        if not mask.any():
            st.error("No report found for this Student ID.")
            return

        row = df[mask].iloc[0]

        # Simple card-style report
        st.markdown("---")
        st.markdown(
            f"""
        <div style="padding:1.5rem 2rem; border-radius:16px;
                    background-color:#ffffff; border:1px solid #e0e0e0;">
            <h3 style="margin-top:0;">📚 Student report</h3>
            <p><b>Student ID:</b> {row['Student_ID']}</p>
            <p><b>Name:</b> {row['Student_Name']}</p>
            <p><b>Class:</b> {row['Class']}</p>
            <p><b>Term / Week:</b> {row['Term']}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        def subject_block(title_en, mark, comment):
            st.markdown(
                f"""
            <div style="padding:1rem 1.5rem; border-radius:14px;
                        background-color:#F7F7F9; margin-top:0.8rem;">
                <h4 style="margin-top:0;">{title_en}</h4>
                <p><b>Mark:</b> {mark if mark else '-'}</p>
                <p><b>Comment:</b> {comment if comment else '-'}</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        subject_block("🇦🇪 Arabic", row["Arabic"], row["Arabic_Comment"])
        subject_block("🇬🇧 English", row["English"], row["English_Comment"])
        subject_block("🧮 Math", row["Math"], row["Math_Comment"])
        subject_block("🔬 Science", row["Science"], row["Science_Comment"])
        subject_block("🕌 Islamic", row["Islamic"], row["Islamic_Comment"])
        subject_block("🌍 Social Studies", row["Social_Studies"], row["Social_Studies_Comment"])

        st.markdown(
            f"""
        <div style="padding:1rem 1.5rem; border-radius:14px;
                    background-color:#FFF9E6; margin-top:0.8rem;">
            <h4 style="margin-top:0;">📝 Overall teacher comment</h4>
            <p>{row['Overall_Comment'] if row['Overall_Comment'] else '-'}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )


# =========================================================
#                     TEACHER VIEW
# =========================================================
def teacher_view(df: pd.DataFrame):
    render_header()

    # Blue label heading
    st.markdown(
        """
    <div style="display:inline-block; background-color:#1E64E6; color:white;
                padding:0.4rem 1.2rem; border-radius:4px; font-size:26px;
                margin-top:1.5rem; margin-bottom:0.5rem;">
        🖊️ Teacher entry form
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.write("")

    with st.form("teacher_form", clear_on_submit=False):
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            student_id = st.text_input("Student ID")
            student_name = st.text_input("Student name")
        with info_col2:
            student_class = st.text_input("Class")
            term = st.text_input("Term (e.g. T1 Week 3)")

        st.markdown("### 📊 Marks & comments")

        subjects = [
            ("Arabic", "🇦🇪 Arabic"),
            ("English", "🇬🇧 English"),
            ("Math", "🧮 Math"),
            ("Science", "🔬 Science"),
            ("Islamic", "🕌 Islamic"),
            ("Social_Studies", "🌍 Social Studies"),
        ]

        subject_values = {}

        for col_name, label in subjects:
            st.markdown(f"#### {label}")
            c_mark, c_comment = st.columns([1, 3])

            with c_mark:
                # use float to allow empty (NaN); will convert to text later
                mark = st.number_input(
                    "Mark",
                    min_value=0,
                    max_value=100,
                    step=1,
                    key=f"{col_name}_mark",
                )
            with c_comment:
                comment = st.text_area(
                    "Comment",
                    height=110,
                    key=f"{col_name}_comment",
                )

            subject_values[col_name] = str(mark)
            subject_values[f"{col_name}_Comment"] = comment

        st.markdown("### 💡 Overall teacher comment")
        overall_comment = st.text_area(
            "Overall comment for this week",
            height=130,
            key="overall_comment",
        )

        submitted = st.form_submit_button("💾 Save / Update report")

    if submitted:
        sid = student_id.strip()
        if not sid:
            st.error("Student ID is required.")
            return

        row_data = {
            "Student_ID": sid,
            "Student_Name": student_name,
            "Class": student_class,
            "Term": term,
            "Overall_Comment": overall_comment,
        }
        row_data.update(subject_values)

        # update or append
        mask = df["Student_ID"].astype(str) == sid
        if mask.any():
            df.loc[mask, list(row_data.keys())] = list(row_data.values())
            st.success("✅ Updated existing student report.")
        else:
            df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
            st.success("✅ Added new student report.")

        save_data(df)


# =========================================================
#                     SIDEBAR + ROUTING
# =========================================================
role = st.sidebar.radio("Who is using the app?", ["Parent", "Teacher"])

if role == "Parent":
    st.sidebar.markdown("### 👨‍👩‍👧 Parent view")
    st.sidebar.write("Enter a student ID to view the weekly report.")
    parent_view(df)
else:
    st.sidebar.markdown("### 🧑‍🏫 Teacher view")
    st.sidebar.write("Add or update a weekly report for a student.")
    teacher_view(df)
