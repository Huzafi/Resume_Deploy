import streamlit as st
import pypdf
import docx
import google.generativeai as genai

# -------------------------
# 1️⃣ Resume Parser
# -------------------------
def parse_resume(file):
    text = ""
    name = file.name.lower()
    try:
        if name.endswith(".pdf"):
            pdf = pypdf.PdfReader(file)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        elif name.endswith(".docx"):
            doc = docx.Document(file)
            for para in doc.paragraphs:
                if para.text.strip():
                    text += para.text + "\n"
    except Exception as e:
        st.error(f"Error reading file: {e}")
    return text.strip()

# -------------------------
# 2️⃣ Configure Gemini
# -------------------------
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

# -------------------------
# 3️⃣ Feedback Function
# -------------------------
def get_feedback(resume_text):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        prompt = f"""
You are an experienced professional recruiter, career coach, and ATS expert.
Analyze the following resume content and provide a detailed yet concise review.

At the very start of your output, display the candidate's full name on a separate line as:
**Candidate Name:** <Full Name>

### 1. Executive Summary
- 1–2 short sentences summarizing candidate fit.

### 2. Key Strengths (Score: X/10)
- Up to 5 bullet points.

### 3. Weaknesses (Score: X/10)
- Up to 5 bullet points.

### 4. Suggestions for Improvement (Score: X/10)
- Actionable, specific steps the candidate can take.
- Include 1 example rewritten bullet: Before → After.

### 5. ATS Optimization Tips (Score: X/10)
- Up to 8–10 keywords to add.
- Suggested section headings and formatting tips.

### 6. Suggested Job Titles
- 3–5 relevant job titles.

### 7. One-line LinkedIn Headline
- 8–12 words.

### 8. Overall Rating: X/10
- One-line summary.

| Category                | Score |
|------------------------|-------|
| Key Strengths          | X/10  |
| Weaknesses             | X/10  |
| Suggestions            | X/10  |
| ATS Optimization       | X/10  |
| Language & Presentation| X/10  |
| **Overall**            | X/10  |

Resume Text:
{resume_text}
"""
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating feedback: {e}"

# -------------------------
# 4️⃣ Streamlit UI
# -------------------------
st.set_page_config(page_title="Expert Resume Analyzer", page_icon="📄", layout="centered")

st.title("📄 Expert Resume Analyzer Agent")
st.caption("Analyze, Improve, and Stand Out")
st.header("Upload Your Resume or CV")

uploaded_file = st.file_uploader("📂 Upload your resume", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("🔍 Analyzing your resume..."):
        resume_text = parse_resume(uploaded_file)
        if not resume_text:
            st.error("❌ Could not extract text from this file. Please upload a clear resume.")
        else:
            feedback = get_feedback(resume_text)
            st.subheader("✅ Analysis Result")
            st.markdown(feedback)

st.caption("Built with ❤️ using Streamlit + Google Gemini")
