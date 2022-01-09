from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db



# Creating router object to be able to split all our route operations
router = APIRouter(
    tags=['Posts']
)

# CRUD operation starts here


# Get all posts
@router.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    '''
    Displays the posts stored
    '''
    posts = db.query(models.Post).all()

    return posts




# Create single post
# See here we are using our pydentic model also for defining our structure of request
@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    '''
    Create a post and store it in database
    '''
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post




# Get single post path operation
@router.get("/posts/{id}", response_model=schemas.PostResponse)
def get_singlepost(id: int, db: Session = Depends(get_db)):
    '''
    Fetch a single post by providing its ID
    '''
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found!")
    
    return post



# Delete path operation
@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db)):
    '''
    Deletes a single post using its ID
    '''
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found!")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)




# Update single post path operation
# See here we are using our pydentic model also for defining our structure of request
@router.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    '''
    Updates a single post and store it in database by utilizing its ID
    '''
    # Saving the query in a variable
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id : {id} not found!")

    # you can pass {'title': 'some', 'content':'content'} this also.
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()