from typing import Optional

from fastapi import status, HTTPException, Depends, APIRouter
from ..DB import get_db
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2

router = APIRouter(tags=["Note"])


# Note requests
@router.post("/create_note", status_code=status.HTTP_201_CREATED, )
async def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    # new_note = models.Note(id=note.id, title=note.title, description=note.description)
    # print(f"id is {user_id}")
    print(current_user.id)
    new_note = models.Note(owner_id=current_user.id, **note.model_dump())  # convert the note into a dict and unpack
    db.add(new_note)
    db.commit()
    db.refresh(new_note)  # returns newly created note like returning in SQL

    return {"New Note": new_note}


@router.get("/all_notes", response_model=list[schemas.NoteOut])  # get all notes
def get_all_notes(db: Session = Depends(get_db), skip: int = 0, limit: int = 10, search: Optional[str] = ""):
    data = db.query(models.Note).filter(models.Note.title.contains(search)).limit(limit).offset(skip).all()
    print(search)
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found any note")

    return data


@router.get("/one_note/{note_id}")  # get single note
def get_one_note(note_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #    note = db.query(models.Note).get({"id": note_id})
    note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized for requested action")

    return note


# update the existing note
@router.put("/update_note/{note_id}", status_code=status.HTTP_202_ACCEPTED)
def update_note(note_id: int, updated_note: schemas.NoteCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    update_q = db.query(models.Note).filter(models.Note.id == note_id)
    note = update_q.first()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for requested action")

    update_q.update(updated_note.model_dump(), False)  # convert updated_note into a dict & pass

    db.commit()
    return {"Updated Note": update_q.first()}


@router.delete("/delete_note/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    del_response = db.query(models.Note).filter(models.Note.id == note_id)
    note = del_response.first()

    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")

    if note.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized for requested action")

    del_response.delete(synchronize_session=False)
    db.commit()


@router.delete("/delete_all_notes", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    del_response = db.query(models.Note).delete(synchronize_session=False)

    db.commit()

    if del_response == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The Notes table might be empty")
