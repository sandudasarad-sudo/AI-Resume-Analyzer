import re
from io import BytesIO

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PyPDF2 import PdfReader
from resume_ml import compare_resume_to_roles
# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🚀",
    layout="wide"
)

# --------------------------------------------------
# PROFESSIONAL DASHBOARD STYLE
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0b1020, #111827);
    color: #f8fafc;
}

.main-title {
    font-size: 44px;
    font-weight: 800;
    color: #60a5fa;
}

.subtitle {
    font-size: 18px;
    color: #cbd5e1;
}

div[data-testid="stMetric"] {
    background: #1e293b;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 15px;
}

div[data-testid="stMetricValue"] {
    color: #60a5fa;
}

section[data-testid="stSidebar"] {
    background: #111827;
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 9px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# JOB ROLE SKILL DATABASE
# --------------------------------------------------

ROLE_SKILLS = {
    "Python Developer": [
        "Python", "SQL", "Git", "Flask", "Django",
        "REST API", "Pandas", "NumPy"
    ],
    "Web Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Node.js", "SQL", "Git", "REST API"
    ],
    "Machine Learning Intern": [
        "Python", "Pandas", "NumPy", "Scikit-learn",
        "Machine Learning", "Matplotlib", "SQL"
    ],
    "Flutter Developer": [
        "Flutter", "Dart", "Firebase",
        "REST API", "Git", "SQL"
    ],
    "Full Stack Developer": [
        "HTML", "CSS", "JavaScript", "React",
        "Node.js", "Express", "MongoDB", "SQL", "Git"
    ]
}

ALL_SKILLS = sorted({
    skill
    for skills in ROLE_SKILLS.values()
    for skill in skills
})

# --------------------------------------------------
# PDF TEXT EXTRACTION
# --------------------------------------------------

def extract_resume_text(pdf_file):
    try:
        reader = PdfReader(pdf_file)

        if reader.is_encrypted:
            return None, "This PDF is password-protected."

        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        if not text.strip():
            return None, (
                "No readable text was found. "
                "Please try a text-based PDF."
            )

        return text, None

    except Exception:
        return None, (
            "Unable to read this PDF. "
            "Please upload another PDF file."
        )


# --------------------------------------------------
# SKILL DETECTION
# --------------------------------------------------

def extract_skills(text):
    detected = []

    for skill in ALL_SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text, re.IGNORECASE):
            detected.append(skill)

    return detected


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🚀 AI Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Understand your skills. Explore career opportunities. '
    'Build your future.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("🎯 Career Dashboard")

    st.write("Choose your career target.")

    target_role = st.selectbox(
        "Target Job Role",
        list(ROLE_SKILLS.keys())
    )

    st.divider()

    st.markdown("### 📌 Available Features")
    st.write("📄 Resume PDF parsing")
    st.write("🎯 Job role skill matching")
    st.write("📊 Visual skill analysis")
    st.write("💡 Learning recommendations")
    st.write("📥 Downloadable report")

    st.divider()

    st.caption(
        "Student Project | Python + Streamlit"
    )

# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

st.subheader("📄 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose a text-based PDF resume",
    type=["pdf"]
)

if uploaded_file is None:
    st.info(
        "Upload your resume to see your skill analysis "
        "and career recommendations."
    )

    st.markdown("### ✨ Explore the Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📄 Resume Parsing")
        st.write("Extract readable text from a PDF resume.")

    with col2:
        st.markdown("#### 🎯 Skill Matching")
        st.write("Compare detected skills with a target role.")

    with col3:
        st.markdown("#### 📊 Visual Dashboard")
        st.write("Explore skill coverage and learning suggestions.")

    st.stop()

# --------------------------------------------------
# ANALYZE RESUME
# --------------------------------------------------

resume_text, error = extract_resume_text(uploaded_file)

if error:
    st.error(error)
    st.stop()

resume_skills = extract_skills(resume_text)

