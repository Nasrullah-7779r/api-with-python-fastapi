from pydantic import BaseModel


class Note(BaseModel):
    title: str
    description: str = None

#     @staticmethod
#     def get_note(note_title: str, note_desc: str):
#         return {"title": note_title, "description": note_desc}
# n3 = Notes.get_note("3rd Note", "This is my 3rd note")
