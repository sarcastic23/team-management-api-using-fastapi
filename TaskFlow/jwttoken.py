from fastapi import APIRouter,Depends,HTTPException,status
from TaskFlow import models,database,schemas
from TaskFlow.routers import authentication
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import JWTError,jwt
from datetime import datetime,timedelta

OAuth2_scheme=OAuth2PasswordBearer(tokenUrl='auth/login')
error=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

algorithm="HS256"
secret_key="fjvksjdnfksdnfjbsdlfjeahf"
time=30

def create_token(payload: dict):
    
   data= payload.copy()
   access_time=datetime.utcnow()+timedelta(minutes=time)
   data.update({"exp":access_time})
    
   token=jwt.encode(data,secret_key,algorithm)
   return token


def verify_token(token: str):
   try:
      payload=jwt.decode(token,secret_key,algorithms=[algorithm])
      user_id=payload.get("user_id")
      if user_id==None:
         raise error
      user_data=schemas.Token(user_id=int(user_id))
   except JWTError:
      raise error
   return user_data

def current_user(token:str=Depends(OAuth2_scheme),db:Session=Depends(database.get_db)):
      user_token=verify_token(token)
      user=db.query(models.User).filter(models.User.user_id==user_token.user_id).first()
      if user==None:
         raise error
      return user
   
   
    
        
    
