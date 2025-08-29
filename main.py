import streamlit as st
from parser import parse_resume
from Agent_feedback import get_feedback

st.title("📄 Expert Resume Analyzer Agent")
st.caption("Analyze, Improve, and Stand Out")
st.header("Upload Your Resume or CV")

uploaded_file = st.file_uploader("Upload your resume",type=["pdf", "docx"])
if uploaded_file:
    with st.spinner("Analyzing..."):
        resume_text = parse_resume(uploaded_file)
        if not resume_text:
            st.error("Could not extract text from this file. Please upload a clear resume.")
        else:
            feedback = get_feedback(resume_text)
            st.subheader("Analysis Result")
            st.write(feedback)
          
# uv run streamlit run main.py
