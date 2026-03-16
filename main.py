from fastapi import FastAPI, UploadFile, File
import PyPDF2
from skills import skills_list

app = FastAPI()

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text.lower()


@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):

    text = extract_text_from_pdf(file.file)

    found_skills = []
    missing_skills = []

    # check skills
    for skill in skills_list:
        if skill in text:
            found_skills.append(skill)
        else:
            missing_skills.append(skill)

    score = int((len(found_skills) / len(skills_list)) * 100)

    # suggestions
    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Learn {skill} to improve your resume")

    return {
        "score": score,
        "skills_found": found_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions
    }