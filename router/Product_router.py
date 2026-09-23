from fastapi import APIRouter,Depends
from fastapi import HTTPException,Path
from typing import Annotated
from starlette import status
from utilities.database import SessionLocal
from sqlalchemy.orm import Session
from models.Product_model import Product
from Validation.Product_validation import ProductRequest

router=APIRouter()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

@router.get("/products/",status_code=status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Product).all()

@router.get("/products/{product_id}",status_code=status.HTTP_200_OK)
async def read_product(db:db_dependency,product_id:int=Path(gt=0)):
    product_model=db.query(Product).filter(Product.id==product_id).first()
    if product_model is not None:
        return product_model
    raise HTTPException(status_code=404,detail="product is not found")

@router.post("/product/",status_code=status.HTTP_201_CREATED)
async def create_product(db:db_dependency,product_request:ProductRequest):
    product_model=Product(**product_request.dict())
    db.add(product_model)
    db.commit()
    return product_model

@router.put("/product/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_product(db:db_dependency,product_id:int,product_request:ProductRequest):
    product_model=db.query(Product).filter(Product.id==product_id).first()
    if product_model is None:
        raise HTTPException(status_code=404,detail="product is not found")
    product_model.name=product_request.name
    product_model.description=product_request.description
    product_model.price=product_request.price
    product_model.stock_quantity=product_request.stock_quantity
    product_model.brand=product_request.brand
    product_model.image_url=product_request.image_url
    product_model.status=product_request.status
    product_model.created_at=product_request.created_at
    product_model.updated_at=product_request.updated_at
    db.add(product_model)
    db.commit()
    return product_model

@router.delete("/product/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(db:db_dependency,product_id:int):
    product_model=db.query(Product).filter(product_id==Product.id).first()
    if product_model is None:
        raise HTTPException(status_code=404,detail="product is not found")
    db.query(Product).filter(Product.id==product_id).delete()
    db.commit()