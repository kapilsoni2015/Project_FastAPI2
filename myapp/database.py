'''
Creating Database URL and engine to connect to our database.
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

# we will use the function declarative_base() that returns a class. 
# Later we will inherit from this class to create each of the database models or classes (the ORM models):
Base = declarative_base()


# Dependency when we use sqlalchemy
# function to get a connection to a database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()