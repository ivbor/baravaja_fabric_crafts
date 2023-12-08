import secrets


class Config:
    WTF_CSRF_SECRET_KEY = secrets.token_hex(16)
    SECRET_KEY = secrets.token_hex(16)
    DEBUG = True  # Set to False in production
    # write the db name if it exists already, if you want to create new -
    # do not write name
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/bfc_database'
    SESSION_TYPE = 'filesystem'
    LANGUAGES = ['en', 'pl', 'ru']
