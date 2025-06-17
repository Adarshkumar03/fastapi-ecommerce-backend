from fastapi import FastAPI, Depends
from .core.database import engine, Base


from .auth import routes as auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My API", version="1.0")

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])




