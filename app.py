
import streamlit as st
import re

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and compare it with a job description.")

resume_file = st.file_uploader(
    "Upload your resume (.txt)",
    type=["txt"]
)

job_description = st.text_area(
    "Paste the job description here"
)

if st.button("Analyze Resume"):
    if resume_file is not None and job_description.strip():
        resume = resume_file.read().decode(
            "utf-8", errors="ignore"
        ).lower()

        job = job_description.lower()

        words = re.findall(r"\b[a-zA-Z0-9+#.]+\b", job)
        keywords = list(set(words))

        matched = [
            word for word in keywords
            if word in resume and len(word) > 2
        ]

        missing = [
            word for word in keywords
            if word not in resume and len(word) > 2
        ]

        score = round(
            len(matched) / max(len(keywords), 1) * 100
        )

        st.subheader("Analysis Results")
        st.metric("Keyword Match Score", f"{score}%")

        st.success("Matching keywords")
        st.write(", ".join(matched) if matched else "None found")

        st.warning("Missing keywords")
        st.write(", ".join(missing) if missing else "None found")

        st.info(
            "This is a basic keyword-matching prototype, "
            "not a complete AI assessment."
        )
    else:
        st.error(
            "Please upload a resume and enter a job description."
        )

