# config.py

class Config:
    SECRET_KEY = 'admin'
    DEBUG = True  # Set to False in production
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/database'
    SESSION_TYPE = 'filesystem'
