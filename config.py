import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/job_tracker"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "---"
