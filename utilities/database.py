from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utilities.constants import *
SQLALCHEMY_DATABASE_URL=f"{DB_TYPE}+psycopg2://{POSTGRES_DB_USERNAME}:{POSTGRES_DB_PSWD}@{POSTGRES_DB_URL}:5432/{POSTGRES_DB_NAME}"
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
print("DATABASE URL FROM DATABASE.PY:",SQLALCHEMY_DATABASE_URL)