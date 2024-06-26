from .. import models,schemas,utils,oauth2
from fastapi import Depends,Response ,status , HTTPException , APIRouter
from sqlalchemy.orm import Session
from ..database import engine,get_db
from typing import List, Optional
from sqlalchemy import func

router =APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",response_model=List[schemas.PostOut])
async def get_posts( db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user),limit :int =10,skip :int=0 , search : Optional[str]=""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts=cursor.fetchall()
    # post1 = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes") ).join(models.Vote,models.Vote.post_id ==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    
    results = [{"post": post,"votes": votes} for post,votes in posts]  #drom tuples to list of dict

    print(results)
    return results



@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
async def create_post(post : schemas.PostCreate,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(post.title,post.content,post.published))
    # new_post= cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
async def get_post(id : int,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):  # ,response :Response 
    # cursor.execute(" SELECT * FROM posts WHERE id = %s ",(str(id)))
    # post =cursor.fetchone()
    post=db.query(models.Post).filter(models.Post.id==id ).first()
    query=db.query(
        models.Post, func.count(models.Vote.post_id).label("votes") 
        ).join(
            models.Vote,models.Vote.post_id ==models.Post.id, isouter=True
        ).group_by(
            models.Post.id
        ).filter(models.Post.id==id ).first()
    post={"post": query[0],"votes":query[1]}
    

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} was not found")
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id : {id} was not found"}
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id:int,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    # cursor.execute(" DELETE FROM posts WHERE id = %s RETURNING * ",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post=db.query(models.Post).filter(models.Post.id==id )
   
    
    if post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} was not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform this action")
    
    post.delete(synchronize_session=False)
    db.commit()

    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate,db: Session = Depends(get_db),current_user : int =Depends(oauth2.get_current_user)):
    # cursor.execute(" UPDATE posts SET title=%s,content=%s, published=%s WHERE id = %s RETURNING *" ,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    updated_post=db.query(models.Post).filter(models.Post.id==id)

    if updated_post.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id : {id} was not found")
    
    
    if updated_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform this action")
    updated_post.update(post.model_dump(),synchronize_session=False)
    db.commit()
    return updated_post.first()

