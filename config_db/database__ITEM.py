from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import mysql.connector



# Конфигурация SQLAlchemy
DATABASE_URL = "mysql+pymysql://root:@localhost/covid"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='covid'
)

cursor = connection.cursor()

def get_sync_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)
