from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

from DB_with_SQL import DB

curser, conn = DB.start_db()
if not curser:
    print("DB error")
    exit(1)

app = FastAPI()


class Note(BaseModel):
    id: int
    title: str
    description: str


# @app.post("/create_note")
# async def create_note(payload: dict = Body(...)):
#     print(payload)
#     return {"new note": f"title: {payload['title']} \ncontent: {payload['description']}"}

notes_list = [{"title": "Life", "description": "Life is unpredictable", "note_no": 1},
              {"title": "Understanding", "description": "Understanding is the key to learn", "note_no": 2}
              ]


@app.get("/")  # get all notes
def get_notes():
    curser.execute("""select * from public."Note" """)
    notes = curser.fetchall()
    return {"data:": notes}


def find_note(no: int):
    for n in notes_list:
        if n["note_no"] == no:
            return n


def find_note_index(no: int):
    for index, n in enumerate(notes_list):
        if n["note_no"] == no:
            return index
    return -1


@app.post("/create_note", status_code=status.HTTP_201_CREATED)
async def create_note(new_note: Note):
    create_query = """insert into public."Note" values (%s,%s,%s) returning * """
    curser.execute(create_query, (new_note.id, new_note.title, new_note.description))
    note = curser.fetchone()
    conn.commit()
    return {"data": note}


@app.get("/{note_id}")  # get single note
def get_note(note_id: int):
    get_query = """select * from public."Note" where id = (%s)"""
    curser.execute(get_query, str(note_id))
    note = curser.fetchall()

    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")

    return {"data": note}


@app.put("/{note_id}", status_code=status.HTTP_202_ACCEPTED)
def update_note(note_id: int, note: Note):
    update_query = """update public."Note" set id = %s, title=%s, description=%s where id=%s returning *"""

    curser.execute(update_query, (note.id, note.title, note.description, note_id))
    updated_note = curser.fetchone()
    row_affected = curser.rowcount
    conn.commit()
    if row_affected > 0:
        return {"data": updated_note}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")


@app.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int):

    get_query = """select * from public."Note" where id = (%s)"""
    curser.execute(get_query, str(note_id))
    deleted_note = curser.fetchone()

    delete_query = """delete from public."Note" where id = %s """
    curser.execute(delete_query, str(note_id))
    row_affected = curser.rowcount

    conn.commit()

    if row_affected > 0:
        return {"deleted note": deleted_note}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Note with note no {note_id} was not found")
