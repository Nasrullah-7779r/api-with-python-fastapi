import pydantic
import uvicorn
from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
# from . import models
# from .DB import engine
from .routers import user, note, auth, like
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)   its no longer needed, because Alembic has taken over for DB operations

# notes_list = [{"title": "Life", "description": "Life is unpredictable", "note_no": 1},
#               {"title": "Understanding", "description": "Understanding is the key to learn", "note_no": 2}
#               ]
app = FastAPI()


# middleWare = [Middleware(TrustedHostMiddleware,
#                          allowed_hosts=['example.com', '*.example.com'])
#               ]

# app = Starlette(routes=[user.router, note.router, auth.router, like.router], middleware=middleWare)
@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


origins = ["https://www.google.com", "https://vulms.vu.edu.pk"]
# origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user.router)
app.include_router(router=note.router)
app.include_router(router=auth.router)
app.include_router(router=like.router)

# To debug FastAPI
# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)

# print(pydantic.__version__)
