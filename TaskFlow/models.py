from TaskFlow.database import Base 
from sqlalchemy import Column, Integer, String, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func




    
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    password=Column(String,nullable=False)
    
    teams = relationship("TeamMember", back_populates="user")
    tasks = relationship("Task", back_populates="assigned_user")
    comments = relationship("Comment", back_populates="user")
    
    
    
class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_by = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))

    members = relationship("TeamMember", back_populates="team")
    tasks = relationship("Task", back_populates="team")
    
    
    
class TeamMember(Base):
    __tablename__ = "team_members"

    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), primary_key=True)

    joined_at = Column(TIMESTAMP, server_default=func.now())

    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="teams")
    
    
    
    
class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.team_id", ondelete="CASCADE"))
    assigned_to = Column(Integer, ForeignKey("users.user_id", ondelete="SET NULL"))

    title = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")

    created_at = Column(TIMESTAMP, server_default=func.now())
    deadline = Column(TIMESTAMP)

    team = relationship("Team", back_populates="tasks")
    assigned_user = relationship("User", back_populates="tasks")
    comments = relationship("Comment", back_populates="task")
    
    
    
    
class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)

    task_id = Column(Integer, ForeignKey("tasks.task_id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")