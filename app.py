
import re
import io
import streamlit as st
from pypdf import PdfReader

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------- SKILL DATABASE ----------

SKILLS = {
    "Python": ["python"],
    "Java": ["java"],
    "C": ["c programming", " c language"],
    "C++": ["c++"],
    "JavaScript": ["javascript", "js"],
    "HTML": ["html"],
    "CSS": ["css"],
    "SQL": ["sql", "structured query language"],
    "MySQL": ["mysql"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "Artificial Intelligence": [
        "artificial intelligence", " ai "
    ],
    "Data Analysis": ["data analysis", "data analytics"],
    "Excel": ["excel", "microsoft excel"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Communication": ["communication", "communicate"],
    "Teamwork": ["teamwork", "team work", "collaboration"],
    "Leadership": ["leadership", "lead"],
    "Problem Solving": ["problem solving", "problem-solving"],
    "Critical Thinking": ["critical thinking"],
    "Project Management": ["project management"],
    "Git": ["git", "github"],
    "Linux": ["linux"],
    "Verilog HDL": ["verilog", "verilog hdl"],
    "MATLAB": ["matlab"],
    "Digital Logic Design": [
        "digital logic design", "digital electronics"
    ],
    "VLSI": ["vlsi"],
    "Embedded Systems": ["embedded systems", "embedded system"],
    "Electronics": ["electronics", "electronic circuits"],
    "Communication Systems": ["communication systems"],
    "Circuit Design": ["circuit design"],
    "Signal Processing": ["signal processing"],
    "Statistics": ["statistics", "statistical analysis"],
    "Research": ["research", "research skills"],
    "Time Management": ["time management"],
    "Creativity": ["creativity", "creative thinking"],
    "Presentation": ["presentation", "presentations"],
    "Cloud Computing": ["cloud computing"],
    "AWS": ["aws", "amazon web services"],
    "Docker": ["docker"],
    "Cybersecurity": ["cybersecurity", "cyber security"],
    "Networking": ["networking", "computer networks"],
}

# ---------- HELPER FUNCTIONS ----------

def normalize(text):
    text = text.lower()
    text = text.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", text).strip()


def extract_text(uploaded_file):
    filename = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    if filename.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")

    if filename.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(data))
        pages = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return "\n".join(pages)

    return ""


def find_skills(text):
    text = normalize(text)
    found = set()

    for skill, aliases in SKILLS.items():
        for alias in aliases:
            # Match complete words or phrases, not partial words.
            pattern = (
                r"(?<![a-z0-9+#])"
                + re.escape(alias.strip())
                + r"(?![a-z0-9+#])"
            )

            if re.search(pattern, text):
                found.add(skill)
                break

    return found


# ---------- USER INTERFACE ----------

st.title("📄 AI Resume Analyzer")
st.caption(
    "Compare your resume with a job description "
    "and identify relevant skills."
)

with st.container(border=True):
    st.subheader("1. Upload your resume")

    resume_file = st.file_uploader(
        "Choose a PDF or TXT file",
        type=["pdf", "txt"],
        help="Text-based PDFs and TXT files are supported."
    )

    st.subheader("2. Enter the job description")

    job_description = st.text_area(
        "Paste the complete job description",
        height=200,
        placeholder=(
            "Example: We need a Python developer "
            "with SQL, data analysis, communication "
            "and problem-solving skills."
        )
    )

    analyze = st.button(
        "🔍 Analyze Resume",
        type="primary",
        use_container_width=True
    )


if analyze:
    if resume_file is None:
        st.error("Please upload a PDF or TXT resume.")

    elif not job_description.strip():
        st.error("Please enter a job description.")

    else:
        try:
            resume_text = extract_text(resume_file)

            if not resume_text.strip():
                st.error(
                    "No readable text was found. "
                    "Try a text-based PDF or TXT file."
                )

            else:
                resume_skills = find_skills(resume_text)
                job_skills = find_skills(job_description)

                if not job_skills:
                    st.warning(
                        "No supported skills were detected "
                        "in the job description. Add specific "
                        "technical or professional skills."
                    )

                else:
                    matched = sorted(
                        resume_skills & job_skills
                    )
                    missing = sorted(
                        job_skills - resume_skills
                    )

                    score = round(
                        len(matched) / len(job_skills) * 100
                    )

                    st.divider()
                    st.header("📊 Analysis Results")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Skill Match",
                        f"{score}%"
                    )
                    col2.metric(
                        "Matched Skills",
                        len(matched)
                    )
                    col3.metric(
                        "Missing Skills",
                        len(missing)
                    )

                    st.progress(score / 100)

                    st.caption(
                        "Score = matched detected skills / "
                        "all detected job-description skills. "
                        "Each skill has equal weight."
                    )

                    left, right = st.columns(2)

                    with left:
                        st.subheader("✅ Matching Skills")

                        if matched:
                            for skill in matched:
                                st.write(f"• {skill}")
                        else:
                            st.info(
                                "No matching skills detected."
                            )

                    with right:
                        st.subheader("📌 Missing Skills")

                        if missing:
                            for skill in missing:
                                st.write(f"• {skill}")
                        else:
                            st.success(
                                "All detected job skills "
                                "appear in your resume."
                            )

                    st.subheader("💡 Improvement Suggestions")

                    if missing:
                        st.write(
                            "Review these skills and add "
                            "them to your resume only if you "
                            "genuinely possess them."
                        )

                        st.write(
                            "**Skills to review:** "
                            + ", ".join(missing)
                        )

                    if score < 50:
                        st.write(
                            "• Highlight relevant projects "
                            "and technical skills."
                        )
                        st.write(
                            "• Tailor your resume to the "
                            "job requirements."
                        )

                    elif score < 80:
                        st.write(
                            "• Improve the visibility of "
                            "relevant skills and projects."
                        )

                    else:
                        st.write(
                            "• Review your experience and "
                            "achievements for relevance."
                        )

                    st.info(
                        "This tool uses a predefined skill "
                        "database. It does not assess actual "
                        "proficiency, verify qualifications, "
                        "or guarantee hiring outcomes."
                    )

        except Exception as error:
            st.error(
                "Could not read this resume. Please try "
                "another PDF or TXT file."
            )
            st.caption(
                f"Technical detail: {type(error).__name__}"
            )

st.divider()
st.caption(
    "Resume analysis project | Python + Streamlit"
)

