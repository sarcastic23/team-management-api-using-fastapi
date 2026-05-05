from fastapi import FastAPI,APIRouter
from TaskFlow.models import Base
from TaskFlow.database import engine
from TaskFlow.routers import task,team,authentication,comments,users


Base.metadata.create_all(bind=engine)


app=FastAPI()


    




app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(task.router)
app.include_router(team.router)
app.include_router(comments.router)