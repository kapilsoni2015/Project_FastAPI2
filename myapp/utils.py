# password encrypt library
from passlib.context import CryptContext

# encrypt password by using hashing algorythm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# creating a function for generating the password hash
def hash(password: str):
    return pwd_context.hash(password)