from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id =Column(Integer, primary_key=True, nullable=False)
    title =Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="TRUE" ,nullable=False )
    created_at = Column(TIMESTAMP,server_default=text("now()"),nullable=False)
    owner_id= Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")
    


class User(Base):
    __tablename__ ="users"
    id = Column(Integer,nullable=False, primary_key=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(TIMESTAMP,server_default=text("now()"),nullable=False)

class Vote(Base):
    __tablename__ ="votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,primary_key=True,  )
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),nullable=False,primary_key=True)
    