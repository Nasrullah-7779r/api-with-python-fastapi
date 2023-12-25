from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from Model.note_schema import Note

app = FastAPI()

client = MongoClient("CONNECTION_STRING")

db = client["testDB"]

collection = db["Notes"]


@app.get("/{title}")
async def get_note(title: str):
    note = collection.find_one({"title": title})
    if note is None:
        return {"message": "Note not found"}
    else:
        note["_id"] = str(note["_id"])
        return {"message": "Note retrieved successfully", "note": note}


@app.post("/note")
async def add_note(note: Note):
    # title_pattern = re.compile(r"^[a-zA-Z0-9\s]+$")
    # if not title_pattern.match(title):
    #     raise HTTPException(status_code=400, detail="Title contains special character")
    try:
        new_note = {"title": note.title, "description": note.description}

        if new_note:
            collection.insert_one(dict(new_note))
            return {"message": "Note added successfully", "Note": new_note}
        else:
            return {"message": "Note insertion failed", "Note": new_note}
    except Exception as e:
        error_msg = f"Error occurred: {e}"
        print(error_msg)
        return {"error": error_msg}


@app.put("/note")
async def update_note(note: Note):
    filter = {"title": note.title}
    update = {"$set": {"description": note.description}}
    result = collection.update_one(filter, update)
    if result.modified_count == 1:
        return {"message": "Note updated successfully", "updated_note_title": note.title,
                "updated_note_desc": note.description}

    return {"message": "Note updation is failed"}


@app.delete("/note")
async def delete_note(note: Note):
    desc = None

    filter = {"title": note.title}
    note_to_be_deleted = collection.find_one(filter)

    if note_to_be_deleted:
        desc = note_to_be_deleted.get("description")

    result = collection.delete_one(filter)

    if result.deleted_count == 1:
        return {"message": "Note deleted successfully", "deleted_note_title": note.title,
                "deleted_note_desc": note.description}

    return {"message": "Note deletion is fail", "Note": note_to_be_deleted}
