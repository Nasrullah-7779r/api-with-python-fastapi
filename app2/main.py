import uvicorn
from fastapi import FastAPI
from app2 import models
from app2.DB import engine
from app2.routers import user, note, auth

models.Base.metadata.create_all(bind=engine)

notes_list = [{"title": "Life", "description": "Life is unpredictable", "note_no": 1},
              {"title": "Understanding", "description": "Understanding is the key to learn", "note_no": 2}
              ]
app = FastAPI()

app.include_router(router=user.router)
app.include_router(router=note.router)
app.include_router(router=auth.router)

# To debug FastAPI
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

