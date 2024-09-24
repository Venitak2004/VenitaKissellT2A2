import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ('JWT_SECRET_KEY')