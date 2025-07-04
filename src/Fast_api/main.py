from fastapi import Depends,FastAPI,HTTPException,status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime,timedelta
from jose import JWTError,jwt
from passlib.context import CryptContext 


SECRET_KEY="8e2efe3d569cbf6b2db62d727975f8ec3ad85571f1c369ce7bfab98594a67b9e"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINTES=30




db={
    "Abhi":{
        "userName":"abhi",
        "fullName":"abhijit rao",
        "email":"abhijit@gmail.com",
        "hashed_passcode":"",
        "disabled": False
    }
}

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    userName:str or None =None

class User(BaseModel):
    userName:str
    email:str or None =None
    fullName:str or None =None
    disabled:bool or None=None

class UserInDB(User):
    hashed_passcode:str

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth_2_scheme=OAuth2PasswordBearer(tokenUrl="token")
app=FastAPI()

def verfiy_passcode(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db,username:str):
    if username in db:
        user_data=db['userName']
        return UserInDB(**user_data)
    
def authenticate_user(db,username:str,password:str):
    user=get_user(db,username)
    if not user:
        return False
    if not verfiy_passcode(password,user.hashed_passcode):
        return False
    
    return user

def create_access_token(data:dict,expires_delta:timedelta or None = None):
    to_encode= data.copy()
    if expires_delta:
        expire=datetime.utcnow() +expires_delta
    else:
        expire= datetime.utcnow()+timedelta(minutes=15)

    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt