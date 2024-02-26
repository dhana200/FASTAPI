### This Documnetation for connecting database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

### Refernce --> https://fastapi.tiangolo.com/tutorial/sql-databases/

# URL format SQL_ALCHEMY_DATBASE_URL = 'postgressql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQL_ALCHEMY_DATBASE_URL = 'postgresql://postgres:Dhana20@localhost/FastAPI'

engine = create_engine(SQL_ALCHEMY_DATBASE_URL) # this used for establishing connection between database and fastapi


# If we need to do changes on the sql database
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# all the table that we are going to use or extend are going to use a schema which is this
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
