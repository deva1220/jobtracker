from nlp_analyzer import analyze_job_description


text = """
We are looking for a Software Engineer.
The candidate should have a Bachelor's degree in Computer Science or Engineering.
The candidate should have 2+ years of experience in software development.
The candidate should have experience with Python and SQL.
Knowledge of REST APIs is preferred.
"""


result = analyze_job_description(text)

print("Skills:")
for skill in result["skills"]:
    print("-", skill)

print("\nEducation:")
for item in result["education"]:
    print("-", item)

print("\nExperience:")
for item in result["experience"]:
    print("-", item)