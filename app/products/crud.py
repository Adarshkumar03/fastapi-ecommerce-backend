from sqlalchemy.orm import Session
from .schema import ProductCreate, ProductUpdate
from .models import Products
from typing import Optional

def create_product(db: Session, product: ProductCreate):
    db_product = Products(**product.__dict__)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def admin_get_all_products(db: Session, skip: int = 0, limit: int = 10):
    products = db.query(Products).offset(skip).limit(limit).all()
    return products if products else []

def get_product_by_id(db: Session, product_id: int):
    product = db.query(Products).filter(Products.id == product_id).first()
    return product if product else None

def update_product(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if not db_product:
        return None
    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(Products).filter(Products.id == product_id).first()
    if not db_product:
        return None
    db.delete(db_product)
    db.commit()
    
def public_get_all_products(db: Session, category: Optional[str] = None,
    min_price: Optional[float] = None, max_price: Optional[float] = None,
    sort_by: Optional[str] = None, skip: int = 0, limit: int = 10):
    query = db.query(Products)
    
    if category:
        query = query.filter(Products.category == category)
    if min_price is not None:
        query = query.filter(Products.price >= min_price)
    if max_price is not None:
        query = query.filter(Products.price <= max_price)
    
    if sort_by:
        if sort_by == "price":
            query = query.order_by(Products.price)
        elif sort_by == "name":
            query = query.order_by(Products.name)
    total_count = query.count()
    products = query.offset(skip).limit(limit).all()
    return total_count, products

def public_search_products(db:Session, keyword: str):
    if not keyword:
        return 0, []
    query = db.query(Products).filter(
        Products.name.ilike(f"%{keyword}%") | 
        Products.description.ilike(f"%{keyword}%") |
        Products.category.ilike(f"%{keyword}%")
    )
    total_count = query.count()
    products = query.all() 
    return total_count, products