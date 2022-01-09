from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from random import randrange
import time

import psycopg2 #DB driver to talk to underlying/postgres 
from psycopg2.extras import RealDictCursor # to get column name along with column value against your query


# this pydantic library has nothing to do with FastAPI library
# we are using it for its features and we can use it any python applications
# defninig a schema and validating the input
# make sure our front end is sending correct data to backend/database
from pydantic import BaseModel
class Post(BaseModel):
    title : str
    content : str
    published : bool =  True


while True:
    try:
        # this is a bad practice to store your password/credentials hardcoded
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', 
            password = 'postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connecting to Database is failed!")
        print("Error :", error)
        time.sleep(3)


#Creating a FastAPI instance
app = FastAPI()


@app.get("/")
def root():
    return {'message': "Kapil's Website!"}


@app.get("/posts")
def get_posts():
    cursor.execute(''' SELECT * FROM posts ''')
    posts = cursor.fetchall()
    return {'data': posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
        (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    
    conn.commit()
    return {'data': new_post}
    


@app.get("/posts/{id}")
def get_post(id: int):
    #cursor.execute(""" SELECT * FROM posts WHERE id = 1 """)  # hardcoding id
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    test_post = cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found!")
    
    return {"post detail": test_post}



@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #putting a comma at the end of str(id) to work out with code
    #as it was giving error while trying to convert int into str
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id : {id} not found!")

    return Response(status_code=status.HTTP_204_NO_CONTENT)    



@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s 
        WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id : {id} not found!")

    return {"data": update_post}