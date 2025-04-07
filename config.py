import os

class Config:
    # Clave secreta para autenticación (JWT, sesiones, etc.)
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # URI de conexión a la base de datos PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:2902@localhost:5432/SGYC'

    # Desactiva el seguimiento de modificaciones (mejora rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = True
