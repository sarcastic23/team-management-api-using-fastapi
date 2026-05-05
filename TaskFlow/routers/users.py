from fastapi import APIRouter,Depends,HTTPException,status
from TaskFlow import models,database,schemas,jwttoken
from sqlalchemy.orm import Session
from TaskFlow.routers import authentication


router = APIRouter()

@router.get('/users',response_model=list[schemas.user])
def get_users(db:Session=Depends(database.get_db)):
 query=db.query(models.User).all() 
 return query

@router.put('/users')
async def post_users(user:schemas.User_update,db: Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
    
   row=db.query(models.User).filter(models.User.user_id==current_user.user_id)
   query=row.first()
   if query==None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
   user.password=authentication.password_hasher(user.password)
   row.update(**user.dict())
   db.commit()
   db.refresh(query)
   return query
 
 
   
@router.get('/users/{id}',response_model=schemas.user)
async def get_user(id: int,db: Session=Depends(database.get_db),user=Depends(jwttoken.current_user)):
    query=db.query(models.User).filter(models.User.user_id==id).first()
    if query==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return query
    

@router.post('/users/me',response_model=list[schemas.user])
async def get_user(db:Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
  query=db.query(models.User).filter(models.User.user_id==current_user.user_id).first()
  return query

    
    


