from fastapi import status, HTTPException, Depends, APIRouter
from app2.DB import get_db
from sqlalchemy.orm import Session
from app2 import schemas, models, utils

router = APIRouter(tags=["User"])


# User requests

@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # new_user = models.User(name=user.name, email=user.email, password=user.password)
    hashed_pwd = utils.hash_pwd(user.password)
    user.password = hashed_pwd
    new_user = models.User(**user.model_dump())  # convert the user into a dict and unpack
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # returns newly created user like returning in SQL

    return new_user


@router.get("/all_users", response_model=list[schemas.UserOut])  # get all users
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return users


@router.get("/all_users/{user_id}", response_model=schemas.UserOut)  # get single user
def get_user(user_id: int, db: Session = Depends(get_db)):
    # user = db.query(models.User).get({"id": user_id}).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} was not found")

    return user


@router.put("/update_user/{user_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserOut)
def update_user(user_id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db)):
    update_q = db.query(models.User).filter(models.User.id == user_id)
    update_response = update_q.update(updated_user.model_dump(), False)  # convert updated_note into a dict & pass

    if update_response == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} was not found")

    db.commit()
    return {"Updated Note": update_q.first()}


@router.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    del_response = db.query(models.User).filter(models.User.id == user_id).delete(synchronize_session=False)

    db.commit()
    print(f"del response is {del_response}")
    if del_response == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {user_id} was not found")


@router.delete("/delete_user_with_email", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_with_specific_email(user_email: str, db: Session = Depends(get_db)):
    del_response = db.query(models.User).filter(models.User.email == user_email).delete(synchronize_session=False)

    db.commit()
    print(f"del response is {del_response}")
    if del_response == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with email {user_email} was not found")
