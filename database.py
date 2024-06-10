# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:Blue2024+*@localhost/Gestion_Citas"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)
# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Declarar una base para las clases de SQLAlchemy
Base = declarative_base()

