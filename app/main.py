from fastapi import FastAPI, Depends
from .core.database import engine, Base
from .products.routes import admin_router as products_admin_router, public_router as products_public_router
from .cart.routes import router as cart_router
from .checkout.routes import router as checkout_router
from .orders.routes import router as orders_router

from .auth import routes as auth_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My API", version="1.0")

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(products_admin_router, prefix="/admin/products", tags=["Admin Products"])
app.include_router(products_public_router, prefix="/products", tags=["Public Products"])
app.include_router(cart_router, prefix="/cart", tags=["Cart"])
app.include_router(checkout_router, prefix="/checkout", tags=["Checkout"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])




