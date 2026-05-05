from fastapi import APIRouter,Depends,HTTPException,status
from TaskFlow import models,database,schemas,jwttoken
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/tasks/{task_id}/comment')
async def post_task(task_id:int,comment:schemas.Comment,db: Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
    
    query=db.query(models.Task).filter(models.Task.task_id==task_id,
                                                            models.Task.assigned_to==current_user.user_id
                                                            ).first()
    
    query2=db.query(models.Task).join(models.Team).filter(models.Task.task_id==task_id,
        models.Team.created_by==current_user.user_id).first()
    
    if query==None and query2==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    
    data=comment.dict()
    data['task_id']=task_id
    data['user_id']=current_user.user_id
    
    
    row=models.Comment(**data)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@router.get("/tasks/{task_id}/comment",response_model=list[schemas.Comment])
async def get_task(task_id: int,db: Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
    query=db.query(models.Comment).filter(models.Comment.task_id==task_id,
                                          models.Comment.user_id==current_user.user_id).all()
    if query==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return query
    

