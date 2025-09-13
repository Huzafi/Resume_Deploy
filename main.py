import streamlit as st
import pypdf
import docx
import google.generativeai as genai

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


GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=GEMINI_API_KEY)
def get_feedback(resume_text):
        prompt = f"""
You are an experienced professional recruiter, career coach, and ATS expert.
Analyze the following resume content and provide a detailed yet concise review.

At the very start of your output, display the candidate's full name on a separate line as:
**Candidate Name:** <Full Name>

Your output must follow exactly this structure:

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

At the end, provide a **Scorecard Table** in Markdown format:

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


st.set_page_config(page_title="Expert Resume Analyzer", page_icon="📄", layout="centered")

st.title("📄 Expert Resume Analyzer Agent")
st.caption("Analyze, Improve, and Stand Out")
st.header("Upload Your Resume or CV")

uploaded_file = st.file_uploader("📂 Upload your resume", type=["pdf", "docx"])

if uploaded_file and api_key:
    with st.spinner("🔍 Analyzing your resume..."):
        resume_text = parse_resume(uploaded_file)
        if not resume_text:
            st.error("❌ Could not extract text from this file. Please upload a clear resume.")
        else:
            feedback = get_feedback(resume_text, api_key)
            st.subheader("✅ Analysis Result")
            st.markdown(feedback)

elif uploaded_file and not api_key:
    st.warning("⚠️ Please enter your Gemini API key to proceed.")

st.caption("Built with  using Streamlit + Google Gemini")
