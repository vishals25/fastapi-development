from .. import models,schemas,utils,oauth2
from fastapi import status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter(
    prefix="/users",
    tags=['Users'],
    responses={404: {"description": "Not found"}}
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)

def create_user(user : schemas.UserCreate,db: Session = Depends(get_db)):

    #hash the password

    hashed_password=utils.hash(user.password)
    user.password=hashed_password

    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 

    return new_user

@router.get("/{id}",response_model=schemas.UserOut)

def get_user(id:int,db: Session = Depends(get_db),get_current_user:int = Depends(oauth2.get_current_user) ):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id : {id} not found !")
    return user