required_skills = ROLE_SKILLS[target_role]

matched_skills = [
    skill for skill in required_skills
    if skill in resume_skills
]

missing_skills = [
    skill for skill in required_skills
    if skill not in resume_skills
]

match_percentage = round(
    len(matched_skills) / len(required_skills) * 100
) if required_skills else 0

# --------------------------------------------------
# METRICS
# --------------------------------------------------

st.divider()
st.subheader("📊 Resume Analysis Dashboard")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Detected Skills",
    len(resume_skills)
)

col2.metric(
    "Matching Skills",
    len(matched_skills)
)

col3.metric(
    "Skills to Explore",
    len(missing_skills)
)

col4.metric(
    "Role Skill Coverage",
    f"{match_percentage}%"
)

st.progress(match_percentage / 100)

st.caption(
    "Role skill coverage is the percentage of skills in the "
    "selected role's predefined checklist that were detected. "
    "It is not a hiring probability or a complete assessment "
    "of your abilities."
)

# --------------------------------------------------
# SKILL MATCHING
# --------------------------------------------------

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("✅ Matching Skills")

    if matched_skills:
        for skill in matched_skills:
            st.success(f"✓ {skill}")
    else:
        st.info(
            "No skills from this role's checklist were detected."
        )

with right:
    st.subheader("📚 Skills to Explore")

    if missing_skills:
        for skill in missing_skills:
            st.warning(f"• {skill}")
    else:
        st.success(
            "All skills in this role's checklist were detected."
        )

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

st.divider()
st.subheader("📈 Skill Coverage Visualization")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### Role Skill Coverage")

    fig, ax = plt.subplots(figsize=(6, 3))

    categories = ["Matching", "Not Detected"]
    values = [
        len(matched_skills),
        len(missing_skills)
    ]

    ax.barh(categories, values)
    ax.set_xlabel("Number of Skills")
    ax.set_title(target_role)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with chart_col2:
    st.markdown("#### Detected Technical Skills")

    if resume_skills:
        skills_df = pd.DataFrame({
            "Detected Skill": resume_skills
        })

        st.dataframe(
            skills_df,
            width="stretch",
            hide_index=True
        )
    else:
        st.info(
            "No skills from the current skill database "
            "were detected in this resume."
        )

# --------------------------------------------------
# MULTI-ROLE COMPARISON
# --------------------------------------------------

st.divider()
st.subheader("🎯 Compare Different Job Roles")

st.write(
    "Compare your detected skills against the predefined "
    "skill checklist for each available role."
)

comparison_rows = []

for role, skills in ROLE_SKILLS.items():
    role_matches = [
        skill for skill in skills
        if skill in resume_skills
    ]

    coverage = round(
        len(role_matches) / len(skills) * 100
    ) if skills else 0

    comparison_rows.append({
        "Job Role": role,
        "Matching Skills": len(role_matches),
        "Required Checklist Skills": len(skills),
        "Skill Coverage (%)": coverage
    })

comparison_df = pd.DataFrame(comparison_rows)

comparison_df = comparison_df.sort_values(
    by="Skill Coverage (%)",
    ascending=False
).reset_index(drop=True)

st.dataframe(
    comparison_df,
    width="stretch",
    hide_index=True
)

st.caption(
    "Role comparisons use the same keyword-based skill detection. "
    "Results depend on the skills included in each predefined checklist."
)

# --------------------------------------------------
# LEARNING RECOMMENDATIONS
# --------------------------------------------------

st.divider()
st.subheader("💡 Career Improvement Suggestions")

if missing_skills:
    st.write(
        f"For the **{target_role}** checklist, consider exploring "
        "these skills if they fit your career goals:"
    )

    for skill in missing_skills:
        st.markdown(f"- **{skill}**")

    st.info(
        "Prioritize skills based on your interests, coursework, "
        "and the requirements of the jobs you want to pursue."
    )
