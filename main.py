from fastapi import FastAPI
from pymongo import MongoClient

app = FastAPI()

client = MongoClient("mongodb+srv://@mycluster.9g8gat6.mongodb.net/")

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


# class Notes(BaseModel):
#     title: str
#     description: str
#
#     @staticmethod
#     def get_note(note_title: str, note_desc: str):
#         return {"title": note_title, "description": note_desc}
#
#
# n3 = Notes.get_note("3rd Note", "This is my 3rd note")


@app.post("/{title}/{description}")
async def add_note(title: str, description: str):
    new_note = {"title": title, "description": description}
    if new_note:
        collection.insert_one(dict(new_note))
        return {"message": "Note added successfully", "Note": new_note}
    else:
        return {"message": "Note insertion is failed", "Note": new_note}


@app.put("/{title}/{updated_desc}")
async def update_note(title: str, updated_desc: str):
    filter = {"title": title}
    update = {"$set": {"description": updated_desc}}
    result = collection.update_one(filter, update)
    if result.modified_count == 1:
        return {"message": "Note updated successfully", "updated_note_title": title, "updated_note_desc": updated_desc}
    else:
        return {"message": "Note updation is failed"}


@app.delete("/{title}")
async def delete_note(title: str):
    desc = None

    filter = {"title": title}
    note_to_be_deleted = collection.find_one(filter)

    if note_to_be_deleted:
        desc = note_to_be_deleted.get("description")

    result = collection.delete_one(filter)

    if result.deleted_count == 1:
        return {"message": "Note deleted successfully", "deleted_note_title": title, "deleted_note_desc": desc}
    else:
        return {"message": "Note deletion is failed", "Note": note_to_be_deleted}
