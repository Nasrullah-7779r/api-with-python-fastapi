from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, models, utils, oauth2
from ..DB import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post('/login', response_model=schemas.Token)
# instead of OAuth2PasswordRequestForm schemas.UserLogin can also be used
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    # create a token
    # return a token
    access_token = oauth2.create_access_token({"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
