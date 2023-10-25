from typing import Optional
from random import randrange
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from app2.DB import  DB

DB.start_db()

app = FastAPI()


class Note(BaseModel):
    title: str
    description: str
    note_no: Optional[int] = None


# @app.post("/create_note")
# async def create_note(payload: dict = Body(...)):
#     print(payload)
#     return {"new note": f"title: {payload['title']} \ncontent: {payload['description']}"}

notes = [{"title": "Life", "description": "Life is unpredictable", "note_no": 1},
         {"title": "Understanding", "description": "Understanding is the key to learn", "note_no": 2}
         ]


@app.get("/")
def get_notes():
    return {"data:": notes}


def find_note(no: int):
    for n in notes:
        if n["note_no"] == no:
            return n


def find_note_index(no: int):
    for index, n in enumerate(notes):
        if n["note_no"] == no:
            return index
    return -1


@app.get("/{no}")
def get_note(no: int):
    note = find_note(no)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {no} was not found")

    else:
        return {"data": note}


@app.post("/create_note", status_code=status.HTTP_201_CREATED)
async def create_note(new_note: Note):
    note_dict = new_note.model_dump()
    note_dict['note_no'] = randrange(1, 1000000)
    notes.append(note_dict)
    return {"data": notes}


@app.delete("/{no}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(no: int):
    note = find_note(no)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {no} was not found")
    else:
        notes.remove(note)
        # return {"message": "Note was removed successfully"}


@app.put("/{no}", status_code=status.HTTP_202_ACCEPTED)
def update_note(no: int, note: Note):
    note_index = find_note_index(no)
    if not note_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {no} was not found")

    note_dict = note.model_dump()
    note_dict['note_no'] = no
    notes[note_index] = note_dict
    return {"data": note_dict}
