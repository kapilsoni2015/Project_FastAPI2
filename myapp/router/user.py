from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db


# Creating router object to be able to split all our route operations
router = APIRouter(
    tags=['Users']
)



# Create single user
# See here we are using our pydentic model also for defining our structure of request
@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''
    Create a user and store it in database
    '''
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    #new_user = models.User(email=user.email, password=user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# Get all users
@router.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    '''
    Displays the users stored
    '''
    users_list = db.query(models.User).all()

    return users_list




# Get single user
@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_singleuser(id: int, db: Session = Depends(get_db)):
    '''
    Fetch a single user by providing its ID
    '''
    user_query = db.query(models.User).filter(models.User.id == id).first()

    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found!")
    
    return user_query




# Update single user 
@router.put("/users/{id}", response_model=schemas.UserResponse)
def update_users(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    '''
    Updates a single user and store it in database by utilizing its ID
    '''
    # Saving the query in a variable
    user_query = db.query(models.User).filter(models.User.id == id)

    user1 = user_query.first()

    if user1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id : {id} not found!")

    # you can pass {'email': 'some@gmail.com', 'password':'content'} this also.
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()