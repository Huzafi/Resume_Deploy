import google.generativeai as genai

# 🔹 Apni Google Gemini API key yahan likho
GEMINI_API_KEY = "AIzaSyBtA4vuP7K3S26B1zaF2cHqsVRizG-fAZ0"

# Gemini ko configure karo
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

    model = genai.GenerativeModel("gemini-2.5-flash-lite")

    # Generate content
    response = model.generate_content(prompt)

    return response.text
