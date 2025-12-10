import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------- Data helpers -----------------
DATA_FILE = Path("marks.xlsx")

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

# ----------------- Page config & styles -----------------
st.set_page_config(
    page_title="Student Weekly Report",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="expanded",
)

PRIMARY = "#00732F"   # UAE green
ACCENT = "#CE1126"    # UAE red
GOLD   = "#F4B400"    # playful gold
SOFT_BG = "#F8F9FB"

# Global, safe CSS (no position/z-index hacks)
st.markdown(
    f"""
    <style>
    .stApp {{
        background: radial-gradient(circle at top, #FFFFFF 0, {SOFT_BG} 55%, #ECEFF4 100%);
        font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
    }}
    .main-title {{
        font-size: 34px;
        font-weight: 800;
        color: {PRIMARY};
        text-align: center;
        margin-bottom: 0.3rem;
    }}
    .sub-title {{
        font-size: 34px;
        font-weight: 800;
        color: {ACCENT};
        text-align: center;
        margin-bottom: 0.3rem;
    }}
    .subject-chip {{
        display:inline-block;
        padding:0.15rem 0.7rem;
        border-radius:999px;
        background:{PRIMARY};
        color:white;
        font-size:0.85rem;
        font-weight:600;
        margin-bottom:0.3rem;
    }}
    .comment-label {{
        color:#777;
        font-size:0.82rem;
        margin-top:0.15rem;
    }}
    .divider-soft {{
        height:1px;
        background:linear-gradient(to right, transparent, #D0D7E2, transparent);
        margin:0.6rem 0 0.8rem 0;
    }}
    /* Make all text inputs white with rounded corners */
    .stTextInput > div > div > input {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #CCCCCC !important;
        border-radius: 10px !important;
        padding: 8px 10px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------- Header -----------------
st.markdown(
    """
    <div style='text-align:center; padding-top:10px;'>
        <span style="font-size:40px;">📑💯📑</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Removed “AE” here
st.markdown('<div class="main-title">Student Weekly Report</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">تقرير أسبوعي ملون للطالب</div>', unsafe_allow_html=True)

# ----------------- Side bar mode switch -----------------
mode = st.sidebar.radio("Who is using the app?", ["Parent", "Teacher"])
df = load_data()

# ======================================================================
#                               PARENT VIEW
# ======================================================================
if mode == "Parent":
    st.sidebar.markdown("### 👨‍👩‍👧 Parent view")
    st.sidebar.write("Enter your child’s ID to view the report.")

    st.markdown(
    """
    <div style="text-align:center; font-size:22px; margin-top:10px;">
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

    # --- centered icon above the search box ---
    ic1, ic2, ic3 = st.columns([1, 1, 1])
    with ic2:
        st.markdown(
            "<div style='text-align:center; font-size:45px; margin-bottom:10px;'>🔍</div>",
            unsafe_allow_html=True,
        )


    # --- full-width text box ---
    student_id = st.text_input(
        "Enter Student ID / أدخل رقم الطالب",
        placeholder="e.g., 20230045",
    )

    # --- centered Search button ---
    b1, b2, b3 = st.columns([1, 1, 1])
    with b2:
        search_clicked = st.button("🔍 Search / بحث", use_container_width=True)

    if search_clicked:
        sid = student_id.strip()
        if not sid:
            st.warning("Please enter a Student ID.")
        else:
            match = df[df["Student_ID"].astype(str) == sid]
            if match.empty:
                st.error("No report found for this Student ID.")
            else:
                row = match.iloc[0]

                st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
                st.markdown("### 🎓 Student information")

                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**Name:** {row['Student_Name']}")
                    st.write(f"**ID:** {row['Student_ID']}")
                with col2:
                    st.write(f"**Class:** {row['Class']}")
                    st.write(f"**Term:** {row['Term']}")

                st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)
                st.markdown("### 📚 Subjects & teacher notes")

                def subject_block(label, emoji, mcol, ccol):
                    mark = row.get(mcol, "")
                    comm = row.get(ccol, "")
                    st.markdown(
                        f"<div class='subject-chip'>{emoji} {label}</div>",
                        unsafe_allow_html=True,
                    )
                    st.write(f"**Mark:** {mark}")
                    st.markdown(
                        f"<div class='comment-label'>Teacher comment:</div>",
                        unsafe_allow_html=True,
                    )
                    st.write(comm if comm else "*No comment*")
                    st.markdown('<div class="divider-soft"></div>', unsafe_allow_html=True)

                subject_block("Arabic / العربية", "🕌", "Arabic", "Arabic_Comment")
                subject_block("English / الإنجليزية", "📖", "English", "English_Comment")
                subject_block("Math / الرياضيات", "🧮", "Math", "Math_Comment")
                subject_block("Science / العلوم", "🧪", "Science", "Science_Comment")
                subject_block("Islamic / التربية الإسلامية", "☪️", "Islamic", "Islamic_Comment")
                subject_block("Social Studies / الدراسات الاجتماعية", "🌍",
                               "Social_Studies", "Social_Studies_Comment")

                st.markdown("### 💡 Overall teacher comment")
                st.write(row.get("Overall_Comment", ""))

                csv = match.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download this report (CSV)",
                    csv,
                    file_name=f"report_{row['Student_ID']}.csv",
                    mime="text/csv",
                )

# ======================================================================
#                               TEACHER VIEW
# ======================================================================
else:
    st.sidebar.markdown("### 👩‍🏫 Teacher view")
    st.sidebar.write("Add or update a weekly report.")

    st.subheader("✏️ Teacher entry form")

    with st.form("teacher_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("Student ID")
            student_name = st.text_input("Student name")
        with col2:
            student_class = st.text_input("Class")
            term = st.text_input("Term (e.g. T1 Week 3)")

        st.markdown("#### 📊 Marks")
        c1, c2, c3 = st.columns(3)
        with c1:
            arabic  = st.text_input("Arabic")
            math    = st.text_input("Math")
        with c2:
            english = st.text_input("English")
            science = st.text_input("Science")
        with c3:
            islamic = st.text_input("Islamic")
            social  = st.text_input("Social Studies")

        st.markdown("#### 💬 Comments")
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
                st.success("✅ Updated existing student report.")
            else:
                df = pd.concat([df, pd.DataFrame([row_data])], ignore_index=True)
                st.success("✅ Added new student report.")

            save_data(df)
