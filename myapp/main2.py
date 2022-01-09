from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import time

import psycopg2 #DB driver to talk to underlying/postgres 
from psycopg2.extras import RealDictCursor # to get column name along with column value against your query


# Sqlalchemy specific imports : 
# Importing models and database files as package to bind database engine with created model
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db


# engine binding for database connection
models.Base.metadata.create_all(bind=engine)

# importing hashing function/method from utils.py
from . import utils

# importing post and user folders
from .router import post, user


#Creating a FastAPI instance
app = FastAPI()


# including both route operations for post and user
app.include_router(post.router)
app.include_router(user.router)


# # Testing path operation
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return {"data": posts}


# "/" root path operation
@app.get("/")
def root():
    return {"data": "Welcome to Kapil's Website!"}











