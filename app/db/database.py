# app/db/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
import urllib.parse

# Cargar variables de entorno del archivo .env
load_dotenv()

username = 'procemon'
password = 'dnPLKrKJzuz7YIsaXz8VZOW8Zxj1XBXN'  # Asegúrate de que no contenga caracteres especiales
password_encoded = urllib.parse.quote(password)

url = f"postgresql://{username}:{password_encoded}@dpg-csgjfpdds78s73c15oi0-a.oregon-postgres.render.com/procemondash"


engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
