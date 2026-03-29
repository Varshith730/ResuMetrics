import re
import io
import random

def parse_resume_text(uploaded_file) -> str:
    """Extract text from uploaded PDF or DOCX file."""
    filename = uploaded_file.name.lower()
    text = ""
    if filename.endswith(".pdf"):
        try:
            import pdfplumber
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t + "\n"
        except Exception:
            text = "[Could not parse PDF – demo mode active]"
    elif filename.endswith(".docx"):
        try:
            from docx import Document
            doc = Document(uploaded_file)
            text = "\n".join([p.text for p in doc.paragraphs])
        except Exception:
            text = "[Could not parse DOCX – demo mode active]"
    return text.strip()


def generate_demo_resume() -> str:
    return """JOHN A. SMITH
Senior Software Engineer | john.smith@email.com | +1-555-0123 | LinkedIn: linkedin.com/in/johnsmith

PROFESSIONAL SUMMARY
Results-driven Senior Software Engineer with 7+ years of experience designing scalable microservices,
leading cross-functional teams, and delivering high-impact data pipelines. Proven track record in
Python, cloud infrastructure, and ML model deployment.

EXPERIENCE
Senior Software Engineer – TechCorp Inc. (2021–Present)
• Architected a distributed data pipeline processing 10M+ events/day using Apache Kafka and Spark
• Led a team of 8 engineers; reduced deployment time by 40% via CI/CD automation
• Developed ML inference APIs serving 2M+ daily requests with 99.9% uptime

Software Engineer – DataSoft LLC (2018–2021)
• Built REST APIs in Python/FastAPI integrated with PostgreSQL and Redis
• Implemented automated testing suite increasing code coverage from 45% to 92%

EDUCATION
B.Sc. Computer Science – State University (2014–2018) | GPA: 3.8/4.0

SKILLS
Python, Java, Go | TensorFlow, scikit-learn, PyTorch | AWS, GCP, Docker, Kubernetes
PostgreSQL, MongoDB, Redis | Apache Kafka, Spark | React, TypeScript

CERTIFICATIONS
AWS Solutions Architect – Professional | GCP Professional Data Engineer | CKA

ACHIEVEMENTS
• Published 2 papers on distributed systems optimization
• Open-source contributor: 3,200+ GitHub stars across personal projects
• Speaker at PyCon 2023 on scalable ML deployment"""


def extract_skills(text: str) -> list:
    skill_keywords = [
        "python","java","javascript","typescript","go","rust","c++","scala","kotlin","swift",
        "react","vue","angular","nextjs","nodejs","fastapi","django","flask","spring",
        "tensorflow","pytorch","sklearn","scikit-learn","keras","xgboost","nlp","llm",
        "aws","gcp","azure","docker","kubernetes","terraform","ci/cd","jenkins","github actions",
        "postgresql","mysql","mongodb","redis","elasticsearch","kafka","spark","airflow",
        "machine learning","deep learning","data science","mlops","devops","agile","scrum",
        "sql","nosql","graphql","restapi","microservices","distributed systems",
    ]
    text_lower = text.lower()
    found = [s for s in skill_keywords if s in text_lower]
    return list(dict.fromkeys(found))  # deduplicate preserving order


def extract_experience_years(text: str) -> float:
    matches = re.findall(r'(\d+)\+?\s*years?', text, re.IGNORECASE)
    if matches:
        return float(max(int(m) for m in matches))
    # try to count date ranges like 2018–2021
    ranges = re.findall(r'(20\d\d)\s*[–\-]\s*(20\d\d|Present)', text, re.IGNORECASE)
    if ranges:
        total = 0
        import datetime
        current_year = datetime.datetime.now().year
        for start, end in ranges:
            e = current_year if end.lower() == "present" else int(end)
            total += max(0, e - int(start))
        return float(total)
    return 3.0  # default


def count_achievements(text: str) -> int:
    bullets = re.findall(r'[•\-\*]\s+[A-Z]', text)
    quantified = re.findall(r'\d+\s*[\%\+xX]|\$\d+|\d+[Mmk]\+?', text)
    return len(bullets) + len(quantified)
