from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app2.config import setting


SQLALCHEMY_DB_URL = (f'postgresql://{setting.database_username}:{setting.database_password}@'
                     f'{setting.database_hostname}/{setting.database_name}')

engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
