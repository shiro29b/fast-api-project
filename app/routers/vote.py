
from fastapi import Depends,Response ,status , HTTPException, APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db
from .. import schemas,oauth2,models


router =  APIRouter(
    prefix="/vote",
    tags=["Users"]

)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {vote.post_id} does not exit")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted  on post {vote.post_id}")
        new_vote=models.Vote(user_id=current_user.id,post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote Not Found")
        vote_query.delete()
        db.commit()
        return {"message":"Successfully deleted vote"}


