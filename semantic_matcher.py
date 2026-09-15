from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def normalize_skill(skill):
    skill = skill.lower().strip()

    aliases = {
        "nlp": "natural language processing",
        "rest api": "rest apis",
        "rest api development": "rest apis",
        "js": "javascript",
        "postgres": "postgresql",
        "mongo": "mongodb"
    }

    return aliases.get(skill, skill)


def semantic_skill_match(job_skills, resume_skills, threshold=0.70):

    if not job_skills or not resume_skills:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "match_score": 0
        }

    normalized_job = [
        normalize_skill(skill)
        for skill in job_skills
    ]

    normalized_resume = [
        normalize_skill(skill)
        for skill in resume_skills
    ]

    job_embeddings = model.encode(normalized_job)
    resume_embeddings = model.encode(normalized_resume)

    matched_skills = []
    missing_skills = []

    for i, job_skill in enumerate(job_skills):

        # First check exact/normalized match
        if normalized_job[i] in normalized_resume:
            matched_skills.append(job_skill)
            continue

        similarities = cosine_similarity(
            [job_embeddings[i]],
            resume_embeddings
        )[0]

        best_score = max(similarities)

        if best_score >= threshold:
            matched_skills.append(job_skill)
        else:
            missing_skills.append(job_skill)

    match_score = (
        len(matched_skills) / len(job_skills)
    ) * 100

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": round(match_score, 2)
    }