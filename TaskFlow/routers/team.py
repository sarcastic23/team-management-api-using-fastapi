from fastapi import APIRouter,Depends,HTTPException,status
from TaskFlow import models,database,schemas,jwttoken
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/teams')
async def post_teams(team:schemas.Team,db:Session=Depends(database.get_db),user=Depends(jwttoken.current_user)):
    team.created_by=user.user_id
    row=models.Team(**team.dict())
    db.add(row)
    db.commit()
    db.refresh(row)    
    return row


@router.get('/teams',response_model=list[schemas.Team])
async def get_team(db:Session=Depends(database.get_db),user=Depends(jwttoken.current_user)):
    
    row=db.query(models.Team).join(models.TeamMember).filter(models.TeamMember.user_id==user.user_id).all()
    if row==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return row

@router.post('/teams/{team_id}/add_user')
async def post_user(team_id: int,member:schemas.Team_Member,db: Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
    
    
    query=db.query(models.Team).filter(models.Team.team_id==team_id,models.Team.created_by==current_user.user_id).first()
    query2=db.query(models.User).filter(models.User.user_id==member.user_id).first()
    
    if query==None or query2==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    row=models.TeamMember(team_id=team_id,**member.dict())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
    
    
    
@router.get('/teams/members')
async def get_members(db: Session=Depends(database.get_db),current_user=Depends(jwttoken.current_user)):
    teams = db.query(models.Team).join(models.TeamMember).filter(
        models.TeamMember.user_id == current_user.user_id).all()

    return teams
        
        
    