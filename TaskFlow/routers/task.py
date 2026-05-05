from fastapi import APIRouter,Depends,HTTPException,status
from TaskFlow import models,database,schemas,jwttoken
from sqlalchemy.orm import Session






router = APIRouter()



@router.post('/tasks')
async def post_task(task:schemas.Task,db: Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
    query=db.query(models.TeamMember).join(models.Team).filter(models.TeamMember.team_id==task.team_id , 
                                                               models.TeamMember.user_id==task.assigned_to,
                                                               models.Team.created_by==current_user.user_id).first()
    
    if query ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    
    row=models.Task(**task.dict())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row



@router.get('/tasks',response_model=list[schemas.Task])
async def get_task(db: Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
    query=db.query(models.Task).join(models.User).filter(models.User.user_id==current_user.user_id).all()
    if query==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return query
    
    
    
@router.patch('/tasks/{id}/status')
async def change_status(id: int,task_status:schemas.task_status,db:Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
    query=db.query(models.Task).filter(models.Task.task_id==id,models.Task.assigned_to==current_user.user_id).first()
    if query==None:
     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    query.status=task_status.status
    db.commit()
    db.refresh(query)
    return query
    