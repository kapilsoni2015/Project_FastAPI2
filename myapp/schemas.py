# this pydantic library has nothing to do with FastAPI library
# we are using it for its features and we can use it any python applications
# defninig a schema and validating the input
# make sure our front end is sending correct data to backend/database e.g. create operation
from pydantic import BaseModel, EmailStr
from datetime import datetime


# class Post(BaseModel):
#     title : str
#     content : str
#     published : bool =  True # giving a default value

# class CreatePost(BaseModel):
#     title : str
#     content : str
#     published : bool =  True # giving a default value

# class UpdatePost(BaseModel):
#     title : str
#     content : str
#     published : bool

# class for post request structure
class PostBase(BaseModel):
    title : str
    content : str
    published : bool =  True # giving a default value

# Inheritance usecase
class PostCreate(PostBase):
    pass

# New class for response structure for posts
# We can also use our PostBase class as parent class below and use inheritance to shorten our code lines
class PostResponse(BaseModel):
    id : int
    title : str
    content : str
    published : bool
    created_at : datetime

    # sqlalchemy specific tweak as per documentation as pydantic model works with dictionary
    class Config:
        orm_mode = True




##############################################################
# schema for user table structure
class UserCreate(BaseModel):
    email : EmailStr
    password : str

# New class for resonse strucuter for users
# response for user create path operation
class UserResponse(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    # sqlalchemy specific tweak as per documentation as pydantic model works with dictionary
    class Config:
        orm_mode = True
    