else:
    st.success(
        "All skills in this role's predefined checklist "
        "were detected in your resume."
    )

st.markdown(
    "**Resume tip:** Describe your actual project contributions "
    "and the technologies you genuinely used."
)

# --------------------------------------------------
# DOWNLOAD REPORT
# --------------------------------------------------

st.divider()
st.subheader("📥 Download Your Analysis Report")

report = f"""
AI RESUME ANALYZER
==================

Target Role: {target_role}

DETECTED TECHNICAL SKILLS
-------------------------
{', '.join(resume_skills) if resume_skills else 'None detected'}

MATCHING SKILLS
---------------
{', '.join(matched_skills) if matched_skills else 'None detected'}

SKILLS NOT DETECTED IN ROLE CHECKLIST
-------------------------------------
{', '.join(missing_skills) if missing_skills else 'None'}

ROLE SKILL COVERAGE
-------------------
{match_percentage}%

ROLE COMPARISON
---------------
{comparison_df.to_string(index=False)}

IMPORTANT NOTE
--------------
This report uses keyword matching against predefined skill lists.
A skill not detected in the PDF may still be a skill you possess.
The score is not a hiring probability or a prediction of employment.
"""

st.download_button(
    label="⬇️ Download Resume Analysis Report",
    data=report,
    file_name="resume_analysis_report.txt",
    mime="text/plain",
    width="stretch"
)

# --------------------------------------------------
# EXTRACTED TEXT
# --------------------------------------------------

with st.expander("🔍 View Extracted Resume Text"):
    st.text_area(
        "Extracted PDF text",
        resume_text,
        height=250
    )
# --------------------------------------------------
# RESUME SECTION ANALYSIS
# --------------------------------------------------

st.divider()
st.subheader("📝 Resume Section Analysis")

resume_lower = resume_text.lower()

sections = {
    "Contact Information": [
        "email", "phone", "contact", "linkedin", "github"
    ],
    "Education": [
        "education", "bachelor", "b.tech", "university", "college"
    ],
    "Technical Skills": [
        "skills", "technical skills", "technologies"
    ],
    "Projects": [
        "projects", "project experience", "academic project"
    ],
    "Experience / Internships": [
        "experience", "internship", "intern", "employment"
    ],
    "Certifications": [
        "certifications", "certificates", "certification"
    ]
}

section_results = []

for section, keywords in sections.items():
    found = any(
        keyword in resume_lower
        for keyword in keywords
    )

    section_results.append({
        "Resume Section": section,
        "Status": "Detected" if found else "Not detected"
    })

section_df = pd.DataFrame(section_results)

detected_sections = sum(
    row["Status"] == "Detected"
    for row in section_results
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Sections Detected",
        f"{detected_sections}/{len(sections)}"
    )

with col2:
    st.metric(
        "Sections Not Detected",
        len(sections) - detected_sections
    )

st.dataframe(
    section_df,
    width="stretch",
    hide_index=True
)

st.caption(
    "This check searches for section-related keywords. "
    "A section may exist but remain undetected if it uses "
    "different wording or formatting."
)

st.markdown("### 💡 Resume Improvement Tips")

tips = {
    "Contact Information":
        "Include professional contact details and relevant profile links.",
    "Education":
        "Add your degree, institution, and expected graduation year.",
    "Technical Skills":
        "List relevant programming languages, frameworks, and tools.",
    "Projects":
        "Describe projects, technologies used, and your actual contributions.",
    "Experience / Internships":
        "Include relevant internships, volunteering, or practical experience.",
    "Certifications":
        "List relevant courses and certifications you have genuinely completed."
}

for row in section_results:
    if row["Status"] == "Not detected":
        st.write(
            f"📌 **{row['Resume Section']}:** "
            f"{tips[row['Resume Section']]}"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Resume Analyzer | Built with Python, Streamlit, "
    "Pandas, Matplotlib and PyPDF2"
)