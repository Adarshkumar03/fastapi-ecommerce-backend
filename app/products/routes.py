from fastapi import APIRouter, Depends, HTTPException
from .schema import ProductCreate, ProductUpdate
from .crud import create_product, admin_get_all_products, get_product_by_id, update_product, delete_product
from ..core.database import get_db
from ..auth.security import admin_required
from sqlalchemy.orm import Session


admin_router = APIRouter()

@admin_router.post("/products", dependencies=[Depends(admin_required)])
async def product_create(product: ProductCreate, db: Session = Depends(get_db), ):
    if not product.name or not product.price or not product.stock:
        raise HTTPException(status_code=400, detail={"code":"400", "error": "True", "msg": "Name, price, and stock are required fields."})
    return create_product(db, product)

@admin_router.get("/products", dependencies=[Depends(admin_required)])
async def get_products(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
    products = admin_get_all_products(db, skip=(page - 1) * page_size, limit=page_size)
    if not products:
        raise HTTPException(status_code=404, detail={"code":"404", "error": "True", "msg": "No products found."})
    return {
        "total_count": len(products),
        "page": page,
        "page_size": page_size,
        "products": products
    }


@admin_router.get("/products/{product_id}", dependencies=[Depends(admin_required)])
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail={"code":"404", "error": "True", "msg": "Product not found."})
    return product

@admin_router.put("/products/{product_id}", dependencies=[Depends(admin_required)])
async def product_update(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    existing_product = get_product_by_id(db, product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail={"code":"404", "error": "True", "msg": "Product not found."})
    return update_product(db, product_id, product)

@admin_router.delete("/products/{product_id}", dependencies=[Depends(admin_required)])
async def product_delete(product_id: int, db: Session = Depends(get_db)):
    existing_product = get_product_by_id(db, product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail={"code":"404", "error": "True", "msg": "Product not found."})
    return delete_product(db, product_id)

public_router = APIRouter()