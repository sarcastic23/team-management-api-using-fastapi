from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class user(BaseModel):
    user_id:int
    name:str
    
class user_resister(BaseModel):
    user_id:int
    name:str
    password:str
    
class user_login(BaseModel):
    user_id:int
    password:str
    
class Team(BaseModel):
    
    team_id:int
    name:str
    created_by:Optional[int]=None
    
class Team_Member(BaseModel):
    user_id:int
    joined_at:Optional[datetime]=None
    
    
class Task(BaseModel):
    task_id:int
    team_id:int
    assigned_to:int
    title:str
    status:str
    created_at:Optional[datetime]=None
    deadline:Optional[datetime]=None
    
    


    
    
class Comment(BaseModel):
    comment_id:int
    content:str
    created_at:Optional[datetime]=None
    
class User_update(BaseModel):
    name:str
    password:str
    
class task_status(BaseModel):
    status:str
    
class Token(BaseModel):
    user_id:int
    
