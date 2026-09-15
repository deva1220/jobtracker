# AI-Powered Job Tracker

A Flask-based job application tracking system that helps users manage job applications, analyze job descriptions, extract skills from resumes, and compare job requirements with resume skills using NLP and semantic similarity.

## Features

### Job Application Management
- Add job applications
- Edit and delete applications
- View all applications
- Search applications by company or role
- Filter applications by status
- Sort applications by date or company
- Track application status

### Job Description Analysis
- Fetch job descriptions from job URLs
- Extract relevant job description content
- Identify required technical skills
- Extract education requirements
- Extract experience requirements
- Identify other job requirements using NLP

### Resume Analysis
- Upload a PDF resume
- Extract resume text automatically
- Store extracted resume text in PostgreSQL
- Extract technical skills from the resume

### Job-Resume Matching
- Compare skills required by a job with skills found in the resume
- Use semantic similarity to identify related skill terms
- Calculate a match percentage
- Display matched skills
- Display missing skills

## Technologies Used

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL

### NLP and Machine Learning
- spaCy
- Sentence Transformers
- scikit-learn
- Natural Language Processing
- Cosine Similarity

### Web Technologies
- HTML
- CSS
- JavaScript

### Other Libraries
- BeautifulSoup
- Requests
- pypdf

## Project Workflow

```text
Job URL
   ↓
Fetch Job Description
   ↓
NLP Analysis
   ↓
Extract Required Skills
   ↓
Upload Resume
   ↓
Extract Resume Text
   ↓
Extract Resume Skills
   ↓
Semantic Skill Matching
   ↓
Match Score
   ↓
Matched Skills + Missing Skills