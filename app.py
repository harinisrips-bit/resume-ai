import streamlit as st
import nltk
import PyPDF2
import docx

# ---------- CONFIG ----------
st.set_page_config(page_title="ResumeAI", layout="wide")

# ---------- NLTK ----------
nltk.download('stopwords')

# ---------- MODERN UI ----------
st.markdown("""
<style>
body {
    background-color: #0e1117;
}
.big-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #4CAF50;
}
.sub-text {
    text-align: center;
    font-size: 18px;
    color: #aaa;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}
.section-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown("<div class='big-title'>🚀 ResumeAI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Smart Resume Analysis & Optimization Tool</div>", unsafe_allow_html=True)
st.markdown("---")

# ---------- SKILL DATABASE ----------
SKILLS_DB = [
    "python", "java", "c", "c++", "sql", "html", "css", "javascript",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "yolo", "opencv",
    "data analysis", "pandas", "numpy",
    "react", "node", "mongodb", "fastapi", "flask",
    "streamlit", "power bi", "tableau", "git", "github"
]

# ---------- FUNCTIONS ----------
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        if page.extract_text():
            text += page.extract_text()
    return text.lower()

def read_docx(file):
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text.lower()

def extract_skills(text):
    return {skill for skill in SKILLS_DB if skill in text}

def detect_domain(text):
    domains = {
        "Machine Learning 🧠": ["machine learning", "nlp", "tensorflow", "pytorch", "yolo"],
        "Data Analyst 📊": ["sql", "excel", "power bi", "tableau"],
        "Web Development 🌐": ["html", "css", "javascript", "react", "node"],
        "Software Development 💻": ["java", "c++", "algorithms"]
    }
    scores = {d: sum(k in text for k in ks) for d, ks in domains.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "General / Other 🔍"

def generate_suggestions(resume_text, missing_skills, domain):
    suggestions = []

    for skill in list(missing_skills)[:5]:
        suggestions.append(f"Consider adding '{skill}' if you have experience with it.")

    if "Machine Learning" in domain:
        if "project" not in resume_text:
            suggestions.append("Add ML projects with datasets and results.")
        if "model" not in resume_text:
            suggestions.append("Mention ML models you worked on.")

    if "Web Development" in domain:
        suggestions.append("Include frontend/backend projects and APIs.")

    if "Data Analyst" in domain:
        suggestions.append("Add dashboards and data insights.")

    if "%" not in resume_text:
        suggestions.append("Add measurable achievements (e.g., improved accuracy by 20%).")

    if "github" not in resume_text:
        suggestions.append("Include your GitHub profile.")

    return suggestions

def generate_bullet_points(skills, domain):
    bullets = []
    s = list(skills)

    if "Machine Learning" in domain:
        if "python" in s:
            bullets.append("Developed machine learning models using Python.")
        if "nlp" in s:
            bullets.append("Implemented NLP techniques for text processing.")
        if "yolo" in s:
            bullets.append("Built a YOLO-based object detection system.")
        if "streamlit" in s:
            bullets.append("Created dashboards using Streamlit.")

    elif "Web Development" in domain:
        if "javascript" in s:
            bullets.append("Developed web applications using JavaScript.")
        if "react" in s:
            bullets.append("Built responsive UI using React.")
        if "node" in s:
            bullets.append("Implemented backend using Node.js.")

    elif "Data Analyst" in domain:
        if "sql" in s:
            bullets.append("Analyzed data using SQL queries.")
        if "pandas" in s:
            bullets.append("Performed analysis using Pandas.")

    if not bullets:
        for skill in s[:3]:
            bullets.append(f"Used {skill} in technical projects.")

    return bullets

def create_improved_resume(resume_text, bullets, skills):
    new_resume = "IMPROVED RESUME\n\n"

    new_resume += "SUMMARY\n"
    new_resume += "Motivated candidate with strong technical skills and project experience.\n\n"

    new_resume += "KEY SKILLS\n"
    new_resume += ", ".join(skills) + "\n\n"

    new_resume += "PROJECT EXPERIENCE\n"
    for b in bullets:
        new_resume += "• " + b + "\n"

    new_resume += "\nNOTE:\nYou can copy and integrate these points into your original resume."

    return new_resume

# ---------- INPUT UI ----------
st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📂 Upload Resume", type=["pdf", "docx"])

with col2:
    job_desc = st.text_area("📝 Job Description or Keywords", height=200)

st.markdown("</div>", unsafe_allow_html=True)

analyze = st.button("🚀 Analyze Resume")

# ---------- PROCESS ----------
if analyze:
    if uploaded_file and job_desc:

        if uploaded_file.type == "application/pdf":
            resume_text = read_pdf(uploaded_file)
        else:
            resume_text = read_docx(uploaded_file)

        job_desc = job_desc.lower()

        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_desc)

        matched = resume_skills & job_skills
        missing = job_skills - resume_skills

        score = (len(matched) / len(job_skills)) * 100 if job_skills else 0
        domain = detect_domain(job_desc)

        # ---------- RESULTS ----------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📊 Analysis Results</div>", unsafe_allow_html=True)

        st.metric("Match Score", f"{round(score,2)}%")
        st.progress(int(score))
        st.markdown(f"🎯 **Domain:** {domain}")

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- SKILLS ----------
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### ✅ Matched Skills")
            st.write(", ".join(sorted(list(matched))))
            st.markdown("</div>", unsafe_allow_html=True)

        with col4:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown("### ❌ Missing Skills")
            st.write(", ".join(sorted(list(missing))))
            st.markdown("</div>", unsafe_allow_html=True)

        # ---------- SUGGESTIONS ----------
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 💡 Suggestions")

        for s in generate_suggestions(resume_text, missing, domain):
            st.write("👉 " + s)

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- BULLETS ----------
        bullets = generate_bullet_points(matched, domain)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### ✨ Resume Bullet Points")

        for b in bullets:
            st.write("• " + b)

        st.markdown("</div>", unsafe_allow_html=True)

        # ---------- DOWNLOAD ----------
        improved_resume = create_improved_resume(resume_text, bullets, matched)

        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("### 📥 Download Improved Resume")

        st.download_button(
            label="Download Resume",
            data=improved_resume,
            file_name="improved_resume.txt",
            mime="text/plain"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("⚠️ Upload resume and enter job description")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<center>🚀 Built with ❤️ using Streamlit</center>", unsafe_allow_html=True)