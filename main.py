from fastapi import FastAPI
from utilities.database import engine
import models.User_model
import models.Wishlist_model
import models.Order_model
import models.Product_model
import models.Product_model
import models.Cart_model
from router import User_router,Order_router,Product_router, Wishlist_router,Cart_router
from auth import User_auth
app=FastAPI()
models.User_model.Base.metadata.create_all(bind=engine)
models.Product_model.Base.metadata.create_all(bind=engine)
models.Wishlist_model.Base.metadata.create_all(bind=engine)
models.Cart_model.Base.metadata.create_all(bind=engine)
models.Order_model.Base.metadata.create_all(bind=engine)
app.include_router(User_router.router)
app.include_router(User_auth.router)
app.include_router(Wishlist_router.router)
app.include_router(Order_router.router)
app.include_router(Product_router.router)
app.include_router(Cart_router.router)