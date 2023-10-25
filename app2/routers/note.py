from fastapi import status, HTTPException, Depends, APIRouter
from app2.DB import get_db
from sqlalchemy.orm import Session
from app2 import schemas, models

router = APIRouter(tags=["Note"])


# Note requests
@router.post("/create_note", status_code=status.HTTP_201_CREATED)
async def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    # new_note = models.Note(id=note.id, title=note.title, description=note.description)
    new_note = models.Note(**note.model_dump())  # convert the note into a dict and unpack
    db.add(new_note)
    db.commit()
    db.refresh(new_note)  # returns newly created note like returning in SQL

    return {"New Note": new_note}


@router.get("/all_notes")  # get all notes
def get_notes(db: Session = Depends(get_db)):
    data = db.query(models.Note).all()

    return data


@router.get("/all_notes/{note_id}")  # get single note
def get_note(note_id: int, db: Session = Depends(get_db)):
    #    note = db.query(models.Note).get({"id": note_id})
    note = db.query(models.Note).filter(models.Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")

    return note


# update the existing note
@router.put("/update_note/{note_id}", status_code=status.HTTP_202_ACCEPTED)
def update_note(note_id: int, updated_note: schemas.NoteCreate, db: Session = Depends(get_db)):
    update_q = db.query(models.Note).filter(models.Note.id == note_id)
    update_response = update_q.update(updated_note.model_dump(), False)  # convert updated_note into a dict & pass

    if update_response == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")

    db.commit()
    return {"Updated Note": update_q.first()}


@router.delete("/delete_note/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    del_response = db.query(models.Note).filter(models.Note.id == note_id).delete(synchronize_session=False)

    db.commit()
    print(f"del response is {del_response}")
    if del_response == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")
