import re
import spacy
from spacy.matcher import PhraseMatcher

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Technical skills we want to detect
skills = [
    "Python",
    "Java",
    "C",
    "C++",
    "C#",
    "JavaScript",
    "HTML",
    "CSS",
    "SQL",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
    "Flask",
    "Django",
    "React",
    "Node.js",
    "REST API",
    "REST APIs",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "NLP",
    "Data Structures",
    "Algorithms"
]

def extract_education_requirements(text):
    doc = nlp(text)

    education_keywords = [
        "bachelor's degree",
        "bachelor degree",
        "b.tech",
        "btech",
        "b.e",
        "be degree",
        "master's degree",
        "master degree",
        "m.tech",
        "mtech",
        "m.e",
        "me degree",
        "computer science",
        "computer engineering",
        "information technology"
    ]

    found = []

    for keyword in education_keywords:
        if keyword.lower() in text.lower():
            found.append(keyword)

    return found



def extract_experience_requirements(text):
    experience_patterns = [
        r"\b\d+\+?\s+years?\s+of\s+experience\b",
        r"\b\d+\+?\s+years?\s+experience\b",
        r"\b\d+\+?\s+year\s+of\s+experience\b",
        r"\bfresher[s]?\b",
        r"\bentry[- ]level\b"
    ]

    found = []

    for pattern in experience_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:
            if match.lower() not in [item.lower() for item in found]:
                found.append(match)

    return found
def extract_requirements(text):
    requirement_keywords = [
        "software development",
        "software engineering",
        "coding",
        "code reviews",
        "source control",
        "version control",
        "testing",
        "debugging",
        "problem solving",
        "build processes",
        "software development life cycle",
        "SDLC",
        "design and architecture",
        "database",
        "communication skills",
        "teamwork",
        "analytical skills"
    ]

    found = []

    text_lower = text.lower()

    for keyword in requirement_keywords:
        if keyword.lower() in text_lower:
            found.append(keyword)

    return found
# Create matcher
matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

# Convert skills into spaCy patterns
patterns = [nlp.make_doc(skill) for skill in skills]

matcher.add("SKILL", patterns)


def extract_skills(text):
    doc = nlp(text)

    matches = matcher(doc)

    found_skills = []

    for _, start, end in matches:
        skill = doc[start:end].text

        if skill.lower() not in [s.lower() for s in found_skills]:
            found_skills.append(skill)

    return found_skills
def compare_job_and_resume(job_text, resume_text):
    job_skills = extract_skills(job_text)
    resume_skills = extract_skills(resume_text)

    matched_skills = []
    missing_skills = []

    for skill in job_skills:
        if skill.lower() in [s.lower() for s in resume_skills]:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(job_skills) > 0:
        match_score = (len(matched_skills) / len(job_skills)) * 100
    else:
        match_score = 0

    return {
        "job_skills": job_skills,
        "resume_skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2)
    }
def analyze_job_description(text):
    return {
        "skills": extract_skills(text),
        "education": extract_education_requirements(text),
        "experience": extract_experience_requirements(text),
        "requirements": extract_requirements(text)
    }