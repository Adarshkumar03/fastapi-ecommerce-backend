from fastapi import FastAPI, Depends
from .core.database import engine, Base
from .products.routes import admin_router as products_admin_router, public_router as products_public_router

from .auth import routes as auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My API", version="1.0")

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(products_admin_router, prefix="/admin", tags=["Admin Products"])
app.include_router(products_public_router, prefix="/products", tags=["Public Products"])




