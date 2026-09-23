from fastapi import APIRouter,Depends
from fastapi import HTTPException,Path
from typing import Annotated
from starlette import status
from sqlalchemy.orm import Session
from utilities.database import SessionLocal
from models.Wishlist_model import Wishlist
from Validation.Wishlist_validation import WishlistRequest
router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@router.get("/wishlist/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Wishlist).all()

@router.get("/wishlist/{wishlist_id}",status_code=status.HTTP_200_OK)
async def read_wishlist(db:db_dependency,wishlist_id:int=Path(gt=0)):
    wishlist_model=db.query(Wishlist).filter(Wishlist.id==wishlist_id).first()
    if wishlist_model is not None:
        return wishlist_model
    raise HTTPException(status_code=404,detail="wishlist is not found")

@router.post("/wishlist/",status_code=status.HTTP_201_CREATED)
async def create_wishlist(db:db_dependency,wishlist_request:WishlistRequest):
    wishlist_model=Wishlist(**wishlist_request.dict())
    db.add(wishlist_model)
    db.commit()
    return wishlist_model

@router.put("/wishlist/{wishlist_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_wishlist(db:db_dependency,wishlist_id:int,wishlist_request:WishlistRequest):
    wishlist_model=db.query(Wishlist).filter(Wishlist.id==wishlist_id).first()
    if wishlist_model is None:
        raise HTTPException(status_code=404,detail="wishlist is not found")
    wishlist_model.user_id=wishlist_request.user_id
    wishlist_model.product_id=wishlist_request.product_id
    wishlist_model.added_at=wishlist_request.added_at
    wishlist_model.created_at=wishlist_request.created_at
    wishlist_model.updated_at=wishlist_request.updated_at
    db.add(wishlist_model)
    db.commit()
    return wishlist_model

@router.delete("/wishlist/{wishlist_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_wishlist(db:db_dependency,wishlist_id:int):
    wishlist_model=db.query(Wishlist).filter(wishlist_id==Wishlist.id).first()
    if wishlist_model is None:
        raise HTTPException(status_code=404,detail="wishlist is not found")
    db.query(Wishlist).filter(Wishlist.id==wishlist_id).delete()
    db.commit()