from typing import Optional

from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import ColumnElement, func

from .. import oauth2, schemas, models
from ..DB import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Like"])


@router.post("/like", status_code=status.HTTP_201_CREATED)
async def like(vote: schemas.Like, current_user: int = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    result = db.query(models.Note.id, models.Note.title, models.Note.description).join(
        models.Like, models.Like.note_id == models.Note.id, isouter=True)
    print(result)

    note_exist = db.query(models.Like).filter(models.Note.id == vote.note_id)
    note_Exist = note_exist.first()
    if not note_Exist:  # if any note like request received which not exist than raise this exception
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with id {vote.note_id} not found")

    like_query = db.query(models.Like).filter(models.Like.note_id == vote.note_id,
                                              models.Like.user_id == current_user.id)
    found_like = like_query.first()
    if vote.is_like == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already liked"
                                                                             f" the note with id {vote.note_id}")
        new_like = models.Like(user_id=current_user.id, note_id=vote.note_id)
        db.add(new_like)
        db.commit()
        return {"message": "like successfully"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Like doesn't exist")

    like_query.delete(synchronize_session=False)
    db.commit()

    return {"message": "unlike successfully"}


@router.get("/get_no_of_likes_with_single_note/{note_id}", response_model=schemas.NoteOutWithLikes)
async def get_no_of_likes_with_single_user(note_id: int, search: Optional[str] = "", skip: int = 0, limit: int = 10,
                                           current_user: int = Depends(oauth2.get_current_user),
                                           db: Session = Depends(get_db)):
    result = (db.query(models.Note, func.count(models.Like.note_id).label("No of likes")).
              join(models.Like, models.Like.note_id == models.Note.id, isouter=True).group_by(
        models.Note.id).filter(models.Note.id == note_id).first())

    response_data = {"note": {"id": result[0].id, "title": result[0].title, "description": result[0].description,
                              "user_id": result[0].user_id, "user": result[0].user}, "no_of_like": result[1]}

    return response_data


@router.get("/get_no_of_likes", response_model=list[schemas.NoteOutWithLikes])
async def get_no_of_likes_with_all_notes(search: Optional[str] = "", skip: int = 0, limit: int = 10,
                                         current_user: int = Depends(oauth2.get_current_user),
                                         db: Session = Depends(get_db)):
    result = (db.query(models.Note, func.count(models.Like.note_id).label("No of likes")).
              join(models.Like, models.Like.note_id == models.Note.id, isouter=True).group_by(
        models.Note.id).filter(models.Note.title.contains(search)).limit(limit).offset(skip).all())

    response_data = [{"note": {"id": item[0].id, "title": item[0].title, "description": item[0].description,
                               "user_id": item[0].user_id, "user": item[0].user}, "no_of_like": item[1]} for item in
                     result]

    return response_data
