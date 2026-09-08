from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utilities.constants import *
SQLALCHEMY_DATABASE_URL=f"{DB_TYPE}://{POSTGRES_DB_USERNAME}:{POSTGRES_DB_PSWD}@{POSTGRES_DB_URL}/{POSTGRES_DB_NAME}"
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()