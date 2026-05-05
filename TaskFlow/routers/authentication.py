from fastapi import APIRouter,Depends,HTTPException,status
from TaskFlow import models,database,schemas
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from argon2 import PasswordHasher
from TaskFlow import jwttoken


p=PasswordHasher()
def password_hasher(password):
    return p.hash(password)

def verify(p1,p2):
    return p.verify(p1,p2)



router = APIRouter()


@router.post('/auth/register',response_model=schemas.user)
async def register(user:schemas.user_resister,db: Session=Depends(database.get_db)):
    row=db.query(models.User).filter(models.User.name==user.name).first()
    if row!=None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="user_name exists")
    
    user.password=password_hasher(user.password)
        
    query=models.User(**user.dict())
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


@router.post('/auth/login')
async def login(user:OAuth2PasswordRequestForm=Depends(),db: Session=Depends(database.get_db)):
    query=db.query(models.User).filter(models.User.user_id==user.username).first()
    if query ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if verify(query.password,user.password)==False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    token=jwttoken.create_token({"user_id":query.user_id})
    
    return {"token": token,
           "type":"bearer"}
        
        

    

