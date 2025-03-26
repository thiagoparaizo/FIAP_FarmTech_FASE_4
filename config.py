import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-padrao'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/farmtech'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'