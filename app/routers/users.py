from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import engine,get_db
from typing import List, Optional
from fastapi import Depends,Response ,status , HTTPException, APIRouter


router =  APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
async def create_user(user : schemas.UserCreate,db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        # If user already exists, raise an HTTPException with status code 400 (Bad Request)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    user.password= utils.hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
async def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id: {id} does not exist")
    